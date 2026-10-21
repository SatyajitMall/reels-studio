#!/usr/bin/env python3
"""Preview film-stock looks on the director's own stills (skill Phase 0 Round 2: show, don't name).

Each look is one row of the film-stock table in effects-playbook.md §A3. Two kinds:
  exact    Adobe's own film-emulation .cube that ships with Premiere (Lumetri → Creative → Look),
           blended at the look's intensity, the same mix Lumetri's Creative "Intensity" makes.
           The preview matches what the V3 look starts from in Premiere.
  approx   no readable Premiere LUT (SpeedLooks .itx files are encrypted), or an effect Premiere
           doesn't have (halation): an ffmpeg recipe that shows the intent. Labelled "≈" on the sheet.
Previews only. The reel's grade is built in Premiere (CLAUDE.md §2) and verified there by render.

Inputs: stills (.png/.jpg) or clips with a time, e.g. raw/b-roll/C027.mov@8.0
Writes <out>/looks_sheet.png (rows = stills, columns = looks, labelled) and <out>/looks.json
(per look per still: luma, p02, p98, crush%, clip%, sat, R-B, G-M, hue, as in colour_report.py).

Usage:
  ./.venv/bin/python scripts/look_preview.py raw/b-roll/C027.mov@8 raw/b-roll/C152.mov@24.5 -o analysis/looks
  ./.venv/bin/python scripts/look_preview.py stills/*.png -o analysis/looks --looks k500t_2383,eterna_3510,cinestill
  ./.venv/bin/python scripts/look_preview.py stills/*.png -o analysis/looks --intensity 0.4   # override every look
  ./.venv/bin/python scripts/look_preview.py --list
"""
from __future__ import annotations

import argparse
import glob
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from colour_report import KEYS, stats  # noqa: E402  (same measurements as the colour QA)

# id: (label, kind, preview .cube in Premiere's Creative folder or None, default intensity,
#      extra ffmpeg chain after the LUT, Premiere look name for applyLumetriPreset / Creative → Look)
LOOKS: dict[str, tuple[str, str, str | None, float, str, str]] = {
    "k500t_2383": ("Kodak 500T → 2383", "exact", "Kodak 5218 Kodak 2383 (by Adobe)", 0.5, "", "Kodak 5218 Kodak 2383 (by Adobe)"),
    "k500t_2395": ("Kodak 500T → 2395", "exact", "Kodak 5218 Kodak 2395 (by Adobe)", 0.5, "", "Kodak 5218 Kodak 2395 (by Adobe)"),
    "k250d_3510": ("Kodak 250D → Fuji 3510", "exact", "Kodak 5205 Fuji 3510 (by Adobe)", 0.5, "", "Kodak 5205 Fuji 3510 (by Adobe)"),
    "f125_2393": ("Fuji F125 → 2393 (Warm Film)", "exact", "Fuji F125 Kodak 2393 (by Adobe)", 0.5, "", "Fuji F125 Kodak 2393 (by Adobe)"),
    "f125_2395": ("Fuji F125 → 2395", "exact", "Fuji F125 Kodak 2395 (by Adobe)", 0.5, "", "Fuji F125 Kodak 2395 (by Adobe)"),
    "eterna_3510": ("Fuji Eterna 250D → 3510", "exact", "Fuji ETERNA 250D Fuji 3510 (by Adobe)", 0.5, "", "Fuji ETERNA 250D Fuji 3510 (by Adobe)"),
    "eterna_2395": ("Fuji Eterna 250D → 2395", "exact", "Fuji ETERNA 250D Kodak 2395 (by Adobe)", 0.5, "", "Fuji ETERNA 250D Kodak 2395 (by Adobe)"),
    "reala_2393": ("Fuji Reala 500D → 2393", "exact", "Fuji REALA 500D Kodak 2393 (by Adobe)", 0.5, "", "Fuji REALA 500D Kodak 2393 (by Adobe)"),
    # The Monochrome looks are SpeedGrade .look files ffmpeg can't read: preview = the colour film LUT, then grey
    "mono_500t": ("Mono Kodak 500T → 2395 ≈", "approx", "Kodak 5218 Kodak 2395 (by Adobe)", 1.0, "hue=s=0",
                  "Monochrome Kodak 5218 Kodak 2395 (by Adobe)"),
    "mono_eterna": ("Mono Eterna 250D → 2395 ≈", "approx", "Fuji ETERNA 250D Kodak 2395 (by Adobe)", 1.0, "hue=s=0",
                    "Monochrome Fuji ETERNA 250D Kodak 2395 (by Adobe)"),
    # CineStill 800T: 500T base + red-orange halation around the brightest lights (Premiere has none: AE glow op)
    "cinestill": ("CineStill 800T ≈ (500T + halation)", "approx", "Kodak 5218 Kodak 2383 (by Adobe)", 0.5,
                  "split[c][h];[h]colorlevels=rimin=0.70:gimin=0.70:bimin=0.70,gblur=sigma={sig},"
                  "colorchannelmixer=rr=1.0:rg=0.2:gr=0.12:gg=0.12:br=0:bb=0.02[g];"
                  "[c][g]blend=all_mode=screen:all_opacity=0.8", "Kodak 5218 Kodak 2383 (by Adobe) + halation bake"),
    # Bleach bypass: a greyscale copy laid over the colour (Premiere: SL BLEACH NDR, not readable by ffmpeg)
    "bleach": ("Bleach bypass ≈ (SL BLEACH NDR)", "approx", None, 1.0,
               "split[c][m];[m]hue=s=0[m2];[c][m2]blend=all_mode=overlay:all_opacity=0.6,hue=s=0.75", "SL BLEACH NDR"),
}


