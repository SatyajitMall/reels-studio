#!/usr/bin/env python3
"""Reference-matched look, baked per shot (the "baked look" route, effects-playbook §A6).

Promoted from Pujo ki Asolei Sobar (tools/cine_look.py, ref_look.py, shot_render_v5.py), where the director approved
round 11's "natural, but warmer and matched" mode. That mode is the default here. Strengths are partial on purpose:
the director's round-11 note on full strengths was "over-processed and not natural".

Per frame:
  decode (+ reframe crop) → light denoise (hqdn3d 0.8:0.6:2:1.5, at source size) → lanczos to 1080×1920
  → CORRECT: white balance from near-neutral pixels (power 0.6) + tonal levels toward p02/p50/p98 0.035/0.30/0.86 (65 %)
  → clarity (fine detail 0.12)
  → LOOK (pixelwise; exportable as .cube): filmic tone curve + 3-way R/B balance + saturation, fitted to the reference
    reel's measured grade, mixed at 75 %
  → cast match toward the reference's midtone R/G, B/G (60 %) → saturation cap (the reference's median saturation)
  → optical: halation 0.06, vignette 0.12, grain 0.006, black floor 0.025
  → exposure: halfway between the shot's own level and the reference's mean luma.
Constants are measured per shot, on frames that are on screen, so a shot never pumps.

Not in this version (Pujo had them; add per reel if needed): person-gated skin anchor, stabilisation, deflicker.

Commands:
  measure  <reference.mp4> -o ref_stats.json [--frames 18] [--skip-band 0.74,0.88]
  fit      --ref ref_stats.json -o look.json  <shot> ...      fit the look on corrected stills of these shots
  preview  --look look.json [--look look_b.json] [--ours export.mp4] -o sheet.jpg  <shot> ...
  render   --look look.json --clip <src.mov> --in <s> --frames <n> --fps 25 [--crop m,u0,v0] [--handle 0.3] [--full] -o out.mov
  cube     --look look.json -o look.cube                       the LOOK step only, for Lumetri → Creative → Look (by hand)

render: the shot is reframed in the bake (1080×1920 out), or with --full kept at the camera's own size so Premiere's
reframe and push keyframes still fit (replace the clip's media; the file has the same pixel size). With --full, --crop
is the on-screen area: the constants are measured there and the vignette is centred on it. No grain is baked with
--full (V4 adds it, at 0–5 % on night shots). Every source frame plays once at --fps, as when a clip is conformed by
interpretation (CLAUDE.md §3), so --in is in source seconds and --frames counts source frames.

<shot> = clip.mov@seconds[@m,u0,v0[@t_ours]]: source time, optional reframe (magnification m, crop centre u0,v0 in
0–1 of the source frame, as in a reel's crops file) and the time of that shot in --ours (for the comparison column).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage, optimize

W, H = 1080, 1920
TX = np.array([0.0, 0.05, 0.15, 0.30, 0.50, 0.70, 0.90, 1.0])
NATURAL_MATCHED = {"wb": 0.6, "levels": 0.65, "clarity": 0.12, "look_mix": 0.75, "cast": 0.6, "hal": 0.06, "vig": 0.12,
                   "grain": 0.006, "floor": 0.025, "denoise": "hqdn3d=0.8:0.6:2:1.5"}
LEVELS_OUT = np.array([0.0, 0.035, 0.30, 0.86, 0.97])
BT709 = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"


def luma(x: np.ndarray) -> np.ndarray:
    return x @ np.array([0.2126, 0.7152, 0.0722], dtype=x.dtype)


def sat_map(x: np.ndarray) -> np.ndarray:
    mx, mn = x.max(-1), x.min(-1)
    return np.where(mx > 1e-3, (mx - mn) / np.maximum(mx, 1e-3), 0)


# ---------- measuring a grade ----------
def stats(x: np.ndarray) -> dict:
    y = luma(x)
    r = {"luma": float(y.mean()), "p02": float(np.percentile(y, 2)), "p50": float(np.percentile(y, 50)),
         "p98": float(np.percentile(y, 98)), "sat": float(sat_map(x).mean())}
    for nm, (lo, hi) in {"shad": (0, 0.2), "mid": (0.2, 0.6), "high": (0.6, 1.01)}.items():
        m = (y >= lo) & (y < hi)
        g = x[..., 1][m].mean() if m.sum() > 300 else 0
        r[nm] = [float(x[..., 0][m].mean() / g), float(x[..., 2][m].mean() / g)] if g > 1e-3 else None
    return r


def median_stats(S: list[dict]) -> dict:
    out = {k: float(np.median([s[k] for s in S])) for k in ("luma", "p02", "p50", "p98", "sat")}
    for b in ("shad", "mid", "high"):
        v = [s[b] for s in S if s[b]]
        out[b] = [float(np.median([a[0] for a in v])), float(np.median([a[1] for a in v]))] if v else [1.0, 1.0]
    return out


# ---------- decoding ----------
def probe(path: str) -> tuple[float, float]:
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=avg_frame_rate:format=duration",
                        "-of", "json", path], capture_output=True, text=True, check=True)
    j = json.loads(p.stdout)
    n, d = j["streams"][0]["avg_frame_rate"].rstrip(",").split("/")
    return float(j["format"]["duration"]), float(n) / float(d)


def crop_filter(crop: tuple[float, float, float] | None) -> str:
    cw0, ch0 = "min(iw,ih*9/16)", "min(ih,iw*16/9)"
    if not crop:
        return f"crop='{cw0}':'{ch0}'"
    m, u0, v0 = crop
    cw, ch = f"{cw0}/{m}", f"{ch0}/{m}"
    return f"crop='{cw}':'{ch}':'max(0,min(iw-{cw},iw*{u0}-{cw}/2))':'max(0,min(ih-{ch},ih*{v0}-{ch}/2))'"


def decode(path: str, t: float, n: int = 1, crop=None, denoise: str | None = None, width: int = W) -> np.ndarray:
    h = round(width * 16 / 9 / 2) * 2
    vf = ",".join(x for x in [crop_filter(crop), denoise, f"scale={width}:{h}:flags=lanczos", "format=rgb24"] if x)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(t, 0):.3f}", "-i", path, "-an", "-frames:v", str(n), "-vf", vf,
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, width, 3).astype(np.float32) / 255


def frame_size(path: str) -> tuple[int, int]:
    """Display size after rotation, as Premiere reads it."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                         capture_output=True, check=True).stdout
    return Image.open(BytesIO(raw)).size


