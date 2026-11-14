#!/usr/bin/env python3
"""Cinematic grade options for round 1b (director: "cinematic colours grading is not there at all").

Same stills as tools/ref_look.py (one per shot, through the planned crop). Each frame gets the per-clip primary
(normalise: partial grey balance + exposure to a shared target, so shots match), then a parametric look:
filmic S-curve (contrast about a pivot, deep blacks, rolled highlights), global saturation, 3-way split tint
(shadows / mids / highlights), then optics: halation (warm glow off highlights) and vignette.
The pixelwise part (curve + saturation + tints) becomes the .cube; halation + vignette are optical (baked / Lumetri).

Usage: grade_options.py sheet <stills_dir> <out.jpg>        3 options side by side on 6 shots + the reference
       grade_options.py cube <option> <out.cube>             33^3 LUT of the chosen option's pixelwise part
       grade_options.py apply <option> <in.png> <out.png>     full grade (primary + look + optics) on one still
"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

def luma(x): return x @ np.array([0.2126, 0.7152, 0.0722])

OPTIONS = {
 "G1 Amber Film":   {"black": 0.012, "white": 0.95, "contrast": 1.35, "pivot": 0.36, "sat": 0.88,
                     "shad": [0.93, 1.00, 1.05], "mid": [1.12, 1.00, 0.80], "high": [1.05, 1.00, 0.88], "hal": 0.28, "vig": 0.38},
 "G2 Gold & Shadow": {"black": 0.0, "white": 0.97, "contrast": 1.55, "pivot": 0.34, "sat": 1.00,
                     "shad": [1.00, 0.95, 0.86], "mid": [1.15, 1.00, 0.72], "high": [1.05, 1.00, 0.84], "hal": 0.22, "vig": 0.48},
 "G3 Teal & Amber":  {"black": 0.015, "white": 0.95, "contrast": 1.42, "pivot": 0.36, "sat": 0.92,
                     "shad": [0.70, 1.00, 1.30], "mid": [1.12, 1.00, 0.82], "high": [1.04, 1.00, 0.92], "hal": 0.20, "vig": 0.38},
}

def normalise(x, target=0.30, wb=0.5):
    y = luma(x); m = (y > 0.10) & (y < 0.85)
    r, g, b = (x[..., i][m].mean() for i in range(3))
    x = x * np.array([(g / r) ** wb, 1.0, (g / b) ** wb])
    k = min((target / max(luma(x).mean(), 1e-3)) ** 0.8, 2.0)
    return np.clip(x * k, 0, 1)

def curve(y, P):
    # filmic: contrast about the pivot in log-ish space, soft toe and shoulder, then map to [black, white]
    c, p = P["contrast"], P["pivot"]
    t = np.where(y < p, p * (y / p) ** c, 1 - (1 - p) * ((1 - y) / (1 - p)) ** c)
    t = t * t * (3 - 2 * t) * 0.25 + t * 0.75
    return P["black"] + (P["white"] - P["black"]) * t

def look(x, P):
    y = np.clip(luma(x), 0, 1); y2 = curve(y, P)
    w = np.clip(y / 0.02, 0, 1)[..., None]
    x = (w * (x / np.clip(y, 1e-5, None)[..., None]) + (1 - w)) * y2[..., None]
    yy = luma(x)[..., None]; x = yy + (x - yy) * P["sat"]
    ws = np.clip(1 - y2 / 0.30, 0, 1) ** 1.5; wh = np.clip((y2 - 0.55) / 0.40, 0, 1) ** 1.5; wm = np.clip(1 - ws - wh, 0, 1)
    g = sum(np.array(P[b])[None, None, :] * wgt[..., None] for b, wgt in (("shad", ws), ("mid", wm), ("high", wh)))
    x2 = x * g
    x2 = x2 * (luma(x) / np.clip(luma(x2), 1e-5, None))[..., None]
    return np.clip(x2, 0, 1)

def optics(x, P):
    h, w = x.shape[:2]; y = luma(x)
    hi = np.clip((y - 0.62) / 0.38, 0, 1)[..., None] * x
    s = max(h, w) / 960 * 14
    bloom = np.stack([ndimage.gaussian_filter(hi[..., c], s) for c in range(3)], -1) * np.array([1.0, 0.55, 0.30])
    x = 1 - (1 - x) * (1 - P["hal"] * bloom * 1.6)
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h * 0.42) / (h / 2)) ** 2)
    return np.clip(x * (1 - P["vig"] * np.clip((d - 0.45) / 0.85, 0, 1) ** 1.6)[..., None], 0, 1)

def grade(x, P): return optics(look(normalise(x), P), P)

def stats(x):
    y = luma(x); s = x.max(-1) - x.min(-1)
    return {"luma": round(float(y.mean()), 3), "p02": round(float(np.percentile(y, 2)), 3), "p98": round(float(np.percentile(y, 98)), 3), "sat": round(float(s.mean()), 3)}

def sheet(d, out):
    pick = ["01_", "02_", "04_", "05_", "09_", "11_"]
    paths = [p for p in sorted(Path(d).glob("*.png")) if any(p.name.startswith(k) for k in pick)]
    ims = [np.asarray(Image.open(p).convert("RGB").resize((270, 480))).astype(np.float32) / 255 for p in paths]
    REEL = Path(__file__).resolve().parents[1]
    ref = Image.open(REEL / "analysis/look_test/ref_eyes.png").convert("RGB")
    rw, rh = ref.size; ref = ref.crop(((rw - rh * 270 // 480) // 2, 0, (rw + rh * 270 // 480) // 2, rh)).resize((270, 480))
    try: font = ImageFont.truetype("/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf", 26)
    except Exception: font = ImageFont.load_default()
    rows = []; info = {}
    for name, P in OPTIONS.items():
        g = [grade(x, P) for x in ims]; info[name] = [stats(a) for a in g]
        row = Image.fromarray((np.concatenate(g, 1) * 255).astype(np.uint8))
        canvas = Image.new("RGB", (row.width + 274, 480 + 34), (12, 12, 12)); canvas.paste(row, (274, 34)); canvas.paste(ref, (0, 34))
        ImageDraw.Draw(canvas).text((8, 4), name + "   (left: the reference's eye shot)", font=font, fill=(255, 210, 90)); rows.append(canvas)
    S = Image.new("RGB", (rows[0].width, sum(r.height for r in rows)), (12, 12, 12)); y = 0
    for r in rows: S.paste(r, (0, y)); y += r.height
    S.save(out, quality=88); print(json.dumps({k: v[0] for k, v in info.items()}))

def cube(opt, path):
    P = OPTIONS[opt]; n = 33; v = np.linspace(0, 1, n); b, g, r = np.meshgrid(v, v, v, indexing="ij")
    o = look(np.stack([r, g, b], -1).reshape(1, -1, 3), P)[0]
    with open(path, "w") as f:
        f.write(f'TITLE "uski-aankhein {opt}"\nLUT_3D_SIZE 33\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
        for c in o: f.write(f"{c[0]:.6f} {c[1]:.6f} {c[2]:.6f}\n")
    print("wrote", path)

if __name__ == "__main__":
    m = sys.argv[1]
    if m == "sheet": sheet(sys.argv[2], sys.argv[3])
    elif m == "cube": cube(sys.argv[2], sys.argv[3])
    elif m == "apply":
        x = np.asarray(Image.open(sys.argv[3]).convert("RGB")).astype(np.float32) / 255
        Image.fromarray((grade(x, OPTIONS[sys.argv[2]]) * 255).astype(np.uint8)).save(sys.argv[4])
