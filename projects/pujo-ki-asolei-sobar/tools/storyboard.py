"""Storyboard from an EDL json: in / mid / out frames per shot, labelled."""
import json, subprocess, sys, io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
reel = Path(sys.argv[1]); edl = json.load(open(sys.argv[2])); out = sys.argv[3]
gist = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
TW, TH, LW = 180, 320, 300
F = lambda s, b=False: ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial%s.ttf" % (" Bold" if b else ""), s)
def frame(clip, t):
    src = next((reel / "raw/b-roll").glob(f"*_{clip}.mov"))
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1", "-vf", f"scale={TW}:{TH}", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(png)).convert("RGB")
shots = edl["shots"]; cols = 2; rows = (len(shots) + 1) // 2; cw = LW + 3 * TW + 24
sheet = Image.new("RGB", (cols * cw, 70 + rows * (TH + 12)), (16, 16, 16)); d = ImageDraw.Draw(sheet)
d.text((14, 16), sys.argv[5] if len(sys.argv) > 5 else "Storyboard", fill=(255, 220, 120), font=F(32, True))
for i, s in enumerate(shots):
    r, c = divmod(i, cols); x0, y0 = c * cw, 70 + r * (TH + 12)
    for j, t in enumerate([s["in"] + 0.05, (s["in"] + s["out"]) / 2, s["out"] - 0.08]):
        sheet.paste(frame(s["clip"], t), (x0 + LW + j * TW, y0))
    col = (255, 190, 90) if s["look"] == "gold" else (140, 200, 255)
    d.text((x0 + 10, y0 + 6), f'{s["n"]}  {s["clip"]}', fill=col, font=F(26, True))
    d.text((x0 + 10, y0 + 42), f'{s["start"]:.2f}-{s["end"]:.2f}s  ({s["end"]-s["start"]:.2f}s)', fill=(230, 230, 230), font=F(18))
    d.text((x0 + 10, y0 + 66), f'src {s["in"]:.2f}-{s["out"]:.2f}', fill=(170, 170, 170), font=F(16))
    d.text((x0 + 10, y0 + 92), f'{s["vo"]} · {s["role"]} · {s["look"]} look', fill=col, font=F(18))
    y = y0 + 122
    for line in gist.get(s["n"], "").split("|"):
        d.text((x0 + 10, y), line, fill=(235, 235, 235), font=F(17)); y += 22
    if s.get("text"): d.text((x0 + 10, y0 + TH - 30), s["text"][:34], fill=(255, 240, 200), font=F(15, True))
sheet.save(out, quality=88); print(out, sheet.size)
