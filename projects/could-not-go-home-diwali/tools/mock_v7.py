"""v7 placement mock (reel-local, 2026-11-12): the new 03 (C047 bake) and 12 (Pexels 34565049, home diya) placed into the
16:9 window with the planned Scale/Position, their letter line on top, before touching Premiere. Camera colour, no look.
Also L4 bottom-left (now) vs a top-left variant on 10 (from the v6c master) and on the new 12.
Usage (reel folder): ../../.venv/bin/python tools/mock_v7.py"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).parent))
from make_type_v6 import line, LINES  # noqa: E402

WIN = (606, 1214)
def grab(src, t=None, n=None, w=None, h=None, nar=False):
    vf = [] if n is None else ["-vf", f"select=eq(n\\,{n})"]
    ss = [] if t is None else ["-ss", f"{t:.3f}"]
    b = subprocess.run(["ffmpeg", "-v", "error"] + (["-noautorotate"] if nar else []) + ss + ["-i", src] + vf +
                       ["-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return Image.fromarray(np.frombuffer(b, np.uint8).reshape(h, w, 3))
def place(im, scale, pos):
    s = scale / 100; r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c = Image.new("RGB", (1080, 1920)); c.paste(r, (round(pos[0] - r.width / 2), round(pos[1] - r.height / 2))); return c.convert("RGBA")
def lerp(a, b, k): return a + (b - a) * k
def win(c, txt): return Image.alpha_composite(c, txt).crop((0, WIN[0], 1080, WIN[1])).convert("RGB")

L1 = line(LINES[0][0], LINES[0][1], LINES[0][2])
L4 = line(LINES[3][0], LINES[3][1], LINES[3][2])
L4tl = line(LINES[3][0], "TL", {})
C047 = "raw/baked/C047_f2_00.12.mov"; S32 = "raw/stock/pexels-34565049/14645113_1920_1080_25fps.mp4"
V6C = "renders/masters/could-not-go-home-diwali_v6c_master.mov"
rows = []
# new 03: bake frames 22-60, Scale 28.17 -> 29.53, Position (540, 910) -> (540, 924.9), like 01
for k, n in ((0, 22), (0.5, 41), (1, 60)):
    rows.append(("03 C047 f%d + L1" % n, win(place(grab(C047, n=n, w=3840, h=2160, nar=True), lerp(28.17, 29.53, k), (540, lerp(910, 924.9, k))), L1)))
# new 12: stock 26.80-28.76 s, Scale 56.34 -> 59.06, Position (540, 910) -> (540, 924.9)
for k, t in ((0, 26.8), (0.5, 27.78), (1, 28.72)):
    pic = place(grab(S32, t=t, w=1920, h=1080), lerp(56.34, 59.06, k), (540, lerp(910, 924.9, k)))
    rows.append(("12 S32 %.2fs + L4 BL (now)" % t, win(pic, L4)))
    rows.append(("12 S32 %.2fs + L4 TL" % t, win(pic, L4tl)))
# 10 from v6c (its L4 BL is burned in), with the TL variant drawn on top for comparison
for t in (14.5, 15.7, 16.9):
    fr = grab(V6C, t=t, w=1080, h=1920).convert("RGBA")
    rows.append(("10 v6c %.1fs (BL burned in) + L4 TL" % t, win(fr, L4tl)))
f = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 26)
tw = 540; th = round(tw * 608 / 1080); cols = 3
S = Image.new("RGB", (cols * (tw + 8) + 8, ((len(rows) + cols - 1) // cols) * (th + 44) + 8), (16, 16, 16)); d = ImageDraw.Draw(S)
for i, (lab, im) in enumerate(rows):
    x, y = 8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 44)
    d.text((x, y), lab, font=f, fill=(255, 220, 120)); S.paste(im.resize((tw, th), Image.LANCZOS), (x, y + 36))
out = "analysis/v7_notes/mock_v7.jpg"; S.save(out, quality=88); print(out, S.size)
