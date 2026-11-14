"""Roti-shot look for the whole reel (reel-local, v3c): director's note 2026-11-11, "the hand making the roti is the
most cinematic shot ... can we apply that throughout the reel?"

Two parts, both reproducible in Premiere:
  1. per-shot BALANCE (clip Lumetri exposure): each shot's camera-true window is brought to one mid-luma with a
     linear-light gain (clamped to about ±1 stop), so brightness doesn't jump from shot to shot;
  2. a global ROTI LOOK (.cube on V3): per-channel quantile match of the balanced pool to the roti shot as it plays
     in the v3b render, plus a saturation factor (ref_match_lut.py's method).

Writes roti_match.cube (full strength), balance.json (per-shot gain in stops), stats.json and a preview sheet:
v3b now | balance + roti look 60 % | balance + roti look 100 %, every shot's mid frame, 07 (the roti) untouched.

Usage (studio root):
  .venv/bin/python -I projects/could-not-go-home-diwali/tools/roti_match.py \
      --camtrue renders/exports/..._v3b_camtrue.mp4 --render renders/exports/..._v3b_premiere.mp4 -o analysis/grade_v3c
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ref_match_lut as rm  # noqa: E402

STARTS = [0, 39, 78, 117, 156, 196, 236, 276, 316, 356, 395, 435, 475, 515, 555, 595, 635, 674, 714]
NAMES = ["01 auto", "02 auto turn", "03 marigold", "04 parotta", "05 hands", "06 juice", "07 ROTI", "08 cook",
         "09 serve", "10 vendor", "11 vendor cl", "12 show step", "13 paan", "14 paan look", "15 icecream",
         "16 foam", "17 wash", "18 look"]
ROTI = 6
W, H = 540, 405


def grab(vid, n):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(vid), "-vf",
                          f"select=eq(n\\,{n}),crop=1080:810:0:505,scale={W}:{H}", "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.float64) / 255


def lin(x):
    return np.power(np.clip(x, 0, 1), 2.2)


def gam(x):
    return np.power(np.clip(x, 0, 1), 1 / 2.2)


def gain(img, stops):
    return gam(lin(img) * 2.0 ** stops)


def luma(img):
    return float((img @ rm.LUMA).mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--camtrue", required=True); ap.add_argument("--render", required=True)
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--target", type=float, default=None, help="balanced mid-luma (default: pool median)")
    ap.add_argument("--max-stops", type=float, default=1.0)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    # sample 3 frames per shot (25 %, 50 %, 75 %)
    def pick(i):
        s, e = STARTS[i], STARTS[i + 1]
        return [s + (e - s) * k // 4 for k in (1, 2, 3)]
    cam = {i: [grab(a.camtrue, n) for n in pick(i)] for i in range(len(NAMES)) if i != ROTI}
    ref = [grab(a.render, n) for n in range(STARTS[ROTI] + 2, STARTS[ROTI + 1] - 2, 4)]
    now_mid = {i: grab(a.render, (STARTS[i] + STARTS[i + 1]) // 2) for i in range(len(NAMES))}

    # 1. balance
    lum = {i: np.mean([luma(f) for f in fs]) for i, fs in cam.items()}
    target = a.target or float(np.median(list(lum.values())))
    stops = {}
    for i, l in lum.items():
        # solve gain in stops so the window's mean luma lands on target (bisection, linear light)
        lo, hi = -a.max_stops, a.max_stops
        for _ in range(30):
            m = (lo + hi) / 2
            if np.mean([luma(gain(f, m)) for f in cam[i]]) < target:
                lo = m
            else:
                hi = m
        stops[i] = round((lo + hi) / 2, 3)
    bal = {i: [gain(f, stops[i]) for f in fs] for i, fs in cam.items()}

    # 2. roti look on the balanced pool
    rstat, rpx = rm.bands(ref)
    pool = [f for fs in bal.values() for f in fs]
    ostat, opx = rm.bands(pool)
    cs = rm.curves(opx, rpx)
    mid, _ = rm.bands([rm.apply(i, cs, 1.0) for i in pool])
    satk = float(np.clip(rstat["all"]["sat"] / max(mid["all"]["sat"], 1e-6), 0.6, 1.3))
    rm.write_cube(out / "roti_match.cube", cs, satk)
    after, _ = rm.bands([rm.apply(i, cs, satk) for i in pool])

    per_shot = []
    for i in range(len(NAMES)):
        if i == ROTI:
            per_shot.append({"shot": NAMES[i], "stops": 0, "now": luma(now_mid[i]), "look100": luma(now_mid[i])})
            continue
        f = bal[i][1]
        per_shot.append({"shot": NAMES[i], "stops": stops[i], "camtrue": round(lum[i], 3), "now": round(luma(now_mid[i]), 3),
                         "look60": round(luma(rm.apply(f, cs, satk, 0.6)), 3), "look100": round(luma(rm.apply(f, cs, satk, 1.0)), 3)})
    (out / "balance.json").write_text(json.dumps({"target_luma": target, "shots": per_shot}, indent=1))
    (out / "stats.json").write_text(json.dumps({"roti": rstat, "balanced_pool": ostat, "after_look": after, "sat_factor": satk}, indent=1))
    print(f"target mid-luma {target:.3f}, sat factor {satk:.2f}")
    print(f"{'shot':14s} stops   now    look60 look100")
    for d in per_shot:
        print(f"{d['shot']:14s} {d['stops']:+.2f}  {d['now']:.3f}  {d.get('look60', d['now']):.3f}  {d['look100']:.3f}")
    print("roti:", json.dumps(rstat["all"]), "\nafter:", json.dumps(after["all"]))

    # sheet: three 6×3 grids
    tw, th, cols = 270, 203, 6
    font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
    big = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 26, index=1)
    grids = [("v3b now", None), ("roti look, softer (60 %)", 0.6), ("roti look, full (100 %)", 1.0)]
    gh = 3 * (th + 20) + 40
    S = Image.new("RGB", (cols * tw, len(grids) * gh), (16, 16, 16)); d = ImageDraw.Draw(S)
    for g, (title, mix) in enumerate(grids):
        y0 = g * gh
        d.text((8, y0 + 6), title, font=big, fill=(255, 210, 120))
        for i in range(len(NAMES)):
            if mix is None or i == ROTI:
                img = now_mid[i]
            else:
                img = rm.apply(bal[i][1], cs, satk, mix)
            t = Image.fromarray(np.clip(img * 255, 0, 255).astype(np.uint8)).resize((tw, th))
            x = (i % cols) * tw; y = y0 + 40 + (i // cols) * (th + 20)
            S.paste(t, (x, y + 18))
            d.text((x + 4, y + 2), NAMES[i], font=font, fill=(255, 230, 120) if i == ROTI else (225, 225, 225))
    S.save(out / "roti_look_preview.png")
    print("sheet:", out / "roti_look_preview.png")


if __name__ == "__main__":
    main()
