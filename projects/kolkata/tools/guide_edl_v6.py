#!/usr/bin/env python3
"""KOLKATA round 6: "Your guide to Kolkata", cut from what each line of the song means (lyric line table).

Director (2026-11-07, on v5b):
  - cut the guide's name: the spoken line must be "ami … apnader guide" ("I am … your guide"), no name;
  - the Coffee House image is bad ("I had multiple better footage");
  - the frame for "city of surprises" doesn't match;
  - why is the girl in the Metro station there? (no unexplained people);
  - the transition sound and effect: not liked (whip, whoosh, flash, riser, light leaks all removed);
  - understand the lyric and determine the shots from it.

The song edit: song 25.72 → 28.273 s (the name, between "Ami" and "apnader guide") is cut out, exactly 5 beats at
117.5 BPM, so the music bed under the voice stays on its grid. tools/song_edit_v6.py writes music/kolkata_v6_edit.wav.
Reel time = song − OFF before the cut, song − OFF − CUT after it.

Line meanings (summarised from the round-6 Whisper large-v3 re-transcription; never quoted):
  intro (spoken): Kolkata is a city of culture, heritage and surprises; I am your guide, but I call myself an
  explorer; some say Paris is the city of love, I say Kolkata is the city of passion.
  verse: love floods the city like a monsoon; light everywhere; sometimes a stranger drops in out of nowhere and
  loves you; my forever Kolkata.
  chorus: Kolkata, you too walk and see; you too think it over; will you come with me or not.

Usage (studio root):
  python3 projects/kolkata/tools/song_edit_v6.py
  python3 projects/kolkata/tools/guide_edl_v6.py -o projects/kolkata/analysis/edl_v6.json --jobs projects/kolkata/analysis/fx_jobs_v6.json
  .venv/bin/python projects/kolkata/tools/fx_prerender.py --jobs projects/kolkata/analysis/fx_jobs_v6.json
"""
import argparse
import json
from pathlib import Path

OFF = 7.25
END_SONG = 86.00
CUT_A, CUT_B = 25.72, 28.273          # song seconds removed (the guide's name)
CUT = CUT_B - CUT_A
SONG = "projects/kolkata/music/kolkata_v6_edit.wav"
B, S, K = "projects/kolkata/raw/b-roll/", "projects/kolkata/raw/selects/", "projects/kolkata/raw/stock/"
FX = "projects/kolkata/renders/fx_preview/"
C30, C24, C60 = 25 / 30, 25 / 24, 25 / 60
C2398 = 25 / 23.976
STAB = dict(stab="smooth", sigma=15, zoom=1.05)


def push(a, b):
    return ("push", a, b)


def reel(song_t):
    return song_t - OFF - (CUT if song_t >= CUT_B else 0.0)


