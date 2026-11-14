#!/usr/bin/env python3
"""Tracked phone-screen mask for C088 (puja-night-2 v4c; workaround, see CR-20261018-puja-night-2-motion-ai).

Why: v4b's static soft mask (PNG + 12-frame dissolve) left the two lit screens visible for ~1.5 s, and a
soft blob over the second phone punched a hole into the Ganesh figure. This tool:
  1. decodes the C088 source range at 50 % (1080x1920 portrait = the reel frame at scale 50);
  2. estimates the camera pan (phase correlation on the backdrop);
  3. tracks each seeded phone screen (cool-white pixels against the warm tungsten scene) with the pan as
     prediction and the detection as a smoothed offset;
  4. renders a 1080x1920 ProRes 4444 alpha overlay in reel space (C088's Motion: scale 53 -> 50 linear
     over the clip, centred):
       - "black" phones (big screens in front of the crowd): convex hull of the lit glass inside the tracked
         box (+3 px), black, alpha 0.97 -> phones held up with the screen off; a box-shaped mask darkened
         the backdrop next to the phones (v4c first pass);
       - "dark" phones (tiny screens against the lit stage): tracked like "fill", rendered black
         -> phone silhouettes (v4c choice: the inpaint read as a soft smudge on the stage);
       - "fill" phones: harmonic inpaint from the surround, un-graded source colours (the V2 clip
         then needs C088's Lumetri to match V1); not used in v4c;
     alpha ramps with the C083 -> C088 cross dissolve (a = mask * min(1, 1.6 * w)).

Usage:
  .venv/bin/python projects/puja-night-2/tools/phone_mask_tracked.py            # v4c placement
  .venv/bin/python projects/puja-night-2/tools/phone_mask_tracked.py --t0 47.80 --cut 48.04 --end 50.52 \
      --src-at-cut 5.00 --scale 53 51.5 --dissolve 47.80 47.84 -o renders/overlays/c088_phone_mask_v5   # v5 (hard cut)
Writes renders/overlays/c088_phone_mask_tracked.mov, _compare.jpg and _tracks.json.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

REEL = Path(__file__).resolve().parents[1]
SRC = REEL / "raw/b-roll/A001_10152027_C088.mov"
OUT = REEL / "renders/overlays/c088_phone_mask_tracked"
W, H, FPS = 1080, 1920, 25
T_REEL0, T_CUT, T_END = 50.28, 50.52, 55.60      # overlay start (dissolve start), C088 cut, reel end
SRC_AT_CUT = 5.00                                 # C088 source time at the cut
DISSOLVE = (50.28, 50.76)
SCALE = (53.0, 50.0)
OPACITY, HULL_GROW = 1.00, 3                     # black-phone opacity; hull dilation (px, source-50 %)
BOX_SHAPED = {"A"}                                # phones masked with their tracked box instead of the hull                              # Motion scale keyframes at the cut and at T_END
ROI = (30, 1180, 320, 1460)                       # x0, y0, x1, y1 in source-50 % space
SEEDS = {  # box at frame 0 (source-50 % px), kind, association gate
    "A": ([108, 1256, 154, 1336], "black", 24),
    "B": ([184, 1236, 211, 1280], "black", 16),
    "C": ([230, 1284, 243, 1311], "dark", 9),
    # "D" ([254, 1280, 266, 1293]) dropped in v4c: a highlight at Ganesh's foot, not clearly a phone;
    # masking it left a dark blob on the stage.
}


def scale_at(t: float) -> float:
    if t <= T_CUT:
        return SCALE[0]
    return SCALE[0] + (SCALE[1] - SCALE[0]) * min(1.0, (t - T_CUT) / (T_END - T_CUT))


def to_reel(img: np.ndarray, t: float, resample=Image.BILINEAR) -> np.ndarray:
    """Source-50 % image -> reel frame (scale about the centre, crop 1080x1920)."""
    s = scale_at(t) / 50.0
    w, h = round(W * s), round(H * s)
    r = np.asarray(Image.fromarray(img).resize((w, h), resample))
    x0, y0 = (w - W) // 2, (h - H) // 2
    return r[y0:y0 + H, x0:x0 + W]


def pan(g: np.ndarray) -> np.ndarray:
    win = np.outer(np.hanning(850), np.hanning(800)).astype(np.float32)
    cum, out = np.zeros(2), [np.zeros(2)]
    for i in range(1, len(g)):
        F = np.fft.fft2(g[i - 1, 300:1150, 100:900] * win)
        G = np.fft.fft2(g[i, 300:1150, 100:900] * win)
        R = F.conj() * G
        r = np.abs(np.fft.ifft2(R / (np.abs(R) + 1e-9)))
        y, x = np.unravel_index(r.argmax(), r.shape)
        cum = cum + (x if x < r.shape[1] / 2 else x - r.shape[1], y if y < r.shape[0] / 2 else y - r.shape[0])
        out.append(cum.copy())
    return np.array(out)


def components(f: np.ndarray) -> list[list[int]]:
    f = f.astype(np.float32)
    R, G, B = f[..., 0], f[..., 1], f[..., 2]
    m = ((0.299 * R + 0.587 * G + 0.114 * B) > 55) & (B > 0.80 * R)
    roi = np.zeros_like(m)
    roi[ROI[1]:ROI[3], ROI[0]:ROI[2]] = True
    lab, _ = ndi.label(m & roi)
    out = []
    for k, sl in enumerate(ndi.find_objects(lab), 1):
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        if (lab[sl] == k).sum() >= 20 and (y1 - y0) <= 3.2 * (x1 - x0):
            out.append([x0, y0, x1, y1])
    return out


def track(frames: np.ndarray, sh: np.ndarray) -> dict[str, list]:
    n = len(frames)
    comps = [components(f) for f in frames]
    boxes = {}
    for k, (b0, kind, gate) in SEEDS.items():
        c0 = np.array([(b0[0] + b0[2]) / 2, (b0[1] + b0[3]) / 2])
        off, dets = np.full((n, 2), np.nan), [None] * n
        prev = None   # big screens are found every frame: follow the last detection, not the pan estimate
        for i in range(n):
            if kind == "black" and prev is not None:
                p = np.array([(prev[0] + prev[2]) / 2, (prev[1] + prev[3]) / 2])
            else:
                p = c0 + sh[i] + (np.nan_to_num(off[i - 1]) if i else 0)
            sel = [c for c in comps[i] if abs((c[0] + c[2]) / 2 - p[0]) < gate and abs((c[1] + c[3]) / 2 - p[1]) < gate]
            if not sel:
                continue
            if kind != "black":
                sel = [min(sel, key=lambda c: abs((c[0] + c[2]) / 2 - p[0]) + abs((c[1] + c[3]) / 2 - p[1]))]
            else:   # the largest blob, plus pieces inside the screen's own footprint
                big = max(sel, key=lambda c: (c[2] - c[0]) * (c[3] - c[1]))
                sel = [c for c in sel if c is big or (c[0] >= big[0] - 6 and c[2] <= big[2] + 6 and c[1] >= big[1] - 30 and c[3] <= big[3] + 10)]
            bx = [min(c[0] for c in sel), min(c[1] for c in sel), max(c[2] for c in sel), max(c[3] for c in sel)]
            dets[i] = bx
            prev = bx
            if k == "A":   # the big screen's top is dark camera UI: track its right/bottom edges
                off[i] = [bx[2] - b0[2] - sh[i][0], bx[3] - b0[3] - sh[i][1]]
            else:
                off[i] = [(bx[0] + bx[2]) / 2 - c0[0] - sh[i][0], (bx[1] + bx[3]) / 2 - c0[1] - sh[i][1]]
        good, idx = ~np.isnan(off[:, 0]), np.arange(n)
        last = int(idx[good].max())
        for d in (0, 1):
            off[:, d] = ndi.gaussian_filter1d(ndi.median_filter(np.interp(idx, idx[good], off[good, d]), 7), 1.5)
        w, h = b0[2] - b0[0], b0[3] - b0[1]
        seq = []
        for i in range(n):
            if i > last + 3:
                seq.append(None)
                continue
            cx = (b0[0] + b0[2]) / 2 + sh[i][0] + off[i][0]
            cy = (b0[1] + b0[3]) / 2 + sh[i][1] + off[i][1]
            bb = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
            if dets[i] and kind == "black":
                bb = [min(bb[0], dets[i][0]), min(bb[1], dets[i][1]), max(bb[2], dets[i][2]), max(bb[3], dets[i][3])]
            seq.append([round(float(v), 1) for v in bb])
        boxes[k] = seq
    return boxes


def screen_hulls(frames: np.ndarray, boxes: list) -> list:
    """Per frame: convex hull (source-50 % px) of the lit-screen pixels inside the tracked box.
    Frames without enough screen pixels reuse the last hull, moved with the box."""
    from scipy.spatial import ConvexHull
    out, last, last_c = [], None, None
    for f, b in zip(frames, boxes):
        if not b:
            out.append(None)
            continue
        x0, y0, x1, y1 = int(b[0]) - 4, int(b[1]) - 4, int(b[2]) + 5, int(b[3]) + 5
        c = f[y0:y1, x0:x1].astype(np.float32)
        R, G, B = c[..., 0], c[..., 1], c[..., 2]
        m = ((0.299 * R + 0.587 * G + 0.114 * B) > 55) & (B > 0.80 * R)
        lab, nl = ndi.label(m)   # the glass is the largest blob; specks of backdrop in the box are not
        if nl > 1:
            m = lab == (1 + int(np.argmax(ndi.sum(m, lab, range(1, nl + 1)))))
        ys, xs = np.nonzero(m)
        bc = np.array([(b[0] + b[2]) / 2, (b[1] + b[3]) / 2])
        if len(xs) >= 15 and np.ptp(xs) > 2 and np.ptp(ys) > 2:
            pts = np.c_[xs + x0, ys + y0].astype(float)
            pts = np.vstack([pts, pts + [1, 0], pts + [0, 1], pts + [1, 1]])
            poly = pts[ConvexHull(pts).vertices]
            last, last_c = poly, bc
        elif last is not None:
            poly = last + (bc - last_c)
        else:
            poly = None
        out.append(None if poly is None else [[round(float(u), 1), round(float(v), 1)] for u, v in poly])
    return out


def inpaint(img: np.ndarray, hole: np.ndarray, iters: int = 400) -> np.ndarray:
    """Harmonic fill of `hole` (bool) from its surround, on a crop around the hole."""
    ys, xs = np.where(hole)
    if not len(ys):
        return img
    y0, y1, x0, x1 = max(ys.min() - 12, 0), min(ys.max() + 13, H), max(xs.min() - 12, 0), min(xs.max() + 13, W)
    c = img[y0:y1, x0:x1].astype(np.float32).copy()
    m = hole[y0:y1, x0:x1]
    ring = ndi.binary_dilation(m, iterations=3) & ~m
    c[m] = c[ring].mean(0)
    k = np.array([[0, .25, 0], [.25, 0, .25], [0, .25, 0]], np.float32)
    for _ in range(iters):
        for ch in range(3):
            c[..., ch][m] = ndi.convolve(c[..., ch], k, mode="nearest")[m]
    out = img.astype(np.float32).copy()
    out[y0:y1, x0:x1] = c
    return out


def main() -> None:
    import argparse
    global T_REEL0, T_CUT, T_END, SRC_AT_CUT, DISSOLVE, SCALE, OUT
    ap = argparse.ArgumentParser(description="defaults = v4c placement (C088 at 50.52, dissolve from 50.28)")
    ap.add_argument("--t0", type=float, help="overlay start in reel time (source decode starts here; seeds are for source 4.76)")
    ap.add_argument("--cut", type=float, help="C088's first frame in reel time")
    ap.add_argument("--end", type=float)
    ap.add_argument("--src-at-cut", type=float)
    ap.add_argument("--scale", type=float, nargs=2, help="Motion scale at the cut and at the end")
    ap.add_argument("--dissolve", type=float, nargs=2, help="alpha ramp window (reel time)")
    ap.add_argument("-o", "--out", type=Path, help="output path without extension")
    a = ap.parse_args()
    T_REEL0 = a.t0 if a.t0 is not None else T_REEL0
    T_CUT = a.cut if a.cut is not None else T_CUT
    T_END = a.end if a.end is not None else T_END
    SRC_AT_CUT = a.src_at_cut if a.src_at_cut is not None else SRC_AT_CUT
    SCALE = tuple(a.scale) if a.scale else SCALE
    DISSOLVE = tuple(a.dissolve) if a.dissolve else DISSOLVE
    OUT = a.out if a.out else OUT
    n = round((T_END - T_REEL0) * FPS) + 1
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{SRC_AT_CUT - (T_CUT - T_REEL0):.3f}", "-i", str(SRC),
                          "-frames:v", str(n), "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    n = len(frames)
    sh = pan((frames[..., 0] * 0.299 + frames[..., 1] * 0.587 + frames[..., 2] * 0.114).astype(np.float32))
    boxes = track(frames, sh)
    hulls = {k: screen_hulls(frames, boxes[k]) for k, (_, kind, _) in SEEDS.items() if kind in ("black", "dark")}
    json.dump({"pan": sh.tolist(), "boxes": boxes, "hulls": hulls}, open(OUT.with_name(OUT.name + "_tracks.json"), "w"))

    tmp = OUT.parent / "_c088_mask_frames"
    tmp.mkdir(parents=True, exist_ok=True)
    checks = []
    for i in range(n):
        t = T_REEL0 + i / FPS
        mb, mf = Image.new("L", (W, H), 0), Image.new("L", (W, H), 0)
        for k, (_, kind, _) in SEEDS.items():
            b = boxes[k][i]
            if not b:
                continue
            if k in BOX_SHAPED:   # in front of the dark crowd: a box can't spill onto anything bright
                ImageDraw.Draw(mb).rounded_rectangle((b[0] - 3, b[1] - 3, b[2] + 3, b[3] + 3), radius=4, fill=255)
            elif kind in ("black", "dark"):   # next to the backdrop/stage: hug the lit glass (convex hull)
                poly = hulls[k][i]
                if poly:
                    ImageDraw.Draw(mb).polygon([tuple(q) for q in poly], fill=255)
            else:
                ImageDraw.Draw(mf).rounded_rectangle((b[0] - 4, b[1] - 4, b[2] + 4, b[3] + 4), radius=4, fill=255)
        mb = Image.fromarray((ndi.binary_dilation(np.asarray(mb) > 0, iterations=HULL_GROW) * 255).astype(np.uint8))
        reel_rgb = to_reel(frames[i], t).astype(np.float32)
        a_black = ndi.gaussian_filter(to_reel(np.asarray(mb), t).astype(np.float32) / 255, 1.2) * OPACITY
        fill_hard = to_reel(np.asarray(mf), t) > 127
        a_fill = ndi.gaussian_filter(fill_hard.astype(np.float32), 1.5)
        rgb = inpaint(reel_rgb, ndi.binary_dilation(fill_hard, iterations=2))
        rgb = rgb * (1 - (a_black > 0.01)[..., None])           # black under the black-phone alpha
        w = min(1.0, max(0.0, (t - DISSOLVE[0]) / (DISSOLVE[1] - DISSOLVE[0])))
        alpha = np.clip(np.maximum(a_black, a_fill), 0, 1) * min(1.0, 1.6 * w if t < DISSOLVE[1] else 1.0)
        rgba = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
        Image.fromarray(rgba, "RGBA").save(tmp / f"f{i:04d}.png")
        if i in (0, 8, 16, 30, 50, 70, 95, 120, n - 1):
            comp = reel_rgb * (1 - alpha[..., None]) + rgb * alpha[..., None]
            checks.append(Image.fromarray(np.clip(comp * 1.6, 0, 255).astype(np.uint8)).crop((30, 1180, 330, 1420)))
    mov = OUT.with_suffix(".mov")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(tmp / "f%04d.png"),
                    "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-alpha_bits", "16",
                    str(mov)], check=True)
    sheet = Image.new("RGB", (300 * len(checks), 240))
    for k, im in enumerate(checks):
        sheet.paste(im, (k * 300, 0))
    sheet.save(OUT.with_name(OUT.name + "_compare.jpg"), quality=90)
    for p in tmp.glob("f*.png"):
        p.unlink()
    tmp.rmdir()
    print(f"✓ {mov}  ({n} frames from reel {T_REEL0:.2f})")


if __name__ == "__main__":
    main()
