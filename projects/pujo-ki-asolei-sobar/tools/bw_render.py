#!/usr/bin/env python3
"""Black-and-white alternate (director, 2026-10-22: "one version in black and white, only the first Durga in gold").

All shots: film B&W from the graded v5 renders: red-leaning channel mix (skin reads luminous), gentle S-curve for
contrast, luma matched to the colour version.  Shot 1 (--isolate): colour kept on the Durga's gold only: soft hue/sat
key for gold/yellow, inside the idol region, minus a per-frame person matte (priest and attendant go grey).
Usage: bw_render.py <shot n> [--isolate] [--src v6 --out bw6]   (default: from v5b / v5, written as _bw)
"""
import json, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from scipy import ndimage

REEL = Path(__file__).resolve().parents[1]; R = REEL / "renders" / "final_shots"
n = sys.argv[1]; ISO = "--isolate" in sys.argv
SRC = sys.argv[sys.argv.index("--src") + 1] if "--src" in sys.argv else None; OUTS = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "bw"
j = next(R.glob(f"{int(n):02d}_*_{SRC}.json")) if SRC else (next(R.glob(f"{int(n):02d}_*_v5b.json"), None) or next(R.glob(f"{int(n):02d}_*_v5.json")))
r = json.loads(j.read_text()); src = R / r["file"]
W, H = 1080, 1920
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3); N = len(F)
MIX = np.array([0.40, 0.50, 0.10], np.float32)
TX = np.array([0.0, 0.06, 0.18, 0.35, 0.55, 0.75, 0.90, 1.0]); TY = np.array([0.02, 0.035, 0.13, 0.31, 0.56, 0.79, 0.92, 0.97])

def bw(x):
    y = x @ MIX; return np.interp(y, TX, TY)

alphas = None
if ISO:
    with tempfile.TemporaryDirectory(prefix="bw_") as td:
        px = Path(td) / "p.mp4"
        pe = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                               "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(px)], stdin=subprocess.PIPE)
        pe.stdin.write(F.tobytes()); pe.stdin.close(); pe.wait()
        rr = subprocess.run(["npx", "hyperframes", "remove-background", str(px), "-o", str(Path(td) / "fg.mov"), "--device", "cpu"], capture_output=True, text=True, cwd=td)
        araw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(Path(td) / "fg.mov"), "-vf", "alphaextract", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
        alphas = np.frombuffer(araw, np.uint8).reshape(-1, H, W)
    print(f"  person mattes {len(alphas)} frames", flush=True)
    yy = np.arange(H, dtype=np.float32)[:, None]
    region = (np.clip((yy - 230) / 60, 0, 1) * np.clip((1520 - yy) / 60, 0, 1)) * np.ones((1, W), np.float32)   # idol band, feathered

def gold_weight(x):
    mx = x.max(-1); mn = x.min(-1); d = np.maximum(mx - mn, 1e-6); s = (mx - mn) / np.maximum(mx, 1e-6)
    r_, g_, b_ = x[..., 0], x[..., 1], x[..., 2]
    h = np.where(mx == r_, ((g_ - b_) / d) % 6, np.where(mx == g_, (b_ - r_) / d + 2, (r_ - g_) / d + 4)) * 60
    wh = np.clip((1 - np.abs(h - 56) / 32) * 1.4, 0, 1)                # gold after the grade sits at 40-80 deg (measured)
    ws = np.clip((s - 0.08) / 0.10, 0, 1); wv = np.clip((mx - 0.15) / 0.10, 0, 1)
    return wh * ws * wv

enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-vf", "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv",
                        "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-colorspace", "bt709", str(R / f"_tmp_bw_{n}.mov")], stdin=subprocess.PIPE)
cov = []
for i in range(N):
    x = F[i].astype(np.float32) / 255; g = bw(x)
    o = np.repeat(g[..., None], 3, -1)
    if ISO:
        a = alphas[min(i, len(alphas) - 1)].astype(np.float32) / 255
        person = ndimage.gaussian_filter(ndimage.grey_dilation(a, size=(11, 11)), 4)
        m = gold_weight(x) * region * (1 - person)
        m = ndimage.gaussian_filter(m, 1.5)
        GOLD = np.array([1.0, 0.78, 0.36], np.float32); GOLD = GOLD / (GOLD @ np.array([0.2126, 0.7152, 0.0722]))
        col = np.clip(g[..., None] * GOLD * 1.0, 0, 1)                      # true gold at the B&W luminance
        col = np.clip(0.75 * col + 0.25 * x * (g / np.maximum(x @ np.array([0.2126, 0.7152, 0.0722]), 1e-4))[..., None], 0, 1)  # keep some original texture colour
        o = o * (1 - m[..., None]) + np.clip(col, 0, 1) * m[..., None]; cov.append(float((m > 0.5).mean()))
    enc.stdin.write((np.clip(o, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait()
name = f"{int(n):02d}_{r['clip']}_{OUTS}"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(R / f"_tmp_bw_{n}.mov"), "-i", str(src), "-map", "0:v", "-map", "1:a?", "-c", "copy",
                "-movflags", "+write_colr", str(R / f"{name}.mov")], check=True)
(R / f"_tmp_bw_{n}.mov").unlink()
r2 = dict(r, file=f"{name}.mov", bw=True, gold_isolate=ISO, gold_coverage=round(float(np.mean(cov)), 3) if cov else None)
(R / f"{name}.json").write_text(json.dumps(r2, indent=1)); print(f"✓ {name} {N} frames" + (f", gold coverage {np.mean(cov):.3f}" if cov else ""), flush=True)
