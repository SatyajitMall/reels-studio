"""v9 look sheet (reel-local): 01 upright frames, v8b's blur vs the zoom-blur versions given on the command line.
Usage: ../../.venv/bin/python tools/zoom_sheet_v9.py <out.jpg> <label=file> [<label=file> ...]"""
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
f = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 30)
def up(src, n):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", f"select=eq(n\\,{n}),scale=1080:1920", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.rot90(np.frombuffer(b, np.uint8).reshape(1920, 1080, 3), 1)
V = [a.split("=", 1) for a in sys.argv[2:]]
S = Image.new("RGB", (len(V) * 1930, 2 * 1090))
for r, n in enumerate((10, 30)):
    for c, (lab, src) in enumerate(V):
        im = Image.fromarray(up(src, n).copy()); d = ImageDraw.Draw(im); d.rectangle((0, 0, 520, 44), fill=(0, 0, 0)); d.text((8, 5), f"f{n} {lab}", font=f, fill=(255, 220, 0))
        S.paste(im, (c * 1930, r * 1090))
S.resize((S.width // 2, S.height // 2), Image.LANCZOS).save(sys.argv[1], quality=88); print(sys.argv[1])