def decode_stream(path: str, t: float, n: int, vf: str, size: tuple[int, int]):
    """Frames one at a time (a 4K shot doesn't fit in memory as float)."""
    w, h = size
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{max(t, 0):.3f}", "-i", path, "-an", "-frames:v", str(n), "-vf", vf,
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    while (buf := pr.stdout.read(w * h * 3)) and len(buf) == w * h * 3:
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3).astype(np.float32) / 255
    pr.wait()


def view_rect(size: tuple[int, int], crop) -> tuple[float, float, float, float]:
    """The on-screen area (x0, y0, w, h) of a full frame, matching crop_filter."""
    w, h = size
    cw, ch = min(w, h * 9 / 16), min(h, w * 16 / 9)
    if not crop:
        return (w - cw) / 2, (h - ch) / 2, cw, ch
    m, u0, v0 = crop
    cw, ch = cw / m, ch / m
    return max(0, min(w - cw, w * u0 - cw / 2)), max(0, min(h - ch, h * v0 - ch / 2)), cw, ch


def decode_plain(path: str, t: float, width: int, skip_band=None) -> np.ndarray:
    """A frame at its own aspect (reference, or our export), optional subtitle band removed."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-vf", f"scale={width}:-2",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    a = np.asarray(Image.open(BytesIO(raw)).convert("RGB"), np.float32) / 255
    if skip_band:
        keep = np.ones(a.shape[0], bool)
        keep[int(a.shape[0] * skip_band[0]): int(a.shape[0] * skip_band[1])] = False
        a = a[keep]
    return a


# ---------- the treatment ----------
def wb_gains(x: np.ndarray, power: float) -> np.ndarray:
    y, ch = luma(x), sat_map(x)
    m = (y > 0.12) & (y < 0.85)
    if m.sum() < 1000:
        m = y > 0.03
    m = m & (ch <= np.percentile(ch[m], 30))            # near-neutral pixels: walls, cloth, skin shadows
    R, G, B = (np.median(x[..., c][m]) for c in range(3))
    return np.array([(G / max(R, 1e-4)) ** power, 1.0, (G / max(B, 1e-4)) ** power])


class Correction:
    """Per-shot constants (white balance, tonal levels), measured once on frames that are on screen."""

    def __init__(self, samples: list[np.ndarray], p: dict):
        self.wb = np.median([wb_gains(x, p["wb"]) for x in samples], axis=0)
        ys = np.concatenate([luma(np.clip(x * self.wb, 0, 1)).ravel()[::7] for x in samples])
        tin = np.array([0.0, *np.percentile(ys, [2, 50, 98]), 1.0])
        self.tin = np.maximum.accumulate(tin + np.arange(5) * 1e-4)
        self.tout = p["levels"] * LEVELS_OUT + (1 - p["levels"]) * tin
        self.clar = p["clarity"]

    def __call__(self, x: np.ndarray, px: float = 1.0) -> np.ndarray:
        """px = source pixels per output pixel (a --full frame is finer than the 1080-wide view it ends up in)."""
        x = np.clip(x * self.wb, 0, 1.2)
        y = np.clip(luma(x), 1e-5, None)
        x = np.clip(x * (np.interp(y, self.tin, self.tout) / y)[..., None], 0, 1)
        if self.clar:
            y = luma(x)
            y2 = np.clip(y + self.clar * (y - ndimage.gaussian_filter(y, 1.1 * px)), 0, 1)
            x = np.clip(x * (y2 / np.maximum(y, 1e-4))[..., None], 0, 1)
        return x


def look(x: np.ndarray, L: dict) -> np.ndarray:
    if "parts" in L:                                    # a blend of looks (`blend` command): still one pixelwise look
        return sum(w * look(x, P) for P, w in L["parts"])
    ty = np.maximum.accumulate(np.array(L["ty"]))
    y = np.clip(luma(x), 1e-5, 1)
    x = x * (np.interp(y, TX, ty) / y)[..., None]
    y2 = luma(x)
    ws = np.clip(1 - y2 / 0.25, 0, 1) ** 1.3
    wh = np.clip((y2 - 0.45) / 0.35, 0, 1) ** 1.3
    wm = np.clip(1 - ws - wh, 0, 1)
    x = x * sum(np.array(L[k])[None, None, :] * w[..., None] for k, w in (("gs", ws), ("gm", wm), ("gh", wh)))
    yy = luma(x)[..., None]
    return np.clip(yy + (x - yy) * L["sat"], 0, 1)


def optical(x: np.ndarray, p: dict, seed: int, view=None) -> np.ndarray:
    """view = the on-screen (x0, y0, w, h) of a --full frame; sizes are relative to it."""
    h, w = x.shape[:2]
    vx, vy, vw, vh = view or (0, 0, w, h)
    y = luma(x)
    if p["hal"]:
        hi = np.clip((y - 0.80) / 0.20, 0, 1)[..., None] * x
        k = max(1, int(w // 1080))                      # blur a reduced copy: the bloom is soft anyway
        if k > 1:
            hi = hi[: h // k * k, : w // k * k].reshape(h // k, k, w // k, k, 3).mean((1, 3))
        s = vw / 1080 * 26 / k
        bloom = np.stack([ndimage.gaussian_filter(hi[..., c], s) for c in range(3)], -1) * np.array([1.0, 0.62, 0.34])
        if k > 1:
            bloom = np.pad(np.repeat(np.repeat(bloom, k, 0), k, 1), ((0, h - h // k * k), (0, w - w // k * k), (0, 0)), mode="edge")
            bloom = ndimage.uniform_filter(bloom, (k, k, 1))
        x = 1 - (1 - x) * (1 - p["hal"] * bloom)
    fl = p["floor"]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - vx - vw / 2) / (vw / 2)) ** 2 + ((yy - vy - vh * 0.46) / (vh / 2)) ** 2)
    x = fl + (x - fl) * (1 - p["vig"] * np.clip((d - 0.45) / 0.85, 0, 1) ** 1.5)[..., None]
    if p["grain"]:
        g = np.random.default_rng(seed).normal(0, 1, (h // 2, w // 2)).astype(np.float32)
        g = np.asarray(Image.fromarray(g).resize((w, h), Image.BICUBIC))
        x = x + g[..., None] * p["grain"] * (1 - np.abs(luma(x) - 0.5)[..., None] * 1.2)
    return np.clip(x, 0, 1)


class Treatment:
    """Correction → look → cast match → saturation cap → optical → exposure, constants fixed per shot."""

    def __init__(self, samples: list[np.ndarray], L: dict, p: dict = NATURAL_MATCHED):
        self.L, self.p = L, p
        self.corr = Correction(samples, p)
        pre = [self._look(self.corr(x)) for x in samples]
        tr, tb = L["cast_target"]

        def cast(x):
            y, ch = luma(x), sat_map(x)
            m = (y > 0.18) & (y < 0.7) & (ch < 0.35)
            if m.sum() < 500:
                m = (y > 0.15) & (y < 0.8)
            R, G, B = (x[..., c][m].mean() for c in range(3))
            return np.array([(tr * G / R) ** p["cast"], 1.0, (tb * G / B) ** p["cast"]])

        self.cg = np.median([cast(x[::4, ::4]) for x in pre], axis=0)
        s = np.mean([sat_map(np.clip(x * self.cg, 0, 1)[::4, ::4]).mean() for x in pre])
        self.sk = min(1.0, L["sat_cap"] / max(s, 1e-3)) ** 1.15
        own = np.mean([luma(self.corr(x)).mean() for x in samples])
        target = 0.5 * own + 0.5 * L["luma_target"]
        mids = [self._finish(x, 1.0, seed=0) for x in samples]
        self.gain = float(np.clip((target - p["floor"]) / max(np.mean([luma(m).mean() for m in mids]) - p["floor"], 1e-3), 0.75, 1.6))

    def _look(self, x):
        return self.p["look_mix"] * look(x, self.L) + (1 - self.p["look_mix"]) * x

    def _finish(self, x, gain, seed, view=None):
        x = np.clip(self._look(self.corr(x, view[2] / 1080 if view else 1.0)) * self.cg, 0, 1)
        if self.sk < 0.999:
            yy = luma(x)[..., None]
            x = np.clip(yy + (x - yy) * self.sk, 0, 1)
        o = optical(x, self.p, seed, view)
        fl = self.p["floor"]
        return np.clip(fl + (o - fl) * gain, fl - 0.005, 1)

    def __call__(self, x, seed=0, view=None):
        return self._finish(x, self.gain, seed, view)

    def record(self) -> dict:
        return {"wb": np.round(self.corr.wb, 4).tolist(), "levels_in": np.round(self.corr.tin[1:4], 4).tolist(),
                "cast_gains": np.round(self.cg, 4).tolist(), "sat_k": round(self.sk, 3), "gain": round(self.gain, 3)}


# ---------- fitting the look to a reference ----------
def unpack(v):
    return {"ty": list(map(float, v[:8])), "gs": [float(v[8]), 1.0, float(v[9])], "gm": [float(v[10]), 1.0, float(v[11])],
            "gh": [float(v[12]), 1.0, float(v[13])], "sat": float(v[14])}


def pack(L):
    return np.array(L["ty"] + L["gs"][::2] + L["gm"][::2] + L["gh"][::2] + [L["sat"]])


def fit_look(corrected: list[np.ndarray], ref: dict) -> tuple[dict, float]:
    def loss(v):
        m = median_stats([stats(look(f, unpack(v))) for f in corrected])
        e = sum(w * (m[k] - ref[k]) ** 2 for k, w in (("luma", 6), ("p02", 4), ("p50", 6), ("p98", 5), ("sat", 4)))
        e += sum(w * ((m[b][0] - ref[b][0]) ** 2 + (m[b][1] - ref[b][1]) ** 2) for b, w in (("mid", 6), ("high", 3), ("shad", 0.5)))
        gains = np.array(v[8:14])
        return e + 0.05 * np.sum(np.clip(np.abs(gains - 1) - 0.25, 0, None) ** 2)   # keep channel gains plausible
    x0 = pack({"ty": [0.02, 0.055, 0.15, 0.30, 0.50, 0.68, 0.84, 0.92], "gs": [1, 1, 1], "gm": [1, 1, 1], "gh": [1, 1, 1], "sat": 1.0})
    res = optimize.minimize(loss, x0, method="Powell", options={"maxiter": 4000, "xtol": 1e-3, "ftol": 1e-7})
    return unpack(res.x), float(res.fun)


# ---------- shots ----------
def parse_shot(s: str):
    parts = s.split("@")
    crop = tuple(float(v) for v in parts[2].split(",")) if len(parts) > 2 and parts[2] else None
    t_ours = float(parts[3]) if len(parts) > 3 else None
    return parts[0], float(parts[1]), crop, t_ours


def shot_samples(clip, t, crop, p, width, n=4, span=0.6):
    """A few denoised frames around t (temporal denoise needs neighbours: decode 5, keep the middle)."""
    out = []
    for dt in np.linspace(-span / 2, span / 2, n):
        fr = decode(clip, t + dt - 0.08, 5, crop, p["denoise"], width)
        out.append(fr[len(fr) // 2])
    return out


def load_look(path: str) -> dict:
    L = json.loads(Path(path).read_text())
    ref = L.get("ref", {})
    L.setdefault("cast_target", ref.get("mid", [1.05, 0.80]))
    L.setdefault("sat_cap", ref.get("sat", 0.38))
    L.setdefault("luma_target", ref.get("luma", 0.28))
    return L


# ---------- commands ----------
def cmd_measure(a):
    dur, _ = probe(a.reference)
    ts = np.linspace(0.5, dur - 0.5, a.frames)
    band = tuple(float(v) for v in a.skip_band.split(",")) if a.skip_band else None
    S = [stats(decode_plain(a.reference, t, 480, band)) for t in ts]
    out = {"reference": a.reference, "frames": len(S), "median": median_stats(S)}
    Path(a.out).write_text(json.dumps(out, indent=1))
    print(json.dumps(out["median"], indent=1))


def cmd_fit(a):
    ref = json.loads(Path(a.ref).read_text())["median"]
    p = NATURAL_MATCHED
    corrected = []
    for s in a.shots:
        clip, t, crop, _ = parse_shot(s)
        smp = shot_samples(clip, t, crop, p, 180, n=3)
        c = Correction(smp, p)
        corrected += [c(x) for x in smp]
    T = time.time()
    L, err = fit_look(corrected, ref)
    L.update({"ref": ref, "cast_target": ref["mid"], "sat_cap": ref["sat"], "luma_target": ref["luma"], "fit_loss": round(err, 6),
              "fit_shots": a.shots, "mode": "natural-matched"})
    Path(a.out).write_text(json.dumps(L, indent=1))
    got = median_stats([stats(look(f, L)) for f in corrected])
    print(f"fit in {time.time() - T:.0f} s, loss {err:.5f}")
    for k in ("luma", "p02", "p50", "p98", "sat"):
        print(f"  {k:<5} ref {ref[k]:.3f}  fitted {got[k]:.3f}")
    for b in ("shad", "mid", "high"):
        print(f"  {b:<5} ref R/G {ref[b][0]:.3f} B/G {ref[b][1]:.3f}   fitted {got[b][0]:.3f} {got[b][1]:.3f}")


def cmd_preview(a):
    looks = [(Path(l).stem, load_look(l)) for l in a.look]
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 15)
    tw, rows, report = a.tile, [], {}
    for s in a.shots:
        clip, t, crop, t_ours = parse_shot(s)
        smp = shot_samples(clip, t, crop, NATURAL_MATCHED, 540)
        x = smp[len(smp) // 2]
        raw = decode(clip, t, 1, crop, None, 540)[0]
        cols = [("camera original", raw)]
        if a.ours and t_ours is not None:
            cols.append(("current export", decode_plain(a.ours, t_ours, 540)))
        for name, L in looks:
            tr = Treatment(smp, L)
            o = tr(x)
            cols.append((f"baked: {name}", o))
            report[f"{Path(clip).stem}@{t}|{name}"] = tr.record() | {k: round(v, 3) for k, v in stats(o).items() if not isinstance(v, list)}
        rows.append((Path(clip).stem.split("_")[-1], cols))
    th = round(tw * 16 / 9)
    ncol = max(len(c) for _, c in rows)
    sheet = Image.new("RGB", (tw * ncol, 26 + th * len(rows)), (14, 14, 14))
    d = ImageDraw.Draw(sheet)
    for n, (name, _) in enumerate(rows[0][1]):
        d.text((n * tw + 6, 5), name, font=font, fill=(240, 210, 80))
    for r, (lab, cols) in enumerate(rows):
        for n, (_, im) in enumerate(cols):
            t = Image.fromarray((np.clip(im, 0, 1) * 255 + 0.5).astype(np.uint8)).resize((tw, th), Image.LANCZOS)
            sheet.paste(t, (n * tw, 26 + r * th))
        d.text((6, 32 + r * th), lab, font=font, fill=(255, 255, 255))
    sheet.save(a.out, quality=90)
    Path(a.out).with_suffix(".json").write_text(json.dumps(report, indent=1))
    print(f"✓ {len(rows)} shots → {a.out}")


def cmd_render(a):
    L = load_look(a.look)
    p = dict(NATURAL_MATCHED, grain=0.0) if a.full else NATURAL_MATCHED
    crop = tuple(float(v) for v in a.crop.split(",")) if a.crop else None
    _, sf = probe(a.clip)
    hf = int(round(a.handle * sf))
    t0 = max(0.0, a.in_ - hf / sf)
    pa = int(round((a.in_ - t0) * sf))
    n_src = pa + a.frames + hf
    T = time.time()
    # constants from the on-screen area, at view size, over the frames that play
    smp = [decode(a.clip, t, 1, crop, p["denoise"], W)[0] for t in np.linspace(a.in_, a.in_ + (a.frames - 1) / sf, 6)]
    tr = Treatment(smp, L, p)
    if a.full:
        size = frame_size(a.clip)
        view = view_rect(size, crop)
        vf = f"{p['denoise']},format=rgb24"
    else:
        size, view = (W, H), None
        vf = f"{crop_filter(crop)},{p['denoise']},scale={W}:{H}:flags=lanczos,format=rgb24"
    out = Path(a.out)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{size[0]}x{size[1]}", "-r", str(a.fps),
                            "-i", "-", "-vf", f"scale=out_color_matrix=bt709:out_range=tv,format=yuv422p10le,{BT709}",
                            "-c:v", "prores_ks", "-profile:v", "3", "-color_primaries", "bt709", "-color_trc", "bt709",
                            "-colorspace", "bt709", "-movflags", "+write_colr", str(out)], stdin=subprocess.PIPE)
    n = 0
    for n, fr in enumerate(decode_stream(a.clip, t0, n_src, vf, size), 1):
        enc.stdin.write((tr(fr, seed=n, view=view) * 255 + 0.5).clip(0, 255).astype(np.uint8).tobytes())
    enc.stdin.close()
    enc.wait()
    rec = {"clip": a.clip, "src_start": round(t0, 4), "src_fps": sf, "played_at": a.fps, "frames": n, "size": list(size),
           "place_in_frames": pa, "look": a.look, "crop": crop, "full": a.full, **tr.record(), "secs": round(time.time() - T)}
    out.with_suffix(".json").write_text(json.dumps(rec, indent=1))
    print(f"✓ {out.name}: {n} frames in {rec['secs']} s (picture only; every source frame plays once at {a.fps} fps)")


def cmd_blend(a):
    A, B = load_look(a.looks[0]), load_look(a.looks[1])
    w = a.w
    mixv = lambda k: (np.array(A[k]) * (1 - w) + np.array(B[k]) * w).tolist()
    L = {"parts": [[A, 1 - w], [B, w]], "cast_target": mixv("cast_target"), "sat_cap": float(mixv("sat_cap")),
         "luma_target": float(mixv("luma_target")), "blend_of": [a.looks[0], a.looks[1]], "blend_w": w}
    Path(a.out).write_text(json.dumps(L, indent=1))
    print(f"✓ {a.out}: {1 - w:.0%} {Path(a.looks[0]).stem} + {w:.0%} {Path(a.looks[1]).stem}")


def cmd_cube(a, size=33):
    L = load_look(a.look)
    g = np.linspace(0, 1, size, dtype=np.float32)
    b, gg, r = np.meshgrid(g, g, g, indexing="ij")
    grid = np.stack([r, gg, b], -1).reshape(1, -1, 3)
    out = look(grid, L).reshape(-1, 3)
    lines = [f'TITLE "{Path(a.look).stem}"', f"LUT_3D_SIZE {size}"] + [f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}" for v in out]
    Path(a.out).write_text("\n".join(lines) + "\n")
    print(f"✓ {a.out} ({size}³, the LOOK step only, at 100 %: set Lumetri Intensity to {NATURAL_MATCHED['look_mix']:.0%})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("measure"); m.add_argument("reference"); m.add_argument("-o", "--out", required=True)
    m.add_argument("--frames", type=int, default=18); m.add_argument("--skip-band", help="e.g. 0.74,0.88 to skip burned subtitles")
    f = sub.add_parser("fit"); f.add_argument("--ref", required=True); f.add_argument("-o", "--out", required=True); f.add_argument("shots", nargs="+")
    p = sub.add_parser("preview"); p.add_argument("--look", action="append", required=True); p.add_argument("--ours")
    p.add_argument("--tile", type=int, default=300); p.add_argument("-o", "--out", required=True); p.add_argument("shots", nargs="+")
    r = sub.add_parser("render"); r.add_argument("--look", required=True); r.add_argument("--clip", required=True)
    r.add_argument("--in", dest="in_", type=float, required=True); r.add_argument("--frames", type=int, required=True)
    r.add_argument("--fps", type=float, default=25); r.add_argument("--crop"); r.add_argument("--handle", type=float, default=0.3)
    r.add_argument("--full", action="store_true", help="keep the camera's size, for Premiere's own reframe (no grain baked)")
    r.add_argument("-o", "--out", required=True)
    c = sub.add_parser("cube"); c.add_argument("--look", required=True); c.add_argument("-o", "--out", required=True)
    b = sub.add_parser("blend"); b.add_argument("looks", nargs=2); b.add_argument("--w", type=float, default=0.5, help="weight of the 2nd look")
    b.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    {"measure": cmd_measure, "fit": cmd_fit, "preview": cmd_preview, "render": cmd_render, "cube": cmd_cube, "blend": cmd_blend}[a.cmd](a)


if __name__ == "__main__":
    main()
