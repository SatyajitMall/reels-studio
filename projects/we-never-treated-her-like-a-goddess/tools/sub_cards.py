#!/usr/bin/env python3
"""Subtitle cards + end card for this reel, as 1080x1920 transparent PNGs for V5.

Style (brief §Type): Helvetica Neue Medium, yellow #F2D33B, soft 60 % shadow, centred, baseline y≈1540.
End card: আসছে বছর আবার হবে in Kohinoor Bangla (cream) + @satyajitmall in the subtitle style.
Fails if any text leaves the IG safe zone (top 220, bottom 320, right 120 px).
Writes analysis/subtitles_v1.json (card, text, start/end frame at 25 fps) and a composite sheet of every card
over the graded preview, so faces under the text can be checked by eye.

Usage: ../../.venv/bin/python tools/sub_cards.py [--preview renders/previews/grade_a4.mp4]
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 25
SAFE = (0, 220, W - 120, H - 320)          # left, top, right, bottom
YELLOW, CREAM = (0xF2, 0xD3, 0x3B), (0xF1, 0xE6, 0xCF)
HNEUE, KOHINOOR = "/System/Library/Fonts/HelveticaNeue.ttc", "/System/Library/Fonts/KohinoorBangla.ttc"
SIZE, BASELINE = 46, 1540
END_F = 687                                 # picture end (fade to black 681-687), end card 687-746
CARD_END_F = 746

# (text, start s, end s) — starts on word onsets (transcripts/ref_words.json), ends on the next card or line end + 0.5 s
CARDS = [
    ("We never treated her", 0.00, 1.22), ("like a goddess,", 1.22, 2.32), ("and that's", 2.32, 3.02),
    ("the whole point", 3.02, 3.76), ("of Pujo.", 3.76, 4.74),
    ("I grew up", 4.96, 5.66), ("calling her Ma.", 5.66, 6.84),
    ("We dress her,", 6.86, 7.86), ("feed her,", 7.86, 8.38), ("and when she leaves,", 8.38, 9.40),
    ("we cry,", 9.40, 10.24), ("like a home", 10.24, 10.92), ("losing their daughter.", 10.92, 12.32),
    ("It doesn't make sense", 12.50, 13.44), ("at all,", 13.44, 13.90), ("and exactly", 13.90, 14.72),
    ("what makes it ours.", 14.72, 16.18),
    ("We Bangalis", 16.40, 17.08), ("make the divine", 17.08, 17.90), ("one of us.", 17.90, 19.36),
    ("And every year,", 19.36, 20.22), ("when Ma looks", 20.22, 20.82), ("back at us", 20.82, 21.64),
    ("from the pandals", 21.64, 22.48), ("across Kolkata,", 22.48, 23.86),
    ("the city", 23.98, 24.52), ("we are familiar with", 24.52, 25.74), ("feels like home again.", 25.74, END_F / FPS),
]


def frame(t: float) -> int:
    return math.floor(t * FPS + 1e-6)


def text_layer(lines: list[tuple[str, ImageFont.FreeTypeFont, tuple, int]]) -> tuple[Image.Image, list]:
    """lines: (text, font, rgb, baseline y). Returns the RGBA card and the text boxes."""
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dt, ds, dh = ImageDraw.Draw(txt), ImageDraw.Draw(shadow), ImageDraw.Draw(halo)
    boxes = []
    for s, font, rgb, base in lines:
        box = dt.textbbox((W / 2, base), s, font=font, anchor="ms")
        boxes.append(box)
        ds.text((W / 2 + 2, base + 3), s, font=font, anchor="ms", fill=(0, 0, 0, 153))   # 60 % shadow
        # dark halo: keeps yellow readable over gold, the boy's yellow shirt and white drum skin (v1 band check)
        dh.text((W / 2, base), s, font=font, anchor="ms", fill=(0, 0, 0, 200), stroke_width=4, stroke_fill=(0, 0, 0, 200))
        dt.text((W / 2, base), s, font=font, anchor="ms", fill=rgb + (255,))
    shadow = shadow.filter(ImageFilter.GaussianBlur(5))
    halo = halo.filter(ImageFilter.GaussianBlur(2.5))
    return Image.alpha_composite(Image.alpha_composite(shadow, halo), txt), boxes


def check_safe(name: str, boxes: list) -> None:
    for x0, y0, x1, y1 in boxes:
        if x0 < SAFE[0] or y0 < SAFE[1] or x1 > SAFE[2] or y1 > SAFE[3]:
            raise SystemExit(f"{name}: text box {x0, y0, x1, y1} leaves the safe zone {SAFE}")


CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ENDCARD_HTML = """<!doctype html><meta charset="utf-8"><style>
html,body{margin:0;width:1080px;height:1920px;background:transparent}
div{position:absolute;left:0;width:1080px;text-align:center;line-height:1;
 text-shadow:0 0 3px rgba(0,0,0,.8),2px 3px 6px rgba(0,0,0,.6)}
