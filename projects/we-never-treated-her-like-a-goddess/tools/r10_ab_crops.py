#!/usr/bin/env python3
"""Round 10: 1:1 crops of slowed-shot candidates at the same output frames, for spotting ghost/double images and warping.
Rows = candidates, columns = frames. Each candidate is "label|video|first frame|x0,y0,x1,y1" (crop in that video's own pixels;
4K renders are cropped in source space, the reel master in reel space). Output resized to 420 px tiles.
Usage (reel folder): ../../.venv/bin/python tools/r10_ab_crops.py <out.jpg> "<frames,comma>" "<cand>" ["<cand>" ...]"""
import io, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

out, frames, cands = sys.argv[1], [int(x) for x in sys.argv[2].split(",")], sys.argv[3:]
T = 420; font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
g = Image.new("RGB", (len(frames) * (T + 4) + 4, len(cands) * (T + 28) + 4), (18, 18, 18)); d = ImageDraw.Draw(g)
for r, c in enumerate(cands):
    lab, video, a, box = c.split("|"); a = int(a); box = tuple(int(v) for v in box.split(","))
    for j, k in enumerate(frames):
        png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{(a + k) / 25:.3f}", "-i", video, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        im = Image.open(io.BytesIO(png)).convert("RGB").crop(box).resize((T, T), Image.LANCZOS)
        x, y = 4 + j * (T + 4), 4 + r * (T + 28); g.paste(im, (x, y + 24)); d.text((x + 4, y + 2), f"{lab}  out frame {k}", fill=(230, 230, 230), font=font)
g.save(out, quality=88); print(g.size)
