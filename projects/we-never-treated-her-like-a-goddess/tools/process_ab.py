#!/usr/bin/env python3
"""Processing A/B for the director's "over processed instead of looking HD" note (2026-10-30): the same frame of a shot,
reframed exactly as v6b's Motion reframes it, four ways:
  A  v6b now (ProRes master): bake (denoise + clarity 0.12 + look) + Lumetri Sharpen 20 + grain 4 %
  B  the bake alone: no Premiere sharpen, no grain
  C  minimal: the same look and colour constants, but no denoise, no clarity, no sharpen, no grain
  D  camera original, no processing at all
Writes a sheet (full frames + a 1:1 crop per shot) and prints detail / noise per variant inside the crop.
Usage (reels-studio root): .venv/bin/python projects/<reel>/tools/process_ab.py -o sheet.jpg"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "tools"))
import bake_check as BC, bake_tune as BT, shot_look as S  # noqa: E402

# name, reel time, 1:1 crop box (x0, y0) of 360×360 in the 1080×1920 frame, tuned overrides used by v6b
SHOTS = [("01_C010", 1.16, (420, 900), "wb=0,levels=0.95,cast=0.8,warm=1.10"),
         ("08_C020", 9.80, (230, 1050), ""),
         ("15_C143", 22.00, (360, 810), ""),
         ("17_C100", 25.00, (360, 1200), "")]
OFF = {"18_C056": -1}


def reframe(full, scale, pos):
    sc = scale / 100; h, w = full.shape[:2]
    cw, ch = 1080 / sc, 1920 / sc; left, top = (0 - pos[0] * 1080) / sc + w / 2, (0 - pos[1] * 1920) / sc + h / 2
    im = Image.fromarray(full).resize((1080, 1920), Image.LANCZOS, box=(left, top, left + cw, top + ch))
    return np.asarray(im)


def measure(a):
    y = a.astype(np.float32).mean(-1)
    l = -4 * y[1:-1, 1:-1] + y[:-2, 1:-1] + y[2:, 1:-1] + y[1:-1, :-2] + y[1:-1, 2:]
    al = np.abs(l); h, w = (al.shape[0] // 8) * 8, (al.shape[1] // 8) * 8
    b = al[:h, :w].reshape(h // 8, 8, w // 8, 8).mean((1, 3)).ravel()
    return round(float(l.var()), 1), round(float(np.percentile(b, 20)), 2)


def main():
    out = sys.argv[sys.argv.index("-o") + 1]
    V6 = {r["name"]: r for r in json.loads((R / "analysis/_v6_data.jsx").read_text()[len("var V6="):-2])}
    dump = {s["start"]: s for s in json.loads((R / "analysis/_es_out_bake.txt").read_text())["shots"]}
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
    labels = ["A  v6b now", "B  no sharpen, no grain", "C  minimal (no denoise/clarity/sharpen/grain)", "D  camera original"]
    rows = []
    for name, t, (cx, cy), kv in SHOTS:
        r = V6[name]; s = dump[r["start"]]; q = BT.shot(name)
        bake = Path(r["path"]); t_bake = bake.with_name(bake.stem + "_t.mov")
        if t_bake.exists(): bake = t_bake
        side = json.loads(bake.with_suffix(".json").read_text())
        k = round(t * 25) - r["start"]; sc = BC.at(s["Scale"], s["inP"] + k / 25); pos = s["Position"]["val"]
        A = BC.grab(R / "renders/masters/v6b_master_prores422.mov", t=round(t * 25) / 25)
        Bf = BC.grab(bake, vf="null", w=side["size"][0], h=side["size"][1], frame=side["place_in_frames"] + OFF.get(name, 0) + k)
        B = reframe(Bf, sc, pos)
        clip = str(R / q["clip"]); size = S.frame_size(clip); view = S.view_rect(size, tuple(q["crop"]))
        t_src = side["src_start"] + (side["place_in_frames"] + OFF.get(name, 0) + k - 0.25) / side["src_fps"]
        raw = next(S.decode_stream(clip, t_src, 1, "format=rgb24", size))
        o = BT.parse(kv); o.update({"clarity": 0.0, "denoise": 0})
        tr, _, _ = BT.treatment(q, o)
        C = reframe((tr(raw, seed=1, view=view) * 255 + 0.5).clip(0, 255).astype(np.uint8), sc, pos)
        D = reframe((raw * 255 + 0.5).clip(0, 255).astype(np.uint8), sc, pos)
        vs = [A, B, C, D]
        stats = [measure(v[cy:cy + 360, cx:cx + 360]) for v in vs]
        print(name, "detail (Laplacian var) / noise floor in the crop:", "  ".join(f"{l.split()[0]} {d}/{n}" for l, (d, n) in zip(labels, stats)))
        rows.append((name, vs, (cx, cy)))
    tw, th, cs = 270, 480, 360
    sheet = Image.new("RGB", (4 * (tw + cs), len(rows) * (th + 26) + 26), (14, 14, 14)); d = ImageDraw.Draw(sheet)
    for i, lab in enumerate(labels):
        d.text((i * (tw + cs) + 6, 4), lab, font=font, fill=(240, 210, 80))
    for j, (name, vs, (cx, cy)) in enumerate(rows):
        y = 26 + j * (th + 26)
        for i, v in enumerate(vs):
            x = i * (tw + cs)
            sheet.paste(Image.fromarray(v).resize((tw, th), Image.LANCZOS), (x, y))
            sheet.paste(Image.fromarray(v[cy:cy + cs, cx:cx + cs]), (x + tw, y))
        d.text((6, y + th + 4), f"#{ {'01_C010': '1', '08_C020': '7', '15_C143': '14', '17_C100': '16'}[name] } {name[3:]}   (left: whole frame, right: 1:1 crop)", font=font, fill=(255, 255, 255))
    sheet.save(out, quality=92); print("✓", out)


if __name__ == "__main__":
    main()
