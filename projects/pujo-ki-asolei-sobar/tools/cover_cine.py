#!/usr/bin/env python3
"""Cinematic still for the cover (director, after v13: "Rickshaw puller is nice but enhance the picture, make it cinematic").
Source: a real camera frame of shot 11 (11_C216_m5e, frame 41: sharpest eye-contact frame; the v13h build is slow-mo with
synthesised frames). Person matte: hyperframes remove-background (f41_fg.png).
Treatment (display domain unless noted), each step measured in the sheet:
  separation  background -1/6 stop and a touch cooler; a soft key on his face (+0.2 stop, gaussian around the face, inside the matte)
  contrast    gentle S-curve around the face level (deeper blacks, haze off the sky), highlight roll-off
  colour      teal in the shadows, warm in the highlights (small amounts; skin kept)
  halation    warm glow around the street lights / headlight (linear light)
  vignette    elliptical, centred on him
  grain       fine luma grain, strongest in the mid-tones
  focus       (option "dof") gentle depth-based defocus of the far street (lens.py: Depth-Anything + disc blur), the man protected
Usage: cover_cine.py  -> analysis/cover/cover_A1.jpg (cinematic) + cover_A2.jpg (+ shallow focus) + cover_A_compare.jpg
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import cover_design as cd  # noqa: E402
import lens  # noqa: E402
C = REEL / "analysis/cover"; S = C / "c216"
rgb = np.asarray(Image.open(S / "f_41.png").convert("RGB"), np.float32) / 255
mat = np.asarray(Image.open(S / "f41_fg.png").split()[-1], np.float32) / 255
H, W = rgb.shape[:2]; FX, FY = 500, 715                                   # his face
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
luma = lambda x: x @ np.array([0.2126, 0.7152, 0.0722], np.float32)
soft = ndimage.gaussian_filter(mat, 6)

def grade(x):
    # separation: background down 1/3 stop and cooler; face key inside the matte
    bg = 1 - soft
    x = x * (1 - bg * (1 - 2 ** (-1 / 6)))[..., None]
    x = x * (1 + bg[..., None] * np.array([-0.025, 0, 0.03], np.float32))
    key = np.exp(-(((xx - FX) / 230) ** 2 + ((yy - FY) / 260) ** 2)) * soft
    x = x * (1 + key * (2 ** 0.2 - 1))[..., None]
    # S-curve around the face level, applied to luma (hue kept)
    y = luma(x); p = 0.40
    yc = np.where(y < p, p * (y / p) ** 1.08, 1 - (1 - p) * ((1 - y) / (1 - p)) ** 1.10)
    yc = np.where(yc > 0.86, 0.86 + 0.14 * np.tanh((yc - 0.86) / 0.14), yc)     # roll-off
    x = x * (yc / np.maximum(y, 1e-4))[..., None]
    # split tone: teal shadows, warm highlights
    y = luma(x)
    sh = np.clip(1 - y / 0.45, 0, 1) ** 1.5; hi = np.clip((y - 0.55) / 0.45, 0, 1) ** 1.5
    x = x + sh[..., None] * np.array([-0.018, 0.004, 0.022], np.float32) + hi[..., None] * np.array([0.02, 0.004, -0.02], np.float32)
    # halation around lights (linear light)
    lin = np.clip(x, 0, 1) ** 2.2; yl = luma(lin)
    src = (np.clip((yl - 0.6) / 0.4, 0, 1) * (1 - soft))[..., None] * lin       # lights only, never his shirt / face
    glow = ndimage.gaussian_filter(src, (18, 18, 0)) * 0.55 + ndimage.gaussian_filter(src, (60, 60, 0)) * 0.35
    lin = lin + glow * np.array([1.0, 0.72, 0.45], np.float32)
    x = np.clip(lin, 0, None) ** (1 / 2.2); x = x / (1 + np.maximum(x - 1, 0))
    # vignette: elliptical around him, edges about -0.35 stop
    r = np.sqrt(((xx - 540) / 700) ** 2 + ((yy - 980) / 1150) ** 2)
    x = x * (2 ** (-0.35 * np.clip((r - 0.5) / 0.6, 0, 1) ** 1.6))[..., None]
    # grain
    rng = np.random.default_rng(41); g = ndimage.gaussian_filter(rng.normal(0, 1, (H, W)).astype(np.float32), 0.7)
    g = g / g.std() * 0.011; y = luma(x)
    x = x + (g * (4 * y * (1 - y)) ** 0.8)[..., None]
    return np.clip(x, 0, 1)

def dof(x):
    d = lens.depth(x); lo, hi = np.percentile(d, [1, 99.5]); d = np.clip((d - lo) / (hi - lo), 0, 1)
    f = lens.focus_value(d, FX / W, FY / H)
    out, _ = lens.bokeh(x, d, f, far_ref=float(np.percentile(d, 3)), max_r=11.0, near_r=3.0, hi_boost=1.6, protect=ndimage.gaussian_filter(mat, 3))
    return out

if __name__ == "__main__":
    base = cd.Image.fromarray((rgb * 255 + 0.5).astype(np.uint8))
    a1 = grade(rgb); a2 = grade(dof(rgb))
    outs = {}
    for k, im in (("A", rgb), ("A1", a1), ("A2", a2)):
        pic = Image.fromarray((im * 255 + 0.5).clip(0, 255).astype(np.uint8))
        pic = cd.lockup(cd.shade(pic, 0, 680, 0.5, 0.0), cd.TITLE, 280, 128, cd.SUB); pic.save(C / f"cover_{k}.jpg", quality=95); outs[k] = pic
        fm = luma(im)[FY - 90:FY + 90, FX - 70:FX + 70].mean(); print(f"{k}: mean luma {luma(im).mean():.3f}, face {fm:.3f}, clip {np.mean(im.max(-1) > 0.985) * 100:.2f}%")
    labels = {"A": "A  as is (real frame 41)", "A1": "A1 cinematic", "A2": "A2 cinematic + shallow focus"}
    t = Image.new("RGB", (3 * 548, 980 + 330), (18, 18, 18)); d = ImageDraw.Draw(t)
    for i, k in enumerate(outs):
        t.paste(outs[k].resize((540, 960)), (i * 548 + 4, 24)); d.text((i * 548 + 8, 6), labels[k], fill=(255, 220, 0))
        t.paste(outs[k].crop((300, 560, 800, 1060)).resize((300, 300)), (i * 548 + 4, 1000))
        t.paste(outs[k].crop((0, 240, W, 1680)).resize((180, 240)), (i * 548 + 330, 1000))
    t.save(C / "cover_A_compare.jpg", quality=90); print("✓ cover_A1.jpg, cover_A2.jpg, cover_A_compare.jpg")
