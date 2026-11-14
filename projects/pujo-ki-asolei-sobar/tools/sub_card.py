#!/usr/bin/env python3
"""Subtitle card PNG in the reel's style (fitted to the existing cards in renders/overlays/subs: DIN Condensed Bold 68 px,
+1.7 px tracking, line pitch 66 px, warm white, dark soft halo; block centred at x 540). Used in round 14 to re-word cards to the director's own VO.
Usage: sub_card.py <out.png> "line 1|line 2"
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
REEL = Path(__file__).resolve().parents[1]; DIN = str(REEL / "graphics/title/assets/fonts/DINCondensed-Bold.ttf")
COL, SHC = (248, 244, 236), (6, 4, 1)
SIZE, PITCH, CY, SIG, OP, TRACK = 68, 66, 1475, 16, 1.8, 1.7      # TRACK: px letter-spacing (cards were set with ~0.025 em)

def card(lines, size=SIZE, pitch=PITCH, cy=CY, sig=SIG, op=OP):
    f = ImageFont.truetype(DIN, size); m = Image.new("L", (1080, 1920), 0); d = ImageDraw.Draw(m)
    y0 = cy - pitch * (len(lines) - 1) / 2
    for i, ln in enumerate(lines):
        adv = [f.getlength(ln[:k + 1]) - f.getlength(ln[:k]) + TRACK for k in range(len(ln))]; x = 540 - (sum(adv) - TRACK) / 2
        for ch, a in zip(ln, adv): d.text((x, y0 + i * pitch), ch, font=f, fill=255, anchor="lm"); x += a
    sh = np.clip(np.asarray(m.filter(ImageFilter.GaussianBlur(sig)), np.float32) / 255 * op, 0, 1); tm = np.asarray(m, np.float32) / 255
    A = tm + sh * (1 - tm); C = (np.array(COL) * tm[..., None] + np.array(SHC) * (sh * (1 - tm))[..., None]) / np.maximum(A, 1e-6)[..., None]
    return Image.fromarray(np.dstack([C, A * 255]).clip(0, 255).astype(np.uint8), "RGBA")

if __name__ == "__main__":
    card(sys.argv[2].split("|")).save(sys.argv[1]); print("✓", sys.argv[1])
