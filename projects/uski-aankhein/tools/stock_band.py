#!/usr/bin/env python3
"""Bake the hook's V2 stock layer (Screen blend in Premiere): Pexels 4221987, real 10.00 s +104 frames, frame-for-frame at 25 fps.
v2 (review gate v1b row 7: "covers y 330-1300, torso, sleeve and ground screened over her whole face"): only the
instrument neck + bow (stock rows 0.28-0.62) as a narrow band on the eye line (y 768), vertical feather +-150 px,
the dark sleeve (x < 0.15) and the white cloth / mat (x > 0.80) faded out; desat/warm; fades in with the picture and
out 3.60-4.16 s. Output keeps the v1 name + frame count so Premiere's refreshMedia() swaps it in place.
Usage: python tools/stock_band.py
"""
import numpy as np, subprocess
from pathlib import Path
REEL = Path(__file__).resolve().parents[1]
src = REEL / 'raw/stock/pexels-4221987/pexels-4221987_1280x720_30fps.mp4'; out = REEL / 'renders/stock/stock_band_v2.mov'
N = 104; SC = 1.45; W = int(1080 * SC) // 2 * 2; H0 = int(W * 720 / 1280) // 2 * 2
r0, r1 = 0.28, 0.62; yc = 768; xoff = 120
p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '10.0', '-i', str(src), '-frames:v', str(N), '-vf', f'scale={W}:{H0}:flags=lanczos',
                    '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
F = np.frombuffer(p.stdout, np.uint8).reshape(N, H0, W, 3).astype(np.float32) / 255
a, b = int(r0 * H0), int(r1 * H0); band = F[:, a:b]; Hb = b - a
xx = np.linspace(0, 1, W); mx = np.clip(xx / 0.15, 0, 1) * np.clip((0.80 + 0.20 - xx) / 0.20, 0, 1)
mx = mx ** 1.2
yy = np.arange(1920)[:, None]; my = np.clip(1 - np.abs(yy - yc) / 150.0, 0, 1) ** 0.9
x0 = (1080 - W) // 2 + xoff; y0 = yc - Hb // 2
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', '1080x1920', '-r', '25', '-i', '-',
                        '-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                        '-colorspace', 'bt709', str(out)], stdin=subprocess.PIPE)
for i in range(N):
    x = band[i] * mx[None, :, None]
    l = x @ np.array([.2126, .7152, .0722]); x = np.clip(l[..., None] + (x - l[..., None]) * 0.55, 0, 1)
    x = np.clip((x - 0.12) / 0.88, 0, 1) * np.array([1.0, .88, .70])
    c = np.zeros((1920, 1080, 3), np.float32); xs, xe = max(x0, 0), min(x0 + W, 1080)
    c[y0:y0 + Hb, xs:xe] = x[:, xs - x0:xe - x0]; c *= my[..., None]
    t = i / 25; c *= (np.clip((4.16 - t) / 0.56, 0, 1) if t > 3.6 else 1.0) * np.clip(t / 0.3, 0, 1)
    enc.stdin.write((c * 65535).astype('<u2').tobytes())
enc.stdin.close(); enc.wait(); print('band v2', W, Hb, 'rows', r0, r1, 'frames', N)
