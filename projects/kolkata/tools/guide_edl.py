#!/usr/bin/env python3
"""KOLKATA round 5: "Your guide to Kolkata", the EDL written from a line table (song moment → line → shot).

Director (2026-11-07): follow the reference's opening and story; use free stock where our footage can't replicate it;
cinematic effects (slow motion, ramps, designed transitions); then: use the song "Kolkata" (Praktan, Anupam Roy /
Shreya Ghoshal) and its spoken "Urja Mukherjee, your guide" intro as the guide; a story of 60–90 s.

Times below are SONG seconds in music/kolkata.wav (Whisper large-v3-turbo word timings, the bar grid from
research/kolkata_song/beats.json). Reel time = song − OFF. The song's first note is at 9.80 s, so with OFF 7.25 it
lands at reel 2.55, as the record settles on the platter (the reference's "the song starts from the record").
Spoken clauses: cut on the clause onset. Sung part: cut on bar downbeats the band plays.

Usage (studio root):
  python3 projects/kolkata/tools/guide_edl.py -o projects/kolkata/analysis/edl_v5_guide.json
"""
import argparse
import json
from pathlib import Path

OFF = 7.25
END_SONG = 86.00
B, S, K = "projects/kolkata/raw/b-roll/", "projects/kolkata/raw/selects/", "projects/kolkata/raw/stock/"
C30, C24, C60 = 25 / 30, 25 / 24, 25 / 60          # rate for 30 / 24 fps clips conformed to 25, and 60 fps real slow-mo
C2398 = 25 / 23.976


def push(a, b):
    return ("push", a, b)


