#!/usr/bin/env python3
"""KOLKATA round 4: story-first EDL ("Home for Pujo"), written from a line table, not from the pool walk.

Round 3's cuts were slotted by tools/audition_edl.py (priority + energy into beat buckets), so the story lived only in
the brief. Here every shot is chosen for the story line it carries, and every cut sits on a beat the band plays
(onset >= 4x median or a bass hit), never on the tracker's unplayed downbeats (review_v3b_M3 minors).
Same song window as v3b_M3 (mayabee.wav from 164.36 s, 47.50 s), so the IG start stays about 2:40.

Usage (from the studio root):
  python3 projects/kolkata/tools/story_edl.py -o projects/kolkata/analysis/edl_v4_story.json
"""
import argparse
import copy
import json
from pathlib import Path

REEL = Path("projects/kolkata")
S, B, K = "projects/kolkata/raw/selects/", "projects/kolkata/raw/b-roll/", "projects/kolkata/raw/stock/"
PUSH_END = 65.0


def push(dur, a=62.5, b=PUSH_END):
    return [[0, a], [round(dur, 2), b]]


# Reused shots: settings from the reviewed v3b_M3 EDL (src moves, reframes and keys the reviewer passed).
V3B = {s["name"].split("_", 1)[1]: s for s in json.load(open(REEL / "analysis/edl_v3b_M3.json"))["shots"]}

# (story line, end time in reel seconds, shot). Start = previous end. Cuts on played beats, -0.05 s lag, frame-rounded.
LINES = [
    ("the dhak calls you home", 2.00, dict(V3B["Oct21_C047_dhakis"])),
    ("you arrive: across the Howrah Bridge, the city coming the other way", 6.48,
     dict(name="C083_walkway_crowd", clip=B + "A001_10251529_C083.mov", src_in=13.5, rotation=-90, scale=62.5,
          shows="people walking toward camera on the Howrah Bridge walkway, the truss overhead")),
    ("the river below; the song holds its breath", 11.24, dict(V3B["C061_boat"])),
    ("home: Calcutta", 14.48, dict(V3B["C064_setu"])),
    ("the ride in", 17.00,
     dict(name="C094_scooter_pov", clip=B + "A001_10251620_C094.mov", src_in=13.0, scale=50,
          shows="scooter POV, the speedometer in frame, riding a road of red heritage façades")),
    ("the ride in: the old city rushing past", 19.00,
     dict(name="C096_facade_ride", clip=B + "A001_10251623_C096.mov", src_in=2.0, scale=50,
          shows="a red heritage façade and bougainvillea rushing past the scooter")),
    ("the ride in: the old tram", 21.00, dict(V3B["C025_tram"])),
    ("the ride in: the yellow taxi", 24.00,
     dict(name="C101_taxi", clip=B + "A001_10251635_C101.mov", src_in=0.0, scale=50,
          shows="a yellow Ambassador taxi on the tram lines, a man walking past it")),
    ("who you missed: the chai-wallah", 27.00, dict(V3B["C028_chai"])),
    ("who you missed: the bookseller", 29.00, dict(V3B["C105_bookstall"])),
    ("who you missed: the Coffee House", 31.00, dict(V3B["C111_coffee_house"])),
    ("evening: football on the Maidan", 33.00,
     dict(name="C003_football", clip=B + "A001_10311601_C003.mov", src_in=0.5, rotation=-90, scale=62.5,
          shows="boys playing football on the Maidan at dusk")),
    ("Pujo: the pandal", 36.00, dict(V3B["C109_pandal_lake"])),
    ("Pujo: Dashami night at the ghat", 38.48,
     dict(name="Oct21_C039_ghat_lights", clip=S + "Oct21_A001_10212039_C039.mov", src_in=0.3, scale=50,
          shows="steel truss lit gold above the ghat, the immersion crowd at the water")),
    ("Dashami: the goodbye", 42.04, dict(V3B["Oct21_C035_dancers"])),
    ("you leave: Howrah at blue hour", 47.50, dict(V3B["stock_howrah_bluehour"])),
]


def build():
    shots, t = [], 0.0
    for i, (line, end, sh) in enumerate(LINES, 1):
        sh = copy.deepcopy(sh)
        dur = round(end - t, 2)
        base = sh["name"].split("_", 1)[1] if sh["name"][:2].isdigit() else sh["name"]
        sh["name"] = f"{i:02d}_{base}"
        sh.update(start=round(t, 2), end=round(end, 2), line=line, role=f"story: {line}")
        sh.setdefault("rate", 1)
        sh.setdefault("pos", [540, 910])
        # re-time keyed pushes to the new length
        if isinstance(sh.get("scale"), list):
            a, b = sh["scale"][0][1], sh["scale"][-1][1]
            sh["scale"] = [[0, a], [dur, b]]
            sh.setdefault("ease", "ease")
        elif sh.get("rotation") in (90, -90) and sh["scale"] == 62.5:
            sh["scale"] = push(dur)
            sh["ease"] = "ease"
        if isinstance(sh.get("pos"), list) and sh["pos"] and isinstance(sh["pos"][0], list):
            p0, p1 = sh["pos"][0], sh["pos"][-1]
            sh["pos"] = [[0, p0[1], p0[2]], [dur, p1[1], p1[2]]]
        sh.pop("fade_out", None)
        shots.append(sh)
        t = end
    shots[-1]["shows"] = shots[-1]["shows"] + "; fade to black"
    shots[-1]["fade_out"] = 20
    runtime = round(t, 2)
    return {
        "fps": 25, "runtime": runtime,
        "note": "KOLKATA v4 story cut 'Home for Pujo' (round 4). mayabee.wav from 164.36 s for 47.50 s, same window as "
                "v3b_M3. Shots chosen per story line (line table in project.md Round 4); cuts on played beats only.",
        "overlays": [{"file": "projects/kolkata/renders/overlays/window_matte.png", "start": 0.0, "end": runtime},
                     {"file": "projects/kolkata/renders/overlays/title_calcutta.png", "start": 11.24, "end": 13.97}],
        "audio": [{"file": "projects/kolkata/music/mayabee.wav", "start": 0.0, "in": 164.36, "gain_db": 0.0,
                   "fade_in": 0, "fade_out": 1.2}],
        "shots": shots,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", required=True)
    a = ap.parse_args()
    edl = build()
    Path(a.o).write_text(json.dumps(edl, indent=1))
    for s in edl["shots"]:
        print(f'{s["name"]:28s} {s["start"]:6.2f}-{s["end"]:6.2f} ({s["end"]-s["start"]:.2f})  {s["line"]}')
    print("runtime", edl["runtime"])
