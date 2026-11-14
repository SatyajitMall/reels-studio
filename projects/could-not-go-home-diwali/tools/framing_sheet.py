"""Framing options for landscape footage in a 9:16 reel (effects-playbook §B), on the director's own stills.

Reel-local tool (could-not-go-home-diwali). Each option is a 1080×1920 phone frame with the Instagram UI bands
shaded (top 220, bottom 320, right 120) and a sample letter line placed where that option would carry it.

Usage: .venv/bin/python -I tools/framing_sheet.py <still.png> [...] -o analysis/framing/framing_sheet.jpg --line "..."
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
TOP, BOT, RIGHT = 220, 320, 120
SAFE_C = (TOP + (H - BOT)) // 2  # vertical centre of the safe area (910)
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"


def window(still, aspect):
    """Crop the landscape still to `aspect` (w/h) keeping full height, scale to 1080 wide."""
    sw, sh = still.size
    cw = min(sw, int(round(sh * aspect)))
    x0 = (sw - cw) // 2
    crop = still.crop((x0, 0, x0 + cw, sh))
    return crop.resize((W, int(round(W / aspect))), Image.LANCZOS), cw / sw


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur]


def phone(still, opt, line):
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    if opt == "A":
        sw, sh = still.size
        s = H / sh
        big = still.resize((int(sw * s), H), Image.LANCZOS)
        x0 = (big.width - W) // 2
        canvas.paste(big.crop((x0, 0, x0 + W, H)), (0, 0))
        kept = W / big.width
        text_y, on_picture = H - BOT - 170, True
        label = f"A · full-bleed · {kept:.0%} width"
    else:
        aspect = {"B": 16 / 9, "R": 4 / 3, "C": 4 / 5}[opt]
        win, kept = window(still, aspect)
        y0 = SAFE_C - win.height // 2
        canvas.paste(win, (0, y0))
        bottom = y0 + win.height
        if bottom + 190 < H - BOT:
            text_y, on_picture = bottom + 40, False
        else:
            text_y, on_picture = bottom - 230, True
        name = {"B": "16:9 frame", "R": "4:3 (reference)", "C": "4:5 (KOLKATA)"}[opt]
        label = f"{opt} · {name} · {kept:.0%} width"
    d = ImageDraw.Draw(canvas, "RGBA")
    f = ImageFont.truetype(FONT, 46, index=2)  # Helvetica Neue Italic
    fe = ImageFont.truetype(FONT, 32, index=8)  # Light Italic
    hi, en = line
    x = 70
    if on_picture:
        d.rectangle([0, text_y - 20, W, text_y + 170], fill=(0, 0, 0, 90))
    y = text_y
    for ln in wrap(d, hi, f, W - RIGHT - x - 20):
        d.text((x, y), ln, font=f, fill=(255, 255, 255)); y += 58
    for ln in wrap(d, en, fe, W - RIGHT - x - 20):
        d.text((x, y + 4), ln, font=fe, fill=(255, 255, 255, 190)); y += 42
    # IG bands
    d.rectangle([0, 0, W, TOP], fill=(255, 40, 40, 55))
    d.rectangle([0, H - BOT, W, H], fill=(255, 40, 40, 55))
    d.rectangle([W - RIGHT, 0, W, H], fill=(255, 40, 40, 40))
    return canvas, label


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stills", nargs="+")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--line", default="Maa, is baar Diwali pe ghar nahi aa paaunga.|Maa, I can't come home this Diwali.")
    ap.add_argument("--opts", default="R,C,B,A")
    a = ap.parse_args()
    line = a.line.split("|")
    opts = a.opts.split(",")
    tw, th = 405, 720
    lab_f = ImageFont.truetype(FONT, 22, index=1)
    sheet = Image.new("RGB", (len(opts) * (tw + 12) + 12, len(a.stills) * (th + 48) + 12), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    for r, s in enumerate(a.stills):
        still = Image.open(s).convert("RGB")
        for c, o in enumerate(opts):
            ph, label = phone(still, o, line)
            x, y = 12 + c * (tw + 12), 12 + r * (th + 48)
            d.text((x, y + 4), label, font=lab_f, fill=(255, 220, 120))
            sheet.paste(ph.resize((tw, th), Image.LANCZOS), (x, y + 36))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(a.out, quality=88)
    print(a.out, sheet.size)


if __name__ == "__main__":
    main()
