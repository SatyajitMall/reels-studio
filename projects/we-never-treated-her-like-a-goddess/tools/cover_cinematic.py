#!/usr/bin/env python3
"""Cinematic reel cover: moody grade (lifted-black matte, warm highlights, slightly cooler shadows), heavy vignette, fine grain,
film-title type (tracked Didot caps + italic line + small credit line) inside the 4:5 grid-safe area.
Usage (reel folder): ../../.venv/bin/python tools/cover_cinematic.py <still.png> <out.jpg> <title_y>"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

src, out, ty = sys.argv[1], sys.argv[2], int(sys.argv[3])
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255
H, W, _ = a.shape
y = a @ np.array([0.2126, 0.7152, 0.0722], np.float32)
# S-curve contrast, matte blacks, split tone
c = np.clip(a, 0, 1); c = c * c * (3 - 2 * c) * 0.55 + c * 0.45
c = 0.035 + c * 0.94
sh = (1 - y)[..., None] ** 2; hi = y[..., None] ** 2
c = c + sh * np.array([-0.012, 0.0, 0.018]) + hi * np.array([0.03, 0.012, -0.025])
sat = c.mean(-1, keepdims=True); c = sat + (c - sat) * 0.9
# vignette
yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.52) / (H * 0.6)) ** 2)
c = c * (1 - 0.55 * np.clip(r - 0.35, 0, 1) ** 1.4)[..., None]
# top shade for the title
shade = np.clip(1 - (yy - ty - 330) / 500, 0, 1) * 0.45; c = c * (1 - shade[..., None])
rng = np.random.default_rng(7); c = c + rng.normal(0, 0.012, (H, W, 1))
im = Image.fromarray((np.clip(c, 0, 1) * 255).astype(np.uint8))
d = ImageDraw.Draw(im)
caps = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 50, index=0)
ital = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 118, index=1)
small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 30, index=0)
def tracked(text, font, y, fill, track):
    w = sum(d.textlength(ch, font=font) for ch in text) + track * (len(text) - 1); x = (W - w) / 2
    for ch in text: d.text((x, y), ch, font=font, fill=fill); x += d.textlength(ch, font=font) + track
cream = (244, 234, 214); gold = (233, 196, 106)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
tracked("WE NEVER TREATED HER", caps, ty, cream, 9)
t = "like a goddess"; tw = d.textlength(t, font=ital)
gd.text(((W - tw) / 2, ty + 62), t, font=ital, fill=(0, 0, 0, 200)); glow = glow.filter(ImageFilter.GaussianBlur(10)); im.paste(glow, (0, 0), glow); d = ImageDraw.Draw(im)
d.text(((W - tw) / 2, ty + 62), t, font=ital, fill=gold)
d.line([(W / 2 - 60, ty + 230), (W / 2 + 60, ty + 230)], fill=(244, 234, 214), width=2)
tracked("DURGA PUJA  ·  KOLKATA  ·  2026", small, ty + 252, cream, 6)
im.save(out, quality=94)
im.crop((0, (H - 1350) // 2, W, (H + 1350) // 2)).resize((432, 540)).save(out.replace(".jpg", "_grid.jpg"), quality=85)
