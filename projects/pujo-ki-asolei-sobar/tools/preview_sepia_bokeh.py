#!/usr/bin/env python3
"""Preview the v1g treatment on one frame per shot: neutralise -> lens bokeh -> sepia film look -> halation, vignette, grain.
Writes analysis/look_v1g/{neutral,bokeh,final}/ and a before/after sheet."""
import json, subprocess, sys, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import lens, sepia_look as sl  # noqa: E402

FOCUS = json.loads((REEL / "analysis" / "focus_v1g.json").read_text())
OUT = REEL / "analysis" / "look_v1g"
for sub in ("neutral", "bokeh", "final"): (OUT / sub).mkdir(parents=True, exist_ok=True)

def frame(clip, t, crop=None):
    src = next((REEL / "raw" / "b-roll").glob(f"*_{clip}.mov"))
    vf = (f"crop={crop}," if crop else "") + "scale=1080:1920"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3).astype(np.float32) / 255

def optical(x, seed=0):
    H, W = x.shape[:2]; y = sl.luma(x)
    hi = np.clip((y - 0.72) / 0.28, 0, 1)[..., None] * x
    bloom = np.stack([ndimage.gaussian_filter(hi[..., c], 26) for c in range(3)], -1) * np.array([1.0, 0.62, 0.34])
    x = 1 - (1 - x) * (1 - 0.30 * bloom)
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H * 0.46) / (H / 2)) ** 2)
    x = x * (1 - 0.32 * np.clip((d - 0.45) / 0.85, 0, 1) ** 1.5)[..., None]
    g = np.random.default_rng(seed).normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    g = np.asarray(Image.fromarray(g).resize((W, H), Image.BICUBIC))
    x = x + g[..., None] * 0.022 * (1 - np.abs(sl.luma(x) - 0.5)[..., None] * 1.2)
    return np.clip(x, 0, 1)

edl = json.loads((REEL / "analysis" / "edl_v1f.json").read_text())
rows = []
for s in edl["shots"]:
    f = FOCUS[s["n"]]; t = (s["in"] + s["out"]) / 2; t0 = time.time()
    x = frame(s["clip"], t, f.get("crop"))
    xn = sl.normalise(x, sl.measure(x))
    d = lens.depth(xn); lo, hi = np.percentile(d, 2), np.percentile(d, 99.5); dn = np.clip((d - lo) / (hi - lo), 0, 1)
    fv = lens.focus_value(dn, f["fx"], f["fy"])
    xb, coc = lens.bokeh(xn, dn, fv, far_ref=float(np.percentile(dn, 5)), max_r=f.get("max_r", 20), near_r=f.get("near_r", 6))
    xf = optical(sl.look(xb))
    name = f"{int(s['n']):02d}_{s['clip']}.png"
    for sub, img in (("neutral", xn), ("bokeh", xb), ("final", xf)):
        Image.fromarray((img * 255).astype(np.uint8)).save(OUT / sub / name)
    Image.fromarray(np.clip(coc / 23 * 255, 0, 255).astype(np.uint8)).save(OUT / f"coc_{name}")
    rows.append(name); print(f"{name} focus d={fv:.2f} coc max {coc.max():.1f}  {time.time() - t0:.1f}s", flush=True)

F = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
TW, TH = 216, 384; cols = 7
sheet = Image.new("RGB", (cols * TW, 2 * 2 * (TH + 24)), (10, 10, 10)); dr = ImageDraw.Draw(sheet)
for i, n in enumerate(rows):
    r, c = divmod(i, cols); y0 = r * 2 * (TH + 24)
    raw = Image.open(OUT / "neutral" / n)  # placeholder replaced below by true raw
    s = edl["shots"][i]; f = FOCUS[s["n"]]
    rawimg = Image.fromarray((frame(s["clip"], (s["in"] + s["out"]) / 2, f.get("crop")) * 255).astype(np.uint8))
    sheet.paste(rawimg.resize((TW, TH)), (c * TW, y0 + 22)); sheet.paste(Image.open(OUT / "final" / n).resize((TW, TH)), (c * TW, y0 + TH + 46))
    dr.text((c * TW + 4, y0 + 2), n[:-4] + "  iPhone raw", fill=(200, 200, 200), font=F)
    dr.text((c * TW + 4, y0 + TH + 26), "bokeh + sepia", fill=(255, 205, 140), font=F)
sheet.save(OUT / "before_after_v1g.jpg", quality=88); print("sheet", sheet.size)
