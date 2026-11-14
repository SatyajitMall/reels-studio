#!/usr/bin/env python3
"""Contact sheets of every original clip in the pool (round 9: "go through all videos").
4 frames per clip (12/37/62/87 %), 135x240 each, label = <MMDD>/<Cnnn> fps dur; 18 clips per sheet.
Usage: pool_sheets.py -> analysis/pool_r9/sheet_NN.jpg + clips.json (sheet / slot per clip)"""
import json, subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
REEL = Path(__file__).resolve().parents[1]; OUT = REEL / "analysis/pool_r9"
rows = [r for r in json.loads((OUT / "index.json").read_text()) if r.get("folder") not in ("Proxy", "Refference", "Reffernce") and r.get("dur", 0) >= 0.5]
rows.sort(key=lambda r: r["name"])
TW, TH, LB = 135, 240, 16
def cid(r): return r["name"][5:9] + "/" + r["name"].split("_")[-1].split(".")[0]
def strip(r):
    im = Image.new("RGB", (TW * 4, TH + LB), (20, 20, 20))
    for k, q in enumerate((0.12, 0.37, 0.62, 0.87)):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{r['dur'] * q:.2f}", "-i", r["path"], "-frames:v", "1", "-vf", f"scale={TW}:{TH}",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        if len(raw) == TW * TH * 3: im.paste(Image.frombytes("RGB", (TW, TH), raw), (k * TW, LB))
    d = ImageDraw.Draw(im); d.text((3, 2), f"{cid(r)}  {r['fps_r']:.0f}fps  {r['dur']:.1f}s", fill=(255, 220, 0))
    return im
with ThreadPoolExecutor(8) as ex: strips = list(ex.map(strip, rows))
meta = {}
for s in range(0, len(rows), 18):
    sheet = Image.new("RGB", (3 * TW * 4 + 20, 6 * (TH + LB) + 10), (0, 0, 0))
    for k, (r, im) in enumerate(zip(rows[s:s + 18], strips[s:s + 18])):
        sheet.paste(im, ((k % 3) * (TW * 4 + 10), (k // 3) * (TH + LB + 2)))
        meta[cid(r)] = {"sheet": s // 18 + 1, "slot": k + 1, "path": r["path"], "fps": r["fps_r"], "dur": r["dur"]}
    sheet.save(OUT / f"sheet_{s // 18 + 1:02d}.jpg", quality=82)
(OUT / "clips.json").write_text(json.dumps(meta, indent=1)); print(len(rows), "clips,", (len(rows) + 17) // 18, "sheets")
