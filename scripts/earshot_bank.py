#!/usr/bin/env python3
"""Render the studio's earshot sound set into assets/sfx/earshot/ (setup.sh runs it; assets/ isn't in git).

Nine sound effects from earshot's code-made bank (github.com/Leonxlnx/earshot, MIT, pinned in earshot_util.PIN),
one per role in effects-playbook §F, at 48 kHz with fixed seeds, so every Mac renders the same files. No recorded
audio inside, so no licence terms or credit. Each render runs earshot's own audit (clicks, cut tails, clipping, a
rising "synth whip"); this stops on any that isn't clean. Writes bank.json next to them (role, timing, audit).

Usage:  ./.venv/bin/python scripts/earshot_bank.py [--force]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from earshot_util import PIN, need_earshot  # noqa: E402

OUT = ROOT / "assets/sfx/earshot"
# file stem: (bank id, seed, knobs, use)
SET = {
    "earshot_riser_dark": ("riser/dark", 4401, ["--dur", "1.2"], "hook / title riser; put earshot_cut_hit_sub on its peak"),
    "earshot_cut_hit_sub": ("cut_hit/sub", 4101, [], "the hook's hit, a reveal on a cut"),
    "earshot_whoosh_whip": ("whoosh_fast/whip", 4503, ["--dur", "0.8", "--apex", "0.30"],
                            "whip / fast pan: its peak (0.30 s in) lands about a frame after the cut"),
    "earshot_whoosh_swell": ("whoosh_big/swell", 696394185, ["--dur", "1.3", "--apex", "0.60"],
                             "soft long whoosh into a slow move or a dissolve"),
    "earshot_swish_flick": ("swish/flick", 4502, [], "punch-in / snap zoom"),
    "earshot_shutter_dslr": ("shutter/dslr", 1, [], "flash cut, photo-print insert"),
    "earshot_pop_soft": ("ui_pop/soft", 1, [], "text pop, where the playbook allows a sound on type"),
    "earshot_sub_drop": ("sub_drop/pro", 1469265226, [], "reveal / big turn"),
    "earshot_reverse_swell": ("reverse_swell/cymbal", 4301, [], "section change: swells into the cut, peaks just after it"),
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="re-render files that already exist")
    a = ap.parse_args()
    exe = need_earshot()
    OUT.mkdir(parents=True, exist_ok=True)
    sounds = []
    with tempfile.TemporaryDirectory() as tmp:
        for stem, (sid, seed, knobs, use) in SET.items():
            wav, meta_f = OUT / f"{stem}.wav", Path(tmp) / f"{stem}.json"
            target = wav if (a.force or not wav.exists()) else Path(tmp) / f"{stem}.wav"   # existing: re-measure only
            p = subprocess.run([exe, "sfx", "render", sid, "-o", str(target), "--sr", "48000", "--seed", str(seed), *knobs,
                                "--out", str(meta_f)], capture_output=True, text=True)
            if p.returncode != 0 or not meta_f.exists():
                sys.exit(f"{stem}: earshot sfx render failed: {(p.stderr or p.stdout).strip()[-200:]}")
            m = json.loads(meta_f.read_text())["meta"]
            if not m["checks"]["ok"]:
                sys.exit(f"{stem}: earshot's audit failed: {m['checks']['summary']}")
            sounds.append({"file": wav.name, "bank_id": sid, "seed": seed, "knobs": " ".join(knobs), "use": use,
                           "dur_s": m["dur_s"], "onset_s": m["onset_s"], "peak_s": round(m["peak_s"], 3),
                           "end_s": m["end_s"], "audit": m["checks"]["summary"]})
            print(f"{'rendered' if target == wav else 'kept    '}  {wav.name:28s} {sid:22s} peak {m['peak_s']:.3f} s · "
                  f"{m['checks']['summary'].split(': ')[-1]}")
    (OUT / "bank.json").write_text(json.dumps({
        "what": "Sound effects rendered from earshot's code-made bank (MIT). No recorded audio inside, so no licence "
                "terms or credit. Re-render with scripts/earshot_bank.py --force.",
        "earshot_commit": PIN, "sample_rate": 48000, "sounds": sounds}, indent=1) + "\n")
    print(f"✓ {len(sounds)} sounds in {OUT.relative_to(ROOT)} (bank.json)")


if __name__ == "__main__":
    main()
