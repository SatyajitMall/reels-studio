#!/usr/bin/env python3
"""Render kinetic-type word cards as 1080x1920 transparent PNGs for V5.

Bold condensed text with a soft glow and drop shadow, centred horizontally at a given y.
It fails if the text box leaves the Instagram safe zone (clear of top 220 px, bottom 320 px,
right 120 px; CLAUDE.md §3), so a card can't silently sit under the IG buttons.
Default font: the director's type style from studio/director-profile.md (DIN Condensed Bold on this Mac).

Usage:
  ./.venv/bin/python scripts/render_type_cards.py "DUM" "DURGA" -o projects/<reel>/renders/overlays
  ./.venv/bin/python scripts/render_type_cards.py "DURGA PUJA 2026\\n@satyajitmall" --y 400 --size 120 --name endcard -o ...
Options: --font (name or path), --size, --y (centre), --color, --glow, --tracking.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
SAFE = {"top": 220, "bottom": H - 320, "left": 0, "right": W - 120}
FONT_DIRS = [Path("/System/Library/Fonts"), Path("/System/Library/Fonts/Supplemental"),
             Path("/Library/Fonts"), Path.home() / "Library/Fonts"]
FALLBACKS = ["Anton", "Bebas Neue", "DIN Condensed Bold", "Impact"]


def find_font(name: str) -> Path:
    p = Path(name)
    if p.is_file():
        return p
    for want in [name] + [f for f in FALLBACKS if f != name]:
        key = want.lower().replace(" ", "")
        for d in FONT_DIRS:
            for f in d.glob("*.[ot]t[fc]"):
                if f.stem.lower().replace(" ", "").replace("-", "") .startswith(key.replace("-", "")):
                    if want != name:
                        print(f"! font '{name}' not found, using {f.name}", file=sys.stderr)
                    return f
    sys.exit(f"No font found for '{name}' or fallbacks {FALLBACKS}")


def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def render(text: str, font: ImageFont.FreeTypeFont, y: int, color: str, glow: str, tracking: int) -> tuple[Image.Image, tuple[int, int, int, int]]:
    lines = text.split("\\n") if "\\n" in text else text.split("\n")
    # Measure each line with tracking applied.
    def line_w(s: str) -> int:
        return sum(font.getbbox(c)[2] - font.getbbox(c)[0] for c in s) + tracking * max(len(s) - 1, 0) if tracking \
            else font.getbbox(s)[2] - font.getbbox(s)[0]
    asc, desc = font.getmetrics()
    lh = int((asc + desc) * 1.05)
    total_h = lh * len(lines)
    top = y - total_h // 2

    text_layer = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(text_layer)
    boxes = []
    for i, s in enumerate(lines):
        w = line_w(s)
        x = (W - w) // 2
        ly = top + i * lh
        if tracking:
            cx = x
            for c in s:
                d.text((cx, ly), c, font=font, fill=255)
                cx += font.getbbox(c)[2] - font.getbbox(c)[0] + tracking
        else:
            d.text((x, ly), s, font=font, fill=255)
    bbox = text_layer.getbbox()
    if bbox is None:
        sys.exit(f"'{text}' rendered empty")
    l, t, r, b = bbox
    if t < SAFE["top"] or b > SAFE["bottom"] or l < SAFE["left"] or r > SAFE["right"]:
        sys.exit(f"✗ '{text}' leaves the safe zone: box x {l}–{r}, y {t}–{b}; "
                 f"allowed x ≤ {SAFE['right']}, y {SAFE['top']}–{SAFE['bottom']}. Lower --size or move --y.")

    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow = text_layer.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.6))
    out.paste(Image.new("RGBA", (W, H), (0, 0, 0, 255)), (6, 8), shadow)
    glow_mask = text_layer.filter(ImageFilter.GaussianBlur(18)).point(lambda v: min(255, int(v * 1.4)))
    out.paste(Image.new("RGBA", (W, H), (*hex_rgb(glow), 255)), (0, 0), glow_mask)
    out.paste(Image.new("RGBA", (W, H), (*hex_rgb(color), 255)), (0, 0), text_layer)
    return out, bbox


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("texts", nargs="+", help='words or lines; use "\\n" for a line break')
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--font", default="DIN Condensed Bold")
    ap.add_argument("--size", type=int, default=260)
    ap.add_argument("--y", type=int, default=900, help="vertical centre of the text block")
    ap.add_argument("--color", default="#F5E6C8")
    ap.add_argument("--glow", default="#D4A017")
    ap.add_argument("--tracking", type=int, default=6, help="extra px between letters")
    ap.add_argument("--name", help="file name (single text only); default word_<TEXT>.png")
    args = ap.parse_args()

    font = ImageFont.truetype(str(find_font(args.font)), args.size)
    args.out.mkdir(parents=True, exist_ok=True)
    for text in args.texts:
        img, (l, t, r, b) = render(text, font, args.y, args.color, args.glow, args.tracking)
        stem = args.name if (args.name and len(args.texts) == 1) else "word_" + re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
        path = args.out / f"{stem}.png"
        img.save(path)
        print(f"✓ {path}  box x {l}–{r}, y {t}–{b}")


if __name__ == "__main__":
    main()
