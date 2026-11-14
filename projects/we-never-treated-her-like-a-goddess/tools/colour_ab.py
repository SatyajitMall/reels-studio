#!/usr/bin/env python3
"""Colour A/B for the director's note on v6c, "the colours are all over the place, the things hardly look natural" (2026-10-30).
Per shot, the same moment (bake_tune's preview frame: 60 % into the played span, at the on-screen crop), several ways:
  camera = camera file, no processing    v5e = the earlier warm-gold Premiere grade    v6c = the halfway baked look now
  plus any natural-grade override sets given with --set name=k=v,k=v (bake_tune overrides).
Prints, per variant, the shot-to-shot spread of white balance (R/B of the low-saturation midtones), saturation and luma.
Usage (reels-studio root): .venv/bin/python projects/<reel>/tools/colour_ab.py -o sheet.jpg [--shots 01_C010,15_C143] --set nat=wb=1,...
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "tools"))
import bake_check as BC, bake_tune as BT, shot_look as S  # noqa: E402

LAB = {"01": "1", "02": "2a", "03": "2b", "04": "3", "05": "4", "06": "5", "07": "6", "08": "7", "09": "8", "10": "9", "11": "10",
       "12": "11", "13": "12", "14": "13", "15": "14", "16": "15", "17": "16", "18": "17"}


def wb_sat_luma(x):
    y = S.luma(x); s = S.sat_map(x); m = (y > 0.15) & (y < 0.7)
    m2 = m & (s <= np.percentile(s[m], 30))
    rb = float(x[..., 0][m2].mean() / max(x[..., 2][m2].mean(), 1e-3))
    return rb, float(s.mean()), float(y.mean())


def main():
    a = sys.argv[1:]; out = a[a.index("-o") + 1]
    plan = json.loads((R / "analysis/look/bake_plan.json").read_text())
    names = a[a.index("--shots") + 1].split(",") if "--shots" in a else [q["name"] for q in plan]
    sets = [x.split("=", 1) for i, x in enumerate(a) if i > 0 and a[i - 1] == "--set"]
    # --override <shot>=<k=v,...>: that shot uses these overrides in the LAST --set (a per-shot fix, e.g. #1's camera cast)
    over = dict(x.split("=", 1) for i, x in enumerate(a) if i > 0 and a[i - 1] == "--override")
    dump = {s["start"]: s for s in json.loads((R / "analysis/_es_out_bake.txt").read_text())["shots"]}
    base = [c for c in ("camera", "v5e", "v6c") if "--no-" + c not in a]
    cols = base + [n for n, _ in sets]
    meas = {c: [] for c in cols}; rows = []
    for name in names:
        q = BT.shot(name); sf = S.probe(str(R / q["clip"]))[1]
        ts = np.linspace(q["in"], q["in"] + (q["frames"] - 1) / sf, 6); t = ts[3]
        k = int(round((t - q["in"]) * sf)); reel_t = (q["seq"][0] + k) / 25
        tiles = []
        if "camera" in base:
            tiles.append(S.decode(str(R / q["clip"]), t, 1, tuple(q["crop"]), None, 540)[0])
        for v in [f for c, f in (("v5e", "v5e_quality"), ("v6c", "v6c_clean")) if c in base]:
            f = BC.grab(R / f"renders/previews/{v}.mp4", t=reel_t).astype(np.float32) / 255
            tiles.append(np.asarray(Image.fromarray((f * 255).astype(np.uint8)).resize((540, 960), Image.LANCZOS)).astype(np.float32) / 255)
        for si, (_, kv) in enumerate(sets):
            if si == len(sets) - 1 and name in over: kv = over[name]
            tr, smp, _ = BT.treatment(q, BT.parse(kv))
            raw = S.decode(str(R / q["clip"]), t - 0.08, 5, tuple(q["crop"]), BT.params(BT.parse(kv))["denoise"], S.W)
            x = tr(raw[len(raw) // 2])
            tiles.append(np.asarray(Image.fromarray((np.clip(x, 0, 1) * 255 + 0.5).astype(np.uint8)).resize((540, 960), Image.LANCZOS)).astype(np.float32) / 255)
        for c, tl in zip(cols, tiles):
            sub = tl.copy(); sub[int(960 * 0.72):int(960 * 0.82)] = np.nan          # skip the subtitle band
            keep = ~np.isnan(sub[..., 0]); flat = tl[keep].reshape(-1, 1, 3)
            meas[c].append(wb_sat_luma(flat))
        rows.append((name, tiles))
        print(name, "  ".join(f"{c}: R/B {m[-1][0]:.2f} sat {m[-1][1]:.2f} luma {m[-1][2]:.2f}" for c, m in meas.items()), flush=True)
    print("\nshot-to-shot spread (std across shots):")
    for c, m in meas.items():
        arr = np.array(m); print(f"  {c:8s} R/B mean {arr[:, 0].mean():.2f} sd {arr[:, 0].std():.3f} | sat mean {arr[:, 1].mean():.2f} sd {arr[:, 1].std():.3f} | luma sd {arr[:, 2].std():.3f}")
    tw, th = 180, 320; font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 13)
    sheet = Image.new("RGB", (len(cols) * tw + 40, len(rows) * th + 22), (14, 14, 14)); d = ImageDraw.Draw(sheet)
    for i, c in enumerate(cols): d.text((40 + i * tw + 4, 4), c, font=font, fill=(240, 210, 80))
    for j, (name, tiles) in enumerate(rows):
        d.text((4, 22 + j * th + 4), "#" + LAB[name[:2]], font=font, fill=(255, 255, 255))
        for i, tl in enumerate(tiles):
            sheet.paste(Image.fromarray((np.clip(tl, 0, 1) * 255 + 0.5).astype(np.uint8)).resize((tw, th), Image.LANCZOS), (40 + i * tw, 22 + j * th))
    sheet.save(out, quality=90); print("✓", out)


if __name__ == "__main__":
    main()
