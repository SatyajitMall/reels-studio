"""Depth-split look preview (reel-local, v3c). Uses the Cinematic-mode disparity (tools/depth_dump) to grade the
background deeper and lift the subject, on top of the balanced roti look (tools/roti_match.py's roti_match.cube).

Per still: P = the f/2.0 bake frame (natural orientation), D = disparity at the same camera time, f = recorded focus.
  subject mask M = disparity at or in front of the focus plane (soft edge), feathered;
  flat  = balance to the reel's mid-luma, then roti look at --mix;
  depth = background: look at --bg-mix and --bg-stops; subject: look at --subj-mix and --subj-stops.
Usage: .venv/bin/python -I tools/depth_look_preview.py --dir <dump dir> --shots 04 06 ... --cube analysis/grade_v3c/roti_match.cube -o <png>
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter, zoom
sys.path.insert(0, str(Path(__file__).resolve().parent))
import roti_match as R  # noqa: E402
import ref_match_lut as rm  # noqa: E402


def read_cube(p):
    L = [l for l in Path(p).read_text().splitlines() if l and l[0] in "0123456789-"]
    n = round(len(L) ** (1 / 3)); a = np.array([[float(v) for v in l.split()] for l in L]).reshape(n, n, n, 3)  # [b][g][r]
    return a, n


def apply_cube(img, cube, n, mix):
    from scipy.ndimage import map_coordinates
    c = np.clip(img, 0, 1) * (n - 1)
    coords = [c[..., 2].ravel(), c[..., 1].ravel(), c[..., 0].ravel()]
    out = np.stack([map_coordinates(cube[..., k], coords, order=1).reshape(img.shape[:2]) for k in range(3)], -1)
    return img + (out - img) * mix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True); ap.add_argument("--shots", nargs="+", required=True)
    ap.add_argument("--cube", required=True); ap.add_argument("-o", required=True)
    ap.add_argument("--target", type=float, default=0.336); ap.add_argument("--mix", type=float, default=0.5)
    ap.add_argument("--bg-mix", type=float, default=0.8); ap.add_argument("--bg-stops", type=float, default=-0.45)
    ap.add_argument("--subj-mix", type=float, default=0.3); ap.add_argument("--subj-stops", type=float, default=0.3)
    a = ap.parse_args()
    cube, n = read_cube(a.cube)
    d = Path(a.dir); tw = 480; th = 360
    rows = []
    for s in a.shots:
        im = Image.open(d / f"{s}.png").convert("RGB")
        w, h = im.size; cw = h * 4 // 3; x0 = (w - cw) // 2
        P = np.asarray(im.crop((x0, 0, x0 + cw, h)).resize((tw, th))).astype(np.float64) / 255
        meta = json.loads((d / f"{s}.json").read_text())
        D = np.fromfile(d / f"{s}.f32", np.float32)[: meta["w"] * meta["h"]].reshape(meta["h"], meta["w"]).astype(np.float64)
        D = np.nan_to_num(D, nan=0.0)
        dx0 = int(round(x0 / w * meta["w"])); dcw = int(round(cw / w * meta["w"]))
        D = D[:, dx0:dx0 + dcw]
        f = meta["focus"][0]
        # subject = the focus plane ± a band: behind it by >20 % → background; far in front of it (> +45 %, e.g. a lit
        # counter or a passer-by between camera and subject) → treated like background too
        back = np.clip((D - 0.80 * f) / (0.15 * f), 0, 1)
        front = np.clip((1.60 * f - D) / (0.15 * f), 0, 1)
        M = back * front
        M = gaussian_filter(M, 3)
        M = zoom(M, (th / M.shape[0], tw / M.shape[1]), order=1); M = gaussian_filter(M, 4)[..., None]
        lo, hi = -1.0, 1.0
        for _ in range(30):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if R.luma(R.gain(P, m)) < a.target else (lo, m)
        B = R.gain(P, (lo + hi) / 2)
        flat = apply_cube(B, cube, n, a.mix)
        bg = apply_cube(R.gain(B, a.bg_stops), cube, n, a.bg_mix)
        sj = apply_cube(R.gain(B, a.subj_stops), cube, n, a.subj_mix)
        dep = M * sj + (1 - M) * bg
        rows.append((s, flat, dep, np.repeat(M, 3, -1), f))
        print(s, "focus", round(f, 3), "subject share", round(float(M.mean()), 2), "flat luma", round(R.luma(flat), 3), "depth luma", round(R.luma(dep), 3))
    font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 22, index=1)
    cols = ["roti look 50 %, even", "+ depth: background deeper, subject lifted", "depth matte (white = subject)"]
    S = Image.new("RGB", (3 * (tw + 6) + 6, 40 + len(rows) * (th + 6)), (16, 16, 16)); dr = ImageDraw.Draw(S)
    for j, c in enumerate(cols): dr.text((6 + j * (tw + 6), 8), c, font=font, fill=(255, 210, 120))
    for i, (s, *ims, f) in enumerate(rows):
        for j, im in enumerate(ims):
            S.paste(Image.fromarray(np.clip(im * 255, 0, 255).astype(np.uint8)), (6 + j * (tw + 6), 40 + i * (th + 6)))
        dr.text((12, 46 + i * (th + 6)), s, font=font, fill=(255, 255, 255))
    S.save(a.o); print("sheet", a.o)


if __name__ == "__main__":
    main()
