#!/usr/bin/env python3
"""HQ test: the C047 gap fill with depth-aware clarity, from the phone's own depth map (Cinematic disparity track).

  real frames (a cine_bake at --fnumber F) | AI fill frames 0..K-1 | real frames from still B on
  1. AI fill: colour + saturation matched to the real 3–7 s; its background (far plane, from the real depth map: the
     interior and windscreen stay fixed to the camera) blurred until its fine detail matches the real bokeh, measured.
  2. Every frame: light denoise; then fine sharpening + local contrast weighted by the in-focus mask
     exp(-((d - d_focus) / (0.25 d_focus))^2), so only the plane the camera focused on (the driver, the interior) gains
     clarity and the street stays soft.
  3. 3-frame dissolves at both seams.
Usage: depth_enhance.py <workdir> <real_bake.mov> <disparity.f16> <ai.mp4> <out.mov>
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

W = Path(sys.argv[1]); REAL, DISP, AI, OUT = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
FW, FH, FPS = 1920, 1080, 25
A0, B0, D = 75, 175, 3
FINE, LOCAL = 1.0, 0.45
LUMA = np.array([0.2126, 0.7152, 0.0722], np.float32)


def read(path, vf):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, FH, FW, 3)


real = read(REAL, f"transpose=2,scale={FW}:{FH},fps={FPS},hqdn3d=3:2.5:4:3")
ai = read(AI, f"scale={FW}:{FH},fps={FPS},hqdn3d=1.5:1.5:2:2")
meta = json.loads(Path(DISP + ".json").read_text())
disp = np.memmap(DISP, dtype=np.float16, mode="r").reshape(-1, meta["h"], meta["w"])
focus = meta["focus"]


def masks(i):
    d = np.nan_to_num(np.asarray(disp[min(i, len(disp) - 1)], np.float32))
    df = focus[min(i, len(focus) - 1)]
    near = np.exp(-((d - df) / (0.25 * df)) ** 2)
    far = np.clip((0.6 * df - d) / (0.4 * df), 0, 1)
    up = lambda m: ndimage.gaussian_filter(ndimage.zoom(m, (FH / m.shape[0], FW / m.shape[1]), order=1), 4)[..., None]
    return up(near), up(far)


def fine_ratio(f, region):
    y = f.astype(np.float32) @ LUMA
    g1 = ndimage.gaussian_gradient_magnitude(y, 1.0); g4 = ndimage.gaussian_gradient_magnitude(y, 4.0)
    r = g1 / (g4 + 1e-3); sel = region[..., 0] > 0.7
    sel &= g4 > np.percentile(g4[sel], 80) if sel.any() else sel
    return float(np.median(r[sel])) if sel.any() else 1.0


def sh(f, m):
    y = f.astype(np.float32) @ LUMA; sel = m[..., 0] > 0.7
    g = np.abs(ndimage.laplace(ndimage.gaussian_filter(y, 1.0)))
    return float(g[sel].mean() / max(y[sel].mean(), 1)) if sel.any() else 0.0


def clarity(f, near, c=1.0):
    fine = f - ndimage.gaussian_filter(f, (1.2, 1.2, 0))
    local = f - ndimage.gaussian_filter(f, (12, 12, 0))
    return np.clip(f + c * near * (FINE * fine + LOCAL * local), 0, 255)


small = lambda f: f[::8, ::8].astype(np.float32)
k = int(np.argmin([np.abs(small(f) - small(real[B0])).mean() for f in ai]))
# colour (mean/std at 0.5) and saturation from subsampled frames (memory: never hold the whole clip in float)
sub_ai = np.stack([f[::4, ::4] for f in ai[:k:5]]).astype(np.float32)
sub_rf = np.stack([f[::4, ::4] for f in real[A0:B0:5]]).astype(np.float32)
m_ai, s_ai = sub_ai.reshape(-1, 3).mean(0), sub_ai.reshape(-1, 3).std(0)
m_rf, s_rf = sub_rf.reshape(-1, 3).mean(0), sub_rf.reshape(-1, 3).std(0)
gain = 1 + 0.5 * (s_rf / np.maximum(s_ai, 1e-3) - 1); shift = 0.5 * (m_rf - m_ai)
sat = lambda x: float(np.mean((x.max(-1) - x.min(-1)) / np.maximum(x.max(-1), 1)))
col = lambda f: np.clip((f - m_ai) * gain + m_ai + shift, 0, 255)
s_gain = sat(sub_rf) / max(sat(col(sub_ai)), 1e-3)


def match(f):
    f = col(f.astype(np.float32)); L = (f @ LUMA)[..., None]
    return np.clip(L + (f - L) * s_gain, 0, 255)


# AI calibration on two frames (a third and two thirds in), against the real frames at the same times:
#   background blur until its far-plane detail matches the real bokeh; then the clarity amount for the AI
#   until its near plane matches the real near plane after the same pass.
probe = [k // 3, 2 * k // 3]
cal = []
for j in probe:
    near_j, far_j = masks(A0 + j)
    cal.append((match(ai[j]), real[A0 + j].astype(np.float32), near_j, far_j))
target_far = np.mean([sh(r, fa) for _, r, _, fa in cal])
before = np.mean([sh(a, fa) for a, _, _, fa in cal])
blur = lambda a, fa, sg: a * (1 - fa) + ndimage.gaussian_filter(a, (sg, sg, 0)) * fa if sg else a
sig = min((0, 1.6, 2.4, 3.2, 4.0, 5.0, 6.0, 7.5),
          key=lambda sg: abs(np.mean([sh(blur(a, fa, sg), fa) for a, _, _, fa in cal]) - target_far))
target_near = np.mean([sh(clarity(r, ne), ne) for _, r, ne, _ in cal])
ai_c = min((0, 0.25, 0.5, 0.75, 1.0),
           key=lambda c: abs(np.mean([sh(clarity(blur(a, fa, sig), ne, c), ne) for a, _, ne, fa in cal]) - target_near))
# Still crisper than the real near plane with no clarity at all? Soften the AI near plane a touch instead.
soft = lambda a, ne, sg: a * (1 - ne) + ndimage.gaussian_filter(a, (sg, sg, 0)) * ne if sg else a
near_sig = 0.0
if ai_c == 0:
    near_sig = min((0, 0.4, 0.6, 0.8, 1.0, 1.2),
                   key=lambda sg: abs(np.mean([sh(soft(blur(a, fa, sig), ne, sg), ne) for a, _, ne, fa in cal]) - target_near))
target = target_far; mid = probe[0]


def ai_frame(j):
    f = match(ai[j])
    near, far = masks(A0 + j)
    if sig:
        f = f * (1 - far) + ndimage.gaussian_filter(f, (sig, sig, 0)) * far
    if near_sig:
        f = f * (1 - near) + ndimage.gaussian_filter(f, (near_sig, near_sig, 0)) * near
    if j < D:
        w = (j + 1) / (D + 1); f = f * w + real[A0 + j].astype(np.float32) * (1 - w)
    if j >= k - D:
        v = (k - j) / (D + 1); f = f * v + real[B0 - (k - j)].astype(np.float32) * (1 - v)
    return f


plan = [("r", i) for i in range(A0)] + [("a", j) for j in range(k)] + [("r", i) for i in range(B0, len(real))]
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{FW}x{FH}", "-r", str(FPS),
                        "-i", "-", "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le",
                        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", OUT], stdin=subprocess.PIPE)
outs = []
for kind, i in plan:
    f = real[i].astype(np.float32) if kind == "r" else ai_frame(i)
    near, _ = masks(i if kind == "r" else A0 + i)
    o = clarity(f, near, 1.0 if kind == "r" else ai_c).astype(np.uint8)
    enc.stdin.write(o.tobytes()); outs.append(o[::8, ::8].astype(np.float32))
enc.stdin.close(); enc.wait()

luma = lambda x: (x @ LUMA) / 255
steps = [float(np.abs(luma(outs[i + 1]) - luma(outs[i])).mean()) for i in range(len(outs) - 1)]
rep = {"ai_frames_used": k, "ai_background_blur_sigma": sig, "far_detail_real": round(float(target_far), 4),
       "far_detail_ai_before": round(float(before), 4), "ai_clarity_scale": ai_c, "ai_near_soften_sigma": near_sig, "near_detail_real_after": round(float(target_near), 4),
       "sat_gain": round(s_gain, 3),
       "seam_in": round(steps[A0 - 1], 4), "seam_out": round(steps[A0 + k - 1], 4),
       "median_step": round(float(np.median(steps)), 4), "frames": len(outs)}
print(json.dumps(rep, indent=1))
(W / (Path(OUT).stem + ".json")).write_text(json.dumps(rep, indent=1))
