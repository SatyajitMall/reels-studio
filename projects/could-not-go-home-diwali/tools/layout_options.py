"""Layout options for the director (reel-local, 2026-11-11 note on v3f: "text at the bottom eats up a lot of the screen.
Can we have the text on the video like on the reference ... use the padding to stretch out the video in the proper
aspect ratio").

From the graded v3f master: each sample shot's 4:3 window (the camera's full height, 75 % of its width) is scaled up to a
taller window and cropped at the sides (that is all a taller window can do with landscape footage), the letter line is
set ON the picture top-left like the reference (Baskerville Italic, cream, soft shadow), and the IG UI bands are shaded.

Options per shot: A = now (4:3, text in the band) · B = 4:3, text on picture · C = 1:1 · D = 4:5.
Usage (reel folder): python3 tools/layout_options.py -o analysis/layout_v3f/layout_options.jpg
"""
import argparse
import io
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

MASTER = "renders/masters/could-not-go-home-diwali_v3f_master.mov"
SUP = Path("/System/Library/Fonts/Supplemental")
# frame, shot, Hinglish line, English line, horizontal anchor of the crop (0 = left, .5 = centre, 1 = right)
SHOTS = [
    (380, "10 vendor", "Phone pe aarti dikha dena.", "Show me the aarti on the phone.", 0.4),
    (535, "14 paan look", "Papa se kehna, main theek hoon.", "Tell Papa I'm fine.", 0.5),
]
OPTS = [("A  now: 4:3, text below", 810, "band"), ("B  4:3, text on picture", 810, "on"),
        ("C  1:1, text on picture", 1080, "on"), ("D  4:5, text on picture", 1350, "on")]


def frame(n):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", MASTER, "-vf", f"select=eq(n\\,{n})", "-frames:v", "1",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(raw)).convert("RGB")


def text_on(img, x, y, l1, l2, s1=54, s2=34):
    f1 = ImageFont.truetype(str(SUP / "Baskerville.ttc"), s1, index=2)
    f2 = ImageFont.truetype(str(SUP / "Baskerville.ttc"), s2, index=2)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    d.text((x, y), l1, font=f1, fill=(0, 0, 0, 170)); d.text((x, y + s1 + 12), l2, font=f2, fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img.convert("RGBA"), sh)
    d = ImageDraw.Draw(img)
    d.text((x, y), l1, font=f1, fill=(245, 230, 200, 255)); d.text((x, y + s1 + 12), l2, font=f2, fill=(255, 255, 255, 204))
    return img.convert("RGB")


def build(fr, h, mode, l1, l2, ax):
    win = fr.crop((0, 505, 1080, 1315))                       # graded 4:3 window, full camera height
    canvas = Image.new("RGB", (1080, 1920), (0, 0, 0))
    if h == 810:
        pic = win
    else:
        s = h / 810; big = win.resize((round(1080 * s), h), Image.LANCZOS)
        x0 = round((big.width - 1080) * ax); pic = big.crop((x0, 0, x0 + 1080, h))
    y0 = (1920 - h) // 2 if h != 810 else 505
    canvas.paste(pic, (0, y0))
    if mode == "band":
        canvas = text_on(canvas, 70, 1340, l1, l2)
    else:
        canvas = text_on(canvas, 60, y0 + 40, l1, l2, 46, 30)  # top-left of the picture, like the reference
    # IG UI bands (CLAUDE.md §3): top 220, bottom 320, right 120
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for yy in (220, 1600):
        d.line((0, yy, 1080, yy), fill=(255, 80, 80, 200), width=4)
    d.line((960, 220, 960, 1600), fill=(255, 80, 80, 200), width=4)
    return Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("-o", "--out", default="analysis/layout_v3f/layout_options.jpg")
    a = ap.parse_args()
    tw, th = 360, 640
    f = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 20)
    S = Image.new("RGB", (len(OPTS) * (tw + 10), 100 + len(SHOTS) * (th + 40)), (18, 18, 18)); d = ImageDraw.Draw(S)
    for j, (lab, h, mode) in enumerate(OPTS):
        width_pct = round(100 * 0.75 * 810 / h)
        d.text((j * (tw + 10) + 4, 6), lab, font=f, fill=(255, 225, 140))
        d.text((j * (tw + 10) + 4, 32), f"shows {width_pct} % of camera width", font=f, fill=(200, 200, 200))
    d.text((4, S.height - 30), "red lines = where Instagram's own buttons and caption sit", font=f, fill=(255, 120, 120))
    for i, (n, name, l1, l2, ax) in enumerate(SHOTS):
        fr = frame(n)
        y = 60 + i * (th + 40)
        d.text((4, y + 4), name, font=f, fill=(255, 255, 255))
        for j, (lab, h, mode) in enumerate(OPTS):
            S.paste(build(fr, h, mode, l1, l2, ax).resize((tw, th), Image.LANCZOS), (j * (tw + 10), y + 34))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    S.save(a.out, quality=88); print(a.out, S.size)


if __name__ == "__main__":
    main()
