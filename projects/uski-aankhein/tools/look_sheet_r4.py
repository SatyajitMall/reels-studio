#!/usr/bin/env python3
"""Round 4 ("colour grading not on point"): a look sheet the director can actually choose from.
Rows = pre-look stills from the bakes (primary only). Columns = Source, the current G2 grade (.cube + vignette, as the
previz), then lettered Premiere built-in film looks at a strong intensity (scripts/look_preview.py chains, reused).
Usage: python tools/look_sheet_r4.py analysis/looks_r4/stills/*.png -o analysis/looks_r4/looks_sheet_r4.jpg
"""
import sys, subprocess, tempfile, argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
STUDIO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(STUDIO / "scripts"))
import look_preview as lp

REEL = Path(__file__).resolve().parents[1]
G2 = REEL / "grade" / "uski_aankhein_G2_gold_shadow_v1.cube"
COLS = [("A", "k500t_2383", 0.8), ("B", "eterna_2395", 0.8), ("C", "reala_2393", 0.8),
        ("D", "cinestill", 0.8), ("E", "bleach", 1.0), ("F", "muted_red", 0.35)]
NAMES = {"k500t_2383": "Kodak 2383 (classic cinema)", "eterna_2395": "Eterna → 2395 (soft, muted)",
         "reala_2393": "Reala → 2393 (natural, rich)", "cinestill": "CineStill 800T (night glow)",
         "bleach": "Bleach bypass (moody)", "muted_red": "Red & gold (rest muted)"}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("stills", nargs="+"); ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--tile", type=int, default=300); a = ap.parse_args()
    lut_dir = lp.creative_lut_dir(); W = 540; rows = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for n, s in enumerate(a.stills):
            st = tmp / f"s{n}.png"; lp.grab(s, st, W); tiles = [("Source (no look)", st)]
            g = tmp / f"s{n}_g2.png"; f = str(G2).replace(":", "\\:")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(st), "-vf", f"format=gbrp,lut3d=file='{f}',vignette=angle=0.42,format=rgb24", str(g)], check=True)
            tiles.append(("NOW: G2 Gold & Shadow", g))
            for letter, look, k in COLS:
                o = tmp / f"s{n}_{look}.png"
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(st), "-filter_complex", lp.chain(look, lut_dir, k, W) + ",format=rgb24", "-frames:v", "1", str(o)], check=True)
                if lp.LOOKS[look][4] == "py:leave_red":
                    arr = np.asarray(Image.open(o).convert("RGB"), dtype=np.float32) / 255.0
                    Image.fromarray((lp.leave_red(arr, 25.0) * 255 + 0.5).astype(np.uint8)).save(o)   # 25 deg keeps saffron/gold too
                tiles.append((f"{letter}  {NAMES[look]}", o))
            rows.append([(l, Image.open(p).convert("RGB")) for l, p in tiles])
        w, h = rows[0][0][1].size; tw = a.tile; th = round(h * tw / w)
        sheet = Image.new("RGB", (tw * len(rows[0]), th * len(rows)), "black")
        try: font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 15)
        except OSError: font = ImageFont.load_default()
        for r, imgs in enumerate(rows):
            for c, (label, im) in enumerate(imgs):
                t = im.resize((tw, th), Image.LANCZOS); d = ImageDraw.Draw(t)
                if r == 0: d.rectangle([0, 0, tw, 26], fill=(0, 0, 0)); d.text((6, 5), label, font=font, fill=(255, 220, 120) if c == 1 else (255, 255, 255))
                sheet.paste(t, (c * tw, r * th))
        sheet.save(a.out, quality=90); print("✓", a.out, sheet.size)

if __name__ == "__main__":
    main()
