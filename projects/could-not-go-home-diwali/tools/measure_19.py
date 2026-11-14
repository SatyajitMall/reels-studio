"""Measure shot 19 the way review_v4f did: the 4:3 window, L6 text block excluded, full-range RGB.
Usage (reel folder): ../../.venv/bin/python tools/measure_19.py <file> <frame> [<file> <frame> ...]"""
import subprocess, sys
import numpy as np


def fr(f, n):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", f"select=eq(n\\,{n})", "-frames:v", "1", "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(1920, 1080, 3).astype(float)[505:1315]


args = sys.argv[1:]
for f, n in zip(args[::2], args[1::2]):
    a = fr(f, int(n)); m = np.ones(a.shape[:2], bool); m[810 - 170:, :560] = False
    mx = a.max(2); y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    s = np.where(mx > 0, (mx - a.min(2)) / np.maximum(mx, 1), 0)
    print(f"{f.split('/')[-1]} @{n}: maxch max {mx[m].max():.0f} p99.9 {np.percentile(mx[m], 99.9):.0f} | luma p1 {np.percentile(y[m], 1):.0f} "
          f"p50 {np.percentile(y[m], 50):.0f} mean {y[m].mean():.1f} | face/shirt p99 {np.percentile(y[100:560, 0:640], 99):.0f} "
          f"| sat(y>30) {s[m & (y > 30)].mean():.2f} all {s[m].mean():.2f}")
