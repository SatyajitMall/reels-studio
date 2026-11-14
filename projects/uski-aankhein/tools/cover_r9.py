#!/usr/bin/env python3
"""Designed cover options (director at Checkpoint 3: "Use a better cover"). 1080x1920, the reel's look (G2r cube + vignette)
and its title type (DIN Condensed Bold, cream #F5E6C8, dark soft halo). Every option keeps the eyes and the title inside the
3:4 profile-grid crop (y 240-1680) and clear of the IG safe zone.
  A  eyes band: black frame, a wide band of the red clay Durga's eyes (the reference's letterbox idea), title above, line below
  B  her gaze: the red clay Durga full bleed, tighter than the reel (AI still, no ghost), title low
  C  the double exposure: reel 6.0 s (the player on the left, her eyes clear), title low
  D  the clay face: reel 20.4 s, title in the dark above her
Writes analysis/ig/covers/cover_<X>.jpg and analysis/ig/cover_options_v2.jpg. Usage: python tools/cover_r9.py
"""
import sys, subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import bake_r9b as R9, bake_r7 as R7
R, B = R9.R, R9.B
OUT = REEL / "analysis/ig/covers"; CUBE = REEL / "grade/uski_aankhein_G2r_rich_deep.cube"
EXPORT = REEL / "renders/exports/uski-aankhein_v9c_IG.mp4"
FONT = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
CREAM, HALO = (245, 230, 200), (26, 15, 5)

def look(rgb):
    """the V3 look on a pre-look float frame: cube + vignette (as the previz)"""
    with tempfile.TemporaryDirectory() as td:
        i, o = Path(td) / "i.png", Path(td) / "o.png"; Image.fromarray((np.clip(rgb, 0, 1) * 255 + .5).astype(np.uint8)).save(i)
        f = str(CUBE).replace(":", "\\:")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(i), "-vf", f"format=gbrp,lut3d=file='{f}',vignette=angle=0.42,format=rgb24", str(o)], check=True)
        return Image.open(o).convert("RGB")

def export_frame(t):
    with tempfile.TemporaryDirectory() as td:
        o = Path(td) / "f.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(EXPORT), "-frames:v", "1", "-vf", "scale=in_range=tv:out_range=pc", str(o)], check=True)
        return Image.open(o).convert("RGB")

def red_clay(span):
    """the red clay Durga (C163 AI still, v9b grade) with her eye pair at `span` of the frame width, eyes at (.5, .40)"""
    big, meta = R9.a_base(); cw0 = meta["cw0"]
    gains = B.primary_params(R.push_from_big(big, cw0, cw0), wb=0.5, exp=R.PRIM163["exp"])
    x = R.push_from_big(big, cw0, R.CW(R.EYE163, span))
    return look(R7.clarity(B.halation(R.grade(x, gains, R.PRIM163))))

def text(im, s, size, cx, top, track=0.08):
    """centred line, cap top at `top`, letter-spaced, with the reel's dark soft halo"""
    f = ImageFont.truetype(FONT, size); sp = size * track
    widths = [f.getlength(c) for c in s]; w = sum(widths) + sp * (len(s) - 1)
    asc = f.getbbox("H")[1]; y = top - asc
    layer = Image.new("L", im.size, 0); d = ImageDraw.Draw(layer); x = cx - w / 2
    for c, cwid in zip(s, widths): d.text((x, y), c, font=f, fill=255); x += cwid + sp
    for r, a in ((22, .85), (7, .70)):
        halo = layer.filter(ImageFilter.GaussianBlur(r)).point(lambda v, a=a: int(v * a))
        im.paste(Image.new("RGB", im.size, HALO), (0, 0), halo)
    im.paste(Image.new("RGB", im.size, CREAM), (0, 0), layer); return im

def title(im, top, gap=136, size=120):
    text(im, "USKI AANKHEIN", size, 540, top); return text(im, "if her eyes were music", round(size * 50 / 120), 540, top + gap, 0.10)

def cover_A():
    src = red_clay(0.62)                                       # eyes band: 1080 x 560 around the eye-line (y 768)
    band = src.crop((0, 768 - 300, 1080, 768 + 260)); im = Image.new("RGB", (1080, 1920), (8, 6, 4)); im.paste(band, (0, 640))
    text(im, "USKI AANKHEIN", 150, 540, 455)
    return text(im, "if her eyes were music", 56, 540, 1262, 0.10)

def cover_B(): return title(red_clay(0.50), 1300)
def cover_C(): return title(export_frame(6.0), 1330)
def cover_D(): return title(export_frame(20.4), 300)

def main():
    OUT.mkdir(parents=True, exist_ok=True); ims = {}
    for k, fn in {"A": cover_A, "B": cover_B, "C": cover_C, "D": cover_D}.items():
        ims[k] = fn(); ims[k].save(OUT / f"cover_{k}.jpg", quality=95)
    try: lab = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
    except OSError: lab = ImageFont.load_default()
    names = {"A": "A  eyes band", "B": "B  her gaze", "C": "C  double exposure", "D": "D  clay face"}
    sheet = Image.new("RGB", (4 * 470, 60 + 800 + 20 + 560), (16, 16, 16)); d = ImageDraw.Draw(sheet)
    for i, k in enumerate("ABCD"):
        d.text((i * 470 + 8, 12), names[k], font=lab, fill=(255, 215, 120))
        sheet.paste(ims[k].resize((450, 800)), (i * 470, 60))
        sheet.paste(ims[k].crop((0, 240, 1080, 1680)).resize((420, 560)), (i * 470 + 15, 880))
    sheet.save(REEL / "analysis/ig/cover_options_v2.jpg", quality=90); print("✓ covers", list(ims))

if __name__ == "__main__":
    main()
