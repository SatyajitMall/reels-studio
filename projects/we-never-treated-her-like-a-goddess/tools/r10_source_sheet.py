#!/usr/bin/env python3
"""Round 10 (director: "slow down the frame ... apply slowing down frame technique in a few other places"): one row per shot of the
current cut, 8 frames spread over the whole camera clip, each labelled with its source time; frames inside the window the reel uses
now get a yellow border. Shows what each clip holds before and after the used window, so slow-motion picks can use the calm part.
Usage (reel folder): ../../.venv/bin/python tools/r10_source_sheet.py [shot numbers, default all] -> analysis/r10/source_sheet.jpg"""
import json, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

clips = json.load(open("analysis/_es_out_v9read.txt"))["clips"]
pick = [int(a) for a in sys.argv[1:]] or list(range(1, len(clips) + 1))
W, H, N = 150, 267, 8
font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
rows = []
for i in pick:
    c = clips[i - 1]; path = f"raw/b-roll/A001_{c['name']}.mov"
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))
    fps = 30.004 if c["name"].endswith("C017") else 25.0
    i0, i1 = c["inP"], c["outP"]
    if c["name"].endswith("C017"): i0, i1 = i0 * 25 / fps, i1 * 25 / fps   # interpreted 25 fps times -> native seconds
    row = Image.new("RGB", (N * (W + 4) + 210, H + 26), (20, 20, 20)); d = ImageDraw.Draw(row)
    d.text((6, 6), f"#{i} {c['name'][-4:]}\nreel {c['start']/25:.2f}-{c['end']/25:.2f}\nsrc {i0:.2f}-{i1:.2f}\nclip {dur:.1f}s", fill=(240, 240, 240), font=font)
    for k in range(N):
        t = min(dur - 0.05, (k + 0.5) * dur / N)
        png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-vf", f"scale={W}:{H}", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        im = Image.open(__import__("io").BytesIO(png)).convert("RGB"); x = 210 + k * (W + 4)
        row.paste(im, (x, 0))
        if i0 - 0.01 <= t <= i1 + 0.01: d.rectangle([x, 0, x + W - 1, H - 1], outline=(255, 210, 0), width=4)
        d.text((x + 4, H + 4), f"{t:.1f}s", fill=(200, 200, 200), font=font)
    rows.append(row)
out = Image.new("RGB", (rows[0].width, sum(r.height for r in rows)), (0, 0, 0)); y = 0
for r in rows: out.paste(r, (0, y)); y += r.height
out.save(sys.argv[0].replace("tools/r10_source_sheet.py", "") + "analysis/r10/source_sheet.jpg" if False else "analysis/r10/source_sheet.jpg", quality=85)
print(out.size)
