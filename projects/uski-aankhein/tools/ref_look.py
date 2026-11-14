#!/usr/bin/env python3
"""Match-reference look for uski-aankhein (director's choice A), tuned to the measured reference grade.

Adapted from projects/pujo-ki-asolei-sobar/tools/ref_look.py (see CR-20261020-pujo-ki-asolei-sobar-reference-grade-match).
Reference (analysis/ref_grade/ref_grade.json, picture area only, medians over both sections):
  luma ~0.28, p02 ~0.065 (lifted blacks), p98 ~0.53 (no whites), saturation (max-min) ~0.23,
  mids R/G ~1.50 B/G ~0.62, shadows R/G ~1.50 B/G ~0.85.

Pipeline per frame:
  1. normalise  = what the per-clip Lumetri primary must do in Premiere: partial grey balance + exposure to luma 0.30
  2. look       = the .cube (pixelwise): lifted/rolled tone curve, desaturation, warm amber 2-way tint
  3. optical    = Lumetri vignette on the V3 layer (not in the .cube); grain on V4
Usage:
  ref_look.py tune  <stills_dir>                  auto-tune the look params to the reference, write look_params.json
  ref_look.py preview <stills_dir> <out_dir>      graded stills + stats table vs the reference
  ref_look.py cube <out.cube>                     33^3 LUT of step 2 (Lumetri > Creative > Look, loaded by hand)
"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parents[1]
PARAMS = HERE / "analysis" / "look_test" / "look_params.json"
REF = {"luma": 0.28, "p02": 0.065, "p98": 0.53, "sat": 0.23, "mid_RG": 1.50, "mid_BG": 0.62, "shad_RG": 1.50, "shad_BG": 0.85}
DEF = {"black": 0.06, "white": 0.58, "gamma": 1.0, "sat": 0.55,
       "mid": [1.30, 1.0, 0.70], "shad": [1.30, 1.0, 0.90]}

def luma(x): return x @ np.array([0.2126, 0.7152, 0.0722])

def stats(x):
    y = luma(x); s = x.max(-1) - x.min(-1)
    d = {"luma": y.mean(), "p02": np.percentile(y, 2), "p98": np.percentile(y, 98), "sat": s.mean()}
    for b, m in (("shad", y < 0.2), ("mid", (y >= 0.2) & (y <= 0.6))):
        if m.sum() > 200:
            r, g, bb = (x[..., i][m].mean() for i in range(3)); d[b + "_RG"] = r / g; d[b + "_BG"] = bb / g
    return d

def normalise(x, target=0.30, wb=0.35):
    y = luma(x); m = (y > 0.10) & (y < 0.85)
    r, g, b = (x[..., i][m].mean() for i in range(3))
    gains = np.array([(g / r) ** wb, 1.0, (g / b) ** wb])
    x = x * gains
    k = min((target / max(luma(x).mean(), 1e-3)) ** 0.8, 2.0)   # cap +1 stop (C025 is a deliberate dark shot)
    return np.clip(x * k, 0, 1), {"wb_gains": gains.round(3).tolist(), "exposure_stops": round(float(np.log2(k)), 2)}

def look(x, P):
    y = np.clip(luma(x), 0, 1)
    # tone: soft S on the way, then map [0,1] -> [black, white] (lifted blacks, rolled-off highlights)
    t = y ** P["gamma"]
    t = t * t * (3 - 2 * t) * 0.35 + t * 0.65
    y2 = P["black"] + (P["white"] - P["black"]) * t
    # chroma ratio x/y; fade to neutral grey near true black so (0,0,0) lifts to the same warm black
    # as its neighbours (v1 cube left pure black at 0 next to lifted 0.03: blotchy crushed areas, e.g. C025)
    w = np.clip(y / 0.02, 0, 1)[..., None]
    ratio = w * (x / np.clip(y, 1e-5, None)[..., None]) + (1 - w)
    x = ratio * y2[..., None]
    yy = luma(x)[..., None]; x = yy + (x - yy) * P["sat"]
    ws = np.clip(1 - y2 / 0.25, 0, 1)[..., None]
    g = np.array(P["shad"]) * ws + np.array(P["mid"]) * (1 - ws)
    x2 = x * g
    x2 = x2 * (luma(x) / np.clip(luma(x2), 1e-5, None))[..., None]   # keep the tone curve's luma
    return np.clip(x2, 0, 1)

def load(d):
    return [np.asarray(Image.open(p).convert("RGB")).astype(np.float32) / 255 for p in sorted(Path(d).glob("*.png"))], sorted(Path(d).glob("*.png"))

def med(ss, k): return float(np.median([s[k] for s in ss if k in s]))

def tune(d):
    ims, _ = load(d); N = [normalise(x)[0] for x in ims]; P = json.loads(json.dumps(DEF))
    for it in range(40):
        ss = [stats(look(x, P)) for x in N]; m = {k: med(ss, k) for k in REF}
        P["black"] += 0.5 * (REF["p02"] - m["p02"])
        P["white"] += 0.6 * (REF["p98"] - m["p98"])
        P["gamma"] *= (m["luma"] / REF["luma"]) ** 0.6
        P["sat"] *= (REF["sat"] / m["sat"]) ** 0.7
        for b in ("mid", "shad"):
            P[b][0] *= (REF[b + "_RG"] / m[b + "_RG"]) ** 0.7
            P[b][2] *= (REF[b + "_BG"] / m[b + "_BG"]) ** 0.7
            # warm look only: never cool (B up) or de-red (R down) a band; idols are already orange, so
            # band ratios are content-dependent and must not be forced (first tune pushed shadows to B x2.1)
            P[b][0] = float(np.clip(P[b][0], 1.0, 1.6)); P[b][2] = float(np.clip(P[b][2], 0.55, 1.0))
        P["sat"] = float(np.clip(P["sat"], 0.35, 1.0)); P["black"] = float(np.clip(P["black"], 0.03, 0.10))
    ss = [stats(look(x, P)) for x in N]; m = {k: round(med(ss, k), 3) for k in REF}
    P = {k: (np.round(v, 4).tolist() if isinstance(v, list) else round(float(v), 4)) for k, v in P.items()}
    PARAMS.write_text(json.dumps({"params": P, "result_medians": m, "reference": REF}, indent=1))
    print(json.dumps({"params": P, "result": m, "ref": REF}, indent=1))

def preview(d, out):
    P = json.loads(PARAMS.read_text())["params"]; ims, paths = load(d); out = Path(out); out.mkdir(parents=True, exist_ok=True)
    rows = []; tiles = []
    for x, p in zip(ims, paths):
        n, prim = normalise(x); g = look(n, P)
        h, w = g.shape[:2]; yy, xx = np.mgrid[0:h, 0:w]
        dd = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h * 0.42) / (h / 2)) ** 2)
        g = g * (1 - 0.30 * np.clip((dd - 0.5) / 0.8, 0, 1) ** 1.6)[..., None]    # Lumetri vignette stand-in
        Image.fromarray((g * 255).astype(np.uint8)).save(out / p.name.replace(".png", "_A.jpg"), quality=90)
        s = stats(g); rows.append((p.stem, prim, {k: round(float(v), 3) for k, v in s.items()}))
        tiles.append(np.concatenate([x, g], 1))
    sheet = np.concatenate([np.concatenate(tiles[i:i + 5], 1) for i in range(0, len(tiles) - len(tiles) % 5, 5)], 0) if len(tiles) >= 5 else tiles[0]
    Image.fromarray((sheet * 255).astype(np.uint8)).resize((sheet.shape[1] // 2, sheet.shape[0] // 2)).save(out / "before_after.jpg", quality=86)
    (out / "stats.json").write_text(json.dumps(rows, indent=1))
    for r in rows: print(r[0], r[1], r[2])

def cube(path):
    P = json.loads(PARAMS.read_text())["params"]; n = 33
    v = np.linspace(0, 1, n); b, g, r = np.meshgrid(v, v, v, indexing="ij")
    grid = np.stack([r, g, b], -1).reshape(-1, 3)        # .cube order: R fastest
    o = look(grid[None], P)[0]
    with open(path, "w") as f:
        f.write('TITLE "uski-aankhein match reference v1"\nLUT_3D_SIZE 33\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
        for c in o: f.write(f"{c[0]:.6f} {c[1]:.6f} {c[2]:.6f}\n")
    print("wrote", path)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "tune": tune(sys.argv[2])
    elif mode == "preview": preview(sys.argv[2], sys.argv[3])
    elif mode == "cube": cube(sys.argv[2])
