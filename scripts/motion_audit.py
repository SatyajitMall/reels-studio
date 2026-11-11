#!/usr/bin/env python3
"""Motion audit (v0.10.2): camera shake, jerk, jumps and step-print holds per shot, on the export. Run by pregate.py.

Promoted from projects/could-not-go-home-diwali/tools/motion_audit.py (CR-20261110-could-not-go-home-diwali-gate-missed-glitch):
the gate passed a step-print whose every held image jumped 6–21 px, because nothing measured motion against a limit.

Per shot (cuts ±2 frames ignored), inside the picture window (--window, default the whole frame), at 360 px wide:
  camera   frame-to-frame shift of the frame's OUTER RING (four edge bands, median of their phase correlations).
           The edges are usually background or the vehicle's interior, so this is the camera moving, not a subject
           (Diwali S1: the hands moved 28 px, the camera didn't). Limits apply to this series.
  subject  the same shift on the whole window, for information.
  jitter   the camera path minus its smooth path (gaussian, 6 frames); jerk = frame-to-frame change of that jitter.
  jumps    steps far off the local motion trend.
In a step-print span (--step-print T0-T1): the held images are found (frame difference ≈ 0 inside a hold), and the
camera shift from one held image to the next, minus the smooth path through the holds, is the HOLD SHIFT. A steady
source keeps it near 0; a handheld one turns every bump into a visible jump.

Limits (1080-wide px; --limits to change):
  hold shift > 4 px in a step-print            FAIL    (step-print from a locked-off or well-stabilised shot only)
  camera jerk p95 > 6, or a jump off trend > 8   REVIEW  (the reviewer must judge it on a full-rate strip; the
                                                          editor can't waive it)
Writes -o motion.json and prints one line per shot. Exit 1 when any FAIL.

Usage:
  ./.venv/bin/python scripts/motion_audit.py <export> --shots shots.json -o motion.json [--window 0,505,1080,810]
      [--step-print 0-1.56 17.4-18.96] [--fps 25] [--limits hold=4,jerk=6,jump=8]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter1d, median_filter

AW = 360            # analysis width
EDGE = 2            # frames ignored next to each cut
RING = 0.18         # edge-band width, as a fraction of each side


def frames(path: Path, win: tuple[int, int, int, int] | None, fps: float) -> tuple[np.ndarray, float]:
    vf = (f"crop={win[2]}:{win[3]}:{win[0]}:{win[1]}," if win else "") + f"fps={fps:g}"
    probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                       "-of", "json", str(path)], capture_output=True, text=True).stdout)["streams"][0]
    ww, hh = (win[2], win[3]) if win else (probe["width"], probe["height"])
    ah = int(round(AW * hh / ww / 2)) * 2
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", vf + f",scale={AW}:{ah}:flags=area,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8)
    return a[: a.size // (AW * ah) * AW * ah].reshape(-1, ah, AW).astype(np.float32), ww / AW


def phase(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    hh, ww = a.shape
    win = np.outer(np.hanning(hh), np.hanning(ww)).astype(np.float32)
    A = np.fft.fft2((a - a.mean()) * win); B = np.fft.fft2((b - b.mean()) * win)
    R = A * np.conj(B); R /= np.abs(R) + 1e-6
    c = np.fft.ifft2(R).real
    y, x = np.unravel_index(c.argmax(), c.shape)

    def sub(cm, c0, cp):
        d = cm - 2 * c0 + cp
        return 0.0 if d == 0 else 0.5 * (cm - cp) / d
    yy = y + sub(c[(y - 1) % hh, x], c[y, x], c[(y + 1) % hh, x])
    xx = x + sub(c[y, (x - 1) % ww], c[y, x], c[y, (x + 1) % ww])
    return (xx - ww if xx > ww / 2 else xx), (yy - hh if yy > hh / 2 else yy)


def ring_shift(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    """Median shift of the four edge bands: the camera, not a subject in the middle."""
    hh, ww = a.shape
    bh, bw = max(int(hh * RING), 16), max(int(ww * RING), 16)
    bands = [(slice(0, bh), slice(None)), (slice(hh - bh, hh), slice(None)), (slice(None), slice(0, bw)), (slice(None), slice(ww - bw, ww))]
    s = np.array([phase(a[r, c], b[r, c]) for r, c in bands])
    return float(np.median(s[:, 0])), float(np.median(s[:, 1]))


def path_stats(dx: np.ndarray, dy: np.ndarray, t0: float, fps: float, jump_px: float) -> dict:
    tx, ty = np.cumsum(dx), np.cumsum(dy)
    jx, jy = tx - gaussian_filter1d(tx, 6), ty - gaussian_filter1d(ty, 6)
    jit = np.hypot(jx, jy)
    res = np.hypot(dx - gaussian_filter1d(dx, 3), dy - gaussian_filter1d(dy, 3))
    jumps = [{"t": round(t0 + (i + 1) / fps, 2), "off_trend_px": round(float(res[i]), 1)} for i in range(len(res)) if res[i] > jump_px]
    return {"jit_rms": round(float(np.sqrt((jit ** 2).mean())), 2), "jerk_p95": round(float(np.percentile(np.hypot(np.diff(jx), np.diff(jy)), 95)), 2)
            if len(jx) > 2 else 0.0, "pan_px_s": round(float(np.hypot(dx.mean(), dy.mean()) * fps), 1), "jumps": jumps}


def holds(fr: np.ndarray, cam: np.ndarray, t0: float, fps: float) -> dict:
    """Held images in a step-print: where the picture changes, the camera shift from one image to the next."""
    mad = np.array([np.abs(fr[i + 1] - fr[i]).mean() for i in range(len(fr) - 1)])
    if not len(mad):
        return {}
    thr = max(0.6, 0.25 * float(np.percentile(mad, 90)))
    change = np.where(mad > thr)[0]
    if len(change) < 3:
        return {"images": int(len(change)) + 1, "note": "too few held images to measure"}
    sx, sy = cam[change, 0], cam[change, 1]
    off = np.hypot(sx - gaussian_filter1d(sx, 1.0), sy - gaussian_filter1d(sy, 1.0))
    lengths = np.diff(np.concatenate([[-1], change, [len(fr) - 1]]))
    worst = int(off.argmax())
    return {"images": int(len(change)) + 1, "hold_frames_median": float(np.median(lengths)),
            "hold_shift_px_max": round(float(off.max()), 1), "hold_shift_px_median": round(float(np.median(off)), 1),
            "worst_t": round(t0 + (change[worst] + 1) / fps, 2)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", type=Path)
    ap.add_argument("--shots", type=Path, required=True, help="JSON list of [name, start_s, end_s] (pregate's shots.json)")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--window", help="x,y,w,h of the picture in the export (a 4:3 or 4:5 window); default the whole frame")
    ap.add_argument("--step-print", nargs="*", default=[], metavar="T0-T1")
    ap.add_argument("--fps", type=float, default=25.0)
    ap.add_argument("--limits", default="hold=4,jerk=6,jump=8")
    a = ap.parse_args()
    lim = {k: float(v) for k, v in (p.split("=") for p in a.limits.split(","))}
    win = tuple(int(v) for v in a.window.split(",")) if a.window else None
    fr, k = frames(a.export, win, a.fps)
    steps = [tuple(float(x) for x in s.split("-")) for s in a.step_print]
    shots = json.loads(a.shots.read_text())
    rep, fail = [], False
    for name, st, en in shots:
        i0, i1 = int(round(st * a.fps)) + EDGE, min(int(round(en * a.fps)) - EDGE, len(fr) - 1)
        seg = fr[i0:i1 + 1]
        if len(seg) < 6:
            continue
        cam = np.array([ring_shift(seg[i], seg[i + 1]) for i in range(len(seg) - 1)]) * k
        sub = np.array([phase(seg[i], seg[i + 1]) for i in range(len(seg) - 1)]) * k
        r = {"shot": name, "t": [st, en], "camera": path_stats(cam[:, 0], cam[:, 1], i0 / a.fps, a.fps, lim["jump"]),
             "subject": path_stats(sub[:, 0], sub[:, 1], i0 / a.fps, a.fps, lim["jump"])}
        sp = next(((t0, t1) for t0, t1 in steps if t0 < en - 0.05 and t1 > st + 0.05), None)
        if sp:
            r["step_print"] = holds(seg, cam, i0 / a.fps, a.fps)
            hs = r["step_print"].get("hold_shift_px_max", 0)
            r["verdict"] = "FAIL" if hs > lim["hold"] else "PASS"
            r["why"] = (f"step-print hold shift {hs} px > {lim['hold']:g} (every held image jumps: make it from a steadier shot)"
                        if hs > lim["hold"] else f"step-print hold shift {hs} px")
        else:
            c = r["camera"]
            over = [f"jerk p95 {c['jerk_p95']} > {lim['jerk']:g}"] if c["jerk_p95"] > lim["jerk"] else []
            if c["jumps"]:
                over.append(f"{len(c['jumps'])} jump(s) off trend > {lim['jump']:g} px at {', '.join(str(j['t']) for j in c['jumps'][:4])} s")
            r["verdict"] = "REVIEW" if over else "PASS"
            r["why"] = "; ".join(over) or f"camera jerk p95 {c['jerk_p95']}, jitter {c['jit_rms']} px"
        fail |= r["verdict"] == "FAIL"
        rep.append(r)
        print(f"{r['verdict']:6s} {name:26s} {r['why']}")
    a.out.write_text(json.dumps({"export": str(a.export), "window": win, "limits": lim, "shots": rep}, indent=1))
    print(f"✓ {a.out}")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
