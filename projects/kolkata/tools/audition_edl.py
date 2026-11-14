#!/usr/bin/env python3
"""audition_edl.py: Stage 6 of research/SONG_RESEARCH_METHOD.md (KOLKATA, reel-local).

Cuts ONE shot pool (the 6-beat "Bengali far from home" spine) to a candidate song, so three songs can be compared on
the same pictures. Every cut lands on a beat of that song (bar downbeats preferred). Shot length follows the song's own
energy (song-wide): quiet bars get long holds (≈5 s, two bars) and loud bars shorter ones (≈2.2 s), plus the brief's arc
(slower open, softer end), capped by each shot's usable length. The last two shots are re-split so the end is the longest.
When the song is short of slots, low-priority shots are dropped, keeping the spine order.

Writes an EDL for scripts/preview_edl.py (the window matte, the "Calcutta" title on shot 2, the song from --start).

Usage (studio root):
  ./.venv/bin/python projects/kolkata/tools/audition_edl.py --song projects/kolkata/music/x.wav --start 61.3 \
      --name shantiniketan -o projects/kolkata/analysis/audition/edl_shantiniketan.json [--length 45]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from gemini_audio_and_beat_analyzer import analyze_music_beats  # noqa: E402

S = "projects/kolkata/raw/selects/"
K = "projects/kolkata/raw/stock/"
PUSH = [[0, 62.5], [None, 65.0]]          # slow push on rotated landscape clips (end key filled per shot)

# spine order; pri: 1 = always kept … 4 = dropped first; max = usable reel seconds from src_in (measured 2026-11-07)
POOL = [
    dict(name="C061_boat", clip=S + "A001_10251448_C061.mov", src_in=4.0, rotation=-90, scale=PUSH, max=7.0, pri=1,
         beat=1, shows="two boatmen rowing a country boat on the Hooghly, morning"),
    dict(name="C064_setu", clip=S + "A001_10251452_C064.mov", src_in=1.0, rotation=-90, scale=PUSH, max=5.8,
         pri=1, beat=1, shows="Vidyasagar Setu over the river, open sky; 'Calcutta' in the sky"),
    dict(name="stock_howrah_river", clip=K + "pexels-40180894/17164810_2160_3840_60fps.mp4", src_in=5.0, rate=0.4167,
         scale=50, max=8.0, pri=2, beat=1, shows="Howrah Bridge from the river (stock, 60 fps conformed)"),
    dict(name="C083_walkway", clip=S + "A001_10251529_C083.mov", src_in=11.0, rotation=-90, scale=62.5, max=8.0, pri=3,
         beat=2, shows="people walking the Howrah Bridge walkway"),
    dict(name="C096_facade_ride", clip=S + "A001_10251623_C096.mov", src_in=2.0, scale=50, max=4.0, pri=3, beat=2,
         shows="red heritage façade rushing past from the scooter"),
    dict(name="C093_scooter", clip=S + "A001_10251619_C093.mov", src_in=1.0, scale=50, max=4.9, pri=2, beat=2,
         shows="scooter POV down an open road"),
    dict(name="C100_taxi", clip=S + "A001_10251635_C100.mov", src_in=1.0, scale=50, max=4.8, pri=1, beat=2,
         shows="yellow Ambassador taxi on tram lines"),
    dict(name="C027_tram", clip=S + "A001_10311639_C027.mov", src_in=1.5, rotation=-90, scale=PUSH, max=5.1, pri=3,
         beat=2, shows="an old Kolkata tram under the trees"),
    dict(name="C028_chai", clip=S + "A001_10311640_C028.mov", src_in=0.5, rotation=-90, scale=PUSH, max=6.5, pri=2,
         beat=3, shows="chai pot steaming at a roadside stall"),
    dict(name="C106_bookseller", clip=S + "A001_10251641_C106.mov", src_in=0.5, rotation=90, scale=62.5, max=3.0,
         pri=1, beat=3, shows="College Street bookseller among stacks of books"),
    dict(name="C111_coffee_house", clip=S + "A001_10251657_C111.mov", src_in=0.0, rotation=-90, scale=PUSH, max=3.0,
         pri=1, beat=3, shows="Indian Coffee House hall from the balcony"),
    dict(name="stock_flowers", clip="projects/kolkata/renders/stock/flowers_dedup_25_709.mov", src_in=5.4, scale=50,
         max=6.0, pri=4, beat=3, shows="Mallick Ghat flower seller (stock)"),
    dict(name="C117_uttam_mural", clip=S + "A001_10251753_C117.mov", src_in=1.5, scale=50, max=3.6, pri=4, beat=3,
         shows="Uttam Kumar on the film-strip mural"),
    dict(name="C007_maidan", clip=S + "A001_10311604_C007.mov", src_in=1.52, rotation=-90, scale=PUSH, max=4.4, pri=1,
         beat=4, shows="boys playing football on the Maidan under a pink sky"),
    dict(name="stock_victoria", clip=K + "pexels-38386435/16301337_2160_3840_30fps.mp4", src_in=13.5, rate=0.8333,
         scale=50, max=4.9, pri=2, beat=4, shows="Victoria Memorial at dusk (stock)"),
    dict(name="Oct21_C035_dancers", clip=S + "Oct21_A001_10211954_C035.mov", src_in=0.2, scale=50, max=3.7, pri=1,
         beat=5, shows="women in lal-paar saris dancing at a ghat on Dashami"),
    dict(name="Oct21_C047_dhakis", clip=S + "Oct21_A001_10212056_C047.mov", src_in=31.4, scale=50, max=3.1, pri=3,
         beat=5, shows="dhakis with kaash plumes beside the idol truck, fairy lights"),
    dict(name="Oct21_C039_ghat_lights", clip=S + "Oct21_A001_10212039_C039.mov", src_in=0.3, scale=50, max=4.3,
         pri=2, beat=5, shows="steel truss lit gold above the ghat, the immersion crowd at the water"),
    dict(name="stock_howrah_bluehour", clip=K + "pexels-38584444/16387667_2160_3840_30fps.mp4", src_in=2.0, rate=0.8333,
         scale=50, max=8.0, pri=1, beat=6, shows="Howrah Bridge at blue hour, lights coming on (stock)"),
    dict(name="C033_academy_night", clip=S + "A001_10311733_C033.mov", src_in=3.4, rotation=-90, scale=PUSH, max=4.9,
         pri=1, beat=6, shows="Academy of Fine Arts lit at night; fade to black"),
]
POOL += [   # opener-only shots (pri 5): used only when named in --open
    dict(name="C028_chai_close", clip=S + "A001_10311640_C028.mov", src_in=11.6, rotation=-90, scale=PUSH, push=(72, 75),
         max=3.2, pri=5, beat=3, shows="close on the chai pot, steam rising off the boil"),
    dict(name="C070_boat_close", clip=S + "A001_10251455_C070.mov", src_in=9.6, rotation=-90, scale=PUSH, max=4.4, pri=5,
         beat=1, shows="close on a country boat's bow on the Hooghly, the oar across it"),
    dict(name="C078_ferry_ghat", clip=S + "A001_10251512_C078.mov", src_in=1.0, rotation=90, scale=PUSH, max=9.0, pri=5,
         beat=1, shows="the Chandpal 1 Ferry Ghat gate"),
]
B = "projects/kolkata/raw/b-roll/"
V2 = {p["name"]: p for p in POOL}
# v3 pool (2026-11-07): the best of all 101 clips by eye on upright 4:5 sheets (analysis/pool_v3/), with the orientation
# fixes (C018, C025, C109 → −90; C014 → 180). pri 1 keeps the fixed clips the director asked to be used.
POOL_V3 = [
    dict(name="C072_ghat_steps", clip=B + "A001_10251456_C072.mov", src_in=0.5, scale=50, max=7.0, pri=2, beat=1,
         shows="ghat steps going down into the Hooghly, morning"),
    V2["C061_boat"],
    dict(name="C068_moored_boat", clip=B + "A001_10251455_C068.mov", src_in=1.0, rotation=-90, scale=PUSH, max=7.5,
         pri=3, beat=1, shows="a country boat moored on still water, the far bank behind"),
    dict(name="C060_ganges_ferries", clip=B + "A001_10251444_C060.mov", src_in=4.0, rotation=-90, scale=PUSH, max=3.1,
         pri=3, beat=1, shows="the 'Ganges' river ferries tied up at the jetty"),
    V2["stock_howrah_river"], V2["C064_setu"],
    {**V2["C083_walkway"], "pri": 2},
    V2["C093_scooter"],
    {**V2["C096_facade_ride"], "pri": 3},
    dict(name="C025_tram", clip=B + "A001_10311638_C025.mov", src_in=0.0, rotation=-90, scale=PUSH, max=3.5, pri=1,
         beat=2, shows="an old blue-and-white Kolkata tram under the trees (orientation fixed)"),
    V2["C100_taxi"],
    {**V2["C028_chai"], "pri": 1},
    dict(name="C105_bookstall", clip=B + "A001_10251641_C105.mov", src_in=0.3, rotation=90, scale=PUSH, max=4.3, pri=1,
         beat=3, shows="a College Street bookseller sitting in his blue-and-green stall, books laid out on the pavement"),
    {**V2["C106_bookseller"], "pri": 2},
    V2["C111_coffee_house"],
    {**V2["C117_uttam_mural"], "pri": 4},
    dict(name="C003_football", clip=B + "A001_10311601_C003.mov", src_in=0.3, rotation=-90, scale=PUSH, max=3.5, pri=3,
         beat=4, shows="boys playing football on the Maidan at dusk"),
    V2["C007_maidan"],
    dict(name="C018_kids_in_red", clip=B + "A001_10311614_C018.mov", src_in=0.5, rotation=-90, scale=PUSH, max=7.5,
         pri=1, beat=4, shows="two children in red walking a Maidan path under the trees (orientation fixed)"),
    dict(name="C019_bus_sunset", clip=B + "A001_10311629_C019.mov", src_in=2.9, rotation=-90, scale=PUSH, max=3.2,
         pri=2, beat=4, shows="people round a city bus, the sun bursting through the palms"),
    dict(name="C089_sunset_lamps", clip=B + "A001_10251601_C089.mov", src_in=6.4, rotation=-90, scale=PUSH, max=5.3,
         pri=2, beat=4, shows="the low sun through the riverside lamps, the Setu far off"),
    dict(name="C014_monument", clip=B + "A001_10311612_C014.mov", src_in=0.0, rotation=180, scale=50, max=3.5, pri=2,
         beat=4, shows="a stone memorial on the Maidan at dusk (was upside down; fixed)"),
    {**V2["stock_victoria"], "pri": 3},
    dict(name="C036_st_pauls", clip=B + "A001_11011710_C036.mov", src_in=5.2, rotation=-90, scale=PUSH, max=3.0, pri=3,
         beat=4, shows="St Paul's Cathedral at dusk"),
    dict(name="C109_pandal_lake", clip=B + "A001_10251647_C109.mov", src_in=0.5, rotation=-90, scale=PUSH, max=8.0,
         pri=1, beat=5, shows="a red-and-gold temple pandal in bamboo scaffolding, mirrored in a lake (was sideways and "
         "marked unusable; fixed)"),
    {**V2["Oct21_C047_dhakis"], "pri": 3}, V2["Oct21_C035_dancers"], V2["Oct21_C039_ghat_lights"],
    V2["stock_howrah_bluehour"],
    dict(name="C034_academy_crowd", clip=B + "A001_10311733_C034.mov", src_in=0.2, rotation=-90, scale=PUSH, max=5.0,
         pri=3, beat=6, shows="the evening crowd outside the Academy of Fine Arts"),
    V2["C033_academy_night"],
    dict(name="C010_road_dusk", clip=B + "A001_10311605_C010.mov", src_in=0.0, rotation=180, scale=50, max=3.1, pri=4,
         beat=4, shows="a Maidan road at dusk, one walker (was upside down; fixed)"),
] + [p for p in POOL if p["pri"] == 5]
# v3 ranking by eye (0 = never dropped: the ending, the fixed clips, Pujo; 1 = the strongest pictures; 4 = weakest)
V3B = {   # review gate v3 (2026-11-07) fixes, by shot name
    "C025_tram": dict(src_in=1.1, max=2.45, note="src 1.1: past the camera's auto-exposure ramp (review M1 #4, M3 #2)"),
    "C105_bookstall": dict(src_in=1.6, max=3.0, note="src 1.6: past the AE ramp (review M1 #5, M3 #3)"),
    "C064_setu": dict(src_in=2.6, max=4.2, push=(85, 87), pos=[740, 960], scale=PUSH,
                      note="src 2.6 + 85 %: after the pan clears the lamp post; bridge bigger (review M1 #7)"),
    "C109_pandal_lake": dict(src_in=48.9, rate=0.9933, max=4.5, push=(64, 66), pos=[540, 900],
                             shows="a red-and-gold temple pandal in bamboo scaffolding, mirrored in a lake (was sideways and marked unusable; fixed)",
                             note="the ferry ride's later window (48.9 s): the full reflection, clean top (review M1 #8)"),
    "C028_chai": dict(pos_push=(910, 937), shows="a roadside chai stall: the chai-wallah sets out clay cups behind a big steaming pot",
                      note="position keyed with the push so the top edge stays put (review M1 #9)"),
    "C028_chai_close": dict(src_in=11.7, max=3.0, push=(105, 108), pos=[580, 720],
                            shows="close on the pot: steam rolling off the boil, clay cups behind",
                            note="a real cut-in (105 %), pot and steam only (review M1 #1–2)"),
    "Oct21_C047_dhakis": dict(src_in=32.36, max=2.3, scale=54, pos=[570, 900],
                              note="54 %: clears the half-face at the left edge; head trimmed to the song's hit (review M3 #1, #7)"),
    "C061_boat": dict(shows="two men on a country boat drifting on the Hooghly, morning"),
    "C033_academy_night": dict(src_in=2.9, max=5.4, note="src 2.9 so the last hold can reach the section end"),
}
V3_PRI = {"C033_academy_night": 0, "C109_pandal_lake": 0, "C018_kids_in_red": 0, "C025_tram": 0, "Oct21_C035_dancers": 0,
          "C061_boat": 1, "C064_setu": 1, "C028_chai": 1, "C105_bookstall": 1, "C100_taxi": 1, "C089_sunset_lamps": 1,
          "stock_howrah_bluehour": 1, "C111_coffee_house": 1,
          "C072_ghat_steps": 2, "C019_bus_sunset": 2, "C007_maidan": 2, "C083_walkway": 2, "stock_howrah_river": 2,
          "Oct21_C039_ghat_lights": 2, "C014_monument": 2,
          "C093_scooter": 3, "C106_bookseller": 3, "C003_football": 3, "C068_moored_boat": 3, "C060_ganges_ferries": 3,
          "Oct21_C047_dhakis": 3, "C034_academy_crowd": 3, "C036_st_pauls": 3, "stock_victoria": 3,
          "C096_facade_ride": 4, "C117_uttam_mural": 4, "C010_road_dusk": 4}
POOL_V3 = [{**p, "pri": V3_PRI.get(p["name"], p["pri"])} for p in POOL_V3]
POOL_V3B = [{**p, **V3B.get(p["name"], {})} for p in POOL_V3]
BEAT_NAMES = {1: "river morning", 2: "the roads", 3: "where we gathered", 4: "evening play", 5: "Pujo calls you back",
              6: "night, the ache"}


def grid(mus: dict, start: float, length: float):
    beats = np.array([b for b in mus["beat_times_s"] if start - 0.05 <= b <= start + length + 6]) - start
    downs = np.array([d for d in mus["bar_downbeats_s"] if start - 0.05 <= d <= start + length + 6]) - start
    allb = mus["bars"]
    e_all = np.array([b["energy_db"] if "energy_db" in b else 20 * np.log10(max(b["energy"], 1e-9)) for b in allb], float)
    lo, hi = np.percentile(e_all, 5), np.percentile(e_all, 98)          # song-wide, as song_fit.py
    en_all = np.clip((e_all - lo) / max(hi - lo, 1e-6), 0, 1)
    sel = [i for i, b in enumerate(allb) if b["end_s"] > start and b["start_s"] < start + length + 6]
    bstart = np.array([allb[i]["start_s"] for i in sel]) - start
    return beats, downs, bstart, en_all[sel]


def walk(beats, downs, bstart, en, length, caps, lo=1.5, forced=(), pace=1.0):
    """Greedy cut walk. caps: per-shot max lengths (None = 5.4). Quiet bars → ~5 s holds (2 bars), loud → ~2.2 s.
    Returns cut times (0 … end)."""
    cuts, t, i = [0.0], 0.0, 0
    while t < length - 1.0:
        cap = caps[i] if caps and i < len(caps) else 5.4
        e = float(np.interp(t + 1.5, bstart, en)) if len(bstart) else 0.5
        pos = t / max(length, 1e-6)                      # the brief's arc: slow open, soft end, whatever the energy
        bias = 1.0 if pos < 0.15 else 1.4 if pos > 0.85 else 0.0
        target = min((5.0 - 2.8 * e + bias) * pace, cap)
        hi = min(cap, 6.0, length + 0.3 - t) if length - t > lo else min(cap, 6.0)
        cand_d = downs[(downs >= t + lo) & (downs <= t + hi)]
        cand_b = beats[(beats >= t + lo) & (beats <= t + hi)]
        if len(cand_d) and (not len(cand_b) or abs(cand_d - (t + target)).min() <= 0.45):
            nxt = float(cand_d[np.argmin(abs(cand_d - (t + target)))])
        elif len(cand_b):
            nxt = float(cand_b[np.argmin(abs(cand_b - (t + target)))])
        else:
            nxt = t + min(target, hi)
        f = [x for x in forced if t + 1.0 < x <= max(nxt, t + hi) + 0.05]   # a hit the cut must land on
        if f and (f[0] <= nxt + 0.3 or f[0] - t <= cap):
            nxt = f[0]
        cuts.append(round(nxt, 2)); t = nxt; i += 1
        if caps and i >= len(caps):
            break
    return cuts


def main() -> None:
    global POOL
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--song", type=Path, required=True)
    ap.add_argument("--start", type=float, required=True, help="song seconds where the reel starts (the IG start)")
    ap.add_argument("--length", type=float, default=45.0)
    ap.add_argument("--name", required=True)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--open", default="", help="comma list of shot names that open the reel, in order")
    ap.add_argument("--title-at", type=float, help="reel s of the musical hit the title lands on (a forced cut)")
    ap.add_argument("--cuts-at", default="", help="comma list of extra reel s every cut plan must land on")
    ap.add_argument("--audio-fade", type=float, default=1.2)
    ap.add_argument("--fade-in", type=int, default=6, help="frames from black at the head (3 = open on the hit)")
    ap.add_argument("--pool", default="v3", choices=["v2", "v3", "v3b"], help="v3 = best-of-all-clips pool with orientation fixes; v3b = + review-gate fixes")
    ap.add_argument("--beat-lag", type=float, default=0.0, help="s subtracted from detected beats (the tracker lands late)")
    ap.add_argument("--pace", type=float, default=1.0, help="× every target shot length (0.8 = 20 %% faster)")
    a = ap.parse_args()
    if a.pool == "v3":
        POOL = POOL_V3
    elif a.pool == "v3b":
        POOL = POOL_V3B
    opens = [x for x in a.open.split(",") if x]
    forced = sorted([float(x) for x in a.cuts_at.split(",") if x] + ([a.title_at] if a.title_at else []))
    mus = analyze_music_beats(ROOT / a.song if not a.song.is_absolute() else a.song)
    beats, downs, bstart, en = grid(mus, a.start, a.length)
    beats, downs = beats - a.beat_lag, downs - a.beat_lag
    head = [next(p for p in POOL if p["name"] == o) for o in opens]
    rest = [k for k, p in enumerate(POOL) if p["name"] not in opens and p["pri"] < 5]
    order = sorted(rest, key=lambda k: (POOL[k]["pri"], k))   # who survives when slots are short
    best = None
    for n in range(6, len(order) + 1):                   # n shots by priority, spine order; every shot must get a slot
        pool = head + [POOL[k] for k in sorted(order[:n])]
        cuts = walk(beats, downs, bstart, en, a.length, [p["max"] for p in pool], forced=forced, pace=a.pace)
        if len(cuts) - 1 != len(pool) or any(min(abs(np.array(cuts) - f)) > 0.05 for f in forced):
            continue
        gap = abs(cuts[-1] - a.length)
        if best is None or gap < best[0] - 1e-6:
            best = (gap, pool, cuts)
    _, pool, cuts = best
    if cuts[-1] < a.length - 0.3:                        # stretch the last shot to the section end, on a beat
        ok = beats[(beats > cuts[-1]) & (beats <= min(a.length + 0.3, cuts[-2] + pool[-1]["max"]))]
        if len(ok):
            cuts[-1] = round(float(ok[-1]), 2)
    if len(cuts) > 3 and not any(abs(cuts[-2] - f) < 0.06 for f in forced):   # soft end (never moves a forced cut)
        t0, t2 = cuts[-3], cuts[-1]
        ok = beats[(beats >= t0 + 2.0) & (beats <= t2 - 2.0) & (beats - t0 <= pool[-2]["max"]) &
                   (t2 - beats <= pool[-1]["max"])]
        if len(ok):
            cuts[-2] = round(float(ok[np.argmin(abs((t2 - ok) - 0.58 * (t2 - t0)))]), 2)
    fps, shots = 25, []
    for k, p in enumerate(pool):
        s0, s1 = cuts[k], cuts[k + 1]
        sh = {kk: v for kk, v in p.items() if kk not in ("max", "pri", "beat", "pos_push")}
        sh["name"] = f"{k + 1:02d}_{p['name']}"
        sh.update(start=round(s0, 2), end=round(s1, 2), pos=p.get("pos", [540, 910]), role=f"beat {p['beat']}: {BEAT_NAMES[p['beat']]}")
        if "pos_push" in p:
            sh["pos"] = [[0, 540, p["pos_push"][0]], [round(s1 - s0, 2), 540, p["pos_push"][1]]]
        sh.pop("push", None)
        if isinstance(p["scale"], list):
            a0, a1 = p.get("push", (62.5, 65.0))
            sh["scale"] = [[0, a0], [round(s1 - s0, 2), a1]]; sh["ease"] = "ease"
        sh.setdefault("rate", 1)
        shots.append(sh)
    shots[0]["fade_in"] = a.fade_in
    shots[-1]["fade_out"] = 20
    runtime = shots[-1]["end"]
    if a.title_at is not None:
        title = next(s for s in shots if abs(s["start"] - a.title_at) < 0.06)
    else:
        title = next(s for s in shots if "C064" in s["name"])
    title["shows"] += "; 'Calcutta' title"
    edl = {"fps": fps, "runtime": runtime,
           "note": f"KOLKATA song audition ({a.name}). {a.song.name} from {a.start:.2f} s for {runtime:.2f} s; "
                   f"{mus['bpm']:.0f} BPM. Same 6-beat pool as the other auditions; cuts on this song's beats."
                   + (f" Opens on {', '.join(opens)}." if opens else "")
                   + (f" Title on the hit at {a.title_at:.2f} s." if a.title_at is not None else ""),
           "shots": shots,
           "overlays": [{"file": "projects/kolkata/renders/overlays/window_matte.png", "start": 0.0, "end": runtime},
                        {"file": "projects/kolkata/renders/overlays/title_calcutta.png", "start": title["start"],
                         "end": title["end"]}],
           "audio": [{"file": str(a.song), "start": 0.0, "in": a.start, "gain_db": 0.0, "fade_in": 0, "fade_out": a.audio_fade}]}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(edl, indent=1))
    lens = np.diff(cuts[:len(shots) + 1])
    print(f"✓ {a.out}  {len(shots)} shots, {runtime:.2f} s, shot {lens.min():.2f}–{lens.max():.2f} s "
          f"(median {np.median(lens):.2f}), dropped: {[p['name'] for p in POOL if p not in pool and p['pri'] < 5]}, "
          f"title on {title['name']} at {title['start']:.2f}")


if __name__ == "__main__":
    main()
