"""Letter lines ON the picture for v4 (reel-local). Director, 2026-11-11: "text at the bottom eats up a lot of the
screen ... can we have the text on the video like on the reference" → layout B (4:3 window kept, text on picture).

The reference sets a small italic line on the picture, top-left. Here top-left would sit on a head or the working hands
in 9 of 18 shots (heads are framed near the top), so each line takes the corner that is clear through all three of its
shots (analysis/layout_v3f/placement_check.jpg): L1 bottom-right, L5 top-right (v4b: top-left touched the paan maker's head on 14, review_v4 #1), L2/L3/L4/L6 bottom-left; long lines wrap
into two balanced lines so the block stays narrow (clear of hands at the bottom centre).
Type as the brief: Baskerville Italic, Hinglish cream #F5E6C8, English 80 % white; smaller than the band version
(44 / 28 px against 54 / 34) and with a soft shadow so it reads on the picture.

Writes renders/overlays/v4/line_0N.png (1080×1920 RGBA) and analysis/layout_v3f/lines_v4_preview.jpg.
Usage (reel folder): python3 tools/make_lines_v4.py
"""
import io
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SUP = Path("/System/Library/Fonts/Supplemental")
F1 = ImageFont.truetype(str(SUP / "Baskerville.ttc"), 44, index=2)
F2 = ImageFont.truetype(str(SUP / "Baskerville.ttc"), 28, index=2)
WIN = (0, 505, 1080, 1315)
MX, MB, RIGHT = 64, 46, 930          # left margin, bottom margin in the window, right edge (clear of IG's buttons at x ≥ 960)
LINES = [
    ("Maa, is baar ghar nahi aa paaunga.", "Maa, I can't come home this time.", "BR", [20, 58, 97]),
    ("Yahan Diwali pe sabse zyada kaam hai.", "Diwali is our busiest night here.", "BL", [136, 176, 216]),
    ("Tumhare haath ka khaana yaad aata hai.", "I miss food made by your hands.", "BL", [256, 296, 336]),
    ("Phone pe aarti dikha dena.", "Show me the aarti on the phone.", "BL", [375, 415, 455], {"mb": 26}),   # v4c: 20 px lower, clear of the phone hand
    ("Papa se kehna, main theek hoon.", "Tell Papa I'm fine.", "TR", [480, 518, 522, 535, 575], {"right": 950}),   # v4c: 20 px right, clear of his hair
    ("Agle saal, pakka.", "Next year. Promise.", "BL", [614, 654, 694]),
]
MAXW = 430


def wrap(text, font, maxw):
    """One line if it fits, else two balanced lines (no orphan word)."""
    if font.getlength(text) <= maxw:
        return [text]
    words = text.split()
    best = min(range(1, len(words)), key=lambda k: abs(font.getlength(" ".join(words[:k])) - font.getlength(" ".join(words[k:]))))
    return [" ".join(words[:best]), " ".join(words[best:])]


def render(hi, en, corner, ov=None):
    ov = ov or {}; mb = ov.get("mb", MB); right = ov.get("right", RIGHT)
    hl, el = wrap(hi, F1, MAXW), wrap(en, F2, MAXW)
    rows = [(t, F1, (245, 230, 200, 255), 52) for t in hl] + [(t, F2, (255, 255, 255, 204), 36) for t in el]
    h = sum(r[3] for r in rows) + 8
    y = WIN[1] + MB - 6 if corner in ("TL", "TR") else WIN[3] - mb - h
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh); d = ImageDraw.Draw(img)
    yy = y
    for i, (t, f, col, lh) in enumerate(rows):
        if i == len(hl):
            yy += 8
        w = f.getlength(t)
        x = MX if corner in ("BL", "TL") else right - w
        ds.text((x + 1, yy + 2), t, font=f, fill=(0, 0, 0, 230))
        d.text((x, yy), t, font=f, fill=col, stroke_width=1, stroke_fill=(20, 16, 12, 150))   # v4b: thin dark edge (review_v4 #3)
        yy += lh
    wide = sh.filter(ImageFilter.GaussianBlur(9))
    tight = sh.filter(ImageFilter.GaussianBlur(2.5))
    base = Image.alpha_composite(Image.alpha_composite(wide, wide), tight)   # soft halo + a tight edge: reads on white too
    return Image.alpha_composite(base, img)


def frame(n):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "renders/masters/could-not-go-home-diwali_v3f_master.mov", "-vf",
                          f"select=eq(n\\,{n})", "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(raw)).convert("RGBA")


def main():
    out = Path("renders/overlays/v4"); out.mkdir(parents=True, exist_ok=True)
    tiles = []
    for i, row in enumerate(LINES, 1):
        hi, en, corner, frames = row[:4]
        ov = render(hi, en, corner, row[4] if len(row) > 4 else None); ov.save(out / f"line_{i:02d}.png"); ov.save(out / f"v4c_line_{i:02d}.png")
        for n in frames:
            fr = Image.alpha_composite(frame(n), ov).crop(WIN).convert("RGB").resize((360, 270), Image.LANCZOS)
            tiles.append(fr)
    S = Image.new("RGB", (3 * 364, 7 * 274), (18, 18, 18))
    for k, t in enumerate(tiles):
        S.paste(t, ((k % 3) * 364, (k // 3) * 274))
    S.save("analysis/layout_v3f/lines_v4_preview.jpg", quality=88)
    print("wrote", out, "and analysis/layout_v3f/lines_v4_preview.jpg")


if __name__ == "__main__":
    main()
