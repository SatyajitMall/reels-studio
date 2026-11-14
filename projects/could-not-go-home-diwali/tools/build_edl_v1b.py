"""Build EDL v1b for could-not-go-home-diwali (reel-local): v1 + the director's note "no slow motions no cinematic effect".

Same letter, cut times, 4:3 window, camera-true colour and plain cuts as v1. Added per shot:
  - Apple Cinematic depth: f/2 as shot; the three rack-focus shots at f/1.4 so the pull reads on a phone
    (tools/cine_bake --rack: focus eased from rect A to rect B, each rect's median disparity per frame);
  - stabilisation (fx_prerender's tracker; the build uses Warp Stabilizer);
  - slow motion 50–80 % / one speed ramp (fx_prerender's minterpolate; the build uses AE Timewarp, Pixel Motion);
  - a visible slow push on every shot (+10 % Scale, eased).
Each shot is baked to raw/baked/v1b/<name>.mov, pre-rendered to renders/fx_preview/<name>.mov (display orientation,
half size → EDL Scale doubles: base 75 = v1's 37.5), and placed with src_in 0, rate 1.

Run from the studio root: .venv/bin/python -I projects/could-not-go-home-diwali/tools/build_edl_v1b.py [--only 02_C048_auto_turn]
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
import build_edl_v1 as v1  # noqa: E402  (cut times, lines, overlays, positions)

FPS = 25
BASE, PUSH = 75.0, 1.10          # Scale on the half-size pre-render (= v1's 37.5); push +10 % over the shot

# name, clip, camera in, rate or speed keys, stab, fnumber, rack (bake-relative t0,t1, rect A, rect B) or None, framing, shows
SHOTS = [
    ("01_C047_auto", "C047", 0.60, 0.6, None, 2.0, None, None,
     "auto driver from the back seat; the Diwali-lit street drifts past the windscreen in slow motion"),
    ("02_C048_auto_turn", "C048", 2.72, 0.65, "smooth", 1.4, ("rack", 1.00, 1.40, (0.64, 0.36, 0.14, 0.14), (0.40, 0.15, 0.14, 0.25)), None,
     "focus pulls from the lit street to the driver as he turns his head"),
    ("03_C054_parotta", "C054", 1.00, [[0, 1.0], [0.70, 1.0], [0.95, 0.4]], "smooth", 2.0, None, None,
     "parotta maker at the tawa; real time, then slow as the parotta lifts"),
    ("04_C054_parotta_close", "C054", 3.92, 0.7, "smooth", 2.0, None, (46.0, 752, 1000),
     "closer: his face and hands at the tawa, slowed"),
    ("05_C052_cook_plating", "C052", 1.20, 0.5, "smooth", 2.0, None, None,
     "young cook's hands plating food, half speed"),
    ("06_C053_cook_serving", "C053", 1.55, 0.6, "smooth", 2.0, None, None,
     "he hands the plate across to a customer, slowed"),
    ("07_C062_vendor", "C062", 0.52, 0.8, "smooth", 1.4, ("rack", 0.90, 1.40, (0.80, 0.02, 0.10, 0.12), (0.27, 0.50, 0.10, 0.12)), None,
     "focus pulls from the festival lights to the vendor looking into his phone"),
    ("08_C062_vendor_close", "C062", 4.92, 0.75, "smooth", 2.0, None, (46.0, 787, 830),
     "closer: the vendor's face and phone"),
    ("09_C050_paan", "C050", 0.40, 0.7, "smooth", 2.0, None, None,
     "paan maker in white wrapping paan, slowed"),
    ("10_C051_paan_look", "C051", 0.20, 0.6, "lock", 2.0, None, None,
     "he looks away, still, lost in thought (locked off, slowed)"),
    ("11_C063_carwash", "C063", 1.20, 0.5, "smooth", 2.0, None, None,
     "next morning: foam on the scooter at half speed"),
    ("12_C064_carwash_look", "C064", 7.20, 0.6, None, 1.4, ("rack", 0.92, 1.32, (0.62, 0.62, 0.20, 0.25), (0, 0, 0, 0)), None,
     "focus pulls from the scooter to his face as he looks up"),
]


def need_src(rate, out_dur):
    if isinstance(rate, list):  # speed keys: integrate the eased ramp numerically
        n = int(round(out_dur * FPS)); t = 0.0
        for i in range(n):
            tt = i / FPS
            ks = sorted(rate)
            r = ks[-1][1]
            for a, b in zip(ks, ks[1:]):
                if tt <= b[0]:
                    u = (tt - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 1
                    u = u * u * (3 - 2 * u); r = a[1] + (b[1] - a[1]) * u; break
            t += r / FPS
        return t
    return out_dur * rate


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only"); ap.add_argument("--edl-only", action="store_true")
    a = ap.parse_args()
    bake_dir = REEL / "raw" / "baked" / "v1b"; bake_dir.mkdir(parents=True, exist_ok=True)
    jobs, shots, bmap = [], [], {}
    for i, (name, cid, cin, rate, stab, fno, rack, framing, shows) in enumerate(SHOTS):
        st, en = v1.CUTS[i], v1.CUTS[i + 1]
        dur = round(en - st, 2)
        need = need_src(rate, dur)
        bstart = max(0.0, round((cin - 0.72) * FPS) / FPS)
        bdur = round((cin - bstart + need + 1.0) * FPS) / FPS
        cam = sorted((REEL / "raw" / "Media").glob(f"*_{cid}.mov"))[0]
        baked = bake_dir / f"{name}.mov"
        bmap[name] = {"camera": str(cam.relative_to(STUDIO)), "baked": str(baked.relative_to(STUDIO)), "start": bstart,
                      "dur": bdur, "fnumber": fno, "rack": rack[1:] if rack else None}
        todo = not a.edl_only and (not a.only or name in a.only.split(","))
        if todo:
            cmd = [str(REEL / "tools" / "cine_bake"), str(cam), str(baked), "--start", f"{bstart:.2f}", "--dur", f"{bdur:.2f}",
                   "--fnumber", f"{fno}"]
            if rack:
                _, t0, t1, ra, rb = rack
                cmd += ["--rack", ",".join(f"{x:g}" for x in (t0, t1, *ra, *rb))]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode:
                raise SystemExit(f"bake {name}: {r.stderr or r.stdout}")
        job = {"id": name, "clip": str(baked.relative_to(STUDIO)), "src_in": round(cin - bstart, 3), "out_dur": dur,
               "stab": stab, "sigma": 15, "zoom": 1.06}
        if isinstance(rate, list):
            job["speed_keys"] = rate
        else:
            job["rate"] = rate
        if todo:
            jobs.append(job)
        fx = f"{R}/renders/fx_preview/{name}.mov"
        if framing:
            sc, px, py = framing
            scale, pos = [[0, sc * 2], [dur, round(sc * 2 * PUSH, 2)]], [px, py]
        else:
            scale, pos = [[0, BASE], [dur, round(BASE * PUSH, 2)]], v1.POS
        rtxt = f"speed ramp {rate}" if isinstance(rate, list) else f"{int(rate * 100)} % speed"
        shots.append({"name": name, "start": st, "end": en, "clip": fx, "src_in": 0.0, "rate": 1, "rotation": -90,
                      "scale": scale, "pos": pos, "ease": "ease", "line": v1.LINES[i // 2][0], "shows": shows,
                      "note": (f"build: camera {cam.name} in {cin:.2f} s, {rtxt} (AE Timewarp), stabilise ({stab}; Warp), "
                               f"depth f/{fno}{' + rack focus' if rack else ''} (bake start {bstart:.2f}); push +10 %; "
                               f"preview = fx pre-render (half size, so Scale ×2)")})
    jf = REEL / "analysis" / "fx_jobs_v1b.json"
    if jobs:
        jf.write_text(json.dumps(jobs, indent=1))
        r = subprocess.run([sys.executable, "-I", str(REEL / "tools" / "fx_prerender.py"), "--jobs", str(jf)], cwd=STUDIO)
        if r.returncode:
            raise SystemExit("fx_prerender failed")
    (REEL / "analysis" / "bake_map_v1b.json").write_text(json.dumps(bmap, indent=1))
    shots.append({"name": "13_end_card", "start": v1.CUTS[-1], "end": v1.RUNTIME, "line": "— tumhara beta (title on black)",
                  "shows": "title 'Mera diya bhi jalaana', sign-off, handle"})
    prev = json.loads((REEL / "analysis" / "edl_v1.json").read_text())
    doc = {"fps": FPS, "runtime": v1.RUNTIME,
           "note": "v1b = v1 + director note 'no slow motions no cinematic effect': slow motion 50–80 % on every shot and one speed ramp "
                   "(parotta lift), rack focus from the Cinematic depth on 02 / 07 / 12 (f/1.4), stabilisation, a +10 % push on every "
                   "shot. Same letter, cuts, 4:3 window, camera-true colour, plain cuts. Preview shots are fx pre-renders.",
           "shots": shots, "overlays": prev["overlays"], "audio": prev["audio"]}
    (REEL / "analysis" / "edl_v1b.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False))
    print("wrote analysis/edl_v1b.json")


if __name__ == "__main__":
    main()
