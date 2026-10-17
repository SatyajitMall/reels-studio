#!/usr/bin/env python3
"""Score every 1 s window of every clip and shortlist each clip's best moments.

Measures per window: sharpness (Laplacian / luma), colourfulness, highlight contrast (p98),
high-frequency shake, pan speed, exposure and crushed shadows. The score rewards sharp,
colourful, contrasty, steady moments and penalises shake, whip-fast pans and crushed frames.
In the my-reel pilot this found better shots than picking from mid-frames.

Writes <out>/selects_windows.json (every window), <out>/selects.json (top moments per clip,
ranked overall) and <out>/selects.md. Review the shortlist by eye before writing the EDL.

Usage:
  ./.venv/bin/python scripts/selects_score.py projects/<reel>/raw/b-roll -o projects/<reel>/analysis \
      [--skip C008,C018] [--top 3] [--window 1.0]
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter1d

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mxf", ".mkv"}
W, H, FPS = 180, 320, 10  # analysis size (9:16) and sample rate
SCALE = 1080 / W          # shift px → 1080-wide px


def clip_id(p: Path) -> str:
    return p.stem.split("_")[-1]


def shift(a: np.ndarray, b: np.ndarray, win: np.ndarray) -> tuple[float, float]:
    """Global translation between two frames by phase correlation (1080-wide px)."""
    A = np.fft.fft2((a - a.mean()) * win)
    B = np.fft.fft2((b - b.mean()) * win)
    R = A * np.conj(B)
    R /= np.abs(R) + 1e-6
    c = np.fft.ifft2(R).real
    y, x = np.unravel_index(c.argmax(), c.shape)
    if y > a.shape[0] / 2:
        y -= a.shape[0]
    if x > a.shape[1] / 2:
        x -= a.shape[1]
    return x * SCALE, y * SCALE


def windows_for(path: Path, window_s: float) -> list[dict]:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={FPS},scale={W}:{H}",
                          "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8)
    if fr.size < W * H * 3 * 12:
        return []
    fr = fr[: fr.size // (W * H * 3) * W * H * 3].reshape(-1, H, W, 3).astype(np.float32) / 255
    Y = fr @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    win = np.outer(np.hanning(H), np.hanning(W)).astype(np.float32)
    sh = np.array([shift(Y[i], Y[i + 1], win) for i in range(len(Y) - 1)] + [(0.0, 0.0)])
    hp = sh - gaussian_filter1d(sh, 2, axis=0)
    shake = np.hypot(*hp.T)
    speed = np.hypot(*gaussian_filter1d(sh, 3, axis=0).T)
    lap = np.abs(4 * Y[:, 1:-1, 1:-1] - Y[:, :-2, 1:-1] - Y[:, 2:, 1:-1] - Y[:, 1:-1, :-2] - Y[:, 1:-1, 2:]).mean((1, 2))
    sharp = lap / (Y.mean((1, 2)) + 0.05)
    r, g, b = fr[..., 0], fr[..., 1], fr[..., 2]
    rg, yb = r - g, 0.5 * (r + g) - b
    colour = np.sqrt(rg.std((1, 2)) ** 2 + yb.std((1, 2)) ** 2) + 0.3 * np.sqrt(rg.mean((1, 2)) ** 2 + yb.mean((1, 2)) ** 2)
    luma = Y.mean((1, 2))
    crush = (Y < 0.03).mean((1, 2))
    p98 = np.percentile(Y.reshape(len(Y), -1), 98, axis=1)

    n = max(int(round(window_s * FPS)), 2)
    rows = []
    for s in range(0, len(Y) - n + 1, max(n // 2, 1)):
        e = s + n
        rows.append({"clip": clip_id(path), "file": path.name, "t0": round(s / FPS, 2), "t1": round(e / FPS, 2),
                     "sharp": float(sharp[s:e].mean()), "shake": float(shake[s:e].mean()),
                     "speed": float(speed[s:e].mean()), "colour": float(colour[s:e].mean()),
                     "luma": float(luma[s:e].mean()), "crush": float(crush[s:e].mean()), "p98": float(p98[s:e].mean())})
    return rows


def score(rows: list[dict]) -> None:
    """z-score each metric across the whole shoot, then combine."""
    def z(k: str) -> np.ndarray:
        v = np.array([r[k] for r in rows])
        return (v - v.mean()) / (v.std() + 1e-9)
    zs = {k: z(k) for k in ("sharp", "shake", "colour", "p98", "luma", "crush")}
    speed = np.array([r["speed"] for r in rows])
    # Pans are fine; whip-fast movement (> ~40 px/step at 10 fps in 1080 space) isn't.
    whip = np.clip((speed - 40) / 40, 0, None)
    total = (1.0 * zs["sharp"] + 0.8 * zs["colour"] + 0.5 * zs["p98"]
             - 1.0 * zs["shake"] - 0.6 * zs["crush"] - 0.8 * whip + 0.2 * zs["luma"])
    for r, s in zip(rows, total):
        r["score"] = round(float(s), 3)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--skip", default="", help="comma-separated clip ids to skip (e.g. unusable or upside-down clips)")
    ap.add_argument("--top", type=int, default=3, help="best moments to keep per clip")
    ap.add_argument("--window", type=float, default=1.0, help="window length in seconds")
    args = ap.parse_args()

    skip = {s.strip() for s in args.skip.split(",") if s.strip()}
    files: list[Path] = []
    for p in args.inputs:
        files += sorted(f for f in p.iterdir() if f.suffix.lower() in VIDEO_EXT and not f.name.startswith("._")) \
            if p.is_dir() else [p]
    files = [f for f in files if clip_id(f) not in skip]

    rows: list[dict] = []
    for f in files:
        rows += windows_for(f, args.window)
        print(f"▸ {f.name}", flush=True)
    if not rows:
        raise SystemExit("No windows scored.")
    score(rows)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "selects_windows.json").write_text(json.dumps(rows))

    # Top moments per clip, at least one window apart.
    best: list[dict] = []
    for cid in sorted({r["clip"] for r in rows}):
        picks: list[dict] = []
        for r in sorted((r for r in rows if r["clip"] == cid), key=lambda r: -r["score"]):
            if all(abs(r["t0"] - p["t0"]) >= args.window for p in picks):
                picks.append(r)
            if len(picks) == args.top:
                break
        best += picks
    best.sort(key=lambda r: -r["score"])
    (args.out / "selects.json").write_text(json.dumps(best, indent=1))

    md = ["# Selects", "", f"Top {args.top} moments per clip ({args.window} s windows), ranked across the shoot. "
          "Score = sharpness + colour + highlight contrast − shake − crushed shadows − whip pans. "
          "**Review by eye before using**: the score can't judge meaning, faces or composition.", "",
          "| # | Clip | In | Out | Score | Sharp | Shake | Pan speed | Luma |", "|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(best[:60], 1):
        md.append(f"| {i} | {r['clip']} | {r['t0']} s | {r['t1']} s | {r['score']} | {r['sharp']:.3f} | "
                  f"{r['shake']:.1f} | {r['speed']:.1f} | {r['luma']:.2f} |")
    (args.out / "selects.md").write_text("\n".join(md) + "\n")
    print(f"✓ {args.out / 'selects.md'} ({len(best)} moments from {len(files)} clips)")


if __name__ == "__main__":
    main()
