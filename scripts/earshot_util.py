"""Find and run earshot (github.com/Leonxlnx/earshot, MIT): the studio's ears for sound effects.

Installed by setup.sh as a uv tool, pinned to a reviewed commit, CLI only (no `llm` extra, so nothing is uploaded).
Its two models (~1.1 GB, CLAP + AST) live in ~/.cache/earshot. `measure`, `sfx` and `kit` need no models.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

PIN = "4ac3d2ac2b151e1c23376f9ce7f3047a17050013"   # v0.4.1, reviewed by HQ 2026-11-12 (studio v0.11.0)


def earshot_bin() -> str | None:
    """$EARSHOT_BIN, then earshot on PATH, then uv's default tool folder (~/.local/bin is often not on PATH)."""
    for cand in (os.environ.get("EARSHOT_BIN"), shutil.which("earshot"), str(Path.home() / ".local/bin/earshot")):
        if cand and Path(cand).exists():
            return cand
    return None


def need_earshot() -> str:
    exe = earshot_bin()
    if not exe:
        raise SystemExit("earshot isn't installed. Run ./setup.sh (it installs earshot pinned to the reviewed commit), "
                         "or set EARSHOT_BIN.")
    return exe


def run_json(args: list[str], out: Path, timeout: int = 900) -> dict:
    """Run `earshot <args> --json --out <out>` and return the JSON. Raises RuntimeError with earshot's error line."""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.unlink(missing_ok=True)
    env = {**os.environ, "EARSHOT_THREADS": os.environ.get("EARSHOT_THREADS", "3")}
    p = subprocess.run([need_earshot(), *args, "--out", str(out)], capture_output=True, text=True, timeout=timeout, env=env)
    if p.returncode != 0 or not out.exists():
        err = [ln for ln in (p.stderr or p.stdout).splitlines() if ln.strip()]
        raise RuntimeError(err[-1] if err else f"earshot {args[0]} failed (exit {p.returncode})")
    return json.loads(out.read_text())
