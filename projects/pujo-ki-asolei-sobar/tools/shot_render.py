#!/usr/bin/env python3
"""Render one EDL shot with the approved v1g treatment, every frame:
   crop/reframe -> 1080x1920 @ exact 30 fps -> per-shot neutral match -> depth-based lens bokeh -> sepia film look
   -> halation + vignette + grain.  ProRes 422 HQ + the source audio, with handles.

Stable over time: neutral gains, depth normalisation range and far reference are fixed per shot; raw depth is
smoothed (EMA) and the focus distance is median-filtered across the shot, so blur doesn't pulse.
Usage: shot_render.py <shot n> [--handle 0.3]
"""
import json, subprocess, sys, time
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import lens, sepia_look as sl  # noqa: E402
from preview_sepia_bokeh_lib import optical  # noqa: E402

n = sys.argv[1]; handle = float(sys.argv[sys.argv.index("--handle") + 1]) if "--handle" in sys.argv else 0.3
VER = sys.argv[sys.argv.index("--ver") + 1] if "--ver" in sys.argv else "v1h"
edl = json.loads((REEL / "analysis" / f"edl_{VER}.json").read_text()); s = next(x for x in edl["shots"] if x["n"] == n)
f = json.loads((REEL / "analysis" / f"focus_{VER}.json").read_text())[n]
src = next((REEL / "raw" / "b-roll").glob(f"*_{s['clip']}.mov"))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout)
t0 = max(0.0, s["in"] - handle); t1 = min(dur - 0.04, s["out"] + handle)
out_dir = REEL / "renders" / "final_shots"; out_dir.mkdir(parents=True, exist_ok=True)
name = f"{int(n):02d}_{s['clip']}_{VER}"; mov = out_dir / f"{name}.mov"
W, H = 1080, 1920
vf = (f"crop={f['crop']}," if f.get("crop") else "") + f"scale={W}:{H}:flags=lanczos,fps=30"
cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", str(src), "-an", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
raw = subprocess.run(cmd, capture_output=True).stdout
frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
N = len(frames); T = time.time()
print(f"▸ {name}: src {t0:.2f}-{t1:.2f}, {N} frames", flush=True)

# person matte (hyperframes remove-background on a proxy of exactly these frames): protects faces/hands from blur
import tempfile
with tempfile.TemporaryDirectory(prefix='matte_') as td:
    td = Path(td); px = td / 'proxy.mp4'
    pe = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-c:v','libx264','-crf','14','-pix_fmt','yuv420p',str(px)], stdin=subprocess.PIPE)
    pe.stdin.write(frames.tobytes()); pe.stdin.close(); pe.wait()
    r = subprocess.run(['npx','hyperframes','remove-background',str(px),'-o',str(td/'fg.mov'),'--device','cpu'], capture_output=True, text=True, cwd=td)
    if r.returncode == 0 and (td/'fg.mov').exists():
        araw = subprocess.run(['ffmpeg','-v','error','-i',str(td/'fg.mov'),'-vf','alphaextract','-f','rawvideo','-pix_fmt','gray','-'], capture_output=True).stdout
        mattes = np.frombuffer(araw, np.uint8).reshape(-1, H, W)
    else:
        print('  ! matte failed, depth only', (r.stdout + r.stderr)[-300:], flush=True); mattes = None
def protect_at(i):
    if mattes is None: return None
    j = min(i, len(mattes) - 1); a = np.mean([mattes[k] for k in range(max(0, j - 1), min(len(mattes), j + 2))], axis=0) / 255
    if f.get('protect', 'hero') == 'hero':
        lab, nl = ndimage.label(a > 0.5)
        if nl == 0: return None
        py, px = int(f['fy'] * H), int(f['fx'] * W)
        k = lab[py, px]
        if k == 0:   # nearest component to the focus point
            ys, xs = np.nonzero(lab); d2 = (ys - py) ** 2 + (xs - px) ** 2; k = lab[ys[d2.argmin()], xs[d2.argmin()]]
            if d2.min() > (0.12 * W) ** 2: return None
        a = a * (lab == k)
    a = ndimage.grey_dilation(a, size=(7, 7)); return ndimage.gaussian_filter(a, 3)
print(f'  matte: {"ok" if mattes is not None else "none"}', flush=True)

