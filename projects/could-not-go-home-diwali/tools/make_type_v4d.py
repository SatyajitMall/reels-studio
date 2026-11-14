"""Letter lines + end card in the Kolkata reel's type (reel-local, v4d). Director, 2026-11-11 on v4c: "I don't like the
text style and the font style ... can we look at how in the reel Kolkata we use text? That would be much better."

Kolkata's title (projects/kolkata/tools/make_title_v7.py, style "amita", the director's pick there): Amita Bold for the
word, Tiro Bangla Italic for the small line, Eczar SemiBold caps with tracking; cream #F5E6C8; a wide soft dark glow
(blur 42) plus a small offset shadow (2,3 px, blur 4); no outline. Fonts are the studio's (assets/fonts, OFL).

Here: each letter line = Hinglish in Amita Bold + the English in Eczar SemiBold caps (tracked), in the same clear corner
per line as v4c (L1 bottom-right, L5 top-right, the rest bottom-left; L4 sits 20 px lower, L5's right edge at 950).
End card: "Mera diya bhi jalaana" Amita · "LIGHT MY DIYA TOO" Eczar caps · "— tumhara beta" Tiro Bangla Italic ·
@satyajitmall Eczar, centred where the old card was.
Writes renders/overlays/v4d/v4d_line_0N.png, v4d_end_card.png, and analysis/v4c_notes/type_v4d_preview.jpg.
Usage (reel folder): python3 tools/make_type_v4d.py
"""
import io
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AF = str(Path.home() / "Documents/reels-studio/assets/fonts") + "/"
CREAM = (245, 230, 200, 255)
WIN = (0, 505, 1080, 1315)
MX, MB, RIGHT = 64, 46, 930
LINES = [
    ("Maa, is baar ghar nahi aa paaunga.", "Maa, I can't come home this time.", "BR", [20, 58, 97], {}),
    ("Yahan Diwali pe sabse zyada kaam hai.", "Diwali is our busiest night here.", "BL", [136, 176, 216], {"maxw": 360}),   # v4e: clear of 04's tongs
    ("Tumhare haath ka khaana yaad aata hai.", "I miss food made by your hands.", "BL", [256, 296, 336], {"maxw": 360}),   # v4e: off 08's board
    ("Phone pe aarti dikha dena.", "Show me the aarti on the phone.", "BL", [375, 400, 420], {"mb": 8}),   # v4e: 18 px lower again
    ("Papa se kehna, main theek hoon.", "Tell Papa I'm fine.", "TR", [480, 518, 535, 575], {"right": 950}),
    ("Agle saal, pakka.", "Next year. Promise.", "BL", [600, 640, 690], {"mb": 14}),   # v4e: lower, under 18's forearm and 19's sparkler
]


def font(name, size, var=None):
    f = ImageFont.truetype(AF + name, size)
    if var:
        f.set_variation_by_name(var)
    return f


F_HI = font("Amita-Bold.ttf", 44)
F_EN = font("Eczar[wght].ttf", 24, "SemiBold")   # v4e: 21 → 24 (phone legibility)
TRACK_EN = 3


def width(text, f, tr=0):
    return sum(f.getlength(c) for c in text) + tr * (len(text) - 1) if tr else f.getlength(text)


def tracked(d, x, y, text, f, tr, fill):
    if not tr:
        d.text((x, y), text, font=f, fill=fill); return
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill); x += f.getlength(ch) + tr


def wrap(text, f, maxw, tr=0):
    """Fewest lines (1–3) whose every line fits maxw; words split to balance the line widths."""
    w = text.split()
    if width(text, f, tr) <= maxw:
        return [text]
    best = None
    for i in range(1, len(w)):
        a, b = " ".join(w[:i]), " ".join(w[i:])
        if max(width(a, f, tr), width(b, f, tr)) <= maxw:
            score = abs(width(a, f, tr) - width(b, f, tr))
            best = min(best, (score, [a, b])) if best else (score, [a, b])
    if best:
        return best[1]
    for i in range(1, len(w) - 1):
        for j in range(i + 1, len(w)):
            parts = [" ".join(w[:i]), " ".join(w[i:j]), " ".join(w[j:])]
            m = max(width(x, f, tr) for x in parts)
            if m <= maxw:
                score = m - min(width(x, f, tr) for x in parts)
                best = min(best, (score, parts)) if best else (score, parts)
    return best[1] if best else [text]


