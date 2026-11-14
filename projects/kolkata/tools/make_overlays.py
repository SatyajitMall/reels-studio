#!/usr/bin/env python3
"""KOLKATA preview overlays (reel-local tool, not a studio script).

Writes into projects/kolkata/renders/overlays/:
  window_matte.png   1080x1920 black with a transparent 4:5 window (1080x1350, centred at y=910): the director's
                     framing choice for every shot (Round 2, CR-20261104-kolkata-landscape-footage-9x16)
  title_calcutta.png the "Calcutta" title: marigold-yellow serif with a red offset drop shadow (Round 1/2), placed in
                     the window's upper part over the chai steam. Preview stand-in for the HyperFrames title.
Usage: ./.venv/bin/python projects/kolkata/tools/make_overlays.py [--title-y 470] [--size 210]
"""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
WIN_W, WIN_H, WIN_CY = 1080, 1350, 910
OUT = Path(__file__).resolve().parents[1] / "renders" / "overlays"
YELLOW = (244, 184, 28, 255)
RED = (196, 22, 38, 255)


def matte() -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    top = WIN_CY - WIN_H // 2
    ImageDraw.Draw(im).rectangle((0, top, WIN_W - 1, top + WIN_H - 1), fill=(0, 0, 0, 0))
    return im


def title(text: str, y: int, size: int) -> Image.Image:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/BigCaslon.ttf", size)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    bw = d.textbbox((0, 0), text, font=font)
    x = (W - (bw[2] - bw[0])) // 2 - bw[0]
    soft = Image.new("RGBA", (W, H), (0, 0, 0, 0))     # soft dark halo so it reads over bright steam
    ImageDraw.Draw(soft).text((x, y), text, font=font, fill=(0, 0, 0, 110))
    im = Image.alpha_composite(im, soft.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(im)
    off = max(4, size // 36)
    d.text((x + off, y + off), text, font=font, fill=RED)  # red offset shadow
    d.text((x, y), text, font=font, fill=YELLOW)
    return im


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--title-y", type=int, default=470)
    ap.add_argument("--size", type=int, default=210)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    matte().save(OUT / "window_matte.png")
    title("Calcutta", a.title_y, a.size).save(OUT / "title_calcutta.png")
    print("✓", OUT / "window_matte.png", OUT / "title_calcutta.png")
