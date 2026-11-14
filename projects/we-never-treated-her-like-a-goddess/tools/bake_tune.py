#!/usr/bin/env python3
"""Per-shot overrides for the baked look (gate v6), without touching HQ's tools/shot_look.py.

The v6 gate found shots whose bake left the reel's warm match: #1 C010 went cool (the auto white balance neutralised the
warm night), #15 C186 olive with lifted smoke, #5/#11 C007 too bright, #3 C042's white shirt tan. This re-runs shot_look's
own Treatment with a few constants overridden per shot:
  wb      white-balance power (shot_look 0.6; 0 = keep the camera's balance)
  levels  how far tonal levels go to p02/p50/p98 0.035/0.30/0.86 (0.65)
  cast    cast-match power toward the reference midtones (0.6)
  gain_k  multiplies the exposure gain (1.0; 0.85 ≈ −0.23 stop)
  warm    extra R×warm, B÷warm on the cast gains, after the look (1.0)
  clarity fine-detail boost (0.12; 0 = none)
  denoise 0 = no hqdn3d denoise (default on)
  look    look mix (0.75; 0 = no creative look)
  hal, vig  halation / vignette (0.06 / 0.12)
  satcap  0 = no saturation cap (default: the look's reference saturation)

  preview <name> [k=v,...] ...   stats of the treated middle frame for each override set (+ --sheet out.jpg)
  render  <name> k=v,...  -o out.mov   the --full render, same as `shot_look.py render --full`, with the overrides

Stats: luma, p02, R−B (frame means), mid hue (HSV hue of the mean colour of pixels at luma 0.2–0.6), saturation.
Run from the reels-studio root with .venv/bin/python."""
import json, subprocess, sys, time
from pathlib import Path
import numpy as np
from PIL import Image

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "tools"))
import shot_look as S  # noqa: E402

LOOK = R / "analysis/look/goddess_halfway_look.json"


def parse(kv):
    o = {}
    for part in filter(None, kv.split(",")):
        k, v = part.split("="); o[k] = float(v)
    return o


def params(o):
    p = dict(S.NATURAL_MATCHED, grain=0.0)
    for k in ("wb", "levels", "cast", "clarity", "hal", "vig"):
        if k in o: p[k] = o[k]
    if "look" in o: p["look_mix"] = o["look"]
    if o.get("denoise", 1.0) == 0:
        p["denoise"] = None
    return p


def shot(name):
    return {q["name"]: q for q in json.loads((R / "analysis/look/bake_plan.json").read_text())}[name]


def treatment(q, o):
    sf = S.probe(str(R / q["clip"]))[1]
    crop = tuple(q["crop"])
    smp = [S.decode(str(R / q["clip"]), t, 1, crop, params(o)["denoise"], S.W)[0]
           for t in np.linspace(q["in"], q["in"] + (q["frames"] - 1) / sf, 6)]
    L = S.load_look(str(LOOK))
    if o.get("satcap", 1.0) == 0:
        L["sat_cap"] = 10.0
    tr = S.Treatment(smp, L, params(o))
    tr.gain = float(np.clip(tr.gain * o.get("gain_k", 1.0), 0.6, 1.8))
    w = o.get("warm", 1.0); tr.cg = tr.cg * np.array([w, 1.0, 1.0 / w])
    return tr, smp, sf


def stats(x):
    y = S.luma(x); m = (y > 0.2) & (y < 0.6)
    c = x[m].mean(0); mx, mn = c.max(), c.min()
    if mx - mn < 1e-6:
        hue = 0.0
    elif mx == c[0]:
        hue = 60 * (((c[1] - c[2]) / (mx - mn)) % 6)
    elif mx == c[1]:
        hue = 60 * ((c[2] - c[0]) / (mx - mn) + 2)
    else:
        hue = 60 * ((c[0] - c[1]) / (mx - mn) + 4)
    return {"luma": round(float(y.mean()), 3), "p02": round(float(np.percentile(y, 2)), 3), "R-B": round(float(x[..., 0].mean() - x[..., 2].mean()), 3),
            "hue": round(float(hue), 1), "sat": round(float(S.sat_map(x).mean()), 3)}


def patch(x, box):
    x0, y0, x1, y1 = box; c = x[y0:y1, x0:x1].reshape(-1, 3).mean(0)
    return {"RGB": [int(round(v * 255)) for v in c], "R-B": round(float(c[0] - c[2]), 3), "sat": round(float((c.max() - c.min()) / max(c.max(), 1e-3)), 2)}


def cmd_preview(name, sets, sheet=None, boxes=()):
    q = shot(name); tiles = []
    for kv in sets:
        o = parse(kv); tr, smp, _ = treatment(q, o)
        x = tr(smp[len(smp) // 2])
        pt = "  ".join(f"patch{i}={patch(x, b)}" for i, b in enumerate(boxes))
        print(f"{name} [{kv or 'shot_look default'}]  {stats(x)}  {pt}  {tr.record()}")
        tiles.append(Image.fromarray((np.clip(x, 0, 1) * 255 + 0.5).astype(np.uint8)).resize((360, 640), Image.LANCZOS))
    if sheet:
        w = Image.new("RGB", (360 * len(tiles), 640)); [w.paste(t, (360 * i, 0)) for i, t in enumerate(tiles)]; w.save(sheet, quality=90)


def cmd_render(name, kv, out):
    q = shot(name); o = parse(kv); T = time.time()
    tr, _, sf = treatment(q, o)
    clip = str(R / q["clip"]); crop = tuple(q["crop"])
    hf = int(round(0.3 * sf)); t0 = max(0.0, q["in"] - hf / sf); pa = int(round((q["in"] - t0) * sf)); n_src = pa + q["frames"] + hf
    size = S.frame_size(clip); view = S.view_rect(size, crop)
    dn = params(o)["denoise"]; vf = f"{dn},format=rgb24" if dn else "format=rgb24"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{size[0]}x{size[1]}", "-r", "25", "-i", "-",
                            "-vf", f"scale=out_color_matrix=bt709:out_range=tv,format=yuv422p10le,{S.BT709}", "-c:v", "prores_ks", "-profile:v", "3",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+write_colr", str(out)], stdin=subprocess.PIPE)
    n = 0
    for n, fr in enumerate(S.decode_stream(clip, t0, n_src, vf, size), 1):
        enc.stdin.write((tr(fr, seed=n, view=view) * 255 + 0.5).clip(0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    rec = {"clip": q["clip"], "src_start": round(t0, 4), "src_fps": sf, "played_at": 25, "frames": n, "size": list(size), "place_in_frames": pa,
           "look": str(LOOK.relative_to(R.parents[1])), "crop": list(crop), "full": True, "overrides": o, **tr.record(), "secs": round(time.time() - T)}
    Path(out).with_suffix(".json").write_text(json.dumps(rec, indent=1))
    print(f"✓ {Path(out).name}: {n} frames in {rec['secs']} s, overrides {o}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "preview":
        sheet, boxes = None, []
        if "--sheet" in a: i = a.index("--sheet"); sheet = a[i + 1]; a = a[:i] + a[i + 2:]
        while "--patch" in a: i = a.index("--patch"); boxes.append(tuple(int(v) for v in a[i + 1].split(","))); a = a[:i] + a[i + 2:]
        cmd_preview(a[1], a[2:] or [""], sheet, boxes)
    elif a[0] == "render":
        cmd_render(a[1], a[2], a[a.index("-o") + 1])
