#!/usr/bin/env python3
"""Round 5 (director: "like the reference", "tight eyes first", "very bad image quality"): hero-idol choice sheet.
For each candidate: the sharpest frame in its window (Laplacian variance on the eye region), denoised before enlarging
(ffmpeg nlmeans), cropped with the eyes at the target span on the 40 % line, Lanczos to 1080x1920, gentle unsharp, G2b2 +
vignette. Row 1: the opening double exposure (the AI singer Screen-blended over her eyes, as the reference); row 2: the eye hold.
Usage: python tools/hero_stills.py -o analysis/round5/heroes.jpg
"""
import subprocess, argparse, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from scipy import ndimage
REEL = Path(__file__).resolve().parents[1]; CUBE = REEL / "grade/uski_aankhein_G2b2_gold_shadow_c18.cube"
HEROES = [("Oct17 C164 red clay Durga", "raw/b-roll/A001_10172024_C164.mov", (0.20, 1.90), (0.518, 0.4763), 267, 0.50),
          ("Oct18 C208 white sholapith Durga", "raw/b-roll/A001_10182155_C208.mov", (0.20, 4.00), (0.522, 0.434), 235, 0.50),
          ("Oct17 C162 giant clay face (art)", "raw/b-roll/A001_10172021_C162.mov", (6.60, 7.10), (0.5343, 0.4589), 800, 0.62)]
SINGER = (REEL / "renders/gen/esraj_final.mp4", 3.0)

def grab(src, t, td, name, vf="scale=in_range=tv:out_range=pc"):
    o = Path(td) / f"{name}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1", "-vf", vf, str(o)], check=True)
    return o

def sharpest(src, win, ex, ey, td):
    best = (-1, win[0])
    for t in np.arange(win[0], win[1], 0.1):
        im = np.asarray(Image.open(grab(src, t, td, "s")).convert("L")).astype(np.float32)
        H, W = im.shape; y0, x0 = int(ey * H), int(ex * W); r = im[max(y0 - 150, 0):y0 + 150, max(x0 - 250, 0):x0 + 250]
        v = ndimage.laplace(r).var(); best = max(best, (v, t))
    return best[1]

def process(src, t, ex, ey, eye_px, span, td):
    # denoise at source resolution (only the crop region), then crop, Lanczos up, gentle unsharp
    p = grab(src, t, td, "f", "scale=in_range=tv:out_range=pc,nlmeans=s=2.0:p=7:r=11")
    im = Image.open(p).convert("RGB"); W, H = im.size; cw = eye_px / (span * W); cwp = cw * W; chp = cwp * 16 / 9
    l = min(max(ex * W - 0.5 * cwp, 0), W - cwp); t_ = min(max(ey * H - 0.40 * chp, 0), H - chp)
    out = im.resize((1080, 1920), Image.LANCZOS, box=(l, t_, l + cwp, t_ + chp)).filter(ImageFilter.UnsharpMask(radius=1.2, percent=45, threshold=2))
    return out, 1080 / cwp

import sys; sys.path.insert(0, str(REEL / "tools")); from comp_board import primary   # the bake's per-clip primary

def grade(im, td, name):
    im = primary(im)
    i = Path(td) / f"{name}_in.png"; o = Path(td) / f"{name}_g.png"; im.save(i); f = str(CUBE).replace(":", "\\:")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(i), "-vf", f"format=gbrp,lut3d=file='{f}',vignette=angle=0.42,format=rgb24", str(o)], check=True)
    return Image.open(o).convert("RGB")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("-o", "--out", required=True); a = ap.parse_args()
    try: f1 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
    except OSError: f1 = ImageFont.load_default()
    cols = []
    with tempfile.TemporaryDirectory() as td:
        singer = Image.open(grab(SINGER[0], SINGER[1], td, "singer", "null")).convert("RGB").resize((1080, 1920), Image.LANCZOS)
        for name, src, win, (ex, ey), px, span in HEROES:
            t = sharpest(REEL / src, win, ex, ey, td); eyes, up = process(REEL / src, t, ex, ey, px, span, td)
            e = np.asarray(eyes).astype(np.float32) / 255; s = np.asarray(singer).astype(np.float32) / 255
            dexp = Image.fromarray(((1 - (1 - e) * (1 - 0.70 * s)) * 255 + 0.5).astype(np.uint8))   # Screen, singer at 70 %
            g1 = grade(dexp, td, "d"); g2 = grade(eyes, td, "e")
            col = Image.new("RGB", (1080, 3840 + 90), (14, 14, 14)); col.paste(g1, (0, 0)); col.paste(g2, (0, 1920))
            d = ImageDraw.Draw(col); d.text((16, 3850), f"{name}  @{t:.1f}s  {up:.1f}x", font=f1, fill=(255, 215, 120)); cols.append(col)
    sheet = Image.new("RGB", (1080 * len(cols), 3930), (14, 14, 14))
    for i, c in enumerate(cols): sheet.paste(c, (1080 * i, 0))
    sheet.resize((sheet.width // 3, sheet.height // 3), Image.LANCZOS).save(a.out, quality=90)
    for i, c in enumerate(cols): c.crop((0, 1920, 1080, 3840)).save(Path(a.out).with_name(f"hero_{i+1}_eyes_fullres.jpg"), quality=92)
    print("✓", a.out)

if __name__ == "__main__":
    main()
