#!/usr/bin/env python3
"""Skin-tone post-pass on a rendered shot: measure skin on the frames that are on screen (person-gated, skin-hue window,
robust median), iterate luminance-preserving channel gains + a skin-saturation factor until skin = target, then apply the
same constants to every frame. Writes <name>_<out_ver>.mov (+ json). Usage: skin_post.py <in_ver> <out_ver> <shot> [...]
"""
import sys, json, subprocess, tempfile, colorsys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent)); import skin_match as sm
R = Path(__file__).resolve().parents[1] / "renders" / "final_shots"
TH, TS = 28.0, 0.45
def skin_px(x, alpha):
    mx = x.max(-1); mn = x.min(-1); v = mx; s = (mx - mn) / np.maximum(mx, 1e-6)
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    h = np.zeros_like(r); d = np.maximum(mx - mn, 1e-6)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    m = sm.skin_mask(x) & (h >= 0) & (h <= 42) & (s > 0.15) & (s < 0.75) & (v > 0.12) & (v < 0.92)
    if alpha is not None: m &= alpha > 0.5
    return x[m]
def skin_rgb(frames, alphas):
    px = [skin_px(x, a) for x, a in zip(frames, alphas)]
    px = np.concatenate([p for p in px if len(p)]) if any(len(p) for p in px) else np.zeros((0, 3))
    return np.median(px, axis=0) if len(px) >= 200 else None
def apply(x, g, k):
    return sm.apply_full(x, g, k)
def solve(frames, alphas):
    g = np.ones(3); k = 1.0
    for _ in range(8):
        cur = [apply(x, g, 1.0) for x in frames]; s = skin_rgb(cur, alphas)
        if s is None: return None, None, None
        h, sa, v = colorsys.rgb_to_hsv(*s)
        if abs(h * 360 - TH) < 1.0: break
        t = np.array(colorsys.hsv_to_rgb(TH / 360, sa, v)); t *= sm.luma(s) / max(sm.luma(t), 1e-6)
        step = t / np.maximum(s, 1e-6); step /= step[1]; g = np.clip(g * step ** 0.8, 0.7, 1.4)
    s = skin_rgb([apply(x, g, 1.0) for x in frames], alphas); sa = colorsys.rgb_to_hsv(*s)[1]
    k = float(np.clip(TS / max(sa, 1e-3), 0.85, 1.2))
    fin = skin_rgb([apply(x, g, k) for x in frames], alphas)
    return g, k, colorsys.rgb_to_hsv(*fin)
def read(f, t=None, scale=None):
    vf = ["-vf", f"scale={scale}"] if scale else []
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{t:.4f}"] if t is not None else []) + ["-i", str(f)] + (["-frames:v", "1"] if t is not None else []) + vf + ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    return subprocess.run(cmd, capture_output=True).stdout
if __name__ == "__main__":
    vin, vout = sys.argv[1], sys.argv[2]
    for n in sys.argv[3:]:
        j = next(R.glob(f"{int(n):02d}_*_{vin}.json")); r = json.loads(j.read_text()); src = R / r["file"]
        ts = [r["place_in"] + (r["place_out"] - r["place_in"]) * k / 7 for k in range(1, 7)]
        S = [np.frombuffer(read(src, t, "540:960"), np.uint8).reshape(960, 540, 3).astype(np.float32) / 255 for t in ts]
        with tempfile.TemporaryDirectory() as td: A = sm.people_alphas(S, td)
        g, k, fin = solve(S, A)
        if g is None: g, k, fin = np.ones(3), 1.0, (0, 0, 0); print(f"{n}: no skin found, unchanged")
        before = skin_rgb(S, A); hb = colorsys.rgb_to_hsv(*before) if before is not None else (0, 0, 0)
        print(f"{n} {r['clip']}: skin hue {hb[0]*360:5.1f} -> {fin[0]*360:5.1f}  sat {hb[1]:.2f} -> {fin[1]:.2f}  gains {np.round(g, 3)} k {k:.2f}", flush=True)
        raw = read(src); X = np.frombuffer(raw, np.uint8).reshape(-1, 1920, 1080, 3)
        name = r["file"].replace(f"_{vin}.mov", f"_{vout}"); vtmp = R / f"{name}_v.mov"
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "30", "-i", "-",
                                "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", str(vtmp)], stdin=subprocess.PIPE)
        for fr in X: enc.stdin.write((apply(fr.astype(np.float32) / 255, g, k) * 255 + 0.5).clip(0, 255).astype(np.uint8).tobytes())
        enc.stdin.close(); enc.wait()
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vtmp), "-i", str(src), "-map", "0:v", "-map", "1:a?", "-c", "copy", str(R / f"{name}.mov")], check=True)
        vtmp.unlink(); r2 = dict(r, file=f"{name}.mov", skin_post_gains=[float(a) for a in g], skin_post_k=k, skin_hue_final=round(fin[0] * 360, 1))
        (R / f"{name}.json").write_text(json.dumps(r2, indent=1))