# (song start, what the line means, shot). One shot per line unless the line is long.
LINES = [
    (7.25, "[instrumental] the record goes on; the song starts from it",
     dict(name="rec_record_on", clip=K + "pexels-8090957/8090957-uhd_2732_1440_24fps.mp4", src_in=0.8, rate=C24,
          scale=push(93.75, 100), pos=[900, 910], fade_in=6,
          shows="hands lower a record onto a vintage wooden record player; it settles as the song's first note plays")),
    (12.91, "[instrumental] title KOLKATA on the bar",
     dict(name="rec_stylus_title", clip=K + "pexels-6742732/6742732-uhd_3840_2160_24fps.mp4", src_in=2.0, rate=C2398,
          scale=push(62.5, 66.0), pos=[-110, 910], shows="stylus in the groove of the spinning record; title 'Kolkata' settles on the bar")),
    (17.80, "guide: Kolkata is a city of culture",
     dict(name="C111_coffee_house", clip=B + "A001_10251657_C111.mov", src_in=0.0, rotation=-90, scale=push(62.5, 65.0),
          fx=dict(rate=0.7),
          shows="the Indian Coffee House hall from the balcony: tables, lamps, waiters in white (locked); 70 % slow motion")),
    (21.74, "guide: city of heritage",
     dict(name="stock_victoria", clip=K + "pexels-38386435/16301337_2160_3840_30fps.mp4", src_in=13.5, rate=C30, scale=50,
          shows="Victoria Memorial at dusk down the tree-lined path, people walking")),
    (23.18, "guide: and city of surprises",
     dict(name="stock_rickshaw_tracks", clip=K + "pexels-32665218/13926753_3840_2160_24fps.mp4", src_in=1.00, rate=C2398, scale=62.5,
          shows="a hand-pulled rickshaw runs toward us down the tram tracks past yellow taxis: the old city still running")),
    (25.16, "guide: I am your guide, but I call myself an explorer (one walk, the name cut from the song)",
     dict(name="C082_walkway_pov", clip=B + "A001_10251528_C082.mov", src_in=0.0, rotation=90, scale=push(62.5, 66.0),
          fx=dict(stab="smooth", sigma=20, zoom=1.06),
          shows="walking POV into the Howrah Bridge walkway, the truss overhead: follow me; stabilised, horizon level")),
    (31.56, "guide (Bengali): some say Paris is the city of love",
     dict(name="C089_sunset_lamps", clip=S + "A001_10251601_C089.mov", src_in=6.4, rotation=-90, scale=push(62.5, 65.0),
          shows="iron lamp posts along the river promenade against the sun")),
    (34.86, "guide (Bengali): I say Kolkata is the city of passion (ramp into slow motion)",
     dict(name="Oct21_C047_dhakis", clip=S + "Oct21_A001_10212056_C047.mov", src_in=32.2, scale=54, pos=[570, 900],
          fx=dict(speed_keys=[[0, 1.0], [0.8, 1.0], [1.7, 0.4]], stab="smooth", sigma=12, zoom=1.05),
          shows="a dhaki in white drumming; real speed, then easing into 40 % slow motion on 'passion'; stabilised")),
    (37.27, "guide: … passion (hard cut on the accent)",
     dict(name="Oct21_C035_dancers", clip=S + "Oct21_A001_10211954_C035.mov", src_in=0.2, scale=50,
          fx=dict(rate=0.65),
          shows="women in lal-paar saris dancing at a ghat on Dashami, 65 % slow motion")),
    (39.31, "verse: love floods the city like a monsoon",
     dict(name="stock_setu_sunset", clip=K + "pexels-3939524/3939524-hd_1920_1080_25fps.mp4", src_in=0.5, scale=push(125, 130),
          dissolve=10, shows="the sun over the Vidyasagar Setu, a country boat on the Hooghly")),
    (43.28, "verse: light everywhere",
     dict(name="stock_ghat_bathers", clip=K + "pexels-4200197/4200197-hd_1920_1080_30fps.mp4", src_in=2.0, rate=C30, scale=125,
          shows="people bathing on the ghat steps in the light, Howrah Bridge across the river")),
    (47.58, "verse: … everywhere",
     dict(name="stock_ghat_cricket", clip=K + "pexels-5013993/5013993-hd_1920_1080_25fps.mp4", src_in=0.5, scale=125, pos=[1200, 910],
          shows="a boy batting on the ghat, Howrah Bridge behind")),
    (49.62, "verse: sometimes a stranger drifts in out of nowhere",
     dict(name="C061_boatmen", clip=S + "A001_10251448_C061.mov", src_in=4.0, rotation=-90, scale=push(62.5, 65.0),
          fx=dict(rate=0.7, **STAB),
          shows="a country boat drifting in on the Hooghly, two boatmen; stabilised, 70 % slow motion")),
    (51.76, "verse: … arriving by the river",
     dict(name="stock_under_howrah", clip=K + "pexels-40180894/17164810_2160_3840_60fps.mp4", src_in=5.0, rate=C60, scale=50,
          shows="arriving under Howrah Bridge by the river, the girders sliding overhead, real slow motion")),
    (53.85, "verse: … and loves you",
     dict(name="stock_flower_market", clip=K + "pexels-35071306/14856170_1080_1920_60fps.mp4", src_in=1.0, rate=C60, scale=100,
          shows="the Mallick Ghat flower market from above: heaps of marigolds, slow motion")),
    (55.87, "verse: … loves you",
     dict(name="stock_marigold_porter", clip=K + "pexels-35067019/14854118_1080_1920_60fps.mp4", src_in=0.5, rate=C60, scale=100,
          shows="a porter carrying marigolds on his head under Howrah Bridge, slow motion")),
    (57.96, "verse: my forever Kolkata",
     dict(name="stock_flower_seller", clip=K + "pexels-39276190/16712869_2160_3840_60fps.mp4", src_in=3.0, rate=C60, scale=50,
          shows="a flower seller among red and yellow flowers, slow motion")),
    (60.00, "verse: … forever",
     dict(name="stock_kumartuli", clip=K + "pexels-40160762/17153775_3840_2160_24fps.mp4", src_in=2.0, rate=C24, scale=push(62.5, 65.0), pos=[1000, 910],
          shows="artisans painting a row of idols at Kumartuli, a craft as old as the city")),
    (62.11, "chorus: Kolkata, you too walk and see (one line, one walk)",
     dict(name="C018_walk_red", clip=S + "A001_10311614_C018.mov", src_in=0.5, rotation=-90, scale=push(62.5, 66.0),
          fx=dict(rate=0.6),
          shows="an adult and a child in red walking the Maidan path, 60 % slow motion")),
    (66.27, "chorus: Kolkata, you too think it over",
     dict(name="C105_bookseller", clip=S + "A001_10251641_C105.mov", src_in=1.6, rotation=90, scale=push(62.5, 65.0),
          shows="an old College Street bookseller sitting at his stall, thinking")),
    (68.31, "chorus: Kolkata, you too walk and see (the old streets)",
     dict(name="stock_tram_street", clip=K + "pexels-2843866/2843866-hd_1920_1080_30fps.mp4", src_in=15.5, rate=C30, scale=125,
          fx=dict(interpret=True, half=False, stab="smooth", sigma=18, zoom=1.08),
          shows="old houses, yellow taxis and a Kolkata tram passing; stabilised")),
    (72.42, "chorus: … walk and see",
     dict(name="C101_taxi", clip=B + "A001_10251635_C101.mov", src_in=0.5, scale=push(50, 53),
          shows="a yellow Ambassador taxi on the tram lines, a man walking past it")),
    (74.51, "chorus: Kolkata, you too think it over",
     dict(name="C028_chai", clip=S + "A001_10311640_C028.mov", src_in=0.5, rotation=-90, scale=push(62.5, 65.0),
          pos=[[0, 540, 910], [1, 540, 937]], fx=dict(rate=0.5),
          shows="a chai pot steaming at a stall, the chai-wallah behind: thinking it over a cup of tea; 50 % slow motion")),
    (76.60, "chorus: … dusk",
     dict(name="stock_howrah_bluehour", clip=K + "pexels-38584444/16387667_2160_3840_30fps.mp4", src_in=2.0, rate=C30, scale=50,
          shows="Howrah Bridge at blue hour, the traffic lights coming on")),
    (78.65, "chorus: will you come with me or not?",
     dict(name="C030_tram_night", clip=S + "A001_10311647_C030.mov", src_in=2.0, rotation=-90, scale=push(62.5, 65.0),
          shows="inside a Kolkata tram at night, warm lamps and the windows: the seat beside you (tram bell)")),
    (82.76, "outro: the city waits at night",
     dict(name="C033_academy_night", clip=B + "A001_10311733_C033.mov", src_in=3.80, rotation=-90, scale=push(62.5, 65.5), fade_out=20,
          fx=dict(rate=0.75),
          shows="the Academy of Fine Arts lit at night, people at the door (bookends 'a city of culture'); 75 % slow motion; fade to black")),
]

