#!/usr/bin/env python3
"""Round 4d (director: "why are we not determining a composition and accuracy"; "Both" = a plan + a designed move per shot;
"frame tighter everywhere"; "eyes are the subject"): render the composition plan as a board before baking.
Each slot: start and end frame through the planned crop (eye position from the survey track, crop width from the target
eye span, output eye point u/v), in the G2b2 look, labelled with the move. Plan: analysis/comp_v5/plan.json.
Usage: python tools/comp_board.py analysis/comp_v5/plan.json -o analysis/comp_v5/board.jpg
"""
import json, subprocess, argparse, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
REEL = Path(__file__).resolve().parents[1]
CUBE = REEL / "grade/uski_aankhein_G2b2_gold_shadow_c18.cube"

def track_at(samples, t):
    s = sorted(samples); ts = [x[0] for x in s]
    if t <= ts[0]: return s[0][1], s[0][2]
    if t >= ts[-1]: return s[-1][1], s[-1][2]
    for a, b in zip(s, s[1:]):
        if a[0] <= t <= b[0]:
            f = (t - a[0]) / (b[0] - a[0]); return a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f

def frame(src, t, rot, td):
    o = Path(td) / "f.png"
    vf = "scale=in_range=tv:out_range=pc" + (",hflip,vflip" if rot else "")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", vf, str(o)], check=True)
    return Image.open(o).convert("RGB")

def crop(im, ex, ey, cw, u, v):
    W, H = im.size; cwp = cw * W; chp = cwp * 16 / 9
    l = min(max(ex * W - u * cwp, 0), W - cwp); t = min(max(ey * H - v * chp, 0), H - chp)
    return im.resize((540, 960), Image.LANCZOS, box=(l, t, l + cwp, t + chp))

def primary(im):   # the bake's per-clip primary (grey balance + exposure to one target), so the board's colour matches the reel
    x = np.asarray(im).astype(np.float32) / 255; y = x @ np.array([.2126, .7152, .0722], np.float32)
    m = (y > 0.08) & (y < 0.92); mean = x[m].mean(axis=0) if m.sum() > 100 else x.reshape(-1, 3).mean(axis=0)
    gains = (mean.mean() / np.maximum(mean, 1e-3)) ** 0.5
    k = min((0.30 / max(float((x * gains) @ np.array([.2126, .7152, .0722])).mean() if False else float(((x * gains) @ np.array([.2126, .7152, .0722], np.float32)).mean()), 1e-3)) ** 0.8, 2.0)
    return Image.fromarray((np.clip(x * gains * k, 0, 1) * 255 + 0.5).astype(np.uint8))

def grade(im, td):
    im = primary(im)
    i = Path(td) / "g_in.png"; o = Path(td) / "g_out.png"; im.save(i)
    f = str(CUBE).replace(":", "\\:")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(i), "-vf", f"format=gbrp,lut3d=file='{f}',vignette=angle=0.42,format=rgb24", str(o)], check=True)
    return Image.open(o).convert("RGB")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("plan"); ap.add_argument("-o", "--out", required=True); a = ap.parse_args()
    plan = json.loads(Path(a.plan).read_text())
    try: f1 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22); f2 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 19)
    except OSError: f1 = f2 = ImageFont.load_default()
    cols = []
    with tempfile.TemporaryDirectory() as td:
        for s in plan["slots"]:
            tiles = []
            for which in ("start", "end"):
                p = s[which]; im = frame(s["src"], p["t"], s.get("rot", False), td)
                ex, ey = (p["ex"], p["ey"]) if "ex" in p else track_at(s["track"], p["t"])
                cw = s["eye_px"] / (p["span"] * im.size[0])
                g = grade(crop(im, ex, ey, cw, p.get("u", 0.5), p.get("v", 0.40)), td); d = ImageDraw.Draw(g)
                d.line([(0, 384), (540, 384)], fill=(0, 255, 255), width=1)
                d.rectangle([0, 0, 540, 34], fill=(0, 0, 0)); d.text((8, 6), f"{s['time']}  {which.upper()}  eyes {int(p['span']*100)} %  ({1080/(cw*im.size[0]):.1f}x)", font=f2, fill=(255, 225, 140))
                tiles.append(g)
            col = Image.new("RGB", (540, 960 * 2 + 110), (14, 14, 14)); col.paste(tiles[0], (0, 0)); col.paste(tiles[1], (0, 960))
            d = ImageDraw.Draw(col); d.text((8, 1928), s["clip"], font=f1, fill=(255, 215, 120)); d.text((8, 1958), s["move"], font=f2, fill=(220, 220, 220))
            if len(s["move"]) > 48: d.text((8, 1984), s.get("move2", ""), font=f2, fill=(220, 220, 220))
            cols.append(col)
    board = Image.new("RGB", (540 * len(cols), 960 * 2 + 110), (14, 14, 14))
    for i, c in enumerate(cols): board.paste(c, (540 * i, 0))
    board = board.resize((board.width // 2, board.height // 2), Image.LANCZOS); board.save(a.out, quality=88); print("✓", a.out, board.size)

if __name__ == "__main__":
    main()
