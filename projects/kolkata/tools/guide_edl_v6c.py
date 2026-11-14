#!/usr/bin/env python3
"""KOLKATA round 6c: v6 with shot 21 as a real stock photo of a running Kolkata tram, with a slow push-in.

Director (2026-11-07, while the AI final was generating): "the tram shot in applicable use stock image", read as:
use a real stock photo where one fits, rather than the AI clip. Picked from free stock (see project.md Round 6b/6c):
Unsplash pc_sZ1DLdGU by Subhashis Das, a WBTC tram on the line, front end clear (route board "25 Esplanade–Gariahat").

The still is framed as a 4:5 crop of the full photo height (renders/gen/stock_tram_subhashis_9x16.png: the window
area y 235–1584 is the photo, the rest is a blurred copy under the matte) and pushed 1.00 → 1.06 over 4.2 s by
scripts/conform_clip.py → renders/gen/stock_tram_subhashis_push.mov (1080×1920, 25 fps). Everything else is v6.

Usage (studio root):
  python3 projects/kolkata/tools/guide_edl_v6c.py -o projects/kolkata/analysis/edl_v6c.json --jobs projects/kolkata/analysis/fx_jobs_v6c.json
"""
import argparse
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("g6", Path(__file__).with_name("guide_edl_v6.py"))
g6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g6)

CLIP = "projects/kolkata/renders/gen/stock_tram_subhashis_push.mov"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", required=True)
    ap.add_argument("--jobs", required=True)
    a = ap.parse_args()
    i = next(k for k, (_, _, s) in enumerate(g6.LINES) if s["name"] == "stock_tram_street")
    t0, line, _ = g6.LINES[i]
    g6.LINES[i] = (t0, line, dict(
        name="stock_tram_photo", clip=CLIP, src_in=0.0, scale=100,
        pos=[540, 960],      # the render is already framed in window coordinates (y 235–1584); the default 910 lifts it 50 px
        shows="a real WBTC Kolkata tram on the line, front end clear (route board Esplanade–Gariahat, headlight on), "
              "under trees; still photo with a slow push-in (Unsplash pc_sZ1DLdGU, Subhashis Das)",
        note="build: still renders/gen/stock_tram_subhashis_9x16.png (4:5 crop of the photo at window y 235–1584), "
             "Scale 100 → 106 over the shot in Premiere, or this pre-rendered push"))
    edl, jobs = g6.build()
    edl["note"] = edl["note"].replace("KOLKATA v6", "KOLKATA v6c") + \
        " Round 6c: shot 21 is a stock photo (Unsplash, Subhashis Das) with a push-in; no AI shot in this version."
    Path(a.o).write_text(json.dumps(edl, indent=1, ensure_ascii=False))
    Path(a.jobs).write_text(json.dumps(jobs, indent=1, ensure_ascii=False))
    for s in edl["shots"][18:23]:
        print(f'{s["name"]:26s} {s["start"]:6.2f}-{s["end"]:6.2f} ({s["end"] - s["start"]:.2f}) {s["line"]}')
    print("runtime", edl["runtime"], "shots", len(edl["shots"]), "fx jobs", len(jobs))
