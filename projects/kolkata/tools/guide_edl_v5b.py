#!/usr/bin/env python3
"""KOLKATA round 5b: "Your guide to Kolkata", revised after the director's notes on preview v5.

Director (2026-11-07, on v5): "the final shot I don't like; a few of my shots need stabilisation and cinematic effect;
the swooping shots don't make it good; the shots of 'city of surprises' can be better; we are on the right track".

What changes from v5 (tools/guide_edl.py; same song window, same line timings):
  - swooping shots out: C094 scooter POV (jitter 20–32 px) and C097 façade ride (56 px, 700 px/s);
  - stabilised: C112 Coffee House, C082 walkway, C047 dhakis, C061 boatmen, the stock tram street;
  - slow motion on our own shots (25 fps, so interpolated: AE Timewarp in the build), a speed ramp into slow-mo on
    the dhakis on "passion", a whip pan into "surprises";
  - new "surprises", "explorer" and final shots (analysis/round5b_picks/PICKS.md).
Treated shots are pre-rendered by tools/fx_prerender.py from the jobs file this script writes; in the EDL they point at
renders/fx_preview/<id>.mov (src_in 0, rate 1, Scale doubled for the half-size render). Each shot's "note" keeps the
camera in-point, rate and treatment for the Premiere build.

Usage (studio root):
  python3 projects/kolkata/tools/guide_edl_v5b.py -o projects/kolkata/analysis/edl_v5b.json \
      --jobs projects/kolkata/analysis/fx_jobs_v5b.json
  .venv/bin/python projects/kolkata/tools/fx_prerender.py --jobs projects/kolkata/analysis/fx_jobs_v5b.json
"""
import argparse
import json
from pathlib import Path

OFF = 7.25
END_SONG = 86.00
B, S, K = "projects/kolkata/raw/b-roll/", "projects/kolkata/raw/selects/", "projects/kolkata/raw/stock/"
FX = "projects/kolkata/renders/fx_preview/"
C30, C24, C60 = 25 / 30, 25 / 24, 25 / 60
C2398 = 25 / 23.976
STAB = dict(stab="smooth", sigma=15, zoom=1.05)


def push(a, b):
    return ("push", a, b)


