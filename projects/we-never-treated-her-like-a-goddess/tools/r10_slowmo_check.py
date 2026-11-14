#!/usr/bin/env python3
"""Round 10: check an export's slowed shots. For each span: consecutive-frame mean |diff| (a repeated frame = no interpolation,
a spike = a warp/jump), and a grid of every frame (or every 2nd) for eyeballing Optical Flow warping.
Usage (reel folder): ../../.venv/bin/python tools/r10_slowmo_check.py <video> <tag> -> analysis/r10/<tag>_<shot>_grid.jpg"""
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

video, tag = sys.argv[1], sys.argv[2]
SPANS = [("C051", 205, 260, 1), ("C035", 308, 414, 2)]
W, H = 270, 480
font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)


def frames(a, b):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a / 25:.3f}", "-i", video, "-frames:v", str(b - a), "-vf", f"scale={W}:{H}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


for name, a, b, step in SPANS:
    f = frames(a, b).astype(np.float32) / 255
    d = np.abs(np.diff(f, axis=0)).mean(axis=(1, 2, 3))
    print(name, "frames", a, "-", b - 1)
    print("  diffs", " ".join(f"{a + i + 1}:{x:.3f}" for i, x in enumerate(d)))
    inner = d[4:-5] if len(d) > 10 else d
    print(f"  inside span: min {inner.min():.4f} median {np.median(inner):.4f} max {inner.max():.4f}; repeats(<0.002) {(inner < 0.002).sum()}")
    sel = list(range(4, len(f) - 4, step)); cols = 8; rows = (len(sel) + cols - 1) // cols
    tw, th = 180, 320; g = Image.new("RGB", (cols * (tw + 2), rows * (th + 20)), (20, 20, 20)); dr = ImageDraw.Draw(g)
    for j, i in enumerate(sel):
        x, y = (j % cols) * (tw + 2), (j // cols) * (th + 20)
        g.paste(Image.fromarray((f[i] * 255).astype(np.uint8)).resize((tw, th)), (x, y)); dr.text((x + 4, y + th + 2), str(a + i), fill=(220, 220, 220), font=font)
    g.save(f"analysis/r10/{tag}_{name}_grid.jpg", quality=85)
