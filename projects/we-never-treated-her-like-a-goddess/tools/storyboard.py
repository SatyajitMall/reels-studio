"""Checkpoint storyboard from an EDL json: in / mid / out frame per row, with time, VO clause, clip, night and fps.
Rows whose fps differs from the sequence fps are flagged (they play at seq/fps speed when interpreted).
Usage: .venv/bin/python tools/storyboard.py analysis/edl_v1.json analysis/storyboard_v1.jpg"""
import json, subprocess, sys, textwrap
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
edl = json.loads(Path(sys.argv[1]).read_text()); out = Path(sys.argv[2])
SEQ = edl["seq_fps"]; TW, TH, PER = 160, 284, 4
bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 17)
small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 14)
bn = ImageFont.truetype("/System/Library/Fonts/KohinoorBangla.ttc", 18)


def grab(clip, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(REEL / "raw/b-roll" / f"{clip}.mov"),
                          "-frames:v", "1", "-vf", f"scale={TW}:{TH}:force_original_aspect_ratio=increase,crop={TW}:{TH}", "-f", "image2", "-c:v", "png", "-"],
                         capture_output=True).stdout
    return Image.open(BytesIO(raw))


rows = edl["rows"]; BW = 3 * TW + 16; BH = TH + 92
lines = (len(rows) + PER - 1) // PER
sheet = Image.new("RGB", (PER * BW, 40 + lines * BH), (16, 16, 16))
d = ImageDraw.Draw(sheet)
d.text((10, 10), f"{out.stem}  ·  {edl['runtime']} s  ·  {SEQ} fps", fill=(255, 220, 120), font=bold)
for i, r in enumerate(rows):
    x0, y0 = (i % PER) * BW + 8, 40 + (i // PER) * BH
    dur = r["t1"] - r["t0"]
    if r["clip"]:
        span = dur * SEQ / r["fps"]  # source seconds covered once interpreted to the sequence rate
        for j, f in enumerate((0.04, 0.5, 0.96)):
            sheet.paste(grab(r["clip"], r["src"] + span * f), (x0 + j * TW, y0))
        flag = "" if r["fps"] == SEQ else f"  {r['fps']}fps→{SEQ} ({SEQ / r['fps']:.2f}x)"
        d.text((x0, y0 + TH + 4), f"#{r['n']}  {r['t0']:.2f}–{r['t1']:.2f}  ({dur:.2f}s)  {r['night']} {r['clip'][-4:]} @{r['src']:.2f}{flag}",
               fill=(255, 255, 255) if not flag else (255, 160, 90), font=small)
    else:
        d.rectangle((x0, y0, x0 + 3 * TW, y0 + TH), fill=(0, 0, 0))
        d.text((x0 + 70, y0 + TH // 2 - 30), "আসছে বছর আবার হবে", fill=(245, 230, 200), font=bn)
        d.text((x0 + 150, y0 + TH // 2 + 6), "@satyajitmall", fill=(242, 211, 59), font=small)
        d.text((x0, y0 + TH + 4), f"#{r['n']}  {r['t0']:.2f}–{r['t1']:.2f}  end card", fill=(255, 255, 255), font=small)
    d.text((x0, y0 + TH + 24), f"“{r['vo']}”" if r["vo"] else "", fill=(242, 211, 59), font=bold)
    for k, ln in enumerate(textwrap.wrap(r["role"], 62)[:2]):
        d.text((x0, y0 + TH + 48 + 18 * k), ln, fill=(190, 190, 190), font=small)
sheet.save(out, quality=88)
print("✓", out)
