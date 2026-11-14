#!/usr/bin/env python3
"""KOLKATA round 6d: v6 with the director's 2026-11-08 notes on v6c.

Director (2026-11-08, on v6c), with what each note changes:
  1. "the inside of the tram … goes out of focus" → shot 25 C030: the camera loses focus at 4.8–6.6 s and the shot
     used 2.0–6.12. Now 0.40–4.52 (measured sharp all the way: Laplacian ≥ 1.0× the clip median).
  2. "walking on the lanes and one side Ganga is visible … stabilization issues" → shot 7 C089 (the river promenade)
     was never stabilised. Now stabilised (smooth, σ 30, horizon level) on the steadier window SRC_C089.
  3. "the same one while I'm walking on the bridge … stabilization issue" → shot 6: stronger stabilisation, or the
     steadier walkway clip C084 (WALK_CLIP), picked by measuring both pre-renders.
  4. "city of surprises … the tram line video or the bus depot video … people dancing on the streets during
     bhashan" → shot 5 (was the stock hand-pulled rickshaw): SURPRISE picks one of the candidates below. Default:
     the Dashami dancers (C035), moved here from shot 9; shot 9 ("… passion") becomes the big dhak (C029).
  5. "the standing tram … does not fit in … a Kolkata bus that is moving, or the bus stop that I have captured"
     → shot 21 (was the tram photo): Pexels 39654702, a garlanded Kolkata private bus driving straight at the camera,
     interpreted 30 → 25 fps (0.833×, frame for frame).
Everything else is v6 unchanged (tools/guide_edl_v6.py is imported, not copied).

Usage (studio root):
  python3 projects/kolkata/tools/guide_edl_v6d.py -o projects/kolkata/analysis/edl_v6d.json --jobs projects/kolkata/analysis/fx_jobs_v6d.json
  .venv/bin/python projects/kolkata/tools/fx_prerender.py --jobs projects/kolkata/analysis/fx_jobs_v6d.json --only <ids>
"""
import argparse
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("g6", Path(__file__).with_name("guide_edl_v6.py"))
g6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g6)
B, S, K, push = g6.B, g6.S, g6.K, g6.push

SURPRISES = {
    # Oct 21 (Dashami): women in lal-paar saris dancing on the ghat road at the bhashan, smoke and balloons under a
    # banyan. It was shot 9 ("… passion"); it moves here and shot 9 gets the big dhak (PASSION). The street dance
    # inside C047 (25.2–27.3, a woman dancing by the dhakis) was tried: 7.6 px jitter even locked, smeared, and a
    # passer-by crossing in front, so it fails the steadiness check.
    "dance": dict(name="Oct21_C035_bhashan_dancers", clip=S + "Oct21_A001_10211954_C035.mov", src_in=0.4, scale=50,
                  shows="Dashami night: women in lal-paar saris dancing on the ghat road at the bhashan, smoke and "
                        "balloons under the banyan: the city that surprises you (real speed)"),
    # Oct 31 dusk: the tram rails set in the road under the trees
    "tramline": dict(name="C023_tram_rails", clip=B + "A001_10311635_C023.mov", src_in=4.0, rotation=-90,
                     scale=push(62.5, 65.0),
                     shows="tram rails curving through the road at dusk under big trees, people far off"),
    # Oct 31 sunset: the bus terminus under the trees
    "depot": dict(name="C020_bus_depot", clip=B + "A001_10311630_C020.mov", src_in=3.0, rotation=-90,
                  scale=push(62.5, 65.0),
                  shows="the bus terminus at sunset under the trees, people crossing"),
}
SURPRISE = "dance"
WALK = dict(name="C082_walkway_pov_s40", clip=B + "A001_10251528_C082.mov", src_in=2.0, rotation=90, scale=push(62.5, 66.0),  # 1.0–2.0 s has a 4.7 px lurch
            fx=dict(stab="smooth", sigma=40, zoom=1.08),
            shows="walking POV into the Howrah Bridge walkway, the truss overhead: follow me; stabilised (stronger), horizon level")
SRC_C089 = 6.4          # measured after stabilising: 6.4 → 0.84 px jitter, 2.8 → 2.16 px
# "… passion" accent (was the C035 dancers, now at "surprises"): the big dhak in its red patterned cover at the ghat
PASSION = dict(name="Oct21_C029_dhak", clip=S + "Oct21_A001_10211946_C029.mov", src_in=1.0, scale=push(50, 54),
               pos=[540, 1000],
               shows="the big dhak in its red patterned cover at the ghat on Dashami, the dhaki beside it, the river "
                     "behind: the drum of the city's passion (hard cut on the accent, slow push)")
BUS = dict(name="stock_bus_front", clip=K + "pexels-39654702/16904781_1920_1080_30fps.mp4", src_in=0.5, rate=g6.C30,
           scale=push(125, 130), pos=[490, 910],   # the bus drifts right as it nears: keep its front clear of the IG buttons
           shows="a garlanded Kolkata private bus drives straight at us down the road, front end clear: the city moving "
                 "(Pexels 39654702, Trishik Bose; 30 → 25 fps by interpretation)")


