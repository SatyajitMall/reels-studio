#!/usr/bin/env python3
"""KOLKATA round 6b: v6 with shot 21 replaced by an AI-generated tram running at the camera.

Director (2026-11-07, on v6): "look for a better tram footage … the tram actually running on the line with a clear
front end view". No free stock has a running Kolkata tram front-on (Pexels, Pixabay, Wikimedia Commons searched); the
director chose an AI shot (Veo 3.1 Lite via scripts/gen_video.py, shot `tram_front`) and approved the $0.12 draft.

Everything else is v6 unchanged (tools/guide_edl_v6.py is imported, not copied). The AI clip is conformed with
scripts/conform_clip.py (24 → 25 fps frame for frame, 1080×1920, colour nudged toward C101, the next shot).
The draft is 4 s, so the preview slows it a little (--rate) to fill the 4.08 s line; the 8 s final needs no slow-down.

Usage (studio root):
  python3 projects/kolkata/tools/guide_edl_v6b.py --clip projects/kolkata/renders/gen/tram_front_draft1_conformed.mov \
      --rate 0.82 -o projects/kolkata/analysis/edl_v6b.json --jobs projects/kolkata/analysis/fx_jobs_v6b.json
  .venv/bin/python projects/kolkata/tools/fx_prerender.py --jobs projects/kolkata/analysis/fx_jobs_v6b.json --only ai_tram_front
"""
import argparse
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("g6", Path(__file__).with_name("guide_edl_v6.py"))
g6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g6)


def swap(clip, rate, src_in):
    i = next(k for k, (_, _, s) in enumerate(g6.LINES) if s["name"] == "stock_tram_street")
    t0, line, _ = g6.LINES[i]
    sh = dict(name="ai_tram_front", clip=clip, src_in=src_in, scale=g6.push(100, 103),
              shows="AI-GENERATED: a Kolkata tram runs down the rails straight at the camera, its front end clear "
                    "(blue-and-white car, trolley pole, old shuttered houses); the old city still moving")
    if rate < 1:
        sh["fx"] = dict(rate=rate, half=False)        # draft only: motion-compensated slow-down to fill the line
    g6.LINES[i] = (t0, line, sh)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", required=True, help="the conformed AI clip (1080×1920, 25 fps)")
    ap.add_argument("--rate", type=float, default=1.0, help="< 1 slows the draft to fill the line (preview only)")
    ap.add_argument("--src-in", type=float, default=0.0)
    ap.add_argument("-o", required=True)
    ap.add_argument("--jobs", required=True)
    a = ap.parse_args()
    swap(a.clip, a.rate, a.src_in)
    edl, jobs = g6.build()
    edl["note"] = edl["note"].replace("KOLKATA v6", "KOLKATA v6b") + \
        " Round 6b: shot 21 is AI-generated (Veo 3.1 Lite, labelled in brief.md; turn on Instagram's AI label)."
    Path(a.o).write_text(json.dumps(edl, indent=1, ensure_ascii=False))
    Path(a.jobs).write_text(json.dumps(jobs, indent=1, ensure_ascii=False))
    for s in edl["shots"]:
        print(f'{s["name"]:26s} {s["start"]:6.2f}-{s["end"]:6.2f} ({s["end"] - s["start"]:.2f}) r{s["rate"]:<6} {s["line"]}')
    print("runtime", edl["runtime"], "shots", len(edl["shots"]), "fx jobs", len(jobs))
