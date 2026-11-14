#!/usr/bin/env python3
"""make_title_v7.py: KOLKATA round 7 title card, "KOLKATA / the city of / Culture, Heritage and Surprises" (reel-local).

Director (2026-11-08): "KOLKATA / The city of / Culture Heritage and Surprises — this should be on the video and the
thumbnail", "use better cinematic fonts", then "Find different indo western fonts". Renders a 1080×1920 RGBA PNG (same
convention as renders/overlays/title_kolkata.png: full frame, Position 0.5/0.5 on V5) in one style, cream #F5E6C8 with
a soft shadow and a soft dark band so it reads on the bright record shot. Text stays inside the reel's 4:5 window
(y 235–1584) and x 120–960 (IG safe zone); a line wider than 840 px is shrunk to fit.

Fonts: macOS system fonts, Adobe Fonts' Bebas Neue (synced on this Mac), and free OFL Google Fonts in assets/fonts/
(Rozha One, Yatra One, Eczar, Galada, Tiro Bangla, Amita, Teko; licences beside them). Pillow here has no libraqm, so
Bengali is drawn unshaped: fine for কলকাতা (no conjuncts or pre-base vowels), check any other Bengali by eye.

Usage (studio root):
  .venv/bin/python projects/kolkata/tools/make_title_v7.py --style rozha -o projects/kolkata/renders/overlays/title_v7.png [--y 520]
  .venv/bin/python projects/kolkata/tools/make_title_v7.py --sheet <frame.png> … -o sheet.jpg [--styles a,b,c]
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SUP = "/System/Library/Fonts/Supplemental/"
AF = str(Path.home() / "Documents/reels-studio/assets/fonts") + "/"
BEBAS = "/Users/SATYAJIT.MALL/Library/Application Support/Adobe/CoreSync/plugins/livetype/.r/.37900.otf"  # Adobe Fonts: Bebas Neue Bold
CREAM = (245, 230, 200, 255)
GOLD = (236, 190, 110, 255)
BN = "কলকাতা"

# style → lines: (text, font file, index, size, tracking px, variation name or None, colour), gaps between lines
STYLES = {
    # western cinematic
    "didot":  dict(lines=[("KOLKATA", SUP + "Didot.ttc", 2, 150, 20, None, CREAM), ("the city of", SUP + "Didot.ttc", 1, 62, 1, None, CREAM),
                          ("CULTURE, HERITAGE AND SURPRISES", SUP + "Didot.ttc", 2, 36, 5, None, CREAM)], gaps=(18, 14)),
    "bebas":  dict(lines=[("KOLKATA", BEBAS, 0, 230, 14, None, CREAM), ("THE CITY OF", SUP + "Futura.ttc", 0, 36, 10, None, CREAM),
                          ("CULTURE, HERITAGE AND SURPRISES", SUP + "Futura.ttc", 0, 36, 5, None, CREAM)], gaps=(4, 16)),
    "futura": dict(lines=[("KOLKATA", SUP + "Futura.ttc", 0, 100, 46, None, CREAM), ("the city of", SUP + "Baskerville.ttc", 2, 58, 1, None, CREAM),
                          ("CULTURE, HERITAGE AND SURPRISES", SUP + "Futura.ttc", 0, 32, 7, None, CREAM)], gaps=(24, 14)),
    "bodoni": dict(lines=[("KOLKATA", SUP + "Bodoni 72.ttc", 0, 158, 16, None, CREAM), ("the city of", SUP + "Bodoni 72.ttc", 1, 62, 1, None, CREAM),
                          ("CULTURE, HERITAGE AND SURPRISES", SUP + "Bodoni 72.ttc", 2, 34, 5, None, CREAM)], gaps=(14, 14)),
    # Indo-western
    "rozha":  dict(lines=[(BN, AF + "TiroBangla-Regular.ttf", 0, 64, 6, None, GOLD), ("KOLKATA", AF + "RozhaOne-Regular.ttf", 0, 150, 12, None, CREAM),
                          ("the city of", AF + "TiroBangla-Italic.ttf", 0, 58, 1, None, CREAM),
                          ("CULTURE, HERITAGE AND SURPRISES", AF + "Eczar[wght].ttf", 0, 34, 5, "SemiBold", CREAM)], gaps=(6, 10, 12)),
    "yatra":  dict(lines=[("KOLKATA", AF + "YatraOne-Regular.ttf", 0, 160, 10, None, CREAM), ("the city of", AF + "TiroBangla-Italic.ttf", 0, 58, 1, None, CREAM),
                          ("CULTURE, HERITAGE AND SURPRISES", AF + "Eczar[wght].ttf", 0, 34, 5, "SemiBold", CREAM)], gaps=(14, 12)),
    "galada": dict(lines=[(BN, AF + "Galada-Regular.ttf", 0, 70, 4, None, GOLD), ("Kolkata", AF + "Galada-Regular.ttf", 0, 190, 2, None, CREAM),
                          ("the city of", AF + "TiroBangla-Italic.ttf", 0, 56, 1, None, CREAM),
                          ("CULTURE, HERITAGE AND SURPRISES", AF + "Eczar[wght].ttf", 0, 34, 5, "SemiBold", CREAM)], gaps=(0, 6, 12)),
    "eczar":  dict(lines=[(BN, AF + "TiroBangla-Regular.ttf", 0, 60, 6, None, GOLD), ("KOLKATA", AF + "Eczar[wght].ttf", 0, 150, 24, "SemiBold", CREAM),
                          ("the city of", AF + "TiroBangla-Italic.ttf", 0, 58, 1, None, CREAM),
                          ("CULTURE, HERITAGE AND SURPRISES", AF + "Eczar[wght].ttf", 0, 34, 5, "Medium", CREAM)], gaps=(4, 8, 12)),
    "amita":  dict(lines=[("Kolkata", AF + "Amita-Bold.ttf", 0, 180, 2, None, CREAM), ("the city of", AF + "TiroBangla-Italic.ttf", 0, 56, 1, None, CREAM),
                          ("CULTURE, HERITAGE AND SURPRISES", AF + "Eczar[wght].ttf", 0, 39, 5, "SemiBold", CREAM)], gaps=(4, 14)),
    "teko":   dict(lines=[(BN, AF + "TiroBangla-Regular.ttf", 0, 60, 6, None, GOLD), ("KOLKATA", AF + "Teko[wght].ttf", 0, 250, 10, "SemiBold", CREAM),
                          ("THE CITY OF", AF + "Teko[wght].ttf", 0, 52, 10, "Regular", CREAM),
                          ("CULTURE, HERITAGE AND SURPRISES", AF + "Teko[wght].ttf", 0, 52, 4, "Regular", CREAM)], gaps=(0, 14, 8)),
}


def load(path: str, index: int, size: int, var: str | None):
    f = ImageFont.truetype(path, size, index=index)
    if var:
        f.set_variation_by_name(var)
    return f


def tracked(d: ImageDraw.ImageDraw, x: float, y: float, text: str, font, track: int, fill) -> None:
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + track


def width(text: str, font, track: int) -> float:
    return sum(font.getlength(c) for c in text) + track * (len(text) - 1)


def render(style: str, top: int = 520) -> Image.Image:
    st = STYLES[style]
    layout, y = [], top
    for k, (txt, path, idx, size, tr, var, col) in enumerate(st["lines"]):
        while True:   # shrink a line until it fits 840 px centred (x 120–960)
            font = load(path, idx, size, var)
            if width(txt, font, tr) <= 840 or size < 20:
                break
            size -= 2; tr = max(1, int(tr * 0.97))
        bb = font.getbbox(txt)
        w = width(txt, font, tr)
        x = 540 - w / 2
        assert 120 <= x and x + w <= 960, f"{style}: line {k} too wide ({w:.0f}px)"
        layout.append((txt, font, tr, x, y - bb[1], col))
        y += (bb[3] - bb[1]) + (st["gaps"][k] if k < len(st["gaps"]) else 0)
    glow = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    shadow, text = glow.copy(), glow.copy()
    g, s, d = ImageDraw.Draw(glow), ImageDraw.Draw(shadow), ImageDraw.Draw(text)
    g.ellipse((40, top - 70, 1040, y + 70), fill=(0, 0, 0, 105))   # soft dark band behind the block
    for txt, font, tr, x, yy, col in layout:
        tracked(g, x, yy, txt, font, tr, (0, 0, 0, 170))
        tracked(s, x + 2, yy + 3, txt, font, tr, (0, 0, 0, 210))
        tracked(d, x, yy, txt, font, tr, col)
    out = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    out.alpha_composite(glow.filter(ImageFilter.GaussianBlur(42)))
    out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(4)))
    out.alpha_composite(text)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--style", choices=list(STYLES))
    ap.add_argument("--styles", help="comma list for --sheet (default: all)")
    ap.add_argument("--y", type=int, default=520)
    ap.add_argument("--sheet", nargs="+", type=Path)
    ap.add_argument("-o", type=Path, required=True)
    a = ap.parse_args()
    if a.sheet:
        names = a.styles.split(",") if a.styles else list(STYLES)
        W, H = 432, 540
        sheet = Image.new("RGB", (W * len(names), H * len(a.sheet)))
        lab = ImageFont.truetype(SUP + "Arial Bold.ttf", 22)
        for r, fp in enumerate(a.sheet):
            bg = Image.open(fp).convert("RGBA")
            for c, name in enumerate(names):
                im = bg.copy(); im.alpha_composite(render(name, a.y))
                tile = im.convert("RGB").crop((0, 235, 1080, 1585)).resize((W, H))
                ImageDraw.Draw(tile).text((8, H - 30), name, fill="yellow", font=lab)
                sheet.paste(tile, (c * W, r * H))
        sheet.save(a.o, quality=90)
    else:
        render(a.style, a.y).save(a.o)
    print("✓", a.o)


if __name__ == "__main__":
    main()