SFX = [  # file, song time it starts at (before the reel shift), source in, gain dB, fade out s. No transition SFX (director)
    ("projects/kolkata/sfx/pixabay-37522_vinyl_needle_drop_crackle.mp3", 2.40 - 0.28 + OFF, 0.0, -8.0, 1.0),          # needle drop
    ("projects/kolkata/sfx/pixabay-339952_kolkata_tram_approach_bell.mp3", 78.65 - 0.4, 8.4, -20.0, 0.6),              # tram bell
]


def r(t):
    return round(round(t * 25) / 25, 2)


def scaled(v, k):
    if isinstance(v, tuple):
        return ("push", v[1] * k, v[2] * k)
    return v * k


def build():
    shots, jobs = [], []
    for i, (t0, line, sh) in enumerate(LINES):
        t1 = LINES[i + 1][0] if i + 1 < len(LINES) else END_SONG
        s = dict(sh)
        fx = s.pop("fx", None)
        a, b = r(reel(t0)), r(reel(t1))
        dur = round(b - a, 2)
        s["name"] = f"{i + 1:02d}_{s['name']}"
        s.update(start=a, end=b, line=line)
        s.setdefault("rate", 1)
        s.setdefault("pos", [540, 910])
        if fx:
            jid = s["name"][3:]
            job = dict(id=jid, clip=s["clip"], src_in=s["src_in"], out_dur=round(dur + 0.12, 2), pad=3)
            if "rate" not in fx and "speed_keys" not in fx and s["rate"] != 1:
                fx = dict(fx, rate=round(s["rate"], 4))
            job.update(fx)
            jobs.append(job)
            k = 2 if fx.get("half", True) else 1
            how = ", ".join(f"{key} {val}" for key, val in fx.items())
            s["note"] = f"build: camera {s['clip'].rsplit('/', 1)[-1]} in {s['src_in']:.2f} s, {how}; preview uses the fx pre-render"
            s.update(clip=FX + jid + ".mov", src_in=0.0, rate=1, scale=scaled(s["scale"], k))
        if isinstance(s.get("scale"), tuple):
            s["scale"] = [[0, round(s["scale"][1], 3)], [dur, round(s["scale"][2], 3)]]
            s["ease"] = "ease"
        if isinstance(s["pos"][0], list):
            s["pos"] = [[0, s["pos"][0][1], s["pos"][0][2]], [dur, s["pos"][-1][1], s["pos"][-1][2]]]
        s["rate"] = round(s["rate"], 4)
        shots.append(s)
    runtime = r(reel(END_SONG))
    audio = [{"file": SONG, "start": 0.0, "in": OFF, "gain_db": 0.0, "fade_in": 0, "fade_out": 1.5}]
    audio += [{"file": f, "start": round(reel(st), 2), "in": i, "gain_db": g, "fade_in": 0, "fade_out": fo} for f, st, i, g, fo in SFX]
    edl = {
        "fps": 25, "runtime": runtime,
        "note": f"KOLKATA v6 'Your guide to Kolkata' (round 6): lyric line table. {SONG} (the song with the guide's name cut, "
                f"song {CUT_A}–{CUT_B} s) from {OFF} s for {runtime} s. No transition effects or transition SFX. "
                f"Own-shot slow motion / stabilisation are offline pre-renders; the build uses AE Timewarp and Warp Stabilizer.",
        "overlays": [{"file": "projects/kolkata/renders/overlays/window_matte.png", "start": 0.0, "end": runtime},
                     {"file": "projects/kolkata/renders/overlays/title_kolkata.png", "start": r(reel(15.00)), "end": r(reel(17.80))}],
        "audio": audio,
        "shots": shots,
    }
    return edl, jobs


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", required=True)
    ap.add_argument("--jobs", required=True)
    a = ap.parse_args()
    edl, jobs = build()
    Path(a.o).write_text(json.dumps(edl, indent=1, ensure_ascii=False))
    Path(a.jobs).write_text(json.dumps(jobs, indent=1, ensure_ascii=False))
    for s in edl["shots"]:
        print(f'{s["name"]:26s} {s["start"]:6.2f}-{s["end"]:6.2f} ({s["end"] - s["start"]:.2f}) r{s["rate"]:<6} {s["line"]}')
    print("runtime", edl["runtime"], "shots", len(edl["shots"]), "fx jobs", len(jobs))
