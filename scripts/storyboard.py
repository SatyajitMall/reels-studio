#!/usr/bin/env python3
"""Checkpoint storyboard from an EDL: in / mid / out frame per shot, through its planned framing, with the overlays that
are on screen at that moment and the Instagram UI bands shaded (top 220, bottom 320, right 120 px), so a face under a
caption or the IG buttons shows before the cut is built (skill Phase 2, Checkpoint 1).

Promoted from three reels' own versions (goddess: line and fps flags; uski: frames through the crop; Pujo: notes).
Per shot it labels: name, reel times, camera clip and in-point, speed or conform, the width shown (orange under 80 %,
red under 70 %, effects-playbook §B), the line it carries ("line") and what shows it ("shows", "role", "note").
The EDL is preview_edl.py's (one JSON object with "fps" and "shots"); frames come from the camera files.
Non-Latin lines (Bangla, Devanagari) draw with Arial Unicode but without shaping, so conjuncts may look wrong.

Usage (from the studio root):
  ./.venv/bin/python scripts/storyboard.py projects/<reel>/analysis/edl_v1.json -o projects/<reel>/analysis/storyboard_v1.jpg
      [--per-page 12] [--no-overlays]
Writes storyboard_v1.jpg, or storyboard_v1_p1.jpg, _p2 … past --per-page shots.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import textwrap
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from preview_edl import (EXACT, SAFE, W, H, Framing, Overlay, check, frames, grade_fn, load_edl, over,  # noqa: E402
                         prescale, still)

TW, TH, LW = 180, 320, 330
SUP = "/System/Library/Fonts/Supplemental/"
BOLD, REG, UNI = SUP + "Arial Bold.ttf", SUP + "Arial.ttf", SUP + "Arial Unicode.ttf"
GOLD, GREY, WHITE, ORANGE, RED = (242, 211, 59), (185, 185, 185), (240, 240, 240), (255, 160, 70), (255, 80, 80)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def camera_frame(shot: dict, fact: dict, t_shot: float) -> np.ndarray:
    """The shot's picture t_shot seconds into it, at 1080×1920 through its framing (and approximate grade)."""
    fr = fact["framing"]
    k = prescale(fr)
    pw, ph = max(2, 2 * round(fact["w"] * k / 2)), max(2, 2 * round(fact["h"] * k / 2))
    t_src = float(shot.get("src_in", 0)) + t_shot * float(shot.get("rate", 1.0))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t_src:.4f}", "-i", shot["clip"], "-an", "-frames:v", "1",
                          "-vf", f"scale={pw}:{ph}:flags=area+{EXACT},format=rgb24", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    src = np.frombuffer(raw, np.uint8)[: pw * ph * 3].reshape(ph, pw, 3)
    g = grade_fn(shot.get("grade"))
    if g:
        src = g(src)
    box = fr.crop(pw / fact["w"], ph / fact["h"], pw, ph)
    if box:
        return src[box[1]:box[1] + H, box[0]:box[0] + W].astype(np.float32)
    img = Image.fromarray(src).transform((W, H), Image.AFFINE, fr.affine(t_shot, pw / fact["w"], ph / fact["h"]),
                                         resample=Image.BICUBIC, fillcolor=(0, 0, 0))
    return np.asarray(img, np.float32)


def bands(tile: Image.Image) -> Image.Image:
    k = tile.width / W
    layer = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for box in ((0, 0, W, SAFE["top"]), (0, H - SAFE["bottom"], W, H), (W - SAFE["right"], SAFE["top"], W, H - SAFE["bottom"])):
        d.rectangle(tuple(round(v * k) for v in box), fill=(255, 40, 40, 40), outline=(255, 60, 60, 160))
    return Image.alpha_composite(tile.convert("RGBA"), layer).convert("RGB")