.bn{top:872px;font:500 64px 'Kohinoor Bangla';color:#F1E6CF}
.h{top:976px;font:500 46px 'Helvetica Neue';color:#F2D33B}
</style><div class="bn">আসছে বছর আবার হবে</div><div class="h">@satyajitmall</div>"""


def render_html_card(png: Path) -> Image.Image:
    html = png.with_suffix(".html"); html.write_text(ENDCARD_HTML, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=1080,1920", "--default-background-color=00000000",
                    f"--screenshot={png.resolve()}", html.resolve().as_uri()], check=True, capture_output=True)
    img = Image.open(png).convert("RGBA")
    if img.size != (W, H):
        raise SystemExit(f"Chrome card is {img.size}, expected {(W, H)}")
    return img


def grab(video: Path, t: float) -> Image.Image:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (W, H), raw).convert("RGBA")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", default="renders/previews/grade_a4.mp4")
    a = ap.parse_args()
    out = Path("renders/overlays/subs"); out.mkdir(parents=True, exist_ok=True)
    sub_font = ImageFont.truetype(HNEUE, SIZE, index=10)            # Medium
    rows, widest = [], 0
    for i, (s, t0, t1) in enumerate(CARDS, 1):
        img, boxes = text_layer([(s, sub_font, YELLOW, BASELINE)])
        check_safe(f"sub_{i:02d}", boxes)
        widest = max(widest, boxes[0][2] - boxes[0][0])
        name = f"sub_{i:02d}.png"; img.save(out / name)
        rows.append({"card": name, "text": s, "f0": frame(t0), "f1": frame(t1)})
    for r0, r1 in zip(rows, rows[1:]):
        assert r0["f1"] <= r1["f0"], f"overlap {r0} {r1}"
    # Bangla needs complex shaping (ে sits before its consonant); this PIL has no raqm, so Chrome renders the card
    end = render_html_card(Path("renders/overlays") / "endcard_v1.png")
    alpha = end.getchannel("A").point(lambda v: 255 if v > 40 else 0)
    boxes = [alpha.getbbox()]
    check_safe("endcard", boxes)
    rows.append({"card": "endcard_v1.png", "text": "আসছে বছর আবার হবে / @satyajitmall", "f0": END_F, "f1": CARD_END_F})
    Path("analysis/subtitles_v1.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    print(f"{len(CARDS)} cards, widest {widest} px; end card boxes {boxes}")

    video = Path(a.preview)
    if video.exists():                                  # composite every card over its middle frame
        tw, th = 270, 480
        sheet = Image.new("RGB", (tw * 10, th * 3), "black")
        for i, r in enumerate(rows[:-1]):
            bg = grab(video, (r["f0"] + r["f1"]) / 2 / FPS)
            comp = Image.alpha_composite(bg, Image.open(out / r["card"])).convert("RGB")
            sheet.paste(comp.resize((tw, th), Image.LANCZOS), ((i % 10) * tw, (i // 10) * th))
        card = Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), end).convert("RGB")
        sheet.paste(card.resize((tw, th), Image.LANCZOS), ((len(rows) - 1) % 10 * tw, (len(rows) - 1) // 10 * th))
        sheet.save("analysis/subs_composite_v1.jpg", quality=88)
        print("composite → analysis/subs_composite_v1.jpg")


if __name__ == "__main__":
    main()
