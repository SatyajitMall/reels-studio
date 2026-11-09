#!/usr/bin/env python3
"""Small ffprobe helpers shared by the studio scripts (v0.9.1).

`fps_of` replaces five copies of a csv parser that crashed on the director's camera files: Blackmagic Cam files carry a
rotation side-data block, and ffprobe's `-of csv=p=0` then prints `25/1,` (and the stream twice), so
`float("1,")` raised ValueError in shake_report, colour_report, frame_scan and render_diff (CR-20261107-kolkata-preview-fx,
CR-20261107-kolkata-film-emulation-first-use). JSON output has no such trailing field.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


def _rate(value: str | None) -> float:
    """'25/1' → 25.0, '30000/1001' → 29.97; 0 for '0/0', '', or anything unparsable."""
    num, _, den = (value or "").strip().partition("/")
    try:
        n, d = float(num), float(den or 1)
    except ValueError:
        return 0.0
    return n / d if n > 0 and d > 0 else 0.0


def fps_of(path: Path | str, default: float = 25.0) -> float:
    """The first video stream's frame rate: avg_frame_rate, else r_frame_rate, else `default`."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=avg_frame_rate,r_frame_rate", "-of", "json", str(path)],
                         capture_output=True, text=True).stdout
    try:
        stream = (json.loads(out or "{}").get("streams") or [{}])[0]
    except ValueError:
        return default
    return _rate(stream.get("avg_frame_rate")) or _rate(stream.get("r_frame_rate")) or default


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        print(f"{fps_of(p):.3f}  {p}")