# (song start, line it carries, shot). Each shot ends where the next starts; the last ends at END_SONG.
LINES = [
    (7.25, "[instrumental] the record goes on; the song starts from it",
     dict(name="rec_record_on", clip=K + "pexels-8090957/8090957-uhd_2732_1440_24fps.mp4", src_in=0.8, rate=C24,
          scale=push(93.75, 100), pos=[900, 910], fade_in=6,
          shows="hands lower a record onto a vintage wooden record player; it settles as the song's first note plays")),
    (12.91, "[instrumental] title KOLKATA on the bar",
     dict(name="rec_stylus_title", clip=K + "pexels-6742732/6742732-uhd_3840_2160_24fps.mp4", src_in=2.0, rate=C2398,
          scale=push(62.5, 66.0), pos=[-110, 910], shows="stylus in the groove of the spinning record; title 'Kolkata' settles on the bar")),
    (17.80, "VO: to me Kolkata is a city of culture",
     dict(name="C112_coffee_house", clip=B + "A001_10251658_C112.mov", src_in=0.0, rotation=-90, scale=push(62.5, 65.0),
          shows="Indian Coffee House hall from the balcony: lamps, tables, waiters in white")),
    (21.74, "VO: city of heritage",
     dict(name="stock_victoria", clip=K + "pexels-38386435/16301337_2160_3840_30fps.mp4", src_in=13.5, rate=C30, scale=50,
          shows="Victoria Memorial at dusk down the tree-lined path, people walking")),
    (23.18, "VO: and city of surprises",
     dict(name="C110_pandal_lake", clip=B + "A001_10251648_C110.mov", src_in=0.0, rotation=-90, scale=push(62.5, 66.0),
          shows="a red-gold Pujo pandal built like a palace, mirrored in a lake (whip in, whoosh)")),
    (25.16, "VO: I am Urja Mukherjee, your guide",
     dict(name="C082_walkway_pov", clip=B + "A001_10251528_C082.mov", src_in=0.0, rotation=90, scale=push(62.5, 65.0),
          shows="walking POV into the Howrah Bridge walkway, the truss overhead: follow me")),
    (29.50, "VO: but I call myself an explorer (ramp in)",
     dict(name="C094_scooter_ramp", clip=B + "A001_10251620_C094.mov", src_in=12.0, rate=2.5, scale=50,
          shows="scooter POV, speedometer in frame: a 250 % speed ramp into the ride (whoosh)")),
    (30.10, "VO: … an explorer",
     dict(name="C094_scooter_ride", clip=B + "A001_10251620_C094.mov", src_in=13.5, scale=50,
          shows="scooter POV riding a road of red heritage façades, back to normal speed")),
    (31.56, "VO (Bengali): some say Paris is the city of love",
     dict(name="C089_sunset_lamps", clip=S + "A001_10251601_C089.mov", src_in=6.4, rotation=-90, scale=push(62.5, 65.0),
          shows="iron lamp posts along the river promenade against the sun")),
    (34.86, "VO (Bengali): I say Kolkata is the city of passion",
     dict(name="Oct21_C047_dhakis", clip=S + "Oct21_A001_10212056_C047.mov", src_in=32.2, scale=54, pos=[570, 900],
          shows="dhakis drumming at Pujo")),
    (37.27, "VO: … passion (accent: flash cut)",
     dict(name="Oct21_C035_dancers", clip=S + "Oct21_A001_10211954_C035.mov", src_in=0.2, scale=50,
          shows="women in lal-paar saris dancing at a ghat on Dashami (flash on the accent)")),
    (39.31, "verse 1: the city in golden light (the reference's river)",
     dict(name="stock_setu_sunset", clip=K + "pexels-3939524/3939524-hd_1920_1080_25fps.mp4", src_in=0.5, scale=push(125, 130),
          dissolve=10, shows="the sun over the Vidyasagar Setu, a country boat on the Hooghly")),
    (43.28, "verse 1: people at the ghat",
     dict(name="stock_ghat_bathers", clip=K + "pexels-4200197/4200197-hd_1920_1080_30fps.mp4", src_in=2.0, rate=C30, scale=125,
          shows="people bathing on the ghat steps, Howrah Bridge across the river")),
    (47.58, "verse 1: a boy at play on the ghat",
     dict(name="stock_ghat_cricket", clip=K + "pexels-5013993/5013993-hd_1920_1080_25fps.mp4", src_in=0.5, scale=125, pos=[1200, 910],
          shows="a boy batting on the ghat, Howrah Bridge behind")),
    (49.62, "verse 1: on the river",
     dict(name="C061_boatmen", clip=S + "A001_10251448_C061.mov", src_in=4.0, rotation=-90, scale=push(62.5, 65.0),
          shows="two boatmen on a drifting country boat on the Hooghly")),
    (51.76, "verse 1: under Howrah, from the river (slow motion)",
     dict(name="stock_under_howrah", clip=K + "pexels-40180894/17164810_2160_3840_60fps.mp4", src_in=5.0, rate=C60, scale=50,
          shows="under Howrah Bridge from the river, the girders sliding overhead, real slow motion")),
    (53.85, "verse 1: the flower market (slow motion)",
     dict(name="stock_flower_market", clip=K + "pexels-35071306/14856170_1080_1920_60fps.mp4", src_in=1.0, rate=C60, scale=100,
          shows="Mallick Ghat flower market from above: marigold heaps and the crowd, slow motion")),
    (55.87, "verse 1: a porter under the bridge (slow motion)",
     dict(name="stock_marigold_porter", clip=K + "pexels-35067019/14854118_1080_1920_60fps.mp4", src_in=0.5, rate=C60, scale=100,
          shows="a porter carrying a basket of marigolds on his head under Howrah Bridge, slow motion")),
    (57.96, "verse 1: the flower seller (slow motion)",
     dict(name="stock_flower_seller", clip=K + "pexels-39276190/16712869_2160_3840_60fps.mp4", src_in=3.0, rate=C60, scale=50,
          shows="a Mallick Ghat seller among red and yellow flowers, slow motion")),
    (60.00, "verse 1 end: Kumartuli (the reference's colourful lane)",
     dict(name="stock_kumartuli", clip=K + "pexels-40160762/17153775_3840_2160_24fps.mp4", src_in=2.0, rate=C24, scale=push(62.5, 65.0), pos=[1000, 910],
          shows="artisans painting a row of Durga idols at Kumartuli")),
    (62.11, "chorus: Kolkata, come walk and see",
     dict(name="stock_wall_writing", clip=K + "pexels-2843864/2843864-hd_1920_1080_30fps.mp4", src_in=17.5, rate=C30, scale=125,
          shows="people walking past Bengali wall writing on a weathered wall")),
    (64.18, "chorus: … walk and see",
     dict(name="C018_walk_red", clip=S + "A001_10311614_C018.mov", src_in=0.5, rotation=-90, scale=push(62.5, 65.0),
          shows="an adult and a child in red walking on the Maidan path")),
    (66.27, "chorus: Kolkata, come think it over",
     dict(name="C105_bookseller", clip=S + "A001_10251641_C105.mov", src_in=1.6, rotation=90, scale=push(62.5, 65.0),
          shows="an old College Street bookseller sitting at his stall")),
    (68.31, "chorus: Kolkata, come walk (the old streets)",
     dict(name="stock_tram_street", clip=K + "pexels-2843866/2843866-hd_1920_1080_30fps.mp4", src_in=15.5, rate=C30, scale=125,
          shows="old houses, yellow taxis and a Kolkata tram passing")),
    (72.42, "chorus: … rushing past",
     dict(name="C097_facade_ride", clip=B + "A001_10251624_C097.mov", src_in=3.5, scale=50,
          shows="red heritage façades and bougainvillea rushing past the scooter (step-print in the build)")),
    (74.51, "chorus: Kolkata, think it over",
     dict(name="C028_chai", clip=S + "A001_10311640_C028.mov", src_in=0.5, rotation=-90, scale=push(62.5, 65.0),
          pos=[[0, 540, 910], [1, 540, 937]], shows="a chai pot steaming at a stall, the chai-wallah behind")),
    (76.60, "chorus: dusk on the bridge",
     dict(name="stock_howrah_bluehour", clip=K + "pexels-38584444/16387667_2160_3840_30fps.mp4", src_in=2.0, rate=C30, scale=50,
          shows="Howrah Bridge at blue hour, the traffic lights coming on")),
    (78.65, "chorus: will you come with me? (the tram ride)",
     dict(name="C030_tram_night", clip=S + "A001_10311647_C030.mov", src_in=2.0, rotation=-90, scale=push(62.5, 65.0),
          shows="inside a Kolkata tram at night, warm lamps and the windows (tram bell)")),
    (82.76, "outro: Howrah lit at night",
     dict(name="stock_diya_howrah", clip=K + "pexels-34545518/14637288_2160_3840_17fps.mp4", src_in=0.0, scale=50, fade_out=20,
          shows="a diya floating on the river, Howrah Bridge lit behind; fade to black")),
]

