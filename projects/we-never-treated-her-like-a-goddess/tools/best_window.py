#!/usr/bin/env python3
"""Find the sharpest, steadiest window of a clip *inside the crop it will be shown at*.

Usage: best_window.py <source.mov> <t0> <t1> <window_s> <m> <u0> <v0>
Scores every frame of [t0, t1] by Laplacian variance of the crop region (m = magnification of the fit frame,
u0/v0 = crop centre, 0..1) and by mean frame difference; prints the 5 windows with the highest worst-frame sharpness
(sharpness normalised to the clip's median), plus their mean frame difference."""
import subprocess, sys
import numpy as np
src, t0, t1, L, m, u0, v0 = sys.argv[1], *map(float, sys.argv[2:8])
W, H = 540, 960
raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t0), '-to', str(t1), '-i', src, '-vf', f'scale={W}:{H},format=gray',
                      '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True, check=True).stdout
v = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
cw, ch = int(W / m), int(H / m); x0 = int(W * u0 - cw / 2); y0 = int(H * v0 - ch / 2)
c = v[:, y0:y0 + ch, x0:x0 + cw]
lap = c[:, 1:-1, 1:-1] * 4 - c[:, :-2, 1:-1] - c[:, 2:, 1:-1] - c[:, 1:-1, :-2] - c[:, 1:-1, 2:]
s = lap.reshape(len(c), -1).var(axis=1); s = s / np.median(s)
d = np.r_[0, np.abs(np.diff(c, axis=0)).mean(axis=(1, 2))]
n = int(round(L * 25)); rows = []
for i in range(0, len(s) - n + 1):
    rows.append((s[i:i + n].min(), s[i:i + n].mean(), d[i + 1:i + n].mean(), t0 + i / 25))
rows.sort(reverse=True)
for mn, me, dd, t in rows[:5]:
    print(f'in {t:6.2f}  worst {mn:.2f}  mean {me:.2f}  move {dd:5.1f}')
