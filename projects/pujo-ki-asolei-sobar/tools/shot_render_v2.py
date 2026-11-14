#!/usr/bin/env python3
"""Round 2 shot renderer (director: "bokeh not ok, render without; correction, stability and clarity need to improve").

  4K source -> [punch-in crop] -> temporal+spatial denoise (hqdn3d, at 4K) -> lanczos down to 1188x2112 (10 % margin)
  -> STABILISE: phase-correlation translation per frame, camera path smoothed (gaussian), correction crop 1080x1920
     taken from the margin (no upscaling, no resolution loss)
  -> CORRECTION: white balance from near-neutral (low-chroma) pixels + per-shot tonal match (p02/p50/p98 -> targets),
     constants per shot measured on the frames that are on screen
  -> CLARITY: fine detail sharpen + local-contrast "clarity" on luminance
  -> optional lens bokeh (off by default) -> sepia film look -> halation, vignette, finer grain -> shared floor + luma match
  -> ProRes 422 HQ 1080x1920 @ 30 + source audio, 0.3 s handles.
Usage: shot_render_v2.py <n> [--ver v2] [--bokeh]
"""
import json, subprocess, sys, time, tempfile
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import sepia_look as sl  # noqa: E402
from preview_sepia_bokeh_lib import optical  # noqa: E402

n = sys.argv[1]
VER = sys.argv[sys.argv.index("--ver") + 1] if "--ver" in sys.argv else "v2"
EDLV = sys.argv[sys.argv.index("--edl") + 1] if "--edl" in sys.argv else "v2"
BOKEH = "--bokeh" in sys.argv
edl = json.loads((REEL / "analysis" / f"edl_{EDLV}.json").read_text()); s = next(x for x in edl["shots"] if x["n"] == n)
f = json.loads((REEL / "analysis" / f"focus_{EDLV}.json").read_text())[n]
src = next((REEL / "raw" / "b-roll").glob(f"*_{s['clip']}.mov"))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout)
handle = 0.3; t0 = max(0.0, s["in"] - handle); t1 = min(dur - 0.04, s["out"] + handle)
out_dir = REEL / "renders" / "final_shots"; out_dir.mkdir(parents=True, exist_ok=True)
name = f"{int(n):02d}_{s['clip']}_{VER}"; mov = out_dir / f"{name}.mov"
W, H = 1080, 1920
MG = f.get("stab_margin", 1.10)                                     # 1.10 -> 54 / 96 px margin; shakier shots more
MW, MH = int(round(W * MG / 2)) * 2, int(round(H * MG / 2)) * 2; MW -= MW % 4; MH -= MH % 4
MX, MY = (MW - W) // 2, (MH - H) // 2
T = time.time()

# 1) decode: crop -> denoise at 4K -> supersample down to the margin frame
dn = f.get("denoise", "hqdn3d=1.5:1.2:6:4.5")
vf = (f"crop={f['crop']}," if f.get("crop") else "") + f"{dn},scale={MW}:{MH}:flags=lanczos,fps=30"
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", str(src), "-an", "-vf", vf,
                      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
frames = np.frombuffer(raw, np.uint8).reshape(-1, MH, MW, 3); N = len(frames)
print(f"▸ {name}: src {t0:.2f}-{t1:.2f}, {N} frames, decode {time.time() - T:.0f}s", flush=True)
pa = int(round((s["in"] - t0) * 30)); pb = min(N - 1, pa + (s["endF"] - s["startF"]) - 1)

