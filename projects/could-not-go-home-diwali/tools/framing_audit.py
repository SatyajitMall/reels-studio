"""Framing audit for v3c (reel-local). Director's note 2026-11-11: "frames seem cut or incomplete ... the roti one,
the camera could have been placed a little lower to complete the frame".

Reads analysis/es/_es_framing.txt (dump_v3c_framing.jsx: every V1 clip's source, in point, Scale / Position keys,
Rotation) and, for each shot, draws the 4:3 picture window (seq 0,505 → 1080,1315) on the FULL upright source frame:
green = window at the first key, yellow = at the last key (the +5 % push). Grey = picture the source has but the reel
doesn't show. Prints the spare picture on each side of the window (source px and % of the window), so a reframe that
"puts the camera lower" is only proposed where the source really has picture below.

Usage (reel folder): python3 tools/framing_audit.py -o analysis/framing_v3c
"""
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIN = (0, 505, 1080, 1315)
SEQ_W, SEQ_H = 1080, 1920


def frame(path, n, rot):
    """Upright source frame n (25 fps-interpreted index), as Premiere shows it after Rotation."""
    probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                       "stream=width,height", "-of", "json", path], capture_output=True, text=True).stdout)
    w, h = probe["streams"][0]["width"], probe["streams"][0]["height"]
    vf = f"select=eq(n\\,{n})"
    if rot == -90:
        vf += ",transpose=2"  # autorotated portrait (Premiere's 2160x3840) → Premiere Rotation −90 = CCW
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-frames:v", "1", "-f", "image2pipe",
                          "-vcodec", "png", "-"], capture_output=True).stdout
    from io import BytesIO
    return Image.open(BytesIO(raw)).convert("RGB")


def at(prop, t):
    """Value of a Premiere property dump at clip-source time t (linear between keys)."""
    if "keys" not in prop:
        return prop["v"]
    ks = prop["keys"]
    if t <= ks[0][0]:
        return ks[0][1]
    if t >= ks[-1][0]:
        return ks[-1][1]
    for (t0, v0), (t1, v1) in zip(ks, ks[1:]):
        if t0 <= t <= t1:
            a = (t - t0) / (t1 - t0)
            return [x0 + (x1 - x0) * a for x0, x1 in zip(v0, v1)] if isinstance(v0, list) else v0 + (v1 - v0) * a


def footprint(img_w, img_h, scale, pos):
    s = scale / 100
    px, py = pos[0] * SEQ_W, pos[1] * SEQ_H
    x0, y0, x1, y1 = WIN
    return [(x0 - px) / s + img_w / 2, (y0 - py) / s + img_h / 2, (x1 - px) / s + img_w / 2, (y1 - py) / s + img_h / 2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="analysis/framing_v3c")
    ap.add_argument("--dump", default="analysis/es/_es_framing.txt")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    clips = [c for c in json.load(open(a.dump))["clips"] if c["track"] == 0]
    font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22)
    rows, report = [], []
    for c in clips:
        dur = c["end"] - c["start"]
        rot = c["rot"]["v"]
        t0 = c["inS"]; t1 = t0 + dur / 25
        im = frame(c["path"], c["inF"] + dur // 2, rot)
        W, H = im.size
        f0 = footprint(W, H, at(c["scale"], t0), at(c["pos"], t0))
        f1 = footprint(W, H, at(c["scale"], t1), at(c["pos"], t1))
        # spare picture around the window at the end of the push (source px), and as % of the window's height/width
        ww, wh = f1[2] - f1[0], f1[3] - f1[1]
        spare = {"top": f1[1], "bottom": H - f1[3], "left": f1[0], "right": W - f1[2]}
        pct = {k: round(100 * v / (wh if k in ("top", "bottom") else ww), 1) for k, v in spare.items()}
        report.append({"shot": c["name"], "src": Path(c["path"]).name, "src_wh": [W, H],
                       "window_src_px": [round(x) for x in f1], "spare_pct_of_window": pct})
        # sheet tile: dim outside, draw both footprints
        dim = Image.eval(im, lambda v: int(v * 0.35))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rectangle([round(x) for x in f1], fill=255)
        tile = Image.composite(im, dim, mask)
        d = ImageDraw.Draw(tile)
        lw = max(3, W // 300)
        d.rectangle([round(x) for x in f0], outline=(60, 220, 90), width=lw)
        d.rectangle([round(x) for x in f1], outline=(255, 210, 60), width=lw)
        tile = tile.resize((640, round(640 * H / W)))
        lab = Image.new("RGB", (640, 34), (16, 16, 16))
        ImageDraw.Draw(lab).text((6, 5), f"{c['name']}  bottom spare {pct['bottom']}%", font=font, fill=(235, 235, 235))
        cell = Image.new("RGB", (640, 34 + tile.height), (16, 16, 16)); cell.paste(lab, (0, 0)); cell.paste(tile, (0, 34))
        rows.append(cell)
    cols = 3
    ch = max(r.height for r in rows)
    sheet = Image.new("RGB", (cols * 650, ((len(rows) + cols - 1) // cols) * (ch + 10)), (16, 16, 16))
    for i, r in enumerate(rows):
        sheet.paste(r, ((i % cols) * 650, (i // cols) * (ch + 10)))
    sheet.save(out / "framing_v3c_sheet.jpg", quality=88)
    (out / "framing_v3c.json").write_text(json.dumps(report, indent=1))
    for r in report:
        print(f"{r['shot']:24s} {r['src']:34s} spare % top {r['spare_pct_of_window']['top']:5.1f} bottom {r['spare_pct_of_window']['bottom']:5.1f}"
              f" left {r['spare_pct_of_window']['left']:5.1f} right {r['spare_pct_of_window']['right']:5.1f}")
    print("sheet:", out / "framing_v3c_sheet.jpg")


if __name__ == "__main__":
    main()