# (song start, line, shot). "fx" = pre-render treatment: rate / speed_keys, stab, whip, interpret, half.
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
          fx=dict(rate=0.7, **STAB),
          shows="Indian Coffee House hall from the balcony: lamps, tables, waiters in white; stabilised, 70 % slow motion")),
    (21.74, "VO: city of heritage",
     dict(name="stock_victoria", clip=K + "pexels-38386435/16301337_2160_3840_30fps.mp4", src_in=13.5, rate=C30, scale=50,
          fx=dict(interpret=True, whip_out=3, whip_dir=-1),
          shows="Victoria Memorial at dusk down the tree-lined path; whips out to the left")),
    # SURPRISES: giant LED petal arches over a packed street (round5b_picks slot 1 #2). The forge pandal (C088) was
    # unreadable to the director ("couldn't find a clue what that pandal is"): the arches read at a glance
    (23.18, "VO: and city of surprises",
     dict(name="Oct18_C187_led_arches", clip=S + "Oct18_A001_10182124_C187.mov", src_in=1.00, rate=C30, scale=push(50, 53),
          fx=dict(interpret=True, whip_in=4, whip_dir=-1),
          shows="giant LED arches shaped like lotus petals, nested one behind another over a packed street (whip in, whoosh)")),
    (25.16, "VO: I am Urja Mukherjee, your guide",
     dict(name="C082_walkway_pov", clip=B + "A001_10251528_C082.mov", src_in=0.0, rotation=90, scale=push(62.5, 65.0),
          fx=dict(stab="smooth", sigma=20, zoom=1.06),
          shows="walking POV into the Howrah Bridge walkway, the truss overhead: follow me; stabilised, horizon level")),
    # EXPLORER: free stock (Pexels 35040390): a young woman in a saree on a Kolkata Metro platform, looking around as a
    # train streaks past; 59.94 fps, interpreted to 25 = real slow motion. Own C023 tram rails and C067 (a family on the
    # promenade) didn't read as "explorer"
    (29.50, "VO: but I call myself an explorer",
     dict(name="stock_metro_explorer", clip=K + "pexels-35040390/14843251_1080_1920_60fps.mp4", src_in=2.20, rate=C60,
          scale=push(100, 104),
          shows="a young woman in a saree on a Kolkata Metro platform looks around as a train streaks past behind her, "
                "real slow motion")),
    (31.56, "VO (Bengali): some say Paris is the city of love",
     dict(name="C089_sunset_lamps", clip=S + "A001_10251601_C089.mov", src_in=6.4, rotation=-90, scale=push(62.5, 65.0),
          shows="iron lamp posts along the river promenade against the sun")),
    (34.86, "VO (Bengali): I say Kolkata is the city of passion (ramp into slow motion)",
     dict(name="Oct21_C047_dhakis", clip=S + "Oct21_A001_10212056_C047.mov", src_in=32.2, scale=54, pos=[570, 900],
          fx=dict(speed_keys=[[0, 1.0], [0.8, 1.0], [1.7, 0.4]], stab="smooth", sigma=12, zoom=1.05),
          shows="a dhaki in white drumming at Pujo; real speed, then ramps into 40 % slow motion on 'passion'; stabilised")),
    (37.27, "VO: … passion (accent: flash cut)",
     dict(name="Oct21_C035_dancers", clip=S + "Oct21_A001_10211954_C035.mov", src_in=0.2, scale=50,
          fx=dict(rate=0.65),
          shows="women in lal-paar saris dancing at a ghat on Dashami, 65 % slow motion (flash on the accent)")),
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
          fx=dict(rate=0.7, **STAB),
          shows="two boatmen on a drifting country boat on the Hooghly; stabilised, horizon level, 70 % slow motion")),
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
     dict(name="stock_rickshaw_tracks", clip=K + "pexels-32665218/13926753_3840_2160_24fps.mp4", src_in=1.00, rate=C2398, scale=62.5,
          shows="a hand-pulled rickshaw runs toward us down the tram tracks, yellow taxis parked along the old street "
                "(replaces the wall writing, where passers-by hid the wall)")),
    (64.18, "chorus: … walk and see",
     dict(name="C018_walk_red", clip=S + "A001_10311614_C018.mov", src_in=0.5, rotation=-90, scale=push(62.5, 65.0),
          fx=dict(rate=0.6),
          shows="an adult and a child in red walking on the Maidan path, 60 % slow motion")),
    (66.27, "chorus: Kolkata, come think it over",
     dict(name="C105_bookseller", clip=S + "A001_10251641_C105.mov", src_in=1.6, rotation=90, scale=push(62.5, 65.0),
          shows="an old College Street bookseller sitting at his stall")),
    (68.31, "chorus: Kolkata, come walk (the old streets)",
     dict(name="stock_tram_street", clip=K + "pexels-2843866/2843866-hd_1920_1080_30fps.mp4", src_in=15.5, rate=C30, scale=125,
          fx=dict(interpret=True, half=False, stab="smooth", sigma=18, zoom=1.08),
          shows="old houses, yellow taxis and a Kolkata tram passing; stabilised")),
    (72.42, "chorus: … the yellow taxi waits",
     dict(name="C101_taxi", clip=B + "A001_10251635_C101.mov", src_in=0.5, scale=push(50, 53),
          shows="a yellow Ambassador taxi parked on the tram lines, a man walking past it (replaces the swooping façade ride)")),
    (74.51, "chorus: Kolkata, think it over",
     dict(name="C028_chai", clip=S + "A001_10311640_C028.mov", src_in=0.5, rotation=-90, scale=push(62.5, 65.0),
          pos=[[0, 540, 910], [1, 540, 937]], fx=dict(rate=0.5),
          shows="a chai pot steaming at a stall, the chai-wallah behind; 50 % slow motion on the steam")),
    (76.60, "chorus: dusk on the bridge",
     dict(name="stock_howrah_bluehour", clip=K + "pexels-38584444/16387667_2160_3840_30fps.mp4", src_in=2.0, rate=C30, scale=50,
          shows="Howrah Bridge at blue hour, the traffic lights coming on")),
    (78.65, "chorus: will you come with me? (the tram ride)",
     dict(name="C030_tram_night", clip=S + "A001_10311647_C030.mov", src_in=2.0, rotation=-90, scale=push(62.5, 65.0),
          shows="inside a Kolkata tram at night, warm lamps and the windows (tram bell)")),
    # FINAL: replaces the shaky diya; own footage, not Pujo (round5b_picks slot 3 #3); bookends "a city of culture"
    (82.76, "outro: the city waits at night (culture, again)",
     dict(name="C033_academy_night", clip=B + "A001_10311733_C033.mov", src_in=3.80, rotation=-90, scale=push(62.5, 65.5), fade_out=20,
          fx=dict(rate=0.75),
          shows="the Academy of Fine Arts lit at night, its doorway glowing, people gathered in front; 75 % slow motion, "
                "slow push; fade to black")),
]

