"""Per-frame sharpness (Laplacian energy) and camera shift of an upright 4:3 crop of a bake, to pick a window free of
bumps / motion-blur dips; reel-local.  .venv/bin/python -I .../clean_window.py <bake.mov> [crop_vf]"""
import sys
from pathlib import Path
import numpy as np
from scipy.ndimage import laplace
sys.path.insert(0, str(Path(__file__).resolve().parent))
import motion_audit as ma
clip = sys.argv[1]; vf = sys.argv[2] if len(sys.argv) > 2 else "transpose=2,crop=ih*4/3:ih"
fr = ma.frames(clip, vf, 480, 360)
sh = np.array([np.abs(laplace(f)).mean() for f in fr])
win = np.outer(np.hanning(360), np.hanning(480)).astype(np.float32)
d = [ma.shift(fr[i], fr[i + 1], win) for i in range(len(fr) - 1)]
med = np.median(sh)
for i in range(len(fr)):
    dx, dy = (d[i - 1][0], d[i - 1][1]) if i else (0, 0)
    flag = " <-- soft" if sh[i] < 0.75 * med else ""
    print(f"{i:3d} {i/25:5.2f}s sharp {sh[i]/med:4.2f} shift {dx*1080/480:6.1f} {dy*1080/480:6.1f}{flag}")