def compose(rows, place):
    """rows: [(text, font, track, colour, line_height, gap_before)]; place(i, w) → x. Kolkata glow + shadow."""
    glow = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); shadow, text = glow.copy(), glow.copy()
    g, s, d = ImageDraw.Draw(glow), ImageDraw.Draw(shadow), ImageDraw.Draw(text)
    for (t, f, tr, col, x, y) in rows:
        tracked(g, x, y, t, f, tr, (0, 0, 0, 170)); tracked(s, x + 2, y + 3, t, f, tr, (0, 0, 0, 210)); tracked(d, x, y, t, f, tr, col)
    out = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    out.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18)))   # 42 on Kolkata's big title; scaled to this type size
    out.alpha_composite(glow.filter(ImageFilter.GaussianBlur(6)))
    out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(3)))
    out.alpha_composite(text)
    return out


def line(hi, en, corner, ov):
    mb, right, maxw = ov.get("mb", MB), ov.get("right", RIGHT), ov.get("maxw", 450)
    en = en.upper()
    hl, el = wrap(hi, F_HI, maxw), wrap(en, F_EN, maxw, TRACK_EN)
    spec = [(t, F_HI, 0, CREAM, 54) for t in hl] + [(t, F_EN, TRACK_EN, (245, 230, 200, 225), 33) for t in el]
    h = sum(r[4] for r in spec) + 10
    y = WIN[1] + MB - 6 if corner in ("TL", "TR") else WIN[3] - mb - h
    rows = []
    for i, (t, f, tr, col, lh) in enumerate(spec):
        if i == len(hl):
            y += 10
        w = width(t, f, tr)
        x = MX if corner in ("BL", "TL") else right - w
        rows.append((t, f, tr, col, x, y)); y += lh
    return compose(rows, None)


def end_card():
    spec = [("Mera diya bhi jalaana", font("Amita-Bold.ttf", 92), 1, CREAM, 0),
            ("LIGHT MY DIYA TOO", font("Eczar[wght].ttf", 30, "SemiBold"), 6, (245, 230, 200, 215), 14),
            ("— tumhara beta", font("TiroBangla-Italic.ttf", 58), 0, CREAM, 70)]
    rows, y = [], 846
    for t, f, tr, col, gap in spec:
        while width(t, f, tr) > 840:   # v4e: Kolkata's rule, x 120–960 (review_v4d #1)
            f = ImageFont.truetype(f.path, f.size - 2)
        y += gap; bb = f.getbbox(t); w = width(t, f, tr)
        rows.append((t, f, tr, col, 540 - w / 2, y - bb[1])); y += bb[3] - bb[1]
    h = font("Eczar[wght].ttf", 26, "Regular"); t = "@satyajitmall"
    rows.append((t, h, 1, (255, 255, 255, 140), 540 - width(t, h, 1) / 2, 1500))
    return compose(rows, None)


def frame(n, video="renders/masters/could-not-go-home-diwali_v3f_master.mov"):   # v3f: text in the band, picture clean
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf", f"select=eq(n\\,{n})", "-frames:v", "1",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(raw)).convert("RGBA")


def main():
    out = Path("renders/overlays/v4d"); out.mkdir(parents=True, exist_ok=True)
    tiles = []
    for i, (hi, en, corner, frames, ov) in enumerate(LINES, 1):
        o = line(hi, en, corner, ov); o.save(out / f"v4e_line_{i:02d}.png")
        for n in frames[:3]:
            tiles.append(Image.alpha_composite(frame(n), o).crop(WIN).convert("RGB").resize((360, 270), Image.LANCZOS))
    ec = end_card(); ec.save(out / "v4e_end_card.png"); print("end card bbox", ec.getbbox())
    card = Image.alpha_composite(Image.new("RGBA", (1080, 1920), (0, 0, 0, 255)), ec).convert("RGB").resize((360, 640))
    S = Image.new("RGB", (4 * 364, 6 * 274), (18, 18, 18))
    for k, t in enumerate(tiles):
        S.paste(t, ((k % 3) * 364, (k // 3) * 274))
    S.paste(card.crop((0, 140, 360, 640)).resize((364 * 270 // 500 * 500 // 270 if False else 360, 500)), (3 * 364, 0))
    S.save("analysis/v4c_notes/type_v4e_preview.jpg", quality=88)
    print("wrote", out, "analysis/v4c_notes/type_v4d_preview.jpg")


if __name__ == "__main__":
    main()
