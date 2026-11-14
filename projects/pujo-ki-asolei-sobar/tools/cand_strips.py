#!/usr/bin/env python3
"""Detail strips for shortlisted clips: 8 frames evenly spaced, 180x320, timestamp on each.
Usage: cand_strips.py <out.jpg> <MMDD/Cnnn>[@a-b] [...]   (@a-b: only that window, seconds)"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw
REEL = Path(__file__).resolve().parents[1]; meta = json.loads((REEL / "analysis/pool_r9/clips.json").read_text())
TW, TH = 180, 320
def strip(c):
    c, _, win = c.partition("@"); a, b = (map(float, win.split("-")) if win else (0, None))
    m = meta[c]; b = b if b is not None else m["dur"]; im = Image.new("RGB", (TW * 8, TH + 18), (15, 15, 15)); d = ImageDraw.Draw(im)
    for k in range(8):
        t = a + (b - a) * (k + 0.5) / 8
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", m["path"], "-frames:v", "1", "-vf", f"scale={TW}:{TH}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        if len(raw) == TW * TH * 3: im.paste(Image.frombytes("RGB", (TW, TH), raw), (k * TW, 18))
        d.text((k * TW + 3, 20), f"{t:.1f}s", fill=(0, 255, 0))
    d.text((3, 2), f"{c}  {m['fps']:.0f}fps {m['dur']:.1f}s", fill=(255, 220, 0)); return im
cl = sys.argv[2:]
with ThreadPoolExecutor(6) as ex: S = list(ex.map(strip, cl))
out = Image.new("RGB", (TW * 8, len(S) * (TH + 20)), (0, 0, 0))
for i, s in enumerate(S): out.paste(s, (0, i * (TH + 20)))
out.save(sys.argv[1], quality=84); print("✓", sys.argv[1])
