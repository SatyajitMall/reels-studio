"""Motion audit for could-not-go-home-diwali (reel-local): jumps, shake, frame cadence and window coverage, per shot,
at every stage of the pipeline, so a defect seen in the export can be traced to the camera file, the depth bake,
the preview pre-render or the assembly.

Per shot (from the EDL):
  export   the 4:3 window of the export (y 505–1315): frame-to-frame shift (phase correlation), content change (MAD),
           repeated frames, jumps (shift or MAD far off the local trend), jitter after removing the smooth path,
           window coverage (black at the window edges = the image doesn't fill it)
  clip     the same measures on the file the EDL plays (pre-render, bake or stock), over the span it uses
  camera   the camera file's frame timestamps over that span (gaps or uneven steps = dropped frames / VFR)

Run from the studio root:
  .venv/bin/python -I projects/could-not-go-home-diwali/tools/motion_audit.py <export> --edl <edl.json> -o <out_dir>
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter1d, median_filter

STUDIO = Path(__file__).resolve().parents[3]
REEL = Path(__file__).resolve().parents[1]
FPS = 25
W, H = 360, 270           # analysis size of the 4:3 window (1080×810 → ÷3)
K = 1080 / W              # px in 1080-wide terms
EDGE = 2                  # frames ignored next to each cut


def frames(path, vf, w, h, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"]
    if ss is not None:
        cmd += ["-ss", f"{ss:.3f}"]
    cmd += ["-i", str(path)]
    if t is not None:
        cmd += ["-t", f"{t:.3f}"]
    cmd += ["-vf", vf + f",scale={w}:{h}:flags=area,format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, cwd=STUDIO).stdout
    a = np.frombuffer(raw, np.uint8)
    return a[: a.size // (w * h) * w * h].reshape(-1, h, w).astype(np.float32)


def shift(a, b, win):
    hh, ww = a.shape
    A = np.fft.fft2((a - a.mean()) * win); B = np.fft.fft2((b - b.mean()) * win)
    R = A * np.conj(B); R /= np.abs(R) + 1e-6
    c = np.fft.ifft2(R).real
    y, x = np.unravel_index(c.argmax(), c.shape)

    def sub(cm, c0, cp):
        d = cm - 2 * c0 + cp
        return 0.0 if d == 0 else 0.5 * (cm - cp) / d
    yy = y + sub(c[(y - 1) % hh, x], c[y, x], c[(y + 1) % hh, x])
    xx = x + sub(c[y, (x - 1) % ww], c[y, x], c[y, (x + 1) % ww])
    if yy > hh / 2: yy -= hh
    if xx > ww / 2: xx -= ww
    return xx, yy, float(c.max())


def measure(fr, k, t0=0.0):
    """Per-pair metrics on a stack of frames; k converts px to 1080-wide terms."""
    n = len(fr)
    if n < 6:
        return None
    hh, ww = fr.shape[1:]
    win = np.outer(np.hanning(hh), np.hanning(ww)).astype(np.float32)
    s = np.array([shift(fr[i], fr[i + 1], win) for i in range(n - 1)])
    dx, dy, conf = s[:, 0] * k, s[:, 1] * k, s[:, 2]
    mad = np.array([np.abs(fr[i + 1] - fr[i]).mean() for i in range(n - 1)])
    sm_x, sm_y = gaussian_filter1d(dx, 3), gaussian_filter1d(dy, 3)
    res = np.hypot(dx - sm_x, dy - sm_y)                       # per-step deviation from the local motion trend
    base = max(float(np.median(res)), 0.5)
    mad_trend = median_filter(mad, size=7, mode="nearest")
    jumps = []
    for i in range(len(res)):
        if res[i] > max(4.0, 5 * base) or (mad[i] > 2.5 * mad_trend[i] and mad[i] > 4):
            jumps.append({"t": round(t0 + (i + 1) / FPS, 2), "shift_px": round(float(np.hypot(dx[i], dy[i])), 1),
                          "off_trend_px": round(float(res[i]), 1), "mad": round(float(mad[i]), 2),
                          "mad_trend": round(float(mad_trend[i]), 2)})
    dup = [round(t0 + (i + 1) / FPS, 2) for i in range(len(mad)) if mad[i] < 0.25 and mad_trend[i] > 1.0]
    tx, ty = np.cumsum(dx), np.cumsum(dy)
    jx, jy = tx - gaussian_filter1d(tx, 6), ty - gaussian_filter1d(ty, 6)
    jit = np.hypot(jx, jy)
    pan = float(np.hypot(gaussian_filter1d(dx, 6).mean(), gaussian_filter1d(dy, 6).mean()) * FPS)
    return {"frames": n, "jit_rms": round(float(np.sqrt((jit ** 2).mean())), 2), "jit_max": round(float(jit.max()), 2),
            "jerk_p95": round(float(np.percentile(np.hypot(np.diff(jx), np.diff(jy)), 95)), 2), "pan_px_s": round(pan, 1),
            "worst_t": round(t0 + (int(jit.argmax()) + 1) / FPS, 2), "mad_med": round(float(np.median(mad)), 2),
            "repeats": dup, "jumps": jumps, "dx": [round(float(v), 2) for v in dx], "dy": [round(float(v), 2) for v in dy],
            "mad": [round(float(v), 2) for v in mad]}


def pts(path, ss, t):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-read_intervals", f"{max(0, ss - 0.2):.3f}%+{t + 0.4:.3f}",
                        "-show_entries", "frame=pts_time", "-of", "csv=p=0", str(path)], capture_output=True, text=True, cwd=STUDIO)
    p = np.array([float(x.strip(",")) for x in r.stdout.split() if x.strip(",").strip() and x.strip(",") != "N/A"])
    p = p[(p >= ss - 0.001) & (p <= ss + t + 0.001)]
    if len(p) < 3:
        return {"frames": int(len(p))}
    d = np.diff(np.sort(p))
    bad = [round(float(p[i + 1]), 3) for i in range(len(d)) if abs(d[i] - 1 / FPS) > 0.004]
    return {"frames": int(len(p)), "step_min": round(float(d.min()), 4), "step_max": round(float(d.max()), 4), "uneven_at": bad[:12]}


def camera_of(shot):
    note = shot.get("note") or ""
    m = re.search(r"camera (?:A001_\d+_)?(C\d{3})(?:\.mov)? in ([\d.]+) s", note)
    if not m:
        return None, None
    cam = sorted((REEL / "raw" / "Media").glob(f"*_{m.group(1)}.mov"))
    return (cam[0] if cam else None), float(m.group(2))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("export"); ap.add_argument("--edl", required=True); ap.add_argument("-o", required=True)
    a = ap.parse_args()
    out = Path(a.o); out.mkdir(parents=True, exist_ok=True)
    edl = json.loads(Path(a.edl).read_text())
    ex = frames(a.export, "crop=1080:810:0:505", W, H)
    rep = []
    for s in edl["shots"]:
        if not s.get("clip"):
            continue
        st, en = s["start"], s["end"]
        i0, i1 = int(round(st * FPS)) + EDGE, int(round(en * FPS)) - EDGE
        r = {"shot": s["name"], "t": [st, en]}
        seg = ex[i0:i1 + 1]
        r["export"] = measure(seg, K, i0 / FPS)
        # coverage: dark rows/cols right at the window edge where the image should be
        edges = np.concatenate([seg[:, :2, :].reshape(len(seg), -1), seg[:, -2:, :].reshape(len(seg), -1),
                                seg[:, :, :2].reshape(len(seg), -1), seg[:, :, -2:].reshape(len(seg), -1)], axis=1)
        r["export"]["edge_black_frac_max"] = round(float((edges < 3).mean(axis=1).max()), 3)
        # the clip as played (span in clip time)
        dur = en - st
        rate = s.get("rate") or 1
        rate = rate[0][1] if isinstance(rate, list) else rate
        span = dur * rate
        clip = STUDIO / s["clip"]
        rot = s.get("rotation") == -90
        vf = "null" if not rot else "null"   # ffmpeg autorotates; measuring the upright frame either way
        cf = frames(clip, vf, 270, 480, ss=s["src_in"], t=span) if rot else frames(clip, vf, 480, 270, ss=s["src_in"], t=span)
        r["clip"] = {"file": s["clip"], "pts": pts(clip, s["src_in"], span)}
        m = measure(cf, 1080 / cf.shape[2] if len(cf) else 1, st) if len(cf) else None
        if m:
            for k_ in ("dx", "dy", "mad"):
                m.pop(k_)
        r["clip"]["motion"] = m
        cam, cin = camera_of(s)
        if cam:
            r["camera"] = {"file": cam.name, "in": cin, "pts": pts(cam, cin, span)}
        rep.append(r)
        e = r["export"]
        print(f"{s['name']:24s} jit {e['jit_rms']:5.2f}/{e['jit_max']:5.1f} jerk95 {e['jerk_p95']:5.2f} pan {e['pan_px_s']:6.1f} "
              f"rep {len(e['repeats']):2d} jumps {len(e['jumps']):2d} edge {e['edge_black_frac_max']:.2f} | clip rep "
              f"{len(m['repeats']) if m else '-'} jumps {len(m['jumps']) if m else '-'} pts {r['clip']['pts'].get('uneven_at', [])[:3]}"
              + (f" | cam pts {r['camera']['pts'].get('uneven_at', [])[:3]}" if cam else ""))
    (out / "motion_audit.json").write_text(json.dumps(rep, indent=1))
    print("wrote", out / "motion_audit.json")


if __name__ == "__main__":
    main()
