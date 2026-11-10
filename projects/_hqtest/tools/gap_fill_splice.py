#!/usr/bin/env python3
"""HQ test: put the Omni cinematic gap-fill into the real C047 in place of 3.00–7.00 s, colour-matched, and measure the seams.

real frames 0–74 (0.00–2.96 s) | AI frames 0..K-1 (AI frame 0 = still A = camera 3.00 s) | real frames 175– (camera 7.00 s = still B)
K = the AI frame that best matches still B, so the cut back to camera lands on the matching picture.
Colour: per-channel mean/std transfer of the AI frames toward the real 3–7 s frames at strength 0.5 (as conform_clip.py --match).
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

W = Path(sys.argv[1]); AI = Path(sys.argv[2]); OUT = Path(sys.argv[3])
FW, FH, FPS = 1920, 1080, 25
UPRIGHT = "transpose=2"            # the clip was held landscape but tagged portrait


def read(path: Path, vf: str) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", vf, "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, FH, FW, 3)


real = read(W / "bake_full.mov", f"{UPRIGHT},scale={FW}:{FH},fps={FPS}")
SIGMA = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0     # soften the AI to the camera's sharpness (measured)
ai = read(AI, f"scale={FW}:{FH}," + (f"gblur=sigma={SIGMA}," if SIGMA else "") + f"fps={FPS}")
A0, B0 = 75, 175                                     # camera frames of still A (3.00 s) and still B (7.00 s)
small = lambda f: f[::8, ::8].astype(np.float32)
k = int(np.argmin([np.abs(small(f) - small(real[B0])).mean() for f in ai]))   # best AI match to still B
seg = ai[:k].astype(np.float32)

ref = real[A0:B0].astype(np.float32)
m_ai, s_ai = seg.reshape(-1, 3).mean(0), seg.reshape(-1, 3).std(0)
m_rf, s_rf = ref.reshape(-1, 3).mean(0), ref.reshape(-1, 3).std(0)
strength = 0.5
gain = 1 + strength * (s_rf / np.maximum(s_ai, 1e-3) - 1)
matched = np.clip((seg - m_ai) * gain + m_ai + strength * (m_rf - m_ai), 0, 255)
# Saturation to the camera's (what Premiere's shot match would do), around each pixel's luma.
sat = lambda x: float(np.mean((x.max(-1) - x.min(-1)) / np.maximum(x.max(-1), 1)))
s_gain = sat(ref[::10]) / max(sat(matched[::10]), 1e-3)
L = (matched @ np.array([0.2126, 0.7152, 0.0722], np.float32))[..., None]
matched = np.clip(L + (matched - L) * s_gain, 0, 255)
# 3-frame dissolves at both seams (motion-and-ai.md §3: never cut straight out of a gap fill).
D = 3
for i in range(D):
    w = (i + 1) / (D + 1)                                   # AI weight rising into the fill
    matched[i] = matched[i] * w + real[A0 + i] * (1 - w)
    v = (D - i) / (D + 1)                                   # AI weight falling out of the fill
    matched[k - D + i] = matched[k - D + i] * v + real[B0 - D + i] * (1 - v)
matched = matched.astype(np.uint8)

frames = np.concatenate([real[:A0], matched, real[B0:]])
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{FW}x{FH}", "-r", str(FPS),
                        "-i", "-", "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le",
                        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", str(OUT)],
                       stdin=subprocess.PIPE)
for f in frames:
    enc.stdin.write(f.tobytes())
enc.stdin.close(); enc.wait()

luma = lambda f: (small(f) @ np.array([0.2126, 0.7152, 0.0722], np.float32)) / 255
steps = [float(np.abs(luma(frames[i + 1]) - luma(frames[i])).mean()) for i in range(len(frames) - 1)]
real_steps = [float(np.abs(luma(real[i + 1]) - luma(real[i])).mean()) for i in range(len(real) - 1)]
cut_in, cut_out = A0 - 1, A0 + k - 1                 # step index across each splice
rep = {
    "ai_frames_used": k, "ai_seconds_used": round(k / FPS, 2), "replaces_seconds": 4.0,
    "output_frames": len(frames), "camera_frames": len(real),
    "seam_in_step (camera 2.96→AI)": round(steps[cut_in], 4),
    "seam_out_step (AI→camera 7.00)": round(steps[cut_out], 4),
    "camera_median_step": round(float(np.median(real_steps)), 4), "camera_max_step": round(float(np.max(real_steps)), 4),
    "ai_sat_before": round(sat(seg[::10]), 3), "ai_sat_after": round(sat(matched[::10].astype(np.float32)), 3),
    "camera_sat_3_to_7s": round(sat(ref[::10]), 3),
    "sat_gain": round(s_gain, 3), "blur_sigma": SIGMA, "dissolve_frames": D,
    "gain_rgb": [round(float(g), 3) for g in gain], "mean_shift_rgb": [round(float(x), 1) for x in strength * (m_rf - m_ai)],
}
print(json.dumps(rep, indent=1))
(W / "splice.json").write_text(json.dumps(rep, indent=1))
