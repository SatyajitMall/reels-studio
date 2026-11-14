#!/usr/bin/env python3
"""could-not-go-home-diwali v1b (copied from projects/kolkata/tools/fx_prerender.py): pre-render stabilised / slow-motion versions of our own 25 fps shots for the OFFLINE preview.

The director (round 5 note): "a few of my shots need stabilisation and cinematic effect; the swooping shots don't
make it good". scripts/preview_edl.py can't stabilise, and its slow-mo repeats frames. So each treated shot is
rendered here to a ProRes 422 file of exactly the shot's window, and the EDL points at it with src_in 0, rate 1.

This is an APPROXIMATION for judging the cut, like the rest of the preview:
  - stabilise: our own similarity tracker (phase correlation on 4 quadrants → shift, roll, zoom per frame), the
    camera path smoothed with a Gaussian (σ frames) or locked to its mean, then each frame warped back and
    scaled up to hide the edges. The build uses Premiere's Warp Stabilizer (skill Phase 5).
  - slow: ffmpeg minterpolate (motion-compensated). The build uses After Effects Timewarp, Pixel Motion
    (after-effects.md; Premiere Optical Flow doubled limbs on goddess v10).
Output is the camera's display orientation (rotation flag applied), at half its display size, so in the EDL the shot
keeps its rotation and position and its Scale doubles (fx_scale).

Usage (studio root):
  .venv/bin/python projects/kolkata/tools/fx_prerender.py --jobs projects/kolkata/analysis/fx_jobs_v5b.json [--only C047]
Jobs file: [{"id": "C047_dhakis", "clip": "...mov", "src_in": 32.2, "out_dur": 2.44, "rate": 0.55,
             "stab": "smooth"|"lock"|null, "sigma": 15, "zoom": 1.06,
             "interpret": false, "whip_in": 0, "whip_out": 0, "whip_dir": -1}, ...]
  speed_keys: [[t_out_s, rate], ...] a speed ramp (eased between keys), e.g. [[0, 1.0], [1.0, 1.0], [1.8, 0.45]].
  interpret: true for a 24/30 fps clip conformed to 25 (rate 25/24 or 25/30): frames are used 1:1, never resampled.
  whip_in / whip_out: frames of whip-pan smear at the head / tail (the cut's other side gets the matching one).
  out_dur = reel seconds; source used = out_dur × rate (+ margins for the tracker).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter1d

OUT = Path("projects/could-not-go-home-diwali/renders/fx_preview")
TW = 480  # tracking width


def probe(clip):
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:stream_side_data=rotation", "-of", "json", clip], capture_output=True, text=True)
    s = json.loads(p.stdout)["streams"][0]
    w, h = s["width"], s["height"]
    rot = 0
    for sd in s.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    if abs(rot) % 180 == 90:
        w, h = h, w
    return w, h


def read_frames(clip, t0, dur, w, h, native=False):
    vf = f"scale={w}:{h}:flags=bicubic" + ("" if native else ",fps=25")
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", clip, "-vf", vf,
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (w * h * 3)
    return np.frombuffer(raw[: n * w * h * 3], np.uint8).reshape(n, h, w, 3)


def pc(a, b):
    h, w = a.shape
    win = np.hanning(h)[:, None] * np.hanning(w)[None, :]
    R = np.fft.fft2(a * win) * np.conj(np.fft.fft2(b * win))
    R /= np.abs(R) + 1e-9
    r = np.fft.ifft2(R).real
    y, x = np.unravel_index(np.argmax(r), r.shape)

    def sub(c, m, n):
        p, q, s = m[(c - 1) % n], m[c], m[(c + 1) % n]
        d = p - 2 * q + s
        return c + (0.5 * (p - s) / d if d else 0)
    fx, fy = sub(x, r[y, :], w), sub(y, r[:, x], h)
    if fy > h / 2:
        fy -= h
    if fx > w / 2:
        fx -= w
    return fx, fy


def track(gray):
    """Per-frame similarity (tx, ty, log-scale, angle) from frame i to i+1, from 4 quadrant shifts."""
    n, h, w = gray.shape
    hh, hw = h // 2, w // 2
    quads = [(slice(0, hh), slice(0, hw)), (slice(0, hh), slice(hw, w)), (slice(hh, h), slice(0, hw)), (slice(hh, h), slice(hw, w))]
    centres = np.array([[-hw / 2, -hh / 2], [hw / 2, -hh / 2], [-hw / 2, hh / 2], [hw / 2, hh / 2]], float)
    out = []
    for i in range(n - 1):
        d = np.array([pc(gray[i + 1][q], gray[i][q]) for q in quads])  # shift of content from i to i+1
        # d_k = t + a*c_k + b*perp(c_k);  perp(c) = (-cy, cx); a = scale-1, b = angle
        A, y = [], []
        for (cx, cy), (dx, dy) in zip(centres, d):
            A.append([1, 0, cx, -cy]); y.append(dx)
            A.append([0, 1, cy, cx]); y.append(dy)
        sol, *_ = np.linalg.lstsq(np.array(A), np.array(y), rcond=None)
        out.append(sol)
    return np.array(out)  # tx, ty, a, b per step (tracking px)


def stabilise(frames, mode, sigma, zoom, transl_only=False):
    n, h, w, _ = frames.shape
    th = int(round(h * TW / w))
    gray = np.stack([np.asarray(Image.fromarray(f).convert("L").resize((TW, th), Image.BILINEAR), np.float32) for f in frames])
    steps = track(gray)
    k = w / TW
    path = np.vstack([[0, 0, 0, 0], np.cumsum(steps, axis=0)])  # camera content path
    path[:, :2] *= k
    if mode == "lock":
        smooth = np.tile(path.mean(axis=0), (n, 1))
    else:
        smooth = np.stack([gaussian_filter1d(path[:, j], sigma, mode="nearest") for j in range(4)], 1)
        smooth[:, 3] = path[:, 3].mean()  # level horizon: roll is never wanted on these shots
    corr = smooth - path  # move content by this to follow the smooth path
    # never move further than the zoom margin can hide (the tram street's tail move showed a black top edge)
    corr[:, 0] = np.clip(corr[:, 0], -(zoom - 1) / 2 * w * 0.9, (zoom - 1) / 2 * w * 0.9)
    corr[:, 1] = np.clip(corr[:, 1], -(zoom - 1) / 2 * h * 0.9, (zoom - 1) / 2 * h * 0.9)
    corr[:, 3] = np.clip(corr[:, 3], -0.02, 0.02)
    if transl_only:                # v1c: position only. Scale/roll corrections read as wobble ("distortion") on the phone
        corr[:, 2] = 0
        corr[:, 3] = 0
    res = []
    cx, cy = w / 2, h / 2
    for f, (tx, ty, a, b) in zip(frames, corr):
        s = (1 + a) * zoom
        ca, sa = s * np.cos(b), s * np.sin(b)
        # forward: p' = M (p - c) + c + t ; PIL wants inverse map output->input
        M = np.array([[ca, -sa], [sa, ca]])
        Mi = np.linalg.inv(M)
        off = np.array([cx, cy]) - Mi @ (np.array([cx, cy]) + np.array([tx, ty]))
        coeffs = (Mi[0, 0], Mi[0, 1], off[0], Mi[1, 0], Mi[1, 1], off[1])
        res.append(np.asarray(Image.fromarray(f).transform((w, h), Image.AFFINE, coeffs, Image.BICUBIC)))
    worst = float(np.abs(corr[:, :2]).max())
    return np.stack(res), worst


def retime(frames, slow):
    """Motion-compensated slow motion (ffmpeg minterpolate), raw RGB in and out."""
    n, h, w, _ = frames.shape
    vf = f"minterpolate=fps={25 / slow:.4f}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,setpts=PTS/{slow:.5f},fps=25"
    cmd = ["ffmpeg", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", "25", "-i", "-",
           "-vf", vf, "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, input=frames.tobytes(), capture_output=True).stdout
    m = len(raw) // (w * h * 3)
    return np.frombuffer(raw[: m * w * h * 3], np.uint8).reshape(m, h, w, 3)


def densify(frames, k):
    """k× motion-compensated in-between frames (minterpolate to 25·k fps), for speed ramps."""
    n, h, w, _ = frames.shape
    cmd = ["ffmpeg", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", "25", "-i", "-",
           "-vf", f"minterpolate=fps={25 * k}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, input=frames.tobytes(), capture_output=True).stdout
    m = len(raw) // (w * h * 3)
    return np.frombuffer(raw[: m * w * h * 3], np.uint8).reshape(m, h, w, 3)


def ramp_times(keys, n_out):
    """Camera time (s from the in-point) of each output frame for speed keys [[t_out_s, rate], ...], eased between keys."""
    ts = np.arange(n_out) / 25
    kt = np.array([k[0] for k in keys], float)
    kr = np.array([k[1] for k in keys], float)
    rates = np.empty(n_out)
    for i, t in enumerate(ts):
        j = np.searchsorted(kt, t, side="right") - 1
        if j < 0:
            rates[i] = kr[0]
        elif j >= len(kt) - 1:
            rates[i] = kr[-1]
        else:
            u = (t - kt[j]) / (kt[j + 1] - kt[j])
            u = u * u * (3 - 2 * u)
            rates[i] = kr[j] + (kr[j + 1] - kr[j]) * u
    return np.concatenate([[0], np.cumsum(rates[:-1]) / 25])


def smear(f, radius, shift):
    """Directional (horizontal) motion blur of `radius` px plus a horizontal slide: one whip-pan frame."""
    a = np.roll(f.astype(np.float32), int(shift), axis=1)
    if radius < 2:
        return a.astype(np.uint8)
    r = int(radius)
    c = np.cumsum(np.pad(a, ((0, 0), (r, r), (0, 0)), mode="edge"), axis=1)
    out = (c[:, 2 * r:] - c[:, :-2 * r]) / (2 * r)
    return np.clip(out[:, : f.shape[1]], 0, 255).astype(np.uint8)


def whip(frames, k_in, k_out, sign, pad=0):
    """Whip pan: the first k_in frames arrive with a smear easing out; the last k_out shown frames (before `pad`
    spare frames at the tail) leave with one easing in."""
    frames = frames.copy()
    w = frames.shape[2]
    end = len(frames) - pad
    for i in range(k_in):          # strongest on frame 0
        e = (1 - i / k_in) ** 2
        frames[i] = smear(frames[i], 0.18 * w * e, sign * 0.35 * w * e)
    for j in range(k_out):         # strongest on the last frame
        e = ((j + 1) / k_out) ** 2
        frames[end - k_out + j] = smear(frames[end - k_out + j], 0.18 * w * e, -sign * 0.35 * w * e)
    return frames


def write(frames, path):
    n, h, w, _ = frames.shape
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", "25", "-i", "-",
           "-c:v", "prores_ks", "-profile:v", "2", "-pix_fmt", "yuv422p10le",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", str(path)]
    subprocess.run(cmd, input=frames.tobytes())


def run(job):
    W, H = probe(job["clip"])
    div = 2 if job.get("half", True) else 1      # 1080p sources: keep full size (the window would upscale them)
    w, h = W // div // 2 * 2, H // div // 2 * 2
    rate = job.get("rate", 1.0)
    native = job.get("interpret", False)       # a 24/30 fps clip conformed to 25 by interpretation: every frame once
    nat_fps = 25 / rate if native else 25
    n_out = int(round(job["out_dur"] * 25))
    keys = job.get("speed_keys")                # speed ramp: [[t_out_s, rate], ...]
    if not keys and rate < 0.999 and not native:
        keys = [[0, rate]]                      # constant slow-mo: same 4x in-between route (minterpolate straight to
                                                # 25/rate fps left duplicate frames at 70 %, a judder on C112's pan)
    src_t = ramp_times(keys, n_out) if keys else None
    need = (src_t[-1] + 1 / 25) if keys else job["out_dur"] * rate   # camera seconds
    margin = 0.6 if job.get("stab") else 0.0
    t0 = max(0.0, job["src_in"] - margin)
    lead = job["src_in"] - t0
    frames = read_frames(job["clip"], t0, need + lead + margin + 0.2, w, h, native)
    worst = 0.0
    if job.get("stab"):
        frames, worst = stabilise(frames, job["stab"], job.get("sigma", 15), job.get("zoom", 1.06), job.get("transl_only", False))
    i0 = int(round(lead * nat_fps))
    slow = rate < 0.999 and not native and not keys
    if keys:
        frames = frames[i0: i0 + int(np.ceil(need * 25)) + 3]
        k = 4 if min(k[1] for k in keys) < 0.999 else 1
        dense = densify(frames, k) if k > 1 else frames
        idx = np.clip(np.round(src_t * 25 * k).astype(int), 0, len(dense) - 1)
        frames = dense[idx]
        rate = f"ramp {keys}"
    else:
        frames = frames[i0: i0 + (int(np.ceil(need * 25)) + 3 if slow else n_out)]
    if slow:
        frames = retime(frames, rate)
    frames = frames[:n_out]
    if job.get("whip_in") or job.get("whip_out"):
        frames = whip(frames, job.get("whip_in", 0), job.get("whip_out", 0), job.get("whip_dir", -1), job.get("pad", 0))
    OUT.mkdir(parents=True, exist_ok=True)
    out = Path(job["out"]) if job.get("out") else OUT / f"{job['id']}.mov"
    write(frames, out)
    print(f"{job['id']:22s} {w}x{h} src {job['src_in']:.2f}+{need:.2f}s rate {rate} stab {job.get('stab')} "
          f"max corr {worst:.0f}px -> {out} ({len(frames)} frames, need {n_out})", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", required=True)
    ap.add_argument("--only")
    a = ap.parse_args()
    jobs = json.load(open(a.jobs))
    for j in jobs:
        if a.only and j["id"] not in a.only.split(","):
            continue
        run(j)
