"""Strip of the subtitle band (y 1380-1620) for every card, composited over the graded preview, 2 columns."""
import json, subprocess, sys
from PIL import Image, ImageDraw
W, H, FPS = 1080, 1920, 25
video = sys.argv[1] if len(sys.argv) > 1 else "renders/previews/grade_a4.mp4"
rows = json.load(open("analysis/subtitles_v1.json"))[:-1]
y0, y1 = 1380, 1620; bh = y1 - y0
sheet = Image.new("RGB", (W * 2, bh * ((len(rows) + 1) // 2)), "black")
for i, r in enumerate(rows):
    t = (r["f0"] + r["f1"]) / 2 / FPS
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    bg = Image.frombytes("RGB", (W, H), raw).convert("RGBA")
    comp = Image.alpha_composite(bg, Image.open("renders/overlays/subs/" + r["card"])).convert("RGB").crop((0, y0, W, y1))
    ImageDraw.Draw(comp).text((10, 8), f"{i+1:02d}", fill="white")
    sheet.paste(comp, ((i % 2) * W, (i // 2) * bh))
sheet.save(sys.argv[2] if len(sys.argv) > 2 else "analysis/subs_band_v1.jpg", quality=85)