# per-shot constants
samp = [frames[i].astype(np.float32) / 255 for i in np.linspace(0, N - 1, 5).astype(int)]
gains = tuple(np.median(np.array([sl.measure(x) for x in samp]), axis=0))
ds = [lens.depth(sl.normalise(x, gains)) for x in samp]
lo = float(np.median([np.percentile(d, 2) for d in ds])); hi = float(np.median([np.percentile(d, 99.5) for d in ds]))
norm = lambda d: np.clip((d - lo) / max(hi - lo, 1e-6), 0, 1)
far_ref = float(np.median([np.percentile(norm(d), 5) for d in ds]))

# pass 1: depth per frame (smoothed) + focus per frame
depths, focus = [], []; ema = None
for i in range(N):
    x = sl.normalise(frames[i].astype(np.float32) / 255, gains)
    d = norm(lens.depth(x)); ema = d if ema is None else 0.6 * ema + 0.4 * d
    depths.append(ema.astype(np.float16))
    pr = protect_at(i)
    if f.get('focus_mode') == 'matte' and pr is not None and (pr > 0.5).mean() > 0.01: focus.append(float(np.percentile(ema[pr > 0.5], 60)))
    else: focus.append(lens.focus_value(ema, f["fx"], f["fy"]))
focus = ndimage.median_filter(np.array(focus), size=min(15, N | 1), mode="nearest")
focus = ndimage.uniform_filter1d(focus, size=min(9, N), mode="nearest")

# per-shot luma match to the reel target (gate loop 2: shot 7 was 0.186 vs 0.273), measured on 3 fully treated frames
TARGET, FLOOR = 0.27, 0.03
def treat(i, gain=1.0):
    x = sl.normalise(frames[i].astype(np.float32) / 255, gains)
    xb, _ = lens.bokeh(x, depths[i].astype(np.float32), float(focus[i]), far_ref, max_r=f.get('max_r', 20), near_r=f.get('near_r', 6), protect=protect_at(i))
    o = optical(sl.look(xb), seed=i, hal=f.get('hal', 0.22), vig=f.get('vig', 0.28))
    o = FLOOR + (o - FLOOR) * gain
    return np.clip(o, FLOOR - 0.005, 1)
pa = int(round((s['in'] - t0) * 30)); pb = min(N - 1, pa + (s['endF'] - s['startF']) - 1)   # only frames that are on screen
mids = [treat(i) for i in np.linspace(pa, pb, 5).astype(int)]
gain = float(np.clip((TARGET - FLOOR) / max(np.mean([sl.luma(m).mean() for m in mids]) - FLOOR, 1e-3), 0.75, 1.6))
print(f'  luma gain {gain:.3f}', flush=True)

# pass 2: render
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", str(out_dir / f"{name}_v.mov")], stdin=subprocess.PIPE)
for i in range(N):
    o = treat(i, gain)
    enc.stdin.write((o * 255 + 0.5).clip(0, 255).astype(np.uint8).tobytes())
    if i % 30 == 0: print(f"  {name} {i}/{N}  {time.time() - T:.0f}s", flush=True)
enc.stdin.close(); enc.wait()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out_dir / f"{name}_v.mov"), "-ss", f"{t0:.3f}", "-t", f"{N / 30:.3f}", "-i", str(src),
                "-map", "0:v", "-map", "1:a?", "-c:v", "copy", "-c:a", "pcm_s16le", "-shortest", str(mov)], check=True)
(out_dir / f"{name}_v.mov").unlink()
rec = {"n": n, "clip": s["clip"], "file": mov.name, "src_start": round(t0, 4), "frames": N, "place_in": round(s["in"] - t0, 4),
       "place_out": round(s["in"] - t0 + (s["endF"] - s["startF"]) / 30, 4), "gains": [round(float(g), 4) for g in gains],
       "depth_range": [round(lo, 3), round(hi, 3)], "far_ref": round(far_ref, 3), "luma_gain": round(gain, 3), "focus_range": [round(float(focus.min()), 3), round(float(focus.max()), 3)],
       "secs": round(time.time() - T)}
(out_dir / f"{name}.json").write_text(json.dumps(rec, indent=1)); print(f"✓ {name} {N} frames in {rec['secs']}s", flush=True)
