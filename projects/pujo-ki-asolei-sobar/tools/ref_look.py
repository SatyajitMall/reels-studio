#!/usr/bin/env python3
"""Reference-matched look (preview on stills + exportable .cube), from the reference reel's measured grade.

Reference (analysis/ref_grade, 11 frames, medians): luma 0.25, p02 0.02, p50 0.19, p98 0.89, crushed ~10 %,
saturation 0.55, shadows R/G 1.02 B/G 0.53 (warm olive), mids R/G 1.06 B/G 0.65 (amber), highlights R/G 0.98 B/G 0.75.

Pipeline per frame:
  1. normalise (stands in for the per-clip Lumetri primary): partial grey balance to neutral mids + exposure to luma 0.30
  2. LOOK (pixelwise, = the .cube): low-key filmic tone curve + 3-way warm/olive balance + saturation trim
  3. optical (not in the .cube; done on V4 / adjustment layers in Premiere): highlight halation + soft vignette
Usage:
  ref_look.py preview <in_dir> <out_dir>      graded stills + stats vs the reference
  ref_look.py cube <out.cube>                 33^3 LUT of step 2 (for Lumetri > Creative > Look)
"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

REF = {"luma": 0.254, "p50": 0.188, "sat": 0.545, "shad": (1.019, 0.533), "mid": (1.057, 0.654), "high": (0.976, 0.745)}
# tone curve: input luma -> output luma (low-key, deep but not crushed blacks, rolled-off highlights)
TX = np.array([0.0, 0.04, 0.12, 0.25, 0.40, 0.60, 0.80, 1.00])
TY = np.array([0.0, 0.012, 0.072, 0.198, 0.345, 0.560, 0.800, 0.945])
# 3-way channel gains (R, G, B) per band, applied after the curve
GAIN = {"shad": (1.00, 1.0, 0.36), "mid": (1.06, 1.0, 0.72), "high": (1.00, 1.0, 0.88)}
SAT = 1.12

def luma(x): return 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]

def look(x):
    """Pixelwise look on normalised RGB in [0,1]. Also used to build the .cube."""
    y = np.clip(luma(x), 1e-5, 1)
    y2 = np.interp(y, TX, TY)
    x = x * (y2 / y)[..., None]
    ws = np.clip(1 - y2 / 0.32, 0, 1) ** 1.2
    wh = np.clip((y2 - 0.45) / 0.40, 0, 1) ** 1.5
    wm = np.clip(1 - ws - wh, 0, 1)
    g = sum(np.array(GAIN[b])[None, None, :] * w[..., None] for b, w in (("shad", ws), ("mid", wm), ("high", wh)))
    x = x * g
    yy = luma(x)[..., None]
    x = yy + (x - yy) * SAT
    return np.clip(x, 0, 1)

def normalise(x, target=0.30, wb=0.75):
    y = luma(x); m = (y > 0.12) & (y < 0.80)
    r, g, b = (x[..., i][m].mean() for i in range(3))
    x = x * np.array([(g / r) ** wb, 1.0, (g / b) ** wb])
    k = (target / max(luma(x).mean(), 1e-3)) ** 0.7
    return np.clip(x * k, 0, 1)

def optical(x):
    h, w = x.shape[:2]
    y = luma(x)
    hi = np.clip((y - 0.70) / 0.30, 0, 1)[..., None] * x
    bloom = np.stack([ndimage.gaussian_filter(hi[..., c], 22) for c in range(3)], -1) * np.array([1.0, 0.55, 0.28])
    x = 1 - (1 - x) * (1 - 0.35 * bloom)                   # screen halation, warm
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h * 0.46) / (h / 2)) ** 2)
    x = x * (1 - 0.28 * np.clip((d - 0.5) / 0.8, 0, 1) ** 1.6)[..., None]
    return np.clip(x, 0, 1)

def stats(x):
    y = luma(x); mx = x.max(-1); mn = x.min(-1); sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    r = {"luma": float(y.mean()), "p50": float(np.median(y)), "sat": float(sat.mean()), "crushed": float((y < 0.04).mean())}
    for nm, (lo, hi) in {"shad": (0, 0.2), "mid": (0.2, 0.6), "high": (0.6, 1.01)}.items():
        m = (y >= lo) & (y < hi)
        r[nm] = (float(x[..., 0][m].mean() / x[..., 1][m].mean()), float(x[..., 2][m].mean() / x[..., 1][m].mean())) if m.sum() > 200 else None
    return r

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "cube":
        N = 33; v = np.linspace(0, 1, N)
        b, g, r = np.meshgrid(v, v, v, indexing="ij")            # .cube order: R fastest
        rgb = np.stack([r, g, b], -1).reshape(-1, 1, 3)
        out = look(rgb).reshape(-1, 3)
        with open(sys.argv[2], "w") as f:
            f.write('TITLE "pujo-ki-asolei-sobar reference look v1"\nLUT_3D_SIZE 33\nDOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n')
            for p in out: f.write(f"{p[0]:.6f} {p[1]:.6f} {p[2]:.6f}\n")
        print("wrote", sys.argv[2])
    else:
        src, dst = Path(sys.argv[2]), Path(sys.argv[3]); dst.mkdir(parents=True, exist_ok=True); allst = []
        for f in sorted(src.glob("*.png")):
            x = np.asarray(Image.open(f).convert("RGB"), np.float32) / 255
            o = optical(look(normalise(x)))
            Image.fromarray((o * 255).astype(np.uint8)).save(dst / f.name)
            s = stats(o); allst.append(s)
            print(f"{f.stem:<12} luma {s['luma']:.3f} p50 {s['p50']:.3f} sat {s['sat']:.3f} crush {s['crushed']:.3f} mid {tuple(round(v,2) for v in s['mid']) if s['mid'] else '-'}")
        med = {k: float(np.median([s[k] for s in allst])) for k in ("luma", "p50", "sat", "crushed")}
        for b in ("shad", "mid", "high"):
            v = [s[b] for s in allst if s[b]]; med[b] = (float(np.median([a[0] for a in v])), float(np.median([a[1] for a in v])))
        print("OURS  ", {k: (round(v, 3) if isinstance(v, float) else tuple(round(a, 3) for a in v)) for k, v in med.items()})
        print("REF   ", REF)
