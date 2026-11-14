"""Pick sheet: one row per clip, 6 of its 12 contact frames (with sample times), for choosing by story role.
Usage: .venv/bin/python tools/picksheet.py <out.jpg> "<title>" <analysis_dir>:<clip_stem>[=label] ...
(stems are full file stems, e.g. A001_10202151_C061, because clip numbers repeat across nights)"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

out, title, items = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
TW, TH, PICK, LW = 180, 320, [0, 2, 4, 6, 8, 10], 250
bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 17)
sheet = Image.new("RGB", (LW + 6 * TW + 10, 50 + len(items) * (TH + 8)), (18, 18, 18))
d = ImageDraw.Draw(sheet)
d.text((10, 12), title, fill=(255, 220, 120), font=bold)
for i, it in enumerate(items):
    spec, _, label = it.partition("=")
    adir, stem = spec.split(":")
    cd = Path(adir) / stem
    st = json.loads((cd / "stats.json").read_text())
    con = Image.open(cd / "contact.png")
    cw, ch = con.size[0] // 6, con.size[1] // 2
    y0 = 50 + i * (TH + 8)
    d.text((8, y0 + 6), stem[-4:] + "  " + stem[4:12], fill=(255, 255, 255), font=bold)
    d.text((8, y0 + 36), f'{st["duration_s"]:.1f}s  {st["fps"]}fps', fill=(200, 200, 200), font=small)
    for ln, txt in enumerate(label.split("|")):
        d.text((8, y0 + 62 + 22 * ln), txt[:28], fill=(255, 220, 120), font=small)
    for j, k in enumerate(PICK):
        r, c = divmod(k, 6)
        tile = con.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch)).resize((TW, TH))
        sheet.paste(tile, (LW + j * TW, y0))
        t = st["samples"][k]["t"] if k < len(st["samples"]) else 0
        d.text((LW + j * TW + 4, y0 + TH - 22), f"{t:.1f}s", fill=(255, 255, 0), font=small)
sheet.save(out, quality=88)
print("✓", out)
