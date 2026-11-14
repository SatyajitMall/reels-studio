"""v6 type (reel-local, 2026-11-12). Director on v5b: "I just want the text to be ... Hindi written in English ... I don't
want it to be translated in English and written across. But I want the font to change" → picked "A Avenir Next" from
analysis/v5b_notes/font_options.jpg; and the picture goes to the whole 16:9 camera frame (window y 606–1214).

Each letter line: the Hinglish line only, Avenir Next Medium 46, cream #F5E6C8, the same soft glow + offset shadow as v4e
(make_type_v4d.compose), in a clear corner of the 16:9 window (per-line overrides after checking the v6 frames).
End card: "Mera diya bhi jalaana" (Avenir Next Medium) and "— tumhara beta" (Avenir Next Italic), @satyajitmall small.
Writes renders/overlays/v6/v6_line_0N.png, v6_end_card.png, v6_window_matte_16x9.png.
Usage (reel folder): ../../.venv/bin/python tools/make_type_v6.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from make_type_v4d import compose, width  # noqa: E402

AV = "/System/Library/Fonts/Avenir Next.ttc"
F_LINE = ImageFont.truetype(AV, 46, index=5)      # Medium
CREAM = (245, 230, 200, 255)
WIN = (0, 606, 1080, 1214)                        # 16:9 window, centre y 910
MX, MY, RIGHT = 60, 38, 930
LINES = [  # text, corner, overrides
    ("Maa, is baar ghar nahi aa paaunga.", "BR", {}),
    ("Yahan Diwali pe sabse zyada kaam hai.", "TL", {"maxw": 340}),     # v6 check: BL sat on his hands in 06
    ("Tumhare haath ka khaana yaad aata hai.", "BR", {"maxw": 320, "right": 940, "my": 24}),   # v6 check: 3 narrow lines far right; 08 slid left
    ("Phone pe aarti dikha dena.", "BL", {"my": 18, "mx": 40}),        # v6 check: lower; review_v6 #3: 20 px left
    ("Papa se kehna, main theek hoon.", "TR", {"right": 950}),
    ("Agle saal, pakka.", "BL", {}),
]


def wrap(text, f, maxw):
    """One line if it fits; else the most balanced 2-line split that fits; else greedy lines within maxw."""
    if width(text, f) <= maxw:
        return [text]
    w = text.split()
    two = [(max(width(" ".join(w[:k]), f), width(" ".join(w[k:]), f)), k) for k in range(1, len(w))]
    fit = [t for t in two if t[0] <= maxw]
    if fit:
        k = min(fit)[1]; return [" ".join(w[:k]), " ".join(w[k:])]
    rows, cur = [], []
    for word in w:
        if cur and width(" ".join(cur + [word]), f) > maxw:
            rows.append(" ".join(cur)); cur = [word]
        else:
            cur.append(word)
    return rows + [" ".join(cur)]


def line(text, corner, ov):
    maxw, right, my, mx = ov.get("maxw", 470), ov.get("right", RIGHT), ov.get("my", MY), ov.get("mx", MX)
    rows = wrap(text, F_LINE, maxw)
    lh = 56; h = lh * len(rows)
    y = WIN[1] + my - 8 if corner[0] == "T" else WIN[3] - my - h
    spec = []
    for t in rows:
        x = mx if corner[1] == "L" else right - width(t, F_LINE)
        spec.append((t, F_LINE, 0, CREAM, x, y)); y += lh
    return compose(spec, None)


def end_card():
    t1, f1 = "Mera diya bhi jalaana", ImageFont.truetype(AV, 76, index=5)
    t2, f2 = "— tumhara beta", ImageFont.truetype(AV, 50, index=4)          # Italic
    t3, f3 = "@satyajitmall", ImageFont.truetype(AV, 26, index=7)           # Regular
    rows = [(t1, f1, 0, CREAM, 540 - width(t1, f1) / 2, 846),
            (t2, f2, 0, CREAM, 540 - width(t2, f2) / 2, 960),
            (t3, f3, 1, (255, 255, 255, 140), 540 - width(t3, f3, 1) / 2, 1500)]
    return compose(rows, None)


def matte():
    m = Image.new("RGBA", (1080, 1920), (0, 0, 0, 255))
    m.paste((0, 0, 0, 0), (0, WIN[1], 1080, WIN[3]))
    return m


def main():
    out = Path("renders/overlays/v6"); out.mkdir(parents=True, exist_ok=True)
    for i, (t, c, ov) in enumerate(LINES, 1):
        im = line(t, c, ov); im.save(out / f"v6e_line_{i:02d}.png"); print(i, im.getbbox())
    ec = end_card(); ec.save(out / "v6_end_card.png"); print("end", ec.getbbox())
    matte().save(out / "v6_window_matte_16x9.png")


if __name__ == "__main__":
    main()