# Review gate v6b #1: the ghat bathers (Pexels 4200197) is a timelapse with passers-by crossing the lens all through;
# no clean span longer than ~1.2 s. Replaced by Pexels 36819326 (Souhityo Das, vertical 4K 30 fps): people on the ghat
# steps at sunset, the Vidyasagar Setu behind, a slow pan right; stabilised (handheld jitter 3–5 px).
GHAT_SUNSET = dict(name="stock_ghat_sunset", clip=K + "pexels-36819326/15601155_2160_3840_30fps.mp4", src_in=1.0, rate=g6.C30,
                   scale=50, fx=dict(interpret=True, stab="smooth", sigma=25, zoom=1.06),
                   shows="people on the ghat steps at sunset, the Vidyasagar Setu and the river glowing pink behind: the light "
                         "everywhere (Pexels 36819326, Souhityo Das; stabilised)")


def swap(name, new):
    i = next(k for k, (_, _, s) in enumerate(g6.LINES) if s["name"] == name)
    t0, line, _ = g6.LINES[i]
    g6.LINES[i] = (t0, line, new)


def apply():
    swap("stock_rickshaw_tracks", dict(SURPRISES[SURPRISE]))
    if SURPRISE == "dance":
        swap("Oct21_C035_dancers", dict(PASSION))
    swap("C082_walkway_pov", dict(WALK))
    c089 = next(s for _, _, s in g6.LINES if s["name"] == "C089_sunset_lamps")
    c089 = dict(c089, name="C089_sunset_lamps_stab", src_in=SRC_C089, fx=dict(stab="smooth", sigma=30, zoom=1.06),
                shows=c089["shows"] + "; stabilised, horizon level")
    swap("C089_sunset_lamps", c089)
    swap("stock_tram_street", dict(BUS))
    c030 = next(s for _, _, s in g6.LINES if s["name"] == "C030_tram_night")
    swap("C030_tram_night", dict(c030, src_in=0.40))
    swap("stock_ghat_bathers", dict(GHAT_SUNSET))


def review_fixes(edl):
    """Review gate v6 (Fable, 2026-11-08) fixes, applied to the cut so the EDL stays the shot map:
    - #1 the ghat bathers (Pexels 4200197) is a timelapse with passers-by crossing the lens (whole-frame luma drops of
      12–23 levels). Its only long clean span is camera frames 180–261 (5.98–8.71 s, 82 frames). So the Setu sunset holds
      2 beats longer (the line "light everywhere" opens on the sun on the water) and the bathers start at 34.48 on that span.
      AE Timewarp to stretch the clean span was tried and rejected: Pixel Motion ghosts the timelapse's jumping people.
    - #5 the Dashami dancers: camera 1.0 s (the arms up); v6b review: Scale 62.5, x 405 (crops the camera's left 20 %, the bystander).
    - v6b review #1: the bathers still blinked (smaller crossings) → replaced by GHAT_SUNSET at the same 34.48 cut."""
    sh = {s["name"][3:]: s for s in edl["shots"]}
    setu, bath, dance = sh["stock_setu_sunset"], sh["stock_ghat_sunset"], sh["Oct21_C035_bhashan_dancers"]
    cut = 34.48
    setu["end"] = cut
    setu["scale"] = [[0, 125], [round(cut - setu["start"], 2), 130]]
    bath.update(start=cut)
    dance.update(src_in=1.0, scale=62.5, pos=[405, 910])   # v6b review #2: crop the camera's left 20 % (the bystander)
    for a in edl["audio"]:   # v6b review #3/#4: the bell starts on the tram cut with a strike, −14 dB, ends 73.28 (0.5 s fade)
        if "tram_approach_bell" in a["file"]:
            a.update(start=68.84, dur=4.44, gain_db=-14.0, fade_out=0.5, **{"in": 10.64})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", required=True)
    ap.add_argument("--jobs", required=True)
    ap.add_argument("--surprise", choices=list(SURPRISES), default=SURPRISE)
    ap.add_argument("--walk", choices=["C082", "C084"], default="C082")
    ap.add_argument("--src-c089", type=float, default=SRC_C089)
    a = ap.parse_args()
    SURPRISE, SRC_C089 = a.surprise, a.src_c089
    if a.walk == "C084":
        WALK = dict(WALK, name="C084_walkway_river", clip=B + "A001_10251531_C084.mov", scale=push(62.5, 65.0),
                    fx=dict(stab="smooth", sigma=30, zoom=1.06),
                    shows="walking POV along the Howrah Bridge walkway, the river and moored boats beside: follow me; stabilised")
    apply()
    edl, jobs = g6.build()
    review_fixes(edl)
    edl["note"] = edl["note"].replace("KOLKATA v6", "KOLKATA v6d") + \
        (f" Round 6d: surprises = {SURPRISE} (dance: C035 moved from shot 9, which is now the C029 dhak); walk = {a.walk}; C089 stabilised from {SRC_C089} s; tram interior "
         f"re-timed to its sharp part; shot 21 = a moving Kolkata bus (Pexels 39654702). No AI shot.")
    Path(a.o).write_text(json.dumps(edl, indent=1, ensure_ascii=False))
    Path(a.jobs).write_text(json.dumps(jobs, indent=1, ensure_ascii=False))
    for s in edl["shots"]:
        print(f'{s["name"]:30s} {s["start"]:6.2f}-{s["end"]:6.2f} ({s["end"] - s["start"]:.2f}) r{s["rate"]:<6} {s["line"][:50]}')
    print("runtime", edl["runtime"], "shots", len(edl["shots"]), "fx jobs", len(jobs), [j["id"] for j in jobs])
