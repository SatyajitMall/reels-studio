"""v7 picking sheets (reel-local, 2026-11-12): frames of a clip, labelled, tiled.
Usage: ../../.venv/bin/python tools/sheet_v7.py <video> <out.jpg> <step_s> [cols] [--noautorotate] [--start s] [--end s]"""
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
a = sys.argv
src, out, step = a[1], a[2], float(a[3])
cols = int(a[4]) if len(a) > 4 and a[4].isdigit() else 4
nar = ["-noautorotate"] if "--noautorotate" in a else []
start = float(a[a.index("--start") + 1]) if "--start" in a else 0.0
probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,duration",
                        "-of", "csv=p=0"] + [src], capture_output=True, text=True).stdout.strip().splitlines()[0].split(",")
w, h, dur = int(probe[0]), int(probe[1]), float(probe[2])
end = float(a[a.index("--end") + 1]) if "--end" in a else dur
f = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 22)
tw = 480; th = round(tw * h / w)
times = list(np.arange(start, end - 0.01, step))
rows = (len(times) + cols - 1) // cols
S = Image.new("RGB", (cols * (tw + 4), rows * (th + 4)), (0, 0, 0)); d = ImageDraw.Draw(S)
for i, t in enumerate(times):
    b = subprocess.run(["ffmpeg", "-v", "error"] + nar + ["-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", f"scale={tw}:{th}",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    if len(b) < tw * th * 3: continue
    im = Image.fromarray(np.frombuffer(b, np.uint8)[: tw * th * 3].reshape(th, tw, 3))
    x, y = (i % cols) * (tw + 4), (i // cols) * (th + 4)
    S.paste(im, (x, y)); d.rectangle((x, y, x + 90, y + 28), fill=(0, 0, 0)); d.text((x + 6, y + 3), f"{t:.2f}s", font=f, fill=(255, 220, 0))
S.save(out, quality=85); print(out, S.size, len(times))
