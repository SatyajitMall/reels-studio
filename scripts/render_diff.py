#!/usr/bin/env python3
"""What changed between two renders of a reel: the scope of a focused review (review-gate.md, loop 2 and fix versions).

Compares the two files frame by frame (colour, 54×96: small enough that H.264 noise averages out, while a saturation-only change still counts) and the decoded audio:
  - the spans of frames that differ (mean abs difference > --thresh on 0–255), merged across gaps < 3 frames,
    with the shot names from --shots;
  - whether the audio is identical (md5 of the decoded PCM);
  - "structure": the same frame count and the same shot boundaries (--prev-shots vs --shots, ±1 frame) → a focused review
    of the changed shots is enough; a different length or moved, added or removed cuts → the cut changed, so the next
    review is a full one. Without both shot lists the structure is "unknown" (full review).

Writes <out>.json and prints a summary. Exit 0 always (it informs; pregate.py decides).

Usage:
  ./.venv/bin/python scripts/render_diff.py <previous export> <new export> -o <out.json> \
      --prev-shots map_v<N-1>.json --shots map_vN.json
Shot lists: a list of [name, start_s, end_s] or the camera_fidelity map (objects with name/start/end).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

W, H = 54, 96


def frames(path: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-an", "-vf", f"scale={W}:{H}:flags=area,format=rgb24",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8)
    return fr[: fr.size // (W * H * 3) * W * H * 3].reshape(-1, H, W, 3)


def audio_md5(path: Path) -> str | None:
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "2", "-ar", "48000", "-f", "s16le", "-"],
                       capture_output=True)
    return hashlib.md5(p.stdout).hexdigest() if p.stdout else None


def fps_of(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=avg_frame_rate",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip()
    n, d = (out.splitlines()[0] if out else "25/1").split("/")
    return float(n) / float(d) if float(d) else 25.0


def load_shots(path: Path | None) -> list[tuple[str, float, float]]:
    if not path:
        return []
    out = []
    for s in json.loads(path.read_text()):
        out.append((s["name"], s["start"], s["end"]) if isinstance(s, dict) else (s[0], s[1], s[2]))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prev", type=Path)
    ap.add_argument("new", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--shots", type=Path, help="the new version's shots")
    ap.add_argument("--prev-shots", type=Path, help="the previous version's shots")
    ap.add_argument("--thresh", type=float, default=0.7, help="mean abs difference (0–255) that counts as changed; H.264 noise sits near 0.4")
    a = ap.parse_args()

    fps = fps_of(a.new)
    A, B = frames(a.prev), frames(a.new)
    shots = load_shots(a.shots)
    rep: dict = {"prev": str(a.prev), "new": str(a.new), "fps": fps, "frames": [len(A), len(B)]}
    ma, mb = audio_md5(a.prev), audio_md5(a.new)
    rep["audio_identical"] = ma == mb                 # two silent files (None) count as identical
    spans = []
    if len(A) == len(B):
        d = np.array([np.abs(A[i].astype(np.int16) - B[i]).mean() for i in range(len(A))])
        on = d > a.thresh
        i = 0
        while i < len(on):
            if on[i]:
                j = i
                while j < len(on) and (on[j] or (j + 3 < len(on) and on[j:j + 3].any())):
                    j += 1
                t0, t1 = i / fps, j / fps
                names = [n for n, s0, s1 in shots if s0 < t1 and s1 > t0]
                spans.append({"t0": round(t0, 2), "t1": round(t1, 2), "frames": [i, j - 1], "max_diff": round(float(d[i:j].max()), 2),
                              "shots": names})
                i = j
            else:
                i += 1
    rep["changed_spans"] = spans
    if len(A) != len(B):
        rep["structure"] = "changed"
    elif not shots or not a.prev_shots:
        rep["structure"] = "unknown"
    else:
        def bounds(sh):
            return sorted({round(t * fps) for _, s0, s1 in sh for t in (s0, s1)})
        ba, bb = bounds(load_shots(a.prev_shots)), bounds(shots)
        rep["structure"] = "same" if len(ba) == len(bb) and all(abs(x - y) <= 1 for x, y in zip(ba, bb)) else "changed"
    rep["changed_shots"] = sorted({n for s in spans for n in s["shots"]})
    rep["scope"] = "full review (the cut changed or is unknown)" if rep["structure"] != "same" else \
        ("focused review of the changed shots" if spans else
         "focused review of the sound only (picture unchanged)" if not rep["audio_identical"] else "no change: no review needed")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(rep, indent=1))
    print(f"structure {rep['structure']} · audio {'identical' if rep['audio_identical'] else 'CHANGED'} · {len(spans)} changed span(s)")
    for s in spans:
        print(f"  {s['t0']:6.2f}–{s['t1']:6.2f} s  frames {s['frames'][0]}–{s['frames'][1]}  max Δ {s['max_diff']}  {', '.join(s['shots'])}")
    print(f"→ {rep['scope']} · {a.out}")


if __name__ == "__main__":
    main()
