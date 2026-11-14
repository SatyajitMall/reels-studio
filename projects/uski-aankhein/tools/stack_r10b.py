#!/usr/bin/env python3
"""Review v10 #1 (B softer than A at 100 %): the 21-frame 1x stack lost ~35 % of the high-frequency energy of a single frame
(Laplacian var 0.00108 vs 0.00165): sub-pixel cubic shifts at 1x and residual misalignment average detail away.
Shift-and-add instead: keep the sharpest K frames, upsample each 2x, align at 2x, trimmed mean at 2x; the push then resamples once.
stack2x(src, track, t_s, cw0, n, keep) -> PIL image at 2x the crop size (eyes at u .5, v .40 as box_for)."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import bake_r5 as R, stack_r9d as S
B = R.B
L = lambda x: x @ np.array([.2126, .7152, .0722], np.float32)

def stack2x(src, track, t_s, cw0, n=21, keep=9, fps=30):
    j0 = int(round(t_s * fps)); js = [j for j in range(j0 - n // 2, j0 + n // 2 + 1) if 0 <= j < len(track["ex"])]
    frames = list(B.frames(src, js[0] / fps, len(js), False, R.W4, R.H4))
    crops = [np.asarray(im.crop(tuple(round(v) for v in R.box_for(track["ex"][j], track["ey"][j], cw0)))).astype(np.float32) / 255 for j, im in zip(js, frames)]
    h = min(c.shape[0] for c in crops); w = min(c.shape[1] for c in crops); crops = [c[:h, :w] for c in crops]
    reg = lambda x: x[int(.2 * h):int(.65 * h), int(.15 * w):int(.85 * w)]
    sharp = [float(ndimage.laplace(L(reg(c))).var()) for c in crops]
    order = np.argsort(sharp)[::-1][:keep]; sel = [crops[i] for i in order]; ref = sel[0]
    up = lambda x: np.asarray(Image.fromarray((np.clip(x, 0, 1) * 255 + .5).astype(np.uint8)).resize((w * 2, h * 2), Image.LANCZOS)).astype(np.float32) / 255
    ref2 = up(ref); out = []
    for c in sel:
        dy, dx = S.phase_shift(L(ref), L(c)); c2 = up(c)
        out.append(np.stack([ndimage.shift(c2[..., k], (2 * dy, 2 * dx), order=1, mode="nearest") for k in range(3)], -1))
    a = np.sort(np.stack(out), 0); k = max(1, len(out) // 5); st = a[k:len(out) - k].mean(0)
    m = 8; st[:m] = st[m]; st[-m:] = st[-m - 1]; st[:, :m] = st[:, m:m + 1]; st[:, -m:] = st[:, -m - 1:-m]   # edge rows from the shifts
    return Image.fromarray((np.clip(st, 0, 1) * 255 + .5).astype(np.uint8)), {"sharp_single": [min(sharp), float(np.median(sharp)), max(sharp)], "kept": [js[i] for i in order]}
