#!/usr/bin/env python3
"""Mains-flicker removal (director, 2026-10-23: 1/60 s shutter under 50 Hz mains).

100 Hz light flicker sampled at 30 fps aliases to 10 Hz: a 3-frame brightness cycle, global or as rolling bands
(rolling shutter), and different per lamp.  ffmpeg's `deflicker` only evens out the whole-frame mean, so bands and
local lamps survive.  Here, per tile (default 32 rows x 12 columns, linear light):
  log tile luma -> remove the slow trend (9-frame box = 3 cycles, so it holds no 10 Hz) -> sliding lock-in on the
  3-frame cycle (gaussian window, sigma 5 frames) gives the local 10 Hz amplitude + phase, which may drift (VFR clips)
  -> Wiener shrink by how much of the residual is 10 Hz (people moving through a tile are broadband, so they barely
  count) -> flicker estimate f(t) per tile, smoothed across tiles; 2 passes (the second recovers what the shrink and
  smoothing left); clamped to +-15 % (a bare bulb measured 13 %), upsampled bicubic
  -> each frame x gain exp(-f) in linear light (applied as exp(-f/2.2) on the code values).
Only brightness changes, smoothly in space, so no ghosting.  Frames, handles, audio and BT.709 tags are kept.
Usage: deflicker.py <shot n> <in suffix> <out suffix> [--clip Cnnn] [--grid 32x12] [--clamp 0.15] [--iters 2] [--sps 0.6] [--sig 5] [--wfloor 0] [--global] [--robust] [--display]   e.g. deflicker.py 6 v5b v6
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from scipy import ndimage

REEL = Path(__file__).resolve().parents[1]; R = REEL / "renders" / "final_shots"
n, SIN, SOUT = sys.argv[1], sys.argv[2], sys.argv[3]
CLIP = sys.argv[sys.argv.index("--clip") + 1] if "--clip" in sys.argv else "*"
js = next(R.glob(f"{int(n):02d}_{CLIP}_{SIN}.json")); r = json.loads(js.read_text()); src = R / r["file"]
def opt(k, d): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
W, H = 1080, 1920; GY, GX = map(int, opt("--grid", "32x12").split("x")); CLAMP = float(opt("--clamp", 0.15)); ITERS = int(opt("--iters", 2)); SPS = float(opt("--sps", 0.6))
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3); N = len(F)

# tile luma series (linear light)
DISPLAY = "--display" in sys.argv     # round 13: estimate + correct in display (code-value) brightness, what the viewer sees
lut = ((np.arange(256) / 255.0) ** (1.0 if DISPLAY else 2.2)).astype(np.float32)
T = np.empty((N, GY, GX), np.float32)
ROBUST = "--robust" in sys.argv
if ROBUST:   # round 13: estimate from pixels that can flicker: a fixed mask from the clip's median frame drops clipped highlights
             # (bulbs, burnt walls: constant, they diluted the estimate in linear light) and near-black pixels (noise)
    gm = np.median(F[::max(1, N // 15)].max(-1), axis=0)
    VM = ((gm > 12) & (gm < 232)).astype(np.float32)
    vcount = VM.reshape(GY, H // GY, GX, W // GX).sum((1, 3))
for i in range(N):
    y = lut[F[i]] @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    if ROBUST:
        s_m = (y * VM).reshape(GY, H // GY, GX, W // GX).sum((1, 3)); s_a = y.reshape(GY, H // GY, GX, W // GX).mean((1, 3))
        T[i] = np.where(vcount > 0.1 * (H // GY) * (W // GX), s_m / np.maximum(vcount, 1), s_a)
    else:
        T[i] = y.reshape(GY, H // GY, GX, W // GX).mean((1, 3))
L0 = np.log(np.maximum(T, 1e-4))
t = np.arange(N, dtype=np.float32)[:, None, None]; c = np.cos(2 * np.pi * t / 3); s = np.sin(2 * np.pi * t / 3)
SIG = float(opt("--sig", 5.0)); WFLOOR = float(opt("--wfloor", 0.0)); GLOBAL = "--global" in sys.argv
norm = ndimage.gaussian_filter1d(np.ones(N, np.float32), SIG, mode="constant")[:, None, None]
lp = lambda x: ndimage.gaussian_filter1d(x, SIG, axis=0, mode="constant") / norm
f = np.zeros_like(L0)
for it in range(ITERS):                                 # re-estimate on the corrected series: recovers what the shrink / smoothing left
    L = L0 - f
    res = L - ndimage.uniform_filter1d(L, 9, axis=0, mode="nearest")
    a = 2 * lp(res * c); b = 2 * lp(res * s)
    A2 = (a ** 2 + b ** 2) / 2                          # power of the 10 Hz component
    P = lp(res ** 2)                                    # total residual power
    wien = np.clip(A2 / np.maximum(P, 1e-9), 0, 1) ** 0.5   # 1 = pure flicker, 0 = all motion/noise
    wien = np.maximum(wien, WFLOOR)                     # round 13: a floor so a small leftover flicker isn't shrunk away as 'noise'
    df = (a * c + b * s) * wien
    f = np.clip(f + ndimage.gaussian_filter(df, (0, SPS, SPS), mode="nearest"), -CLAMP, CLAMP)

if GLOBAL:   # round 13: remove the frame-wide 3-frame cycle left after the tile pass (coherent lamp flicker; no shrink, the global series is robust to motion)
    for _ in range(3):
        Lg = np.log(np.maximum((T * np.exp(-f)).mean((1, 2)), 1e-5))
        rg = Lg - ndimage.uniform_filter1d(Lg, 9, mode="nearest"); tt = np.arange(N, dtype=np.float32)
        cg, sg = np.cos(2 * np.pi * tt / 3), np.sin(2 * np.pi * tt / 3); ng = ndimage.gaussian_filter1d(np.ones(N, np.float32), SIG, mode="constant")
        ag = 2 * ndimage.gaussian_filter1d(rg * cg, SIG, mode="constant") / ng; bg = 2 * ndimage.gaussian_filter1d(rg * sg, SIG, mode="constant") / ng
        f = np.clip(f + (ag * cg + bg * sg)[:, None, None], -CLAMP, CLAMP)
# per-frame gain map, applied on code values (gamma 2.2)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-vf", "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv",
                        "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-colorspace", "bt709", str(R / f"_tmp_df_{n}.mov")], stdin=subprocess.PIPE)
zy, zx = H / GY, W / GX
for i in range(N):
    g = np.exp(-f[i] / (1.0 if DISPLAY else 2.2))
    G = ndimage.zoom(np.pad(g, 1, mode="edge"), (zy, zx), order=3)            # pad so the edges interpolate flat
    oy, ox = int(round(zy)), int(round(zx)); G = G[oy:oy + H, ox:ox + W]
    o = F[i].astype(np.float32) * G[..., None]
    enc.stdin.write((np.clip(o * 257, 0, 65535) + 0.5).astype(np.uint16).tobytes())
enc.stdin.close(); enc.wait()
name = js.name.replace(f"_{SIN}.json", f"_{SOUT}")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(R / f"_tmp_df_{n}.mov"), "-i", str(src), "-map", "0:v", "-map", "1:a?", "-c", "copy",
                "-movflags", "+write_colr", str(R / f"{name}.mov")], check=True)
(R / f"_tmp_df_{n}.mov").unlink()
st = {"tiles": [GY, GX], "sigma": SIG, "iters": ITERS, "clamp": CLAMP, "sps": SPS, "f_rms_pct": round(float(100 * np.sqrt((f ** 2).mean())), 3), "f_max_pct": round(float(100 * np.abs(f).max()), 2),
      "wiener_mean": round(float(wien.mean()), 3), "from": r["file"]}
np.savez_compressed(REEL / "analysis/flicker" / f"f_{name}.npz", f=f, T=T)
(R / f"{name}.json").write_text(json.dumps(dict(r, file=f"{name}.mov", deflicker=st), indent=1))
print(f"✓ {name}  {N} frames  correction rms {st['f_rms_pct']}%  max {st['f_max_pct']}%  wiener {st['wiener_mean']}", flush=True)
