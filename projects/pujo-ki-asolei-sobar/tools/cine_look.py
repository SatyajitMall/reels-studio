#!/usr/bin/env python3
"""Round 3 look: match the director's cinematic reference (references/ref_grade_bangkok.webm), replacing the sepia.

look(x, P): pixelwise on the per-shot corrected frame: soft filmic tone curve (rolled-off highlights, gentle toe)
            + 3-way channel balance (shadows / mids / highlights) + saturation.  Exportable as a .cube.
fit:        tunes P so the median stats of our corrected frames match the reference medians
            (luma, p02, p50, p98, saturation, R/G and B/G per tone band; shadows weighted low, their ratios are noisy).
Usage: cine_look.py fit <corrected_frames_dir>   -> analysis/cine_look_params.json
       cine_look.py preview <in_dir> <out_dir>
       cine_look.py cube <out.cube>
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import optimize

REEL = Path(__file__).resolve().parents[1]
REF = json.loads((REEL / "analysis/ref_grade_bkk/ref_stats.json").read_text())["median"]
TX = np.array([0.0, 0.05, 0.15, 0.30, 0.50, 0.70, 0.90, 1.0])
DEFAULT = {"ty": [0.02, 0.055, 0.15, 0.29, 0.47, 0.62, 0.74, 0.78], "gs": [1.0, 1.0, 1.0], "gm": [1.0, 1.0, 0.95], "gh": [0.97, 1.0, 0.97], "sat": 0.72}

def luma(x): return x @ np.array([0.2126, 0.7152, 0.0722])

def look(x, P):
    ty = np.maximum.accumulate(np.array(P["ty"]))
    y = np.clip(luma(x), 1e-5, 1); y2 = np.interp(y, TX, ty)
    x = x * (y2 / y)[..., None]
    ws = np.clip(1 - y2 / 0.25, 0, 1) ** 1.3; wh = np.clip((y2 - 0.45) / 0.35, 0, 1) ** 1.3; wm = np.clip(1 - ws - wh, 0, 1)
    g = sum(np.array(P[k])[None, None, :] * w[..., None] for k, w in (("gs", ws), ("gm", wm), ("gh", wh)))
    x = x * g
    yy = luma(x)[..., None]; x = yy + (x - yy) * P["sat"]
    return np.clip(x, 0, 1)

def stats(x):
    y = luma(x); mx = x.max(-1); mn = x.min(-1); sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    r = {"luma": y.mean(), "p02": np.percentile(y, 2), "p50": np.percentile(y, 50), "p98": np.percentile(y, 98), "sat": sat.mean()}
    for nm, (lo, hi) in {"shad": (0, 0.2), "mid": (0.2, 0.6), "high": (0.6, 1.01)}.items():
        m = (y >= lo) & (y < hi)
        r[nm] = (x[..., 0][m].mean() / x[..., 1][m].mean(), x[..., 2][m].mean() / x[..., 1][m].mean()) if m.sum() > 300 else None
    return r

def med(frames, P):
    S = [stats(look(f, P)) for f in frames]
    out = {k: float(np.median([s[k] for s in S])) for k in ("luma", "p02", "p50", "p98", "sat")}
    for b in ("shad", "mid", "high"):
        v = [s[b] for s in S if s[b]]; out[b] = (float(np.median([a[0] for a in v])), float(np.median([a[1] for a in v]))) if v else (1, 1)
    return out

def pack(P): return np.array(P["ty"] + P["gs"][::2] + P["gm"][::2] + P["gh"][::2] + [P["sat"]])
def unpack(v):
    return {"ty": list(v[:8]), "gs": [v[8], 1.0, v[9]], "gm": [v[10], 1.0, v[11]], "gh": [v[12], 1.0, v[13]], "sat": float(v[14])}

def loss(v, frames):
    P = unpack(v); m = med(frames, P)
    if not np.isfinite(m['luma']): return 1e3
    e = 0
    for k, w in (("luma", 6), ("p02", 4), ("p50", 6), ("p98", 5), ("sat", 4)): e += w * (m[k] - REF[k]) ** 2
    for b, w in (("mid", 6), ("high", 3), ("shad", 0.5)):
        e += w * ((m[b][0] - REF[b][0]) ** 2 + (m[b][1] - REF[b][1]) ** 2)
    e += 0.5 * np.sum(np.diff(v[:8]) < 0)                       # keep the curve monotonic
    return e

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "fit":
        frames = [np.asarray(Image.open(p).convert("RGB").resize((270, 480)), np.float32) / 255 for p in sorted(Path(sys.argv[2]).glob("*.png"))]
        v0 = pack(DEFAULT)
        bounds = [(0.0, 0.12), (0.01, 0.2), (0.05, 0.35), (0.12, 0.5), (0.25, 0.7), (0.4, 0.85), (0.5, 0.95), (0.55, 1.0)] + [(0.7, 1.4)] * 6 + [(0.25, 1.2)]
        r = optimize.minimize(loss, v0, args=(frames,), method="Powell", bounds=bounds, options={"maxiter": 4000, "xtol": 1e-3, "ftol": 1e-6})
        P = unpack(r.x); P["ty"] = list(np.maximum.accumulate(np.clip(P["ty"], 0, 1)))
        P = {k: ([float(a) for a in v] if isinstance(v, list) else float(v)) for k, v in P.items()}
        (REEL / "analysis/cine_look_params.json").write_text(json.dumps(P, indent=1))
        m = med(frames, P)
        print("fit loss", round(float(r.fun), 5))
        print("OURS", {k: (round(v, 3) if isinstance(v, float) else tuple(round(a, 3) for a in v)) for k, v in m.items()})
        print("REF ", REF); print("P", P)
    elif mode == "preview":
        P = json.loads((REEL / "analysis/cine_look_params.json").read_text())
        dst = Path(sys.argv[3]); dst.mkdir(parents=True, exist_ok=True)
        for p in sorted(Path(sys.argv[2]).glob("*.png")):
            x = np.asarray(Image.open(p).convert("RGB"), np.float32) / 255
            Image.fromarray((look(x, P) * 255 + 0.5).astype(np.uint8)).save(dst / p.name)
    elif mode == "cube":
        P = json.loads((REEL / "analysis/cine_look_params.json").read_text())
        N = 33; v = np.linspace(0, 1, N); b, g, r = np.meshgrid(v, v, v, indexing="ij")
        out = look(np.stack([r, g, b], -1).reshape(-1, 1, 3), P).reshape(-1, 3)
        with open(sys.argv[2], "w") as f:
            f.write('TITLE "pujo-ki-asolei-sobar cinematic look (Bangkok ref)"\nLUT_3D_SIZE 33\nDOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n')
            for q in out: f.write(f"{q[0]:.6f} {q[1]:.6f} {q[2]:.6f}\n")
        print("wrote", sys.argv[2])