SFX = [  # file, reel start, source in, gain dB, fade out s
    ("projects/kolkata/sfx/pixabay-37522_vinyl_needle_drop_crackle.mp3", 2.40 - 0.28, 0.0, -8.0, 1.0),   # needle drop at 2.40
    ("assets/sfx/gemini_whoosh_soft.wav", 23.18 - OFF - 0.21, 0.0, -11.0, 0.0),                           # whip into surprises
    ("assets/sfx/gemini_riser_sub_hit.wav", 37.27 - OFF - 1.04, 0.0, -14.0, 0.0),                         # flash on the accent
    ("projects/kolkata/sfx/pixabay-339952_kolkata_tram_approach_bell.mp3", 78.65 - OFF - 0.4, 8.4, -20.0, 0.6),  # tram bell
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
        a, b = r(t0 - OFF), r(t1 - OFF)
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
    runtime = r(END_SONG - OFF)
    flash = r(37.27 - OFF)
    audio = [{"file": "projects/kolkata/music/kolkata.wav", "start": 0.0, "in": OFF, "gain_db": 0.0, "fade_in": 0, "fade_out": 1.5}]
    audio += [{"file": f, "start": round(st, 2), "in": i, "gain_db": g, "fade_in": 0, "fade_out": fo} for f, st, i, g, fo in SFX]
    edl = {
        "fps": 25, "runtime": runtime,
        "note": f"KOLKATA v5b 'Your guide to Kolkata' (round 5b). music/kolkata.wav from {OFF} s for {runtime} s. "
                f"Stabilised / slow-motion own shots are offline pre-renders (tools/fx_prerender.py); the build uses Warp "
                f"Stabilizer and AE Timewarp. Line table in project.md Round 5b.",
        "overlays": [  # leaks first, so the window matte covers them (in the build: V4 Screen, under the V6 matte)
                     {"file": "projects/kolkata/renders/overlays/leak_a_alpha.mov", "start": r(31.56 - OFF - 0.48), "end": r(31.56 - OFF + 0.52)},
                     {"file": "projects/kolkata/renders/overlays/leak_b_alpha.mov", "start": r(39.31 - OFF - 0.4), "end": r(39.31 - OFF + 0.8)},
                     {"file": "projects/kolkata/renders/overlays/window_matte.png", "start": 0.0, "end": runtime},
                     {"file": "projects/kolkata/renders/overlays/title_kolkata.png", "start": r(15.00 - OFF), "end": r(17.80 - OFF)},
                     {"file": "projects/kolkata/renders/overlays/flash_white.png", "start": flash, "end": r(flash + 0.12)}],
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
