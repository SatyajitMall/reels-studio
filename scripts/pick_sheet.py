#!/usr/bin/env python3
"""Pick sheet: one row per clip, 6 of its 12 contact frames with their camera times, for choosing shots by what they show
(skill Phase 2). With --all it covers every clip analyze_footage.py analysed, so a VO line is matched against the whole
pool, not a themed shortlist (goddess and Pujo each lost rounds to picks from a shortlist).

Promoted from goddess's and Pujo's own versions. Reads analyze_footage.py's per-clip folders (<analysis>/<clip stem>/
contact.png + stats.json). Blackmagic Cam names (A001_10202151_C061) are labelled with the shoot date and time
(Oct 20 21:51 · C061), because clip numbers repeat across shoots.

Usage (from the studio root):
  ./.venv/bin/python scripts/pick_sheet.py projects/<reel>/analysis --all -o projects/<reel>/analysis/picks/pool.jpg
  ./.venv/bin/python scripts/pick_sheet.py projects/<reel>/analysis A001_10202151_C061="Ma's face|line 3" A001_10211845_C007 \
      -o projects/<reel>/analysis/picks/line3.jpg --title "Line 3: 'when she leaves we cry'"
A label after "=" is printed beside the clip ("|" starts a new line). Pages of --per-page clips (default 10): pool_p1.jpg …
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TW, TH, LW, PICK = 180, 320, 250, [0, 2, 4, 6, 8, 10]
SUP = "/System/Library/Fonts/Supplemental/"
BOLD, REG = ImageFont.truetype(SUP + "Arial Bold.ttf", 21), ImageFont.truetype(SUP + "Arial.ttf", 16)
TITLE = ImageFont.truetype(SUP + "Arial Bold.ttf", 26)
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
BMD = re.compile(r"_(\d{2})(\d{2})(\d{2})(\d{2})_(C\d+)$")


def clip_label(stem: str) -> tuple[str, str]:
    """Blackmagic Cam stem → ('C061', 'Oct 20 21:51'); anything else → (stem, '')."""
    m = BMD.search(stem)
    if not m or not 1 <= int(m.group(1)) <= 12:
        return stem, ""
    mo, day, hh, mm, c = m.groups()
    return c, f"{MONTHS[int(mo) - 1]} {int(day)} {hh}:{mm}"


def tiles(cd: Path, st: dict) -> list[tuple[Image.Image, float]]:
    con = Image.open(cd / "contact.png").convert("RGB")
    n = len(st.get("samples", [])) or 12
    cols = 6 if st.get("orientation", "vertical") == "vertical" else 4      # analyze_footage.py's grid
    rows = (n + cols - 1) // cols
    cw, ch = con.width // cols, con.height // rows
    out = []
    for k in PICK:
        if k >= n:
            break
        r, c = divmod(k, cols)
        tile = con.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch))
        tile.thumbnail((TW, TH), Image.LANCZOS)
        t = st["samples"][k]["t"] if k < len(st.get("samples", [])) else 0.0
        out.append((tile, t))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("analysis", type=Path, help="analyze_footage.py's output folder")
    ap.add_argument("clips", nargs="*", help="clip stems, each optionally =label")
    ap.add_argument("--all", action="store_true", help="every analysed clip")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--per-page", type=int, default=10)
    a = ap.parse_args()

    items: list[tuple[str, str]] = []
    if a.all:
        items = [(d.name, "") for d in sorted(a.analysis.iterdir()) if (d / "stats.json").exists() and (d / "contact.png").exists()]
    for spec in a.clips:
        stem, _, label = spec.partition("=")
        items.append((stem, label))
    if not items:
        sys.exit("No clips: name clip stems or pass --all")
    missing = [s for s, _ in items if not (a.analysis / s / "stats.json").exists()]
    if missing:
        sys.exit(f"Not analysed in {a.analysis}: {', '.join(missing)} (run analyze_footage.py first)")

    pages = [items[i:i + a.per_page] for i in range(0, len(items), a.per_page)]
    for p, page in enumerate(pages, 1):
        sheet = Image.new("RGB", (LW + len(PICK) * (TW + 4) + 8, 52 + len(page) * (TH + 10)), (18, 18, 18))
        d = ImageDraw.Draw(sheet)
        head = a.title or a.analysis.parent.name
        d.text((10, 12), head + (f"  ·  page {p}/{len(pages)}" if len(pages) > 1 else "") + f"  ·  {len(items)} clips",
               fill=(255, 220, 120), font=TITLE)
        for i, (stem, label) in enumerate(page):
            cd = a.analysis / stem
            st = json.loads((cd / "stats.json").read_text())
            y0 = 52 + i * (TH + 10)
            cid, when = clip_label(stem)
            d.text((8, y0 + 4), cid, fill=(255, 255, 255), font=BOLD)
            y = y0 + 32
            if when:
                d.text((8, y), when, fill=(200, 200, 200), font=REG)
                y += 22
            d.text((8, y), f"{st.get('duration_s', 0):.1f} s  {st.get('fps', '?')} fps  {st.get('orientation', '')}",
                   fill=(200, 200, 200), font=REG)
            y += 22
            for note in st.get("read", [])[:2]:
                d.text((8, y), note[:30], fill=(150, 150, 150), font=REG)
                y += 20
            for ln in [x for x in label.split("|") if x]:
                d.text((8, y), ln[:28], fill=(255, 220, 120), font=REG)
                y += 22
            for j, (tile, t) in enumerate(tiles(cd, st)):
                x = LW + j * (TW + 4)
                sheet.paste(tile, (x + (TW - tile.width) // 2, y0 + (TH - tile.height) // 2))
                d.text((x + 4, y0 + TH - 22), f"{t:.1f}s", fill=(255, 255, 0), font=REG)
        out = a.out if len(pages) == 1 else a.out.with_name(f"{a.out.stem}_p{p}{a.out.suffix}")
        out.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(out, quality=88)
        print(f"✓ {out}")


if __name__ == "__main__":
    main()
