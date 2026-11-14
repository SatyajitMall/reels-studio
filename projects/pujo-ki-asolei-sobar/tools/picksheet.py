"""Build a pick sheet: one row per clip, 4 frames from its contact.png (6x2 grid of 270x480)."""
import sys, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
survey = Path(sys.argv[1]); out = Path(sys.argv[2]); title = sys.argv[3]; ids = sys.argv[4].split(",")
notes = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}
TW, TH, PICK = 162, 288, [0, 4, 7, 11]
LABEL_W = 230
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 17)
tfont = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
dirs = {d.name.split("_")[-1]: d for d in survey.iterdir() if d.is_dir()}
cols = 2  # two clips per sheet row
rows = (len(ids) + cols - 1) // cols
cw = LABEL_W + 4 * TW + 20
sheet = Image.new("RGB", (cols * cw, 60 + rows * (TH + 10)), (18, 18, 18))
d = ImageDraw.Draw(sheet)
d.text((12, 12), title, fill=(255, 220, 120), font=tfont)
for i, cid in enumerate(ids):
    r, c = divmod(i, cols)
    x0, y0 = c * cw, 60 + r * (TH + 10)
    cd = dirs[cid]
    st = json.loads((cd / "stats.json").read_text())
    con = Image.open(cd / "contact.png")
    for j, k in enumerate(PICK):
        fr = con.crop(((k % 6) * 270, (k // 6) * 480, (k % 6) * 270 + 270, (k // 6) * 480 + 480)).resize((TW, TH))
        sheet.paste(fr, (x0 + LABEL_W + j * TW, y0))
    d.text((x0 + 10, y0 + 8), cid, fill=(255, 255, 0), font=font)
    meta = st.get("meta", st)
    dur = meta.get("duration_s", "?"); fps = meta.get("fps", "?")
    d.text((x0 + 10, y0 + 40), f"{dur}s  {round(float(fps)) if fps!='?' else '?'}fps", fill=(200, 200, 200), font=small)
    y = y0 + 66
    for line in notes.get(cid, "").split("|"):
        d.text((x0 + 10, y), line, fill=(230, 230, 230), font=small); y += 22
sheet.save(out, quality=88)
print(out, sheet.size)