# 2) stabilise: phase correlation on a quarter-res luma, smoothed camera path
ROI = f.get("stab_roi")      # [y0, y1, x0, x1] fractions: estimate motion only on a static background region
def gray_small(fr):
    g = fr.astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)
    g = g.reshape(MH // 4, 4, MW // 4, 4).mean(axis=(1, 3))
    if ROI: g = g[int(ROI[0] * g.shape[0]):int(ROI[1] * g.shape[0]), int(ROI[2] * g.shape[1]):int(ROI[3] * g.shape[1])]
    return g
_g0 = gray_small(frames[0]); win = np.outer(np.hanning(_g0.shape[0]), np.hanning(_g0.shape[1])).astype(np.float32)
def shift_between(a, b):
    A = np.fft.fft2((a - a.mean()) * win); B = np.fft.fft2((b - b.mean()) * win)
    R = A * np.conj(B); R /= np.abs(R) + 1e-9; r = np.fft.ifft2(R).real
    py, px = np.unravel_index(np.argmax(r), r.shape)
    def sub(c, m, axis):
        i0, i1, i2 = (c - 1) % m, c, (c + 1) % m
        v0, v1, v2 = (r[i0, px], r[i1, px], r[i2, px]) if axis == 0 else (r[py, i0], r[py, i1], r[py, i2])
        den = v0 - 2 * v1 + v2; d = 0.5 * (v0 - v2) / den if abs(den) > 1e-9 else 0
        c = c + d; return c - m if c > m / 2 else c
    return sub(py, r.shape[0], 0) * 4, sub(px, r.shape[1], 1) * 4       # (dy, dx) of a relative to b, full margin-res px
smalls = [gray_small(fr) for fr in frames]
d = np.array([[0.0, 0.0]] + [shift_between(smalls[i], smalls[i - 1]) for i in range(1, N)])
path = np.cumsum(d, axis=0)                                            # camera path (content position)
sigma = f.get("stab_sigma", 18)
smooth = np.stack([ndimage.gaussian_filter1d(path[:, k], sigma, mode="nearest") for k in range(2)], 1)
if f.get("stab_lock"): smooth[:] = path[pa:pb + 1].mean(axis=0)        # locked-off hold
if f.get("stab_off"): smooth = path.copy()
corr = smooth - path                                                   # shift to apply to each frame
corr[:, 0] = np.clip(corr[:, 0], -MY + 2, MY - 2); corr[:, 1] = np.clip(corr[:, 1], -MX + 2, MX - 2)
raw_jit = float(np.sqrt(np.mean((path[pa:pb + 1] - smooth[pa:pb + 1]) ** 2)))
print(f"  stabilise: raw jitter {raw_jit:.2f}px (margin-res), max corr {np.abs(corr[pa:pb+1]).max():.1f}px", flush=True)

def stab(fr, i):
    dy, dx = corr[i]; iy, ix = int(np.floor(dy)), int(np.floor(dx)); fy, fx = dy - iy, dx - ix
    y0, x0 = MY - iy - 1, MX - ix - 1
    blk = fr[y0:y0 + H + 1, x0:x0 + W + 1].astype(np.float32) / 255
    return (blk[1:, 1:] * (1 - fy) * (1 - fx) + blk[:-1, 1:] * fy * (1 - fx) + blk[1:, :-1] * (1 - fy) * fx + blk[:-1, :-1] * fy * fx)

# 3) correction constants from on-screen frames
def wb_gains(x):
    y = sl.luma(x); mx = x.max(-1); mn = x.min(-1); ch = (mx - mn) / np.maximum(mx, 1e-4)
    m = (y > 0.12) & (y < 0.85)
    if m.sum() < 1000: m = y > 0.03
    cut = np.percentile(ch[m], 30); m = m & (ch <= cut)                 # near-neutral pixels only (walls, cloth, skin shadows)
    R, G, B = (np.median(x[..., c][m]) for c in range(3))
    return np.array([(G / max(R, 1e-4)) ** 0.9, 1.0, (G / max(B, 1e-4)) ** 0.9])
samp = [stab(frames[i], i) for i in np.linspace(pa, pb, 6).astype(int)]
wb = np.median([wb_gains(x) for x in samp], axis=0)
ys = np.concatenate([sl.luma(np.clip(x * wb, 0, 1)).ravel()[::7] for x in samp])
p02, p50, p98 = np.percentile(ys, [2, 50, 98])
TIN = np.array([0.0, p02, p50, p98, 1.0]); TOUT = np.array([0.0, 0.035, 0.30, 0.86, 0.97])
TIN = np.maximum.accumulate(TIN + np.arange(5) * 1e-4)
def correct(x):
    x = np.clip(x * wb, 0, 1.2); y = np.clip(sl.luma(x), 1e-5, None)
    y2 = np.interp(y, TIN, TOUT); return np.clip(x * (y2 / y)[..., None], 0, 1)
print(f"  correction: wb {np.round(wb, 3)}, tonal p02/p50/p98 {p02:.3f}/{p50:.3f}/{p98:.3f}", flush=True)

# 4) clarity on luminance
CL = f.get("clarity", (0.55, 0.20))
def clarity(x):
    y = sl.luma(x)
    det = y - ndimage.gaussian_filter(y, 1.1); loc = y - ndimage.gaussian_filter(y, 22)
    y2 = np.clip(y + CL[0] * det + CL[1] * loc, 0, 1)
    return np.clip(x * (y2 / np.maximum(y, 1e-4))[..., None], 0, 1)

TARGET, FLOOR = 0.27, 0.03
lensmod = None
if BOKEH:
    import lens as lensmod  # noqa: E402
def treat(i, gain=1.0):
    x = clarity(correct(stab(frames[i], i)))
    o = optical(sl.look(x), seed=i, hal=f.get("hal", 0.16), vig=f.get("vig", 0.24), grain=f.get("grain", 0.012))   # finer grain than v1 (clarity)
    o = FLOOR + (o - FLOOR) * gain
    return np.clip(o, FLOOR - 0.005, 1)
mids = [treat(i) for i in np.linspace(pa, pb, 5).astype(int)]
gain = float(np.clip((TARGET - FLOOR) / max(np.mean([sl.luma(m).mean() for m in mids]) - FLOOR, 1e-3), 0.75, 1.6))
print(f"  luma gain {gain:.3f}", flush=True)

enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", str(out_dir / f"{name}_v.mov")], stdin=subprocess.PIPE)
for i in range(N):
    enc.stdin.write((treat(i, gain) * 255 + 0.5).clip(0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out_dir / f"{name}_v.mov"), "-ss", f"{t0:.3f}", "-t", f"{N / 30:.3f}", "-i", str(src),
                "-map", "0:v", "-map", "1:a?", "-c:v", "copy", "-c:a", "pcm_s16le", "-shortest", str(mov)], check=True)
(out_dir / f"{name}_v.mov").unlink()
rec = {"n": n, "clip": s["clip"], "file": mov.name, "src_start": round(t0, 4), "frames": N, "place_in": round(s["in"] - t0, 4),
       "place_out": round(s["in"] - t0 + (s["endF"] - s["startF"]) / 30, 4), "wb": [round(float(v), 4) for v in wb],
       "tonal_in": [round(float(v), 4) for v in (p02, p50, p98)], "raw_jitter_px": round(raw_jit, 2), "luma_gain": round(gain, 3),
       "bokeh": BOKEH, "secs": round(time.time() - T)}
(out_dir / f"{name}.json").write_text(json.dumps(rec, indent=1)); print(f"✓ {name} {N} frames in {rec['secs']}s", flush=True)
