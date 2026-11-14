#!/usr/bin/env python3
"""Round 9: measure v9 stills (one per shot, mid-frame, from analysis/_es_v9_stills.jsx) against the round-9 targets and against the
camera file at the same framing. Targets (HQ/director): luma 0.38–0.46 per shot (bright shots may stay near camera level), crushed
(< 0.03) ≤ 2 % unless the camera frame itself is darker, p98 0.80–0.90 (not below the camera unless it clips), slight warmth.
Usage (reels-studio root): .venv/bin/python projects/<reel>/tools/v9_measure.py <stills dir> [--camera]"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "tools"))
import shot_look as S  # noqa: E402

F = {r["f"]: r for r in json.loads((R / "analysis/_v9_frame.jsx").read_text()[len("var V9F="):-2])}
plan = {q["name"].split("_")[1]: q for q in json.loads((R / "analysis/look/bake_plan.json").read_text())}


def stats(a):
    x = a.astype(np.float32) / 255; y = x @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    m = np.ones(y.shape, bool); m[int(y.shape[0] * 0.72):int(y.shape[0] * 0.82)] = False      # skip the subtitle band
    yy = y[m]; xx = x[m]; mid = (yy > 0.2) & (yy < 0.6)
    c = xx[mid].mean(0) if mid.sum() > 100 else xx.mean(0); mx, mn = c.max(), c.min()
    hue = 0.0 if mx - mn < 1e-6 else (60 * (((c[1] - c[2]) / (mx - mn)) % 6) if mx == c[0] else 60 * ((c[2] - c[0]) / (mx - mn) + 2) if mx == c[1] else 60 * ((c[0] - c[1]) / (mx - mn) + 4))
    return {"luma": round(float(yy.mean()), 3), "p02": round(float(np.percentile(yy, 2)), 3), "p98": round(float(np.percentile(yy, 98)), 3),
            "crushed%": round(float((yy < 0.03).mean() * 100), 1), "clip%": round(float((yy > 0.98).mean() * 100), 2),
            "R-B": round(float(xx[..., 0].mean() - xx[..., 2].mean()), 3), "hue": round(float(hue), 1)}


def camera(f):
    """The camera file at v9's framing (Scale/Position at the mid frame), no grade."""
    r = F[f]; k = None
    q = next(v for v in plan.values() if v["seq"][0] == f) if any(v["seq"][0] == f for v in plan.values()) else None
    return r, q


def main():
    d = Path(sys.argv[1]); rows = []
    for p in sorted(d.glob("*.png*")):
        fm = int(p.name.split(".")[0]); start = max(k for k in F if k <= fm); r = F[start]
        a = np.asarray(Image.open(p).convert("RGB")); s = stats(a)
        rows.append((start, r["n"], fm, s))
        print(f"{r['n'][9:]:6s} f{fm:3d}  " + "  ".join(f"{k} {v}" for k, v in s.items()))
    L = np.array([s["luma"] for *_, s in rows]); print(f"\nreel mean luma {L.mean():.3f}, min {L.min():.3f}; shots under 0.38: {[n[9:] for _, n, _, s in rows if s['luma'] < 0.38]}; crushed > 2 %: {[n[9:] for _, n, _, s in rows if s['crushed%'] > 2]}")


if __name__ == "__main__":
    main()
