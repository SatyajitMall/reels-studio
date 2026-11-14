"""Reference-match look (reel-local): a 3D .cube LUT that moves our footage's tones and colour toward the reference's
(effects-playbook §A3 "Match Reference": measure the reference, mirror its exposure / contrast / warmth).

Method: per-channel quantile matching (our pooled shots → the reference's picture inside its 4:3 window, black bars and
the end card excluded), smoothed and made monotonic, plus a saturation factor from the two pools' mean saturation.
The LUT is written at full strength; Premiere's Creative Intensity (or --mix here) blends it toward camera-true.
In Premiere a custom .cube is loaded by hand (Lumetri → Creative → Look → Browse), so it is one manual step.

Also writes a stats table (reference vs ours, by tone band) and a preview sheet: camera-true | ref-match 50 % |
ref-match 100 % on the given stills.

Usage (studio root):
  .venv/bin/python -I projects/could-not-go-home-diwali/tools/ref_match_lut.py --ref projects/could-not-go-home-diwali/references/ref_city_still_buzzed.mp4 \
      --ours <still.png> ... -o projects/could-not-go-home-diwali/analysis/look_ref
"""
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter1d

LUMA = np.array([0.2126, 0.7152, 0.0722])


def ref_frames(path, n=24, t_end=20.2):
    out = []
    for t in np.linspace(0.3, t_end, n):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(path), "-frames:v", "1",
                              "-vf", "crop=700:530:10:367", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        if len(raw) == 700 * 530 * 3:
            out.append(np.frombuffer(raw, np.uint8).reshape(530, 700, 3).astype(np.float64) / 255)
    return out


def load(p, w=960):
    im = Image.open(p).convert("RGB")
    im = im.resize((w, int(im.height * w / im.width)))
    return np.asarray(im).astype(np.float64) / 255


def sat(x):
    mx, mn = x.max(-1), x.min(-1)
    return np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)


def bands(imgs):
    px = np.concatenate([i.reshape(-1, 3) for i in imgs])
    l = px @ LUMA
    rows = {}
    for name, lo, hi in (("shadows", 0.0, 0.2), ("mids", 0.2, 0.6), ("highs", 0.6, 1.01)):
        m = (l >= lo) & (l < hi)
        p = px[m]
        rows[name] = {"share": float(m.mean()), "R-B": float((p[:, 0] - p[:, 2]).mean()), "G-M": float((p[:, 1] - (p[:, 0] + p[:, 2]) / 2).mean()),
                      "sat": float(sat(p[None])[0].mean())}
    rows["all"] = {"luma": float(l.mean()), "p02": float(np.percentile(l, 2)), "p98": float(np.percentile(l, 98)),
                   "sat": float(sat(px[None])[0].mean())}
    return rows, px


def curves(src_px, ref_px, q=257):
    qs = np.linspace(0, 1, q)
    cs = []
    for c in range(3):
        s = np.quantile(src_px[:, c], qs)
        r = np.quantile(ref_px[:, c], qs)
        x = np.linspace(0, 1, 256)
        y = np.interp(x, s, r)                    # value in ours → value at the same quantile in the reference
        y = gaussian_filter1d(y, 6, mode="nearest")
        y = np.maximum.accumulate(y)              # monotonic
        cs.append(y)
    return np.stack(cs)                           # 3 × 256


def apply(img, cs, satk, mix=1.0):
    idx = np.clip((img * 255).round().astype(int), 0, 255)
    out = np.stack([cs[c][idx[..., c]] for c in range(3)], -1)
    l = (out @ LUMA)[..., None]
    out = np.clip(l + (out - l) * satk, 0, 1)
    return img + (out - img) * mix


def write_cube(path, cs, satk, n=33):
    g = np.linspace(0, 1, n)
    lines = [f'TITLE "could-not-go-home-diwali ref match"', f"LUT_3D_SIZE {n}", "DOMAIN_MIN 0.0 0.0 0.0", "DOMAIN_MAX 1.0 1.0 1.0"]
    for b in g:          # .cube order: R fastest, then G, then B
        for gg in g:
            for r in g:
                v = apply(np.array([[[r, gg, b]]]), cs, satk)[0, 0]
                lines.append(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}")
    Path(path).write_text("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True); ap.add_argument("--ours", nargs="+", required=True)
    ap.add_argument("--sheet", nargs="*", help="stills for the preview sheet (default: --ours)")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    R = ref_frames(a.ref)
    O = [load(p) for p in a.ours]
    rstat, rpx = bands(R)
    ostat, opx = bands(O)
    cs = curves(opx, rpx)
    mid, _ = bands([apply(i, cs, 1.0) for i in O])          # the curves already move saturation; correct what's left
    satk = float(np.clip(rstat["all"]["sat"] / max(mid["all"]["sat"], 1e-6), 0.6, 1.3))
    write_cube(out / "ref_match.cube", cs, satk)
    after, _ = bands([apply(i, cs, satk) for i in O])
    (out / "stats.json").write_text(json.dumps({"reference": rstat, "ours": ostat, "ours_after_lut": after, "sat_factor": satk}, indent=1))
    md = ["| Band | Measure | Reference | Ours (camera-true) | Ours + ref-match 100 % |", "|---|---|---|---|---|"]
    for b in ("shadows", "mids", "highs"):
        for k in ("share", "R-B", "G-M", "sat"):
            md.append(f"| {b} | {k} | {rstat[b][k]:+.3f} | {ostat[b][k]:+.3f} | {after[b][k]:+.3f} |")
    for k in ("luma", "p02", "p98", "sat"):
        md.append(f"| all | {k} | {rstat['all'][k]:.3f} | {ostat['all'][k]:.3f} | {after['all'][k]:.3f} |")
    (out / "STATS.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))
    # sheet
    stills = a.sheet or a.ours
    tw = 520
    f = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 22, index=1)
    cols = [("camera-true", 0.0), ("ref-match 50 %", 0.5), ("ref-match 100 %", 1.0)]
    tiles = []
    for p in stills:
        img = load(p, tw)
        tiles.append([np.clip(apply(img, cs, satk, m) * 255, 0, 255).astype(np.uint8) for _, m in cols])
    th = tiles[0][0].shape[0]
    S = Image.new("RGB", (len(cols) * (tw + 6) + 6, 36 + len(tiles) * (th + 6)), (20, 20, 20))
    d = ImageDraw.Draw(S)
    for j, (lab, _) in enumerate(cols):
        d.text((6 + j * (tw + 6), 6), lab, font=f, fill=(255, 210, 120))
    for i, row in enumerate(tiles):
        for j, t in enumerate(row):
            im = Image.fromarray(t)
            if im.size[1] != th:
                im = im.resize((tw, th))
            S.paste(im, (6 + j * (tw + 6), 36 + i * (th + 6)))
    S.save(out / "ref_match_sheet.jpg", quality=88)
    print("sat factor", round(satk, 3), "→", out / "ref_match.cube")


if __name__ == "__main__":
    main()