def creative_lut_dir() -> Path:
    hits = sorted(glob.glob("/Applications/Adobe Premiere Pro*/Adobe Premiere Pro*.app/Contents/Lumetri/LUTs/Creative"))
    if not hits:
        sys.exit("Premiere's Lumetri Creative LUT folder not found under /Applications")
    return Path(hits[-1])


def grab(src: str, dst: Path, width: int) -> None:
    path, _, t = src.partition("@")
    pre = ["-ss", t] if t else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", *pre, "-i", path, "-frames:v", "1",
                    "-vf", f"scale={width}:-2", str(dst)], check=True)


def chain(look: str, lut_dir: Path, k: float, width: int) -> str:
    label, kind, lut, _, extra, _ = LOOKS[look]
    parts = ["format=gbrp"]
    if lut:
        f = str(lut_dir / f"{lut}.cube").replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        parts.append(f"split[o][l];[l]lut3d=file='{f}':interp=tetrahedral[g];"
                     f"[o][g]blend=all_expr='A*{1 - k:.3f}+B*{k:.3f}'")
    if extra:
        parts.append(extra.format(sig=max(4, width / 36)))  # 30 px at 1080 wide
    return ",".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="*", help="stills, or clip.mov@seconds")
    ap.add_argument("-o", "--out", type=Path)
    ap.add_argument("--looks", help="comma-separated look ids (default: all)")
    ap.add_argument("--intensity", type=float, help="override every look's intensity (0–1)")
    ap.add_argument("--width", type=int, default=540, help="processing width in px (height follows the still)")
    ap.add_argument("--tile", type=int, default=270, help="tile width on the sheet (raise it to judge detail such as halation)")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        for i, (label, kind, lut, k, _, prem) in LOOKS.items():
            print(f"{i:<12} {kind:<6} {k:>4.0%}  {label:<36} Premiere: {prem}")
        return
    if not a.inputs or not a.out:
        ap.error("give inputs and -o")
    looks = a.looks.split(",") if a.looks else list(LOOKS)
    bad = [x for x in looks if x not in LOOKS]
    if bad:
        sys.exit(f"Unknown look(s): {bad}. See --list")
    lut_dir = creative_lut_dir()
    a.out.mkdir(parents=True, exist_ok=True)
    rows, report = [], {}
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for n, src in enumerate(a.inputs):
            name = Path(src.partition("@")[0]).stem + (f"@{src.partition('@')[2]}" if "@" in src else "")
            still = tmp / f"s{n}.png"
            grab(src, still, a.width)
            tiles = [("Source", "", still)]
            for look in looks:
                k = a.intensity if a.intensity is not None else LOOKS[look][3]
                out = tmp / f"s{n}_{look}.png"
                p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(still), "-filter_complex",
                                    chain(look, lut_dir, k, a.width) + ",format=rgb24", "-frames:v", "1", str(out)],
                                   capture_output=True, text=True)
                if p.returncode:
                    sys.exit(f"{look} failed on {name}: {p.stderr.strip()[:300]}")
                tiles.append((LOOKS[look][0], f"{k:.0%}" if LOOKS[look][2] else "", out))
            report[name] = {}
            imgs = []
            for label, k, path in tiles:
                im = Image.open(path).convert("RGB")
                report[name][label] = dict(zip(KEYS, [round(v, 4) for v in stats(np.asarray(im, dtype=np.float32) / 255.0)]))
                imgs.append((label, k, im))
            rows.append(imgs)
    # Sheet
    w, h = rows[0][0][2].size
    tw = a.tile
    th = round(h * tw / w)
    sheet = Image.new("RGB", (tw * len(rows[0]), th * len(rows) + 0), "black")
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    for r, imgs in enumerate(rows):
        for c, (label, k, im) in enumerate(imgs):
            t = im.resize((tw, th), Image.LANCZOS)
            d = ImageDraw.Draw(t)
            d.rectangle([0, th - 40, tw, th], fill=(0, 0, 0))
            d.text((6, th - 37), label, font=font, fill=(255, 255, 255))
            if k:
                d.text((6, th - 19), f"intensity {k}", font=font, fill=(200, 200, 200))
            sheet.paste(t, (c * tw, r * th))
    sheet.save(a.out / "looks_sheet.png")
    (a.out / "looks.json").write_text(json.dumps({"lut_dir": str(lut_dir), "looks": {k: {"label": v[0], "kind": v[1],
                                       "preview_lut": v[2], "premiere": v[5], "intensity": a.intensity if a.intensity is not None else v[3]}
                                       for k, v in LOOKS.items() if k in looks}, "stills": report}, indent=1))
    print(f"✓ {len(rows)} stills × {len(looks)} looks → {a.out / 'looks_sheet.png'}")


if __name__ == "__main__":
    main()
