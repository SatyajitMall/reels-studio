"""Round of notes on v5b (reel-local, 2026-11-12). The director:
  "why does it also have Hindi and English both? ... I just want the text to be ... Hindi written in English ... I don't want
   it to be translated in English and written across. But I want the font to change. Also, the video is coming into 1:1
   frame. Is it not a 16:9 vertical video?"

Two sheets:
  1. analysis/v5b_notes/font_options.jpg: six fonts, the Hinglish line only (no English line), on three shots in their
     current corners (L1 on 02 bottom-right, L3 on 07 bottom-left, L5 on 14 top-right). Frames from the v3f master,
     whose picture has no text burned in (its text sat in the band).
  2. analysis/v5b_notes/frame_options.jpg: the same three own-footage moments in three frame shapes, from the Apple
     Cinematic bakes at 4K, graded to match the reel's own render of that moment (make_cover_v4f.cdf_match):
       A  4:3 window (now): 75 % of the camera width
       B  4:5 window:       45 % of the camera width
       C  full 9:16:        32 % of the camera width (the picture fills the phone)
     Instagram's own buttons and caption bands are marked.
Usage (reel folder): ../../.venv/bin/python tools/font_frame_options.py
"""
import io
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from make_cover_v4f import cdf_match, raw  # noqa: E402
from make_type_v4d import compose, width  # noqa: E402

SUP = "/System/Library/Fonts/Supplemental/"
FONTS = [
    ("A  Avenir Next Medium (clean, modern)", "/System/Library/Fonts/Avenir Next.ttc", 5, 46),
    ("B  Futura Medium (geometric)", SUP + "Futura.ttc", 0, 46),
    ("C  American Typewriter Light (a typed letter)", SUP + "AmericanTypewriter.ttc", 1, 46),
    ("D  Bradley Hand (a handwritten letter)", SUP + "Bradley Hand Bold.ttf", 0, 50),
    ("E  Didot Italic (elegant serif)", SUP + "Didot.ttc", 1, 50),
    ("F  Gill Sans (soft, humanist)", SUP + "GillSans.ttc", 0, 50),
]
CREAM = (245, 230, 200, 255)
WIN = (0, 505, 1080, 1315)
V3F = "renders/masters/could-not-go-home-diwali_v3f_master.mov"
SHOTS = [(60, "Maa, is baar ghar nahi aa paaunga.", "BR"), (262, "Tumhare haath ka khaana yaad aata hai.", "BL"),
         (535, "Papa se kehna, main theek hoon.", "TR")]


def frame(n, video=V3F):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf", f"select=eq(n\\,{n})", "-frames:v", "1", "-f",
                        "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return Image.fromarray(np.frombuffer(b, np.uint8).reshape(1920, 1080, 3)).convert("RGBA")


def wrap2(text, f, maxw):
    if width(text, f) <= maxw:
        return [text]
    w = text.split()
    best = min(range(1, len(w)), key=lambda k: abs(width(" ".join(w[:k]), f) - width(" ".join(w[k:]), f)))
    return [" ".join(w[:best]), " ".join(w[best:])]


def line_layer(text, f, corner, box):
    """box = (x0, y0, x1, y1) of the picture; the block sits 60 px in from its corner."""
    x0, y0, x1, y1 = box
    rows = wrap2(text, f, 470)
    lh = round(f.size * 1.22); h = lh * len(rows)
    y = y0 + 44 if corner[0] == "T" else y1 - 44 - h
    spec = []
    for t in rows:
        w = width(t, f)
        x = x0 + 60 if corner[1] == "L" else min(x1, 960) - 30 - w
        spec.append((t, f, 0, CREAM, x, y)); y += lh
    return compose(spec, None)