def text_font(s: str, size: int) -> ImageFont.FreeTypeFont:
    return font(UNI if any(ord(c) > 0x2FF for c in s) else REG, size)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("edl", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--per-page", type=int, default=12)
    ap.add_argument("--no-overlays", action="store_true", help="frames without the V5 overlays")
    a = ap.parse_args()

    edl = load_edl(a.edl)
    fps, shots = edl["fps"], edl["shots"]
    errs, warns, facts = check(edl)
    for e in errs:
        print(f"  ✗ {e}")
    if errs:
        sys.exit(1)
    overlays = [] if a.no_overlays else [o for o in (Overlay(item, fps) for item in edl["overlays"]) if o.is_still]
    runtime = frames(edl.get("runtime") or shots[-1]["end"], fps) / fps

    cw = LW + 3 * TW + 24                                # one shot: label column + 3 tiles
    pages = [shots[i:i + a.per_page] for i in range(0, len(shots), a.per_page)]
    outs = []
    for p, page in enumerate(pages, 1):
        rows = (len(page) + 1) // 2
        sheet = Image.new("RGB", (2 * cw, 56 + rows * (TH + 14)), (16, 16, 16))
        d = ImageDraw.Draw(sheet)
        d.text((12, 14), f"{a.edl.stem}  ·  {runtime:.2f} s  ·  {fps:g} fps  ·  {len(shots)} shots"
               + (f"  ·  page {p}/{len(pages)}" if len(pages) > 1 else "") + "  ·  red bands = Instagram UI",
               fill=GOLD, font=font(BOLD, 24))
        for j, s in enumerate(page):
            r, c = divmod(j, 2)
            x0, y0 = c * cw + 8, 56 + r * (TH + 14)
            a_f, b_f = frames(s["start"], fps), frames(s["end"], fps)
            dur = (b_f - a_f) / fps
            for k, u in enumerate((0.04, 0.5, 0.96)):
                t_shot = dur * u
                if s.get("clip"):
                    img = camera_frame(s, facts[s["name"]], t_shot)
                elif s.get("image"):
                    img = still(Path(s["image"])).astype(np.float32)
                else:
                    img = np.zeros((H, W, 3), np.float32)
                f = a_f + int(round(t_shot * fps))
                for o in overlays:
                    rgba = o.at(f)
                    if rgba is not None:
                        img = over(img, rgba)
                tile = Image.fromarray(np.clip(img + 0.5, 0, 255).astype(np.uint8)).resize((TW, TH), Image.LANCZOS)
                sheet.paste(bands(tile), (x0 + LW + k * (TW + 4), y0))
            y = y0 + 4
            d.text((x0, y), s["name"], fill=WHITE, font=font(BOLD, 21))
            y += 28
            d.text((x0, y), f"{s['start']:.2f}–{s['end']:.2f} s  ({dur:.2f} s)", fill=WHITE, font=font(REG, 16))
            y += 22
            if s.get("clip"):
                fa = facts[s["name"]]
                rate = float(s.get("rate", 1.0))
                speed = ""
                if rate <= 0:
                    speed = "  freeze"
                elif abs(rate - 1) > 1e-3:
                    conform = abs(rate - fps / fa["fps"]) < 0.01
                    speed = f"  conform {fa['fps']:.0f}→{fps:g}" if conform else f"  speed {100 * rate:.0f} %"
                elif abs(fa["fps"] - fps) > 0.5:
                    speed = f"  {fa['fps']:.0f} fps camera, not conformed"
                d.text((x0, y), f"{Path(s['clip']).stem}  @{float(s.get('src_in', 0)):.2f}{speed}", fill=GREY, font=font(REG, 14))
                y += 20
                wp = fa["width_pct"]
                d.text((x0, y), f"width {wp:.0f} % of the widest framing", font=font(REG, 14),
                       fill=WHITE if wp >= 80 else (ORANGE if wp >= 70 else RED))
                y += 22
            else:
                d.text((x0, y), "still" if s.get("image") else "black", fill=GREY, font=font(REG, 14))
                y += 22
            if s.get("line"):
                for ln in textwrap.wrap(f"“{s['line']}”", 34)[:3]:
                    d.text((x0, y), ln, fill=GOLD, font=text_font(ln, 17))
                    y += 22
            for key in ("shows", "role", "note", "text"):
                if s.get(key):
                    for ln in textwrap.wrap(f"{key}: {s[key]}", 40)[:3]:
                        if y > y0 + TH - 16:
                            break
                        d.text((x0, y), ln, fill=GREY, font=text_font(ln, 14))
                        y += 18
        out = a.out if len(pages) == 1 else a.out.with_name(f"{a.out.stem}_p{p}{a.out.suffix}")
        out.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(out, quality=88)
        outs.append(out)
    for w in warns:
        print(f"  ! {w}")
    for o in outs:
        print(f"✓ {o}")


if __name__ == "__main__":
    main()