SFX = [  # file, reel start, source in, gain dB, fade out s
    ("projects/kolkata/sfx/pixabay-37522_vinyl_needle_drop_crackle.mp3", 2.40 - 0.28, 0.0, -8.0, 1.0),   # needle drop at 2.40
    ("assets/sfx/gemini_whoosh_soft.wav", 23.18 - OFF - 0.21, 0.0, -11.0, 0.0),                           # whip into the pandal
    ("assets/sfx/gemini_whoosh_soft.wav", 29.50 - OFF - 0.10, 0.0, -14.0, 0.0),                           # explorer ramp
    ("assets/sfx/gemini_riser_sub_hit.wav", 37.27 - OFF - 1.04, 0.0, -14.0, 0.0),                         # flash on the accent
    ("projects/kolkata/sfx/pixabay-339952_kolkata_tram_approach_bell.mp3", 78.65 - OFF - 0.4, 8.4, -20.0, 0.6),  # tram bell
]


def r(t):
    return round(round(t * 25) / 25, 2)


def build():
    shots = []
    for i, (t0, line, sh) in enumerate(LINES):
        t1 = LINES[i + 1][0] if i + 1 < len(LINES) else END_SONG
        s = dict(sh)
        a, b = r(t0 - OFF), r(t1 - OFF)
        dur = round(b - a, 2)
        s["name"] = f"{i + 1:02d}_{s['name']}"
        s.update(start=a, end=b, line=line)
        s.setdefault("rate", 1)
        s.setdefault("pos", [540, 910])
        if isinstance(s.get("scale"), tuple):
            s["scale"] = [[0, s["scale"][1]], [dur, s["scale"][2]]]
            s["ease"] = "ease"
        if isinstance(s["pos"][0], list):
            s["pos"] = [[0, s["pos"][0][1], s["pos"][0][2]], [dur, s["pos"][-1][1], s["pos"][-1][2]]]
        s["rate"] = round(s["rate"], 4)
        shots.append(s)
    runtime = r(END_SONG - OFF)
    flash = r(37.27 - OFF)
    audio = [{"file": "projects/kolkata/music/kolkata.wav", "start": 0.0, "in": OFF, "gain_db": 0.0, "fade_in": 0, "fade_out": 1.5}]
    audio += [{"file": f, "start": round(st, 2), "in": i, "gain_db": g, "fade_in": 0, "fade_out": fo} for f, st, i, g, fo in SFX]
    return {
        "fps": 25, "runtime": runtime,
        "note": f"KOLKATA v5 'Your guide to Kolkata' (round 5). music/kolkata.wav from {OFF} s for {runtime} s "
                f"(IG start ≈ the song's spoken intro; first note at reel {9.80 - OFF:.2f}). Line table in project.md Round 5.",
        "overlays": [{"file": "projects/kolkata/renders/overlays/window_matte.png", "start": 0.0, "end": runtime},
                     {"file": "projects/kolkata/renders/overlays/title_kolkata.png", "start": r(15.00 - OFF), "end": r(17.80 - OFF)},
                     {"file": "projects/kolkata/renders/overlays/flash_white.png", "start": flash, "end": r(flash + 0.12)}],
        "audio": audio,
        "shots": shots,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", required=True)
    a = ap.parse_args()
    edl = build()
    Path(a.o).write_text(json.dumps(edl, indent=1, ensure_ascii=False))
    for s in edl["shots"]:
        print(f'{s["name"]:26s} {s["start"]:6.2f}-{s["end"]:6.2f} ({s["end"] - s["start"]:.2f}) r{s["rate"]:<6} {s["line"]}')
    print("runtime", edl["runtime"], "shots", len(edl["shots"]))
