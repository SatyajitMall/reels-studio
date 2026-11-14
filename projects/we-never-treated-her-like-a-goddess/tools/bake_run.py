#!/usr/bin/env python3
"""Run tools/shot_look.py render for the named shots of analysis/look/bake_plan.json, one after another.

Usage (from the reels-studio root): .venv/bin/python projects/<reel>/tools/bake_run.py 01_C010 08_C020 ...
Skips a shot whose .mov and .json sidecar already exist."""
import json, subprocess, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
REL = R.relative_to(R.parents[1])          # projects/<reel>
plan = {p["name"]: p for p in json.loads((R / "analysis/look/bake_plan.json").read_text())}
for name in sys.argv[1:]:
    p = plan[name]
    out = R / p["out"]
    if out.exists() and out.with_suffix(".json").exists():
        print(f"skip {name}: already baked"); continue
    cmd = [sys.executable, str(REL / "tools/shot_look.py"), "render", "--look", str(REL / "analysis/look/goddess_halfway_look.json"),
           "--clip", str(REL / p["clip"]), "--in", str(p["in"]), "--frames", str(p["frames"]), "--crop", ",".join(map(str, p["crop"])),
           "--handle", "0.3", "--full", "-o", str(REL / p["out"])]
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=R.parents[1])
