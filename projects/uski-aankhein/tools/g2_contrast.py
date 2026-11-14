#!/usr/bin/env python3
"""Round 4 (director: "gold and shadow but a little reduced contrast"): G2 variants with less mid-contrast and slightly
lifted shadows / softer highlights, black and white kept anchored (T(x) = x - 4c(x - p)x(1 - x), p = 0.40, per channel on
the cube's output; slope at the pivot = 1 - 0.96c), and a sheet comparing them
with the current G2 on the round-4 stills (vignette as the previz).
Usage: python tools/g2_contrast.py analysis/looks_r4/stills/*.png -o analysis/looks_r4/g2_contrast_sheet.jpg
"""
import subprocess, argparse, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
REEL = Path(__file__).resolve().parents[1]; SRC = REEL / "grade/uski_aankhein_G2_gold_shadow_v1.cube"
VARIANTS = [("G2b1", 0.10, "−10 % contrast"), ("G2b2", 0.18, "−17 % contrast"), ("G2b3", 0.27, "−26 % contrast")]
PIVOT = 0.40

def write_variant(name, k):
    lines = SRC.read_text().splitlines(); out = []
    for ln in lines:
        p = ln.split()
        if len(p) == 3 and all(c[0].isdigit() or c[0] in "-." for c in p):
            v = np.array([float(x) for x in p]); v = np.clip(v - 4 * k * (v - PIVOT) * v * (1 - v), 0, 1); out.append(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}")
        elif ln.startswith("TITLE"): out.append(f'TITLE "uski-aankhein {name} Gold & Shadow, contrast -{k*96:.0f}% at {PIVOT}, black/white anchored"')
        else: out.append(ln)
    dst = REEL / f"grade/uski_aankhein_{name}_gold_shadow_c{int(k*100):02d}.cube"; dst.write_text("\n".join(out) + "\n"); return dst

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("stills", nargs="+"); ap.add_argument("-o", "--out", required=True); a = ap.parse_args()
    cols = [("NOW: G2 Gold & Shadow", SRC)] + [(f"{n}  {lab}", write_variant(n, k)) for n, k, lab in VARIANTS]
    try: font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 17)
    except OSError: font = ImageFont.load_default()
    tw = 360; rows = []
    with tempfile.TemporaryDirectory() as td:
        for s in a.stills:
            r = []
            for lab, cube in cols:
                o = Path(td) / "o.png"; f = str(cube).replace(":", "\\:")
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", s, "-vf", f"scale=540:-2,format=gbrp,lut3d=file='{f}',vignette=angle=0.42,format=rgb24", str(o)], check=True)
                r.append((lab, Image.open(o).convert("RGB").copy()))
            rows.append(r)
    w, h = rows[0][0][1].size; th = round(h * tw / w); sheet = Image.new("RGB", (tw * len(cols), th * len(rows)), "black")
    for ri, r in enumerate(rows):
        for ci, (lab, im) in enumerate(r):
            t = im.resize((tw, th), Image.LANCZOS)
            if ri == 0: d = ImageDraw.Draw(t); d.rectangle([0, 0, tw, 28], fill=(0, 0, 0)); d.text((6, 5), lab, font=font, fill=(255, 220, 120))
            sheet.paste(t, (ci * tw, ri * th))
    sheet.save(a.out, quality=90); print("✓", a.out)

if __name__ == "__main__":
    main()
