#!/usr/bin/env python3
"""Track Durga's eyes in every source frame a shot uses (incl. dissolve handles), for eye-lock stabilisation.

Round 1b note "the videos are unstable": the 3.3x eye-line crops magnify handheld shake ~3x (shake_report on the v1
previz: 10-23 px RMS on holds). Instead of Warp (unscriptable analysis), the crop follows the eyes: a normalised
cross-correlation (FFT) of an eyes+brow template from the shot's middle frame, searched around the previous position,
sub-pixel peak. Output: eye centre per timeline frame as a fraction of the upright source frame.

Usage: python tools/track_eyes.py analysis/edl_v1.json analysis/transitions_v2.json analysis/eye_tracks_v2.json [--only 4,8]
"""
import json, sys, subprocess, math, argparse
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve

FPS = 25
REEL = Path(__file__).resolve().parents[1]

def tl_frame(t):
    x = t * FPS; f = math.floor(x); return f if x - f <= 0.5 else f + 1

def handles(trans, f_in, f_out):
    hin = hout = 0
    for c in trans["cuts"]:
        if c["type"] == "dissolve":
            if c["frame"] == f_in: hin = c["L"] // 2
            if c["frame"] == f_out: hout = c["L"] // 2
        elif c["type"] in ("dexp", "xfade") and c["frame"] == f_in: hin = c["L"]   # round 4c end-aligned fade
    return hin, hout

