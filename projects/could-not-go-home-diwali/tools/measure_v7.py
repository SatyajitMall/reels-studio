"""v7 grade check (reel-local, 2026-11-12): per-shot numbers inside the 16:9 window, text boxes masked, for a test render.
Usage: ../../.venv/bin/python tools/measure_v7.py <video> name:f0-f1 [name:f0-f1 ...] [--mask x0,y0,x1,y1 ...]"""
import subprocess, sys
import numpy as np
a = sys.argv[1:]; src = a[0]
shots = [x for x in a[1:] if ":" in x and not x.startswith("--")]
masks = [tuple(map(int, a[i + 1].split(","))) for i, x in enumerate(a) if x == "--mask"]
b = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", "crop=1080:608:0:606,scale=540:304", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
fr = np.frombuffer(b, np.uint8).reshape(-1, 304, 540, 3).astype(np.float32) / 255
m = np.ones((304, 540), bool)
for x0, y0, x1, y1 in masks: m[max(0, (y0 - 606) // 2):max(0, (y1 - 606) // 2), x0 // 2:x1 // 2] = False
for s in shots:
    n, r = s.split(":"); f0, f1 = map(int, r.split("-"))
    px = fr[f0 + 2:f1 - 2][:, m]
    y = px @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    mx, mn = px.max(-1), px.min(-1); sat = np.where(mx > 0.02, (mx - mn) / np.maximum(mx, 1e-6), 0)
    print(f"{n:28s} luma mean {y.mean():.3f}  p1 {np.percentile(y,1):.3f}  p50 {np.median(y):.3f}  p99 {np.percentile(y,99):.3f}  "
          f"sat {sat.mean():.3f}  R-B {(px[...,0]-px[...,2]).mean()*255:+.1f}  G-mag {(px[...,1]-(px[...,0]+px[...,2])/2).mean()*255:+.1f}")