def font_sheet(out):
    lab = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 22)
    frames = [frame(n) for n, _, _ in SHOTS]
    tw, th = 480, 360
    S = Image.new("RGB", (240 + 3 * (tw + 6), len(FONTS) * (th + 8) + 8), (18, 18, 18)); d = ImageDraw.Draw(S)
    for r, (name, path, idx, size) in enumerate(FONTS):
        f = ImageFont.truetype(path, size, index=idx)
        y = 8 + r * (th + 8)
        d.multiline_text((10, y + 10), name.replace("  ", "\n", 1).replace(" (", "\n("), font=lab, fill=(255, 220, 140), spacing=6)
        for k, ((n, text, corner), fr) in enumerate(zip(SHOTS, frames)):
            im = Image.alpha_composite(fr, line_layer(text, f, corner, WIN)).crop(WIN).convert("RGB").resize((tw, th), Image.LANCZOS)
            S.paste(im, (240 + k * (tw + 6), y))
    S.save(out, quality=88); print(out, S.size)


# frame options: own-footage moments from the bakes (bake, bake frame, reel frame in v5b, crop centre x 0-1)
MOMENTS = [("02 auto driver", "raw/baked/C048_f2_01.92.mov", 41, 60, 0.50),
           ("10 vendor on his phone", "raw/baked/v4/C062_f4_03.60.mov", 35, 380, 0.42),
           ("14 paan maker's look", "raw/baked/C051_f2_00.00.mov", 25, 535, 0.48)]
SHAPES = [("A  4:3 now", 4 / 3, 810), ("B  4:5", 4 / 5, 1350), ("C  full 9:16", 9 / 16, 1920)]
V5B = "renders/masters/could-not-go-home-diwali_v5b_master.mov"


def frame_sheet(out, f_txt):
    lab = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 22)
    tw, th = 300, 533
    S = Image.new("RGB", (3 * (tw + 10) + 10, 70 + len(MOMENTS) * (th + 40)), (18, 18, 18)); d = ImageDraw.Draw(S)
    for j, (name, ar, h) in enumerate(SHAPES):
        pct = round(100 * (2160 * ar) / 3840)
        d.text((10 + j * (tw + 10), 8), name, font=lab, fill=(255, 220, 140))
        d.text((10 + j * (tw + 10), 36), f"{pct} % of camera width", font=lab, fill=(200, 200, 200))
    for i, (mname, bake, bn, rn, cx) in enumerate(MOMENTS):
        cam = raw(bake, bn, 3840, 2160)
        ren = raw(V5B, rn, 1080, 1920)[WIN[1]:WIN[3]]
        sample = cam[86:2074, 576:3264]
        y0 = 70 + i * (th + 40)
        d.text((10, y0 - 2), mname, font=lab, fill=(255, 255, 255))
        for j, (name, ar, h) in enumerate(SHAPES):
            cw = round(2160 * ar)
            x0 = int(min(max(cx * 3840 - cw / 2, 0), 3840 - cw))
            pic = Image.fromarray(cdf_match(cam[:, x0:x0 + cw], ren, sample)).resize((1080, h), Image.LANCZOS)
            canvas = Image.new("RGBA", (1080, 1920), (0, 0, 0, 255)); top = (1920 - h) // 2 if h < 1920 else 0
            canvas.paste(pic, (0, top))
            box = (0, max(top, 220), 1080, min(top + h, 1600))
            canvas = Image.alpha_composite(canvas, line_layer(SHOTS[0][1] if i == 0 else ("Phone pe aarti dikha dena." if i == 1 else SHOTS[2][1]), f_txt, "BL" if i < 2 else "TR", box))
            dd = ImageDraw.Draw(canvas)
            for yy in (220, 1600):
                dd.line((0, yy, 1080, yy), fill=(255, 80, 80, 255), width=5)
            dd.line((960, 220, 960, 1600), fill=(255, 80, 80, 255), width=5)
            S.paste(canvas.convert("RGB").resize((tw, th), Image.LANCZOS), (10 + j * (tw + 10), y0 + 26))
    d.text((10, S.height - 30), "red lines = where Instagram's own buttons and caption sit", font=lab, fill=(255, 120, 120))
    S.save(out, quality=88); print(out, S.size)


def main():
    out = Path("analysis/v5b_notes"); out.mkdir(parents=True, exist_ok=True)
    if '--frames-only' not in sys.argv: font_sheet(out / "font_options.jpg")
    frame_sheet(out / "frame_options.jpg", ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 46, index=5))


if __name__ == "__main__":
    main()
