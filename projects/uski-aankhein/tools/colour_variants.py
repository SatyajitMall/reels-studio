#!/usr/bin/env python3
"""Round 5c (director: "a lot of cinematic colour correction ... need to be done"): colour variants on the three v8 shots.
Columns: NOW (G2b2 + vignette) | A Cinematic Gold & Shadow (G2b2 + split-tone: gold highlights, slightly cool deep
shadows; +8 % mid contrast with soft ends; local clarity) | B Warm film print (G2b2 + 30 % Kodak 2383 + stronger glow) |
C Rich & deep (G2 original + the same finishing as A). Point operations become a .cube for Premiere; clarity is baked.
Usage: python tools/colour_variants.py -o analysis/round5/colour_variants.jpg
"""
import sys, subprocess, tempfile, argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
REEL = Path(__file__).resolve().parents[1]; STUDIO = REEL.parents[1]
sys.path.insert(0, str(STUDIO / "scripts")); import look_preview as lp
G2B2 = REEL / "grade/uski_aankhein_G2b2_gold_shadow_c18.cube"; G2 = REEL / "grade/uski_aankhein_G2_gold_shadow_v1.cube"
SHOTS = [("A singer x red clay", REEL / "renders/bakes_r7/A.mov", 120), ("B white sholapith", REEL / "renders/bakes_r7/B.mov", 150),
         ("C clay face", REEL / "renders/bakes_r7/C.mov", 110)]

def frame(path, n, td):
    o = Path(td) / "f.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vf", f"select=eq(n\\,{n}),scale=in_range=tv:out_range=pc", "-frames:v", "1", str(o)], check=True)
    return o

def lut(png, cube, td, extra=""):
    o = Path(td) / "l.png"; f = str(cube).replace(":", "\\:")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(png), "-vf", f"format=gbrp,lut3d=file='{f}'{extra},vignette=angle=0.42,format=rgb24", str(o)], check=True)
    return np.asarray(Image.open(o).convert("RGB")).astype(np.float32) / 255

def finish_point(x):
    """the cube-able part of A/C: split-tone + soft mid contrast (pointwise)"""
    L = x @ np.array([.2126, .7152, .0722], np.float32)
    sh = np.clip((0.32 - L) / 0.32, 0, 1)[..., None] ** 1.5; hi = np.clip((L - 0.55) / 0.45, 0, 1)[..., None]
    x = x + sh * np.array([-0.022, 0.004, 0.028], np.float32) + hi * np.array([0.030, 0.012, -0.028], np.float32)
    p = 0.40; x = np.where(x < p, p - (p - x) * 1.08 * (1 - 0.08 * (p - x) / p), p + (x - p) * 1.08 * (1 - 0.10 * (x - p) / (1 - p)))
    return np.clip(x, 0, 1)

def clarity(x, amt=0.18, sigma=22):
    bl = np.stack([ndimage.gaussian_filter(x[..., c], sigma) for c in range(3)], -1)
    return np.clip(x + amt * (x - bl), 0, 1)

def glow(x, a=0.25):
    L = x @ np.array([.2126, .7152, .0722], np.float32); hi = np.clip((L - 0.6) / 0.4, 0, 1)[..., None] * x
    bl = np.stack([ndimage.gaussian_filter(hi[..., c], 18) for c in range(3)], -1) * np.array([1.0, 0.6, 0.35], np.float32)
    return 1 - (1 - x) * (1 - a * bl)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("-o", "--out", required=True); a = ap.parse_args()
    lut_dir = lp.creative_lut_dir(); k2383 = str(lut_dir / "Kodak 5218 Kodak 2383 (by Adobe).cube").replace(":", "\\:").replace("'", "\\'")
    try: f1 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
    except OSError: f1 = ImageFont.load_default()
    labels = ["NOW: G2b2", "A  Cinematic Gold & Shadow", "B  Warm film print", "C  Rich & deep"]
    rows = []
    with tempfile.TemporaryDirectory() as td:
        for name, path, n in SHOTS:
            png = frame(path, n, td)
            now = lut(png, G2B2, td)
            va = clarity(finish_point(now))
            vb = glow(lut(png, G2B2, td, f",split[o][l];[l]lut3d=file='{k2383}':interp=tetrahedral[g];[o][g]blend=all_expr='A*0.7+B*0.3'"), 0.35)
            vc = clarity(finish_point(lut(png, G2, td)))
            rows.append([now, va, vb, vc])
    tw, th = 540, 960; sheet = Image.new("RGB", (tw * 4, th * len(rows) + 50), (14, 14, 14)); d = ImageDraw.Draw(sheet)
    for c, lab in enumerate(labels): d.text((c * tw + 10, 8), lab, font=f1, fill=(255, 215, 120))
    for r, imgs in enumerate(rows):
        for c, x in enumerate(imgs): sheet.paste(Image.fromarray((x * 255 + 0.5).astype(np.uint8)).resize((tw, th), Image.LANCZOS), (c * tw, 50 + r * th))
    sheet.save(a.out, quality=90); print("✓", a.out, sheet.size)

if __name__ == "__main__":
    main()
