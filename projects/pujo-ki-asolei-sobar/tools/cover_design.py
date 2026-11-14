#!/usr/bin/env python3
"""Cover options for the IG upload (round 13, after v13 approval: the director asked for a better cover than the bare frame).
Frames come from the graded v13 shot renders (renders/final_shots, no subtitles). Type = the reel's title lockup
(graphics/title/index.html): DIN Condensed Bold, cream #f5e6c8, 0.08 em tracking, dark warm halo. Every title sits inside the
3:4 profile-grid crop (rows 240-1680) so it survives the grid.
Usage: cover_design.py            -> analysis/cover/cover_<K>.jpg for every option + analysis/cover/cover_options.jpg (sheet)
"""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
REEL = Path(__file__).resolve().parents[1]; R = REEL / "renders" / "final_shots"; OUT = REEL / "analysis" / "cover"
FONT = REEL / "graphics" / "title" / "assets" / "fonts" / "DINCondensed-Bold.ttf"
W, H = 1080, 1920; CREAM = (245, 230, 200); HALO = (26, 15, 5); GRID = (240, 1680)
OUT.mkdir(parents=True, exist_ok=True)

def frame(name, t):
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(R / f"{name}.mov"), "-frames:v", "1",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return Image.frombytes("RGB", (W, H), b)

def tracked(draw, x, y, text, font, track):
    """draw text with letter-spacing (Pillow has none); returns the advance width"""
    for ch in text:
        draw.text((x, y), ch, font=font, fill=255); x += font.getlength(ch) + track
    return x

def width(text, font, track): return sum(font.getlength(c) + track for c in text) - track

def lockup(img, lines, top, size, sub=None, sub_size=40):
    """the reel's title lockup: centred lines, cap top at `top`, line pitch 1.08 em, halo as in the HyperFrames CSS"""
    f = ImageFont.truetype(str(FONT), size); tr = 0.08 * size
    mask = Image.new("L", (W, H), 0); d = ImageDraw.Draw(mask)
    asc = f.getbbox("H")[1]                                     # offset from the draw origin to the cap top
    y = top
    for ln in lines:
        tracked(d, (W - width(ln, f, tr)) / 2, y - asc, ln, f, tr); y += 1.08 * size
    if sub:
        fs = ImageFont.truetype(str(FONT), sub_size); ts = 0.3 * sub_size
        tracked(d, (W - width(sub, fs, ts)) / 2, y + 0.25 * size - fs.getbbox("H")[1], sub, fs, ts)
    base = img.convert("RGBA")
    for blur, a, col, dy in ((11, 0.85, HALO, 0), (3.5, 0.70, HALO, 0), (9, 0.65, (0, 0, 0), 5)):
        m = mask.filter(ImageFilter.GaussianBlur(blur)) if not dy else Image.fromarray(np.roll(np.asarray(mask), dy, 0)).filter(ImageFilter.GaussianBlur(blur))
        lay = Image.new("RGBA", (W, H), col + (0,)); lay.putalpha(m.point(lambda v: int(v * a)))
        base = Image.alpha_composite(base, lay)
    lay = Image.new("RGBA", (W, H), CREAM + (0,)); lay.putalpha(mask)
    return Image.alpha_composite(base, lay).convert("RGB")

def shade(img, y0, y1, a0, a1):
    """soft warm-dark gradient (alpha a0 at y0 -> a1 at y1) so the title reads at grid-thumbnail size"""
    a = np.zeros((H, 1), np.float32); yy = np.arange(H)[:, None]
    a = np.clip(a0 + (a1 - a0) * (yy - y0) / (y1 - y0), 0, 1) * ((yy >= min(y0, y1)) | (a0 > a1))
    a = np.where(yy < y0, a0, np.where(yy > y1, a1, a))
    x = np.asarray(img, np.float32); x = x * (1 - a[..., None]) + np.array(HALO, np.float32) * a[..., None]
    return Image.fromarray(x.clip(0, 255).astype(np.uint8))

TITLE = ["PUJO KI", "ASOLEI SOBAR?"]; SUB = "DURGA PUJO 2026"

def opt_A():   # rickshaw puller, eye contact, title over the night sky
    im = shade(frame("11_C216_v13h", 2.2), 0, 700, 0.55, 0.0)
    return lockup(im, TITLE, 300, 128, SUB)

def opt_B():   # the hook frame: the Devi and the priest's aarti
    im = shade(frame("01_C152_m5e", 2.0), 0, 760, 0.62, 0.0)
    return lockup(im, TITLE, 300, 128, SUB)

def opt_C():   # four faces of the reel in the 3:4 grid area, title in the band above
    cells = [("11_C216_v13h", 2.2, (500, 735)), ("09_C213_m5f", 1.2, (520, 665)),
             ("03_C190_m5e", 2.4, (465, 1150)), ("12_C193_v13h", 2.3, (300, 640))]
    can = Image.new("RGB", (W, H), HALO); g = 8; cw, ch = (W - g) // 2, 540; y0 = 1680 - 2 * ch - g
    for i, (nm, t, (fx, fy)) in enumerate(cells):
        src = frame(nm, t); x = int(np.clip(fx - cw / 2, 0, W - cw)); y = int(np.clip(fy - 0.42 * ch, 0, H - ch))
        can.paste(src.crop((x, y, x + cw, y + ch)), ((i % 2) * (cw + g), y0 + (i // 2) * (ch + g)))
    return lockup(can, TITLE, 268, 112, SUB, 34)

def opt_D():   # the last image of the reel: the balloon seller looking up; title low, over his dark shirt
    im = shade(frame("12_C193_v13h", 2.3), 1150, 1720, 0.0, 0.6)
    return lockup(im, TITLE, 1330, 128, SUB)

OPTS = {"A": ("Rickshaw puller, eye contact", opt_A), "B": ("The Devi and the aarti (hook frame)", opt_B),
        "C": ("Four faces, title above", opt_C), "D": ("Balloon seller looking up (last shot)", opt_D)}

if __name__ == "__main__":
    tiles = []
    for k, (lab, fn) in OPTS.items():
        im = fn(); im.save(OUT / f"cover_{k}.jpg", quality=95)
        t = Image.new("RGB", (420, 760 + 290), (18, 18, 18)); d = ImageDraw.Draw(t)
        t.paste(im.resize((405, 720)), (8, 30)); d.text((10, 8), f"{k}: {lab}", fill=(255, 220, 0))
        g = im.crop((0, GRID[0], W, GRID[1])).resize((195, 260)); t.paste(g, (8, 770)); d.text((210, 780), "grid (3:4),\nphone size", fill=(200, 200, 200))
        tiles.append(t)
    s = Image.new("RGB", (420 * len(tiles), tiles[0].height), (18, 18, 18)); [s.paste(t, (i * 420, 0)) for i, t in enumerate(tiles)]
    s.save(OUT / "cover_options.jpg", quality=90); print("✓", ", ".join(f"cover_{k}.jpg" for k in OPTS), "+ cover_options.jpg")
