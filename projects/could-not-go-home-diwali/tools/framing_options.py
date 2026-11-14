"""Framing options sheet for the director (reel-local, 2026-11-11 note: "frames seem cut or incomplete ... the roti
one, the camera could have been placed a little lower"). Phone-sized, ungraded (framing only).

Each row: left = what v3c shows in the 4:3 window (from the source, ungraded); right = the whole camera/stock frame,
yellow box = the window now, cyan box = a proposed reframe where the source has the picture for it.

Usage (reel folder): python3 tools/framing_options.py -o analysis/framing_v3c/framing_options.jpg
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import framing_audit as fa

# shot → (label, proposed source-box fn or None, note)
ROWS = [
    ("07_S1_maa_roti", None, "07 roti: the window already shows the stock's full height. The fire/tawa is below the stock's own edge."),
    ("13_C050_paan", None, "13 paan: same. Full camera height already shown; the table is cut by the camera itself."),
    ("03_F8_marigold", "right", "03 marigold: the working hands sit at the right edge. Slide the window right (cyan) to bring them in."),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="analysis/framing_v3c/framing_options.jpg")
    ap.add_argument("--dump", default="analysis/es/_es_framing.txt")
    a = ap.parse_args()
    clips = {c["name"]: c for c in json.load(open(a.dump))["clips"] if c["track"] == 0}
    f_big = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 26)
    f_sm = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 22)
    TW = 540
    cells = []
    for name, prop, note in ROWS:
        c = clips[name]
        dur = c["end"] - c["start"]
        t1 = c["inS"] + dur / 25
        im = fa.frame(c["path"], c["inF"] + dur // 2, c["rot"]["v"])
        W, H = im.size
        now = [round(x) for x in fa.footprint(W, H, fa.at(c["scale"], t1), fa.at(c["pos"], t1))]
        now = [max(0, now[0]), max(0, now[1]), min(W, now[2]), min(H, now[3])]
        new = None
        if prop == "right":
            w = now[2] - now[0]
            new = [W - w, now[1], W, now[3]]
        left_box = new or now
        crop = im.crop(tuple(now)).resize((TW, round(TW * 3 / 4)))
        prop_crop = im.crop(tuple(new)).resize((TW, round(TW * 3 / 4))) if new else None
        full = im.copy(); d = ImageDraw.Draw(full); lw = max(4, W // 250)
        d.rectangle(now, outline=(255, 210, 60), width=lw)
        if new:
            d.rectangle(new, outline=(60, 220, 255), width=lw)
        full = full.resize((TW, round(TW * H / W)))
        panels = [("now", crop), ("whole frame (yellow = now" + (", cyan = proposed)" if new else ")"), full)]
        if prop_crop is not None:
            panels.append(("proposed", prop_crop))
        ph = max(p.height for _, p in panels)
        row = Image.new("RGB", (TW * 2 + 10, 50 + ((len(panels) + 1) // 2) * (ph + 36) + 10), (18, 18, 18))
        dr = ImageDraw.Draw(row)
        dr.text((8, 10), note, font=f_sm, fill=(255, 225, 140))
        for i, (lab, p) in enumerate(panels):
            x = (i % 2) * (TW + 10); y = 50 + (i // 2) * (ph + 36)
            dr.text((x + 6, y + 4), lab, font=f_sm, fill=(230, 230, 230))
            row.paste(p, (x, y + 32))
        cells.append(row)
    head = Image.new("RGB", (TW * 2 + 10, 60), (18, 18, 18))
    ImageDraw.Draw(head).text((8, 14), "Framing check, v3c (ungraded, framing only)", font=f_big, fill=(255, 255, 255))
    total = Image.new("RGB", (TW * 2 + 10, head.height + sum(r.height for r in cells)), (18, 18, 18))
    total.paste(head, (0, 0)); y = head.height
    for r in cells:
        total.paste(r, (0, y)); y += r.height
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    total.save(a.out, quality=88)
    print(a.out, total.size)


if __name__ == "__main__":
    main()