def gray_frames(src, t0, n, rot, w, h):
    vf = f"scale={w}:{h}:in_range=tv:out_range=pc" + (",hflip,vflip" if rot else "") + ",format=gray"
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(t0,0):.4f}", "-i", src, "-frames:v", str(n), "-vf", vf,
                        "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, np.uint8).astype(np.float32) / 255
    return a[: (a.size // (w * h)) * w * h].reshape(-1, h, w)

def ncc(img, tpl):
    th, tw = tpl.shape; t = tpl - tpl.mean(); tn = np.sqrt((t ** 2).sum()) + 1e-6
    num = fftconvolve(img, t[::-1, ::-1], mode="valid")
    ones = np.ones_like(tpl)
    s1 = fftconvolve(img, ones, mode="valid"); s2 = fftconvolve(img ** 2, ones, mode="valid")
    var = np.clip(s2 - s1 ** 2 / tpl.size, 1e-6, None)
    return num / (np.sqrt(var) * tn)

def subpix(r, y, x):
    def p(a, b, c):
        d = a - 2 * b + c; return 0.0 if abs(d) < 1e-9 else 0.5 * (a - c) / d
    dy = p(r[y - 1, x], r[y, x], r[y + 1, x]) if 0 < y < r.shape[0] - 1 else 0
    dx = p(r[y, x - 1], r[y, x], r[y, x + 1]) if 0 < x < r.shape[1] - 1 else 0
    return y + dy, x + dx

def track(F, ref_k, cx, cy, tw, th, search):
    """F: frames (n,h,w); template centred (cx,cy) px in frame ref_k; returns (x,y,score) per frame (template centre)."""
    n, h, w = F.shape
    tpl = F[ref_k, int(cy - th / 2):int(cy + th / 2), int(cx - tw / 2):int(cx + tw / 2)]
    out = [None] * n
    for order in (range(ref_k, n), range(ref_k - 1, -1, -1)):
        px, py = cx, cy
        for k in order:
            x0 = int(max(px - tw / 2 - search, 0)); x1 = int(min(px + tw / 2 + search, w))
            y0 = int(max(py - th / 2 - search, 0)); y1 = int(min(py + th / 2 + search, h))
            r = ncc(F[k, y0:y1, x0:x1], tpl)
            yy, xx = np.unravel_index(np.argmax(r), r.shape); yy, xx = subpix(r, yy, xx)
            px, py = x0 + xx + tpl.shape[1] / 2, y0 + yy + tpl.shape[0] / 2
            out[k] = (px, py, float(r.max()))
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("edl"); ap.add_argument("trans"); ap.add_argument("out"); ap.add_argument("--only", default="")
    a = ap.parse_args(); edl = json.loads(Path(a.edl).read_text()); trans = json.loads(Path(a.trans).read_text())
    rows = {f"{r['shoot']}:{r['clip_id'].split('_')[-1]}": r for r in json.loads((REEL / "analysis/survey/eyes_candidates.json").read_text())}
    only = {int(x) for x in a.only.split(",") if x}
    res = json.loads(Path(a.out).read_text()) if Path(a.out).exists() else {}
    for s in edl["shots"]:
        n = s["n"]
        if (only and n not in only) or trans["eyelock"][str(n)] in ("none", "plain", "fixed"): continue
        if "src" in s:
            src = str(REEL / s["src"]); rot = bool(s.get("rot")); sfps = float(s["fps"]); big = s.get("res") == "4k"
        else:
            r = rows[s["key"]]; src = str(REEL / "raw" / "b-roll" / Path(r["source"]).name); rot = "UPSIDE" in r["orientation"]
            sfps = float(r["fps"]); big = "3840" in r["resolution_display"]
        W, H = (2160, 3840) if big else (1080, 1920); aw, ah = (1080, 1920)          # analysis at 1080x1920
        last_n = max(x["n"] for x in edl["shots"])
        f_in = tl_frame(s["seq_in"]); f_out = 549 if n == last_n else tl_frame(s["seq_out"])
        hin, hout = handles(trans, f_in, f_out); N = f_out - f_in + hin + hout
        t0 = s["src_in"] - hin / sfps
        F = gray_frames(src, t0, N, rot, aw, ah)
        if len(F) < N: print(f"row {n}: only {len(F)} of {N} frames"); N = len(F)
        if "play_until" in s:   # e.g. C076: only the sharp stretch plays, the rest holds its last frame
            N = min(N, int(round((s["play_until"] - t0) * sfps)) + 1); F = F[:N]
        if s["key"] == "Oct17:C168" and trans["eyelock"][str(n)] == "smooth":   # sweep: template from its last frame (the freeze frame's neighbour), face lands at (ex,ey)
            ref_k = N - 1
        else:
            ref_k = hin + (f_out - f_in) // 2
        cw = s["cw"]; tw = int(cw * aw * 0.70); th = int(cw * aw * 0.26)
        if "tpl" in s: tw, th = int(s["tpl"][0] * aw), int(s["tpl"][1] * aw)   # round 4: small face in a wide crop (C048) needs a tight template
        ex, ey = s["ex"], s["ey"]
        if "eye_ref" in s:      # v1c: template centred on the measured pupils, at the frame nearest the measuring time
            ex, ey = s["eye_ref"][0], s["eye_ref"][1]
            kr = int(round((s["eye_ref"][2] - t0) * sfps)); pre = max(0, -kr); post = max(0, kr - (N - 1))
            if pre or post:   # review v2 #1 (C208 55 px low): eye_ref outside this window -> track from the measured frame, then slice
                F = gray_frames(src, t0 - pre / sfps, N + pre + post, rot, aw, ah)
            ref_k = kr + pre
        if "track" in s and "eye_ref" not in s:   # planned crop-follow: the eye position at the reference frame
            fr = (ref_k - hin) / max(f_out - f_in - 1, 1); tr = s["track"]
            for p, q in zip(tr, tr[1:]):
                if p[0] <= fr <= q[0]:
                    u = (fr - p[0]) / max(q[0] - p[0], 1e-6); ex, ey = p[1] + (q[1] - p[1]) * u, p[2] + (q[2] - p[2]) * u
        cx, cy = ex * aw, ey * ah
        search = int(aw * (0.10 if n != 10 else 0.22))
        tr = track(F, ref_k, cx, cy, tw, th, search)
        if "eye_ref" in s and (pre or post): tr = tr[pre:pre + N]; ref_k -= pre
        xs = np.array([p[0] for p in tr]) / aw; ys = np.array([p[1] for p in tr]) / ah; sc = np.array([p[2] for p in tr])
        res[str(n)] = {"key": s["key"], "f_in": f_in, "f_out": f_out, "hin": hin, "hout": hout, "src_t0": round(t0, 4), "src_fps": sfps,
                       "ref_k": ref_k, "ex": xs.round(5).tolist(), "ey": ys.round(5).tolist(), "score": sc.round(3).tolist()}
        jit = np.hypot(np.diff(xs) * 1080 / cw, np.diff(ys) * 1920 / cw)   # frame-to-frame eye motion in OUTPUT px before lock
        print(f"row {n:>2} {s['key']}: {N} fr (h {hin}/{hout}), score min {sc.min():.2f} med {np.median(sc):.2f}, "
              f"eye drift x {np.ptp(xs)*1080/cw:.0f}px y {np.ptp(ys)*1920/cw:.0f}px (output), step p95 {np.percentile(jit,95):.1f}px", flush=True)
        Path(a.out).write_text(json.dumps(res))

if __name__ == "__main__":
    main()
