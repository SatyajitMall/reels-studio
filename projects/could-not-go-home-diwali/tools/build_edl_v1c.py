"""Build EDL v1c for could-not-go-home-diwali (reel-local): v1b + the director's note
"There is lot of distortion and in and out focus in this and framing issue fix it".

1 Distortion   → interpolated slow motion only where it stays clean: 01 street 70 %, 10 paan look 70 %, 12 look-up 80 %;
                  everything else real time (02 ghosted pedestrians and 07/08 garbled the jewellery at 80 %). Stabilise only the three shakiest
                  (04, 07, 10), position only (no roll or zoom warping), zoom margin 1.04.
2 Focus        → no rack pulls. Every shot uses the camera's recorded focus (measured steady: range ≤ 0.11 per shot).
                  f/2 as shot, f/2.8 on the hands shots (03, 04, 05, 06, 09, 11) so hands and the spatula don't
                  swim in and out of the blur.
3 Framing      → push +5 % (was +10 %), anchored on the window's top edge on head-at-top shots so heads are never cut;
                  L2 held as one shot (the close cut his head); 11 moved to C063 2.0 s and shifted left so he sits centre-right, clear of the IG band.
Same letter, cuts, overlays, audio, 4:3 window, camera-true colour and plain cuts.

Run from the studio root: .venv/bin/python -I projects/could-not-go-home-diwali/tools/build_edl_v1c.py [--only NAME,…]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

STUDIO = Path(__file__).resolve().parents[3]
REEL = Path(__file__).resolve().parents[1]
R = "projects/could-not-go-home-diwali"
sys.path.insert(0, str(REEL / "tools"))
import build_edl_v1 as v1  # noqa: E402

FPS = 25
WIN_TOP = 505
PUSH = 1.05
# v1c: L2 is one held shot (03 + 04 merged), so the cuts are v1's minus 4.68
CUTS = [c for c in v1.CUTS if abs(c - 4.68) > 1e-6]
LINE_OF = [0, 0, 1, 2, 2, 3, 3, 4, 4, 5, 5]

# name, clip, camera in, rate, stab, fnumber, (scale, x) base framing, anchor ("top" keeps the window's top edge fixed), shows
SHOTS = [
    ("01_C047_auto", "C047", 0.60, 0.7, None, 2.0, (75.0, 540), "top",
     "auto driver from the back seat; the Diwali-lit street drifts past the windscreen, slowed"),
    ("02_C048_auto_turn", "C048", 2.72, 1.0, None, 2.0, (75.0, 540), "top",
     "the driver turns his head toward the lit street (real time: 80 % ghosted the pedestrians)"),
    ("03_C054_parotta", "C054", 0.32, 1.0, "smooth", 2.8, (75.0, 540), "top",
     "parotta maker at the tawa, lifting and turning parotta: one held shot for the whole line (real time); "
     "the v1b close cut his head (he stands at the camera's top edge), so the line holds on the wide"),
    ("05_C052_cook_plating", "C052", 1.00, 1.0, None, 2.8, (75.0, 540), "top",
     "young cook's hands plating food (real time)"),
    ("06_C053_cook_serving", "C053", 1.20, 1.0, None, 2.8, (75.0, 540), "top",
     "he hands the plate across to a customer (real time)"),
    ("07_C062_vendor", "C062", 0.52, 1.0, "smooth", 2.0, (75.0, 540), "centre",
     "jewellery vendor at his stall, looking into his phone (real time: slow motion garbled the hanging jewellery)"),
    ("08_C062_vendor_close", "C062", 4.92, 1.0, None, 2.0, (92.0, 787, 830), "centre",
     "closer: the vendor's face and phone (real time)"),
    ("09_C050_paan", "C050", 0.40, 1.0, None, 2.8, (75.0, 540), "top",
     "paan maker in white wrapping paan (real time)"),
    ("10_C051_paan_look", "C051", 0.20, 0.7, "smooth", 2.0, (75.0, 540), "top",
     "he looks away, still, lost in thought, slowed"),
    ("11_C063_carwash", "C063", 0.90, 1.0, None, 2.8, (75.0, 470), "top",
     "next morning: the young car-washer foaming a scooter, his face in profile (real time)"),
    ("12_C064_carwash_look", "C064", 7.10, 0.8, None, 2.0, (75.0, 540), "top",
     "he looks up from the work toward the camera, slowed"),
]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only"); ap.add_argument("--edl-only", action="store_true")
    a = ap.parse_args()
    bake_dir = REEL / "raw" / "baked" / "v1c"; bake_dir.mkdir(parents=True, exist_ok=True)
    fx_dir = REEL / "renders" / "fx_preview_v1c"; fx_dir.mkdir(parents=True, exist_ok=True)
    jobs, shots, bmap = [], [], {}
    for i, (name, cid, cin, rate, stab, fno, framing, anchor, shows) in enumerate(SHOTS):
        st, en = CUTS[i], CUTS[i + 1]
        dur = round(en - st, 2)
        need = dur * rate
        bstart = max(0.0, round((cin - 0.72) * FPS) / FPS)
        bdur = round((cin - bstart + need + 1.0) * FPS) / FPS
        cam = sorted((REEL / "raw" / "Media").glob(f"*_{cid}.mov"))[0]
        baked = bake_dir / f"{name}.mov"
        bmap[name] = {"camera": str(cam.relative_to(STUDIO)), "baked": str(baked.relative_to(STUDIO)), "start": bstart,
                      "dur": bdur, "fnumber": fno, "cam_in": cin, "rate": rate}
        todo = not a.edl_only and (not a.only or name in a.only.split(","))
        if todo:
            r = subprocess.run([str(REEL / "tools" / "cine_bake"), str(cam), str(baked), "--start", f"{bstart:.2f}",
                                "--dur", f"{bdur:.2f}", "--fnumber", f"{fno}"], capture_output=True, text=True)
            if r.returncode:
                raise SystemExit(f"bake {name}: {r.stderr or r.stdout}")
            job = {"id": name, "clip": str(baked.relative_to(STUDIO)), "src_in": round(cin - bstart, 3), "out_dur": dur,
                   "stab": stab, "sigma": 15, "zoom": 1.04, "transl_only": True, "rate": rate,
                   "out": str((fx_dir / f"{name}.mov").relative_to(STUDIO))}
            jobs.append(job)
        sc0 = framing[0]
        sc1 = round(sc0 * PUSH, 2)
        x = framing[1]
        if len(framing) == 3:                 # explicit y (centre anchor)
            pos = [[0, x, framing[2]], [dur, x, framing[2]]]
        elif anchor == "top":                 # keep the image's top edge on the window's top edge: no head is cut
            pos = [[0, x, round(WIN_TOP + 1080 * sc0 / 200, 1)], [dur, x, round(WIN_TOP + 1080 * sc1 / 200, 1)]]
        elif anchor == "bottom":              # keep the bottom edge on the window's bottom edge (a close on hands)
            pos = [[0, x, round(WIN_TOP + 810 - 1080 * sc0 / 200, 1)], [dur, x, round(WIN_TOP + 810 - 1080 * sc1 / 200, 1)]]
        else:
            pos = [[0, x, 910], [dur, x, 910]]
        spd = "real time" if rate >= 0.999 else f"{int(round(rate * 100))} % speed (AE Timewarp)"
        shots.append({"name": name, "start": st, "end": en, "clip": f"{R}/renders/fx_preview_v1c/{name}.mov", "src_in": 0.0,
                      "rate": 1, "rotation": -90, "scale": [[0, sc0], [dur, sc1]], "pos": pos, "ease": "ease",
                      "line": v1.LINES[LINE_OF[i]][0], "shows": shows,
                      "note": (f"build: camera {cam.name} in {cin:.2f} s, {spd}, "
                               f"{'stabilise position-only (Warp, Position only)' if stab else 'no stabilisation'}, depth f/{fno:g} "
                               f"recorded focus (bake start {bstart:.2f}); push +5 % {'' + anchor + '-anchored'}; "
                               f"preview = half-size pre-render (Scale ×2)")})
    if jobs:
        jf = REEL / "analysis" / "fx_jobs_v1c.json"
        jf.write_text(json.dumps(jobs, indent=1))
        r = subprocess.run([sys.executable, "-I", str(REEL / "tools" / "fx_prerender.py"), "--jobs", str(jf)], cwd=STUDIO)
        if r.returncode:
            raise SystemExit("fx_prerender failed")
    (REEL / "analysis" / "bake_map_v1c.json").write_text(json.dumps(bmap, indent=1))
    shots.append({"name": "13_end_card", "start": CUTS[-1], "end": v1.RUNTIME, "line": "— tumhara beta (title on black)",
                  "shows": "title 'Mera diya bhi jalaana', sign-off, handle"})
    prev = json.loads((REEL / "analysis" / "edl_v1.json").read_text())
    doc = {"fps": FPS, "runtime": v1.RUNTIME,
           "note": "v1c = v1b + director note 'lot of distortion and in and out focus … framing issue': slow motion only on calm "
                   "beats (70–80 %), hands/work shots real time; no rack pulls (recorded focus; f/2, f/2.8 on hands shots); "
                   "stabilise 04/07/10 position only; push +5 % top-anchored; 04 and 11 reframed.",
           "shots": shots, "overlays": prev["overlays"], "audio": prev["audio"]}
    (REEL / "analysis" / "edl_v1c.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False))
    print("wrote analysis/edl_v1c.json")


if __name__ == "__main__":
    main()
