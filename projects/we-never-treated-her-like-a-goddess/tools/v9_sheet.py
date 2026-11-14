#!/usr/bin/env python3
"""Round 9 sheet for the director (HQ step 6): each of the 14 shots at its mid-frame, camera | v8b | v9, with luma, crushed % (< 0.03)
and the frame width shown. camera = the camera file at v9's framing, no grade. v9 = analysis/v9_stills/<pass>/<frame>.png.
Usage (reels-studio root): .venv/bin/python projects/<reel>/tools/v9_sheet.py <pass dir name> <out.jpg>"""
import json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bake_check as B, shot_look as S  # noqa: E402
from process_ab import reframe  # noqa: E402

R = B.R
F = json.loads((R / "analysis/_v9_frame.jsx").read_text()[len("var V9F="):-2])
old = {c["start"]: c for c in json.loads((R / "analysis/_es_out_v9read.txt").read_text())["clips"]}   # v8b's state (read before v9 changed it)
NATIVE = {"10192144_C017": 30.004, "10202144_C056": 24.941}


def at(keys, t):
    if not isinstance(keys, list) or not isinstance(keys[0], list):
        return keys
    (t0, v0), (t1, v1) = keys[0], keys[-1]
    return v0 + (v1 - v0) * (t - t0) / (t1 - t0)


def st(a):
    x = a.astype(np.float32) / 255; y = x @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    m = np.ones(y.shape, bool); m[int(y.shape[0] * .72):int(y.shape[0] * .82)] = False
    return float(y[m].mean()), float((y[m] < 0.03).mean() * 100)


def main():
    pdir, out = R / "analysis/v9_stills" / sys.argv[1], Path(sys.argv[2])
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 13); fs = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 12)
    tw, th, cols = 150, 267, 7
    sheet = Image.new("RGB", (cols * (3 * tw + 8), 2 * (th + 58)), (14, 14, 14)); d = ImageDraw.Draw(sheet); rows = []
    for i, f in enumerate(F):
        o = old[f["f"]]; n = f["n"]; a, b = o["start"], o["end"]; mfr = a + (b - a) // 2; k = mfr - a; tp = o["inP"] + k / 25
        v9 = np.asarray(Image.open(pdir / f"{mfr:03d}.png").convert("RGB"))
        v8 = B.grab(R / "renders/masters/v8b_master_prores422.mov", t=mfr / 25)
        nf = NATIVE.get(n, 25.0); tn = tp * 25 / nf if n == "10192144_C017" else ((round(tp * 25) - 1) / nf if n == "10202144_C056" else tp)
        clip = str(R / "raw/b-roll" / f"A001_{n}.mov"); size = S.frame_size(clip)
        raw = next(S.decode_stream(clip, max(0, tn - 0.25 / nf), 1, "format=rgb24", size))
        s9 = f["s"][0] + (f["s"][1] - f["s"][0]) * k / (b - a)
        p9 = f["p"][0] if len(f["p"]) == 1 else [f["p"][0][j] + (f["p"][1][j] - f["p"][0][j]) * k / (b - a) for j in range(2)]
        cam = reframe((raw * 255 + 0.5).clip(0, 255).astype(np.uint8), s9, p9)
        vals = [("camera", cam, 5000 / s9), ("v8b", v8, 5000 / at(o["motion"]["Scale"], tp)), ("v9", v9, 5000 / s9)]
        x0, y0 = (i % cols) * (3 * tw + 8), (i // cols) * (th + 58)
        d.text((x0 + 3, y0 + 2), f"#{i+1} {n.split('_')[1]}", font=font, fill=(240, 210, 80)); row = {"shot": i + 1, "clip": n.split("_")[1]}
        for j, (lab, im, w) in enumerate(vals):
            lu, cr = st(im); row[lab] = {"luma": round(lu, 3), "crushed%": round(cr, 1), "width%": round(w)}
            sheet.paste(Image.fromarray(im).resize((tw, th), Image.LANCZOS), (x0 + j * tw, y0 + 18))
            d.text((x0 + j * tw + 3, y0 + 20 + th), f"{lab}  L{lu:.2f}", font=fs, fill=(255, 255, 255))
            d.text((x0 + j * tw + 3, y0 + 36 + th), f"crush {cr:.1f}%  w{w:.0f}%", font=fs, fill=(200, 200, 200))
        rows.append(row)
    sheet.save(out, quality=90); (pdir / "sheet_numbers.json").write_text(json.dumps(rows, indent=1))
    for lab in ("camera", "v8b", "v9"):
        print(lab, "mean luma", round(float(np.mean([r[lab]["luma"] for r in rows])), 3), "| max crushed", max(r[lab]["crushed%"] for r in rows), "| min width", min(r[lab]["width%"] for r in rows))
    print("✓", out)


if __name__ == "__main__":
    main()
