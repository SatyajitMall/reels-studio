"""Title and letter-line type sheets for Round 2 (reel-local, could-not-go-home-diwali).

1. titles_sheet.jpg: each title option in Western and Indo-western faces, cream on a dark frame of the reel.
2. lines_sheet.jpg: letter-line styles on a 9:16 phone frame (4:3 window, IG bands shaded).

PIL here has no raqm, so only Latin script (Hinglish) is rendered; Devanagari would need HyperFrames (browser shaping).
Usage: .venv/bin/python -I tools/type_sheet.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path(__file__).resolve().parents[3] / "assets" / "fonts"
SUP = Path("/System/Library/Fonts/Supplemental")
CREAM = (245, 230, 200)

FACES = [  # (label, path, index, size scale)
    ("Baskerville Italic · Western letter", SUP / "Baskerville.ttc", 2, 1.0),
    ("Didot Italic · Western editorial", SUP / "Didot.ttc", 1, 1.0),
    ("DIN Condensed Bold · studio profile", SUP / "DIN Condensed Bold.ttf", 0, 1.1),
    ("Snell Roundhand Bold · handwritten", SUP / "SnellRoundhand.ttc", 1, 1.0),
    ("Yatra One · Indo-western brush", FONTS / "YatraOne-Regular.ttf", 0, 0.95),
    ("Rozha One · Indo-western display", FONTS / "RozhaOne-Regular.ttf", 0, 0.95),
    ("Amita Bold · Indo-western calligraphic", FONTS / "Amita-Bold.ttf", 0, 0.9),
    ("Eczar · Indo-western serif", FONTS / "Eczar[wght].ttf", 0, 0.95),
]
TITLES = ["Diwali, door se", "Mera diya bhi jalaana", "Is baar nahi, Maa"]
SUBS = ["Diwali, from afar", "Light my diya too", "Not this time, Maa"]


def font(path, idx, size):
    return ImageFont.truetype(str(path), size, index=idx)


def fit(d, text, path, idx, maxw, start):
    s = start
    while s > 20:
        f = font(path, idx, s)
        if d.textlength(text, font=f) <= maxw:
            return f
        s -= 2
    return font(path, idx, s)


def titles_sheet(bg_still, out):
    tw, th = 520, 230
    lab_h = 30
    bg = Image.open(bg_still).convert("RGB")
    bg = bg.resize((tw, int(bg.height * tw / bg.width))).crop((0, 0, tw, th)).filter(ImageFilter.GaussianBlur(6))
    bg = Image.blend(bg, Image.new("RGB", bg.size, (0, 0, 0)), 0.55)
    lab_f = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 20, index=1)
    sub_f = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 19, index=8)
    W = 12 + len(TITLES) * (tw + 12)
    H = 12 + len(FACES) * (th + lab_h + 12)
    S = Image.new("RGB", (W, H), (22, 22, 22))
    d = ImageDraw.Draw(S)
    for r, (label, path, idx, sc) in enumerate(FACES):
        y = 12 + r * (th + lab_h + 12)
        d.text((12, y + 4), f"{r + 1}. {label}", font=lab_f, fill=(255, 210, 120))
        for c, (t, sub) in enumerate(zip(TITLES, SUBS)):
            x = 12 + c * (tw + 12)
            tile = bg.copy()
            td = ImageDraw.Draw(tile)
            f = fit(td, t, path, idx, tw - 60, int(64 * sc))
            bbox = td.textbbox((0, 0), t, font=f)
            tx = (tw - (bbox[2] - bbox[0])) // 2 - bbox[0]
            ty = (th - (bbox[3] - bbox[1])) // 2 - bbox[1] - 18
            glow = Image.new("RGBA", tile.size, (0, 0, 0, 0))
            ImageDraw.Draw(glow).text((tx, ty), t, font=f, fill=(255, 190, 90, 150))
            glow = glow.filter(ImageFilter.GaussianBlur(7))
            tile.paste(glow, (0, 0), glow)
            td = ImageDraw.Draw(tile)
            td.text((tx, ty), t, font=f, fill=CREAM)
            sw = td.textlength(sub, font=sub_f)
            td.text(((tw - sw) // 2, ty + (bbox[3] - bbox[1]) + 34), sub, font=sub_f, fill=(225, 225, 225))
            S.paste(tile, (x, y + lab_h))
    S.save(out, quality=88)
    print(out, S.size)


def phone_lines(still, out, hi, en):
    W, H, TOP, BOT, RIGHT = 1080, 1920, 220, 320, 120
    styles = [
        ("1 · Reference: Helvetica Neue Italic, white, in quotes", "/System/Library/Fonts/HelveticaNeue.ttc", 2, 44, (255, 255, 255), True, "/System/Library/Fonts/HelveticaNeue.ttc", 8),
        ("2 · Letter serif: Baskerville Italic, cream", str(SUP / "Baskerville.ttc"), 2, 52, CREAM, False, str(SUP / "Baskerville.ttc"), 2),
        ("3 · Handwritten: Snell Roundhand Bold, cream", str(SUP / "SnellRoundhand.ttc"), 1, 54, CREAM, False, str(SUP / "Baskerville.ttc"), 2),
        ("4 · Indo-western: Eczar, cream", str(FONTS / "Eczar[wght].ttf"), 0, 48, CREAM, False, str(SUP / "Baskerville.ttc"), 2),
    ]
    src = Image.open(still).convert("RGB")
    sw, sh = src.size
    cw = int(sh * 4 / 3)
    win = src.crop(((sw - cw) // 2, 0, (sw - cw) // 2 + cw, sh)).resize((W, 810), Image.LANCZOS)
    tw, th = 405, 720
    lab_f = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 19, index=1)
    S = Image.new("RGB", (12 + len(styles) * (tw + 12), th + 60), (22, 22, 22))
    sd = ImageDraw.Draw(S)
    for i, (label, fp, fi, size, col, quotes, efp, efi) in enumerate(styles):
        ph = Image.new("RGB", (W, H), (0, 0, 0))
        y0 = (TOP + H - BOT) // 2 - 405
        ph.paste(win, (0, y0))
        d = ImageDraw.Draw(ph, "RGBA")
        f = ImageFont.truetype(fp, size, index=fi)
        fe = ImageFont.truetype(efp, 32, index=efi)
        text = f"“{hi}”" if quotes else hi
        y = y0 + 810 + 46
        d.text((70, y), text, font=f, fill=col)
        d.text((70, y + size + 22), en, font=fe, fill=(230, 230, 230, 200))
        d.rectangle([0, 0, W, TOP], fill=(255, 40, 40, 55))
        d.rectangle([0, H - BOT, W, H], fill=(255, 40, 40, 55))
        d.rectangle([W - RIGHT, 0, W, H], fill=(255, 40, 40, 40))
        x = 12 + i * (tw + 12)
        sd.text((x, 10), label.split(":")[0], font=lab_f, fill=(255, 210, 120))
        sd.text((x, 32), label.split(": ")[1] if ": " in label else "", font=lab_f, fill=(200, 200, 200))
        S.paste(ph.resize((tw, th), Image.LANCZOS), (x, 58))
    S.save(out, quality=88)
    print(out, S.size)


if __name__ == "__main__":
    out = ROOT / "analysis" / "type"
    out.mkdir(parents=True, exist_ok=True)
    titles_sheet(ROOT / "analysis/stills/C047_baked.png", out / "titles_sheet.jpg")
    phone_lines(ROOT / "analysis/stills/C062_baked.png", out / "lines_sheet.jpg", "Phone pe aarti dikha dena.", "Show me the aarti on the phone.")
