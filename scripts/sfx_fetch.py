#!/usr/bin/env python3
"""Find real, openly licensed sound effects on Openverse, pick the best by listening with earshot, keep them with
their licence, and print the credits.

Openverse (api.openverse.org) searches Freesound and Wikimedia Commons audio with no API key. Without a key it allows
20 requests a minute and 200 a day, and at most 240 results per search; responses are cached for 24 h in
~/.cache/reels-studio/openverse so a repeated search costs nothing. Its `category=sound_effect` filter drops every
Freesound result (2026-11-12), so this script doesn't use it. Files are Freesound's 128 kb/s MP3 previews: fine for
an effect under music, while the lossless original needs a Freesound login (the landing page in the sidecar).

Licences: CC0 and Public Domain Mark by default. CC BY only with --license cc0,by, and then every kept file is marked
credit_required and its credit goes in the Instagram caption. BY-SA, NC, ND and Sampling+ are refused: a reel is an
adaptation (SA would bind the whole reel), may earn money (NC), and trims the sound (ND).

  search  QUERY                       list candidates (no download)
  get     QUERY -o DIR [--rank DESC]  download the top -n into DIR (MP3 + a .json sidecar each); with --rank, earshot
                                      ranks them against a description (Claude can't hear: this is how a pick is made)
  keep    CANDIDATE --name NAME       copy one pick into assets/sfx/openverse/ as NAME.wav (48 kHz) with its sidecar;
          [--from S --to E]           optionally only that span (find it with `earshot find FILE "DESC"`). Never
                                      overwrites: assets are shared between reels.
  credits FILE|DIR ...                the credit lines for the sounds a reel uses (from the sidecars)

Usage (from the studio root):
  ./.venv/bin/python scripts/sfx_fetch.py search "temple bell" --max-s 20
  ./.venv/bin/python scripts/sfx_fetch.py get "temple bell" -o projects/<reel>/sfx/candidates/temple_bell -n 8 \\
      --max-s 20 --rank "a single brass temple bell struck once, close"
  ~/.local/bin/earshot find projects/<reel>/sfx/candidates/temple_bell/<file>.mp3 "a single bell strike" --top 3
  ./.venv/bin/python scripts/sfx_fetch.py keep projects/<reel>/sfx/candidates/temple_bell/<file>.mp3 \\
      --name temple_bell_strike --from 2.10 --to 6.40
  ./.venv/bin/python scripts/sfx_prep.py assets/sfx/openverse/temple_bell_strike.wav -o projects/<reel>/sfx
  ./.venv/bin/python scripts/sfx_fetch.py credits projects/<reel>/sfx
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from earshot_util import run_json  # noqa: E402

API = "https://api.openverse.org/v1/audio/"
UA = "reels-studio-sfx-fetch/1.0"
CACHE = Path.home() / ".cache/reels-studio/openverse"
CACHE_S = 24 * 3600
KEEP_DIR = ROOT / "assets/sfx/openverse"
ALLOWED = {"cc0", "pdm", "by"}
REFUSED = {"by-sa": "share-alike would bind the whole reel", "by-nc": "non-commercial", "by-nc-sa": "non-commercial",
           "by-nd": "no derivatives (a trim is one)", "by-nc-nd": "non-commercial, no derivatives",
           "sampling+": "sampling licence", "nc-sampling+": "non-commercial sampling licence"}
PAGE_MAX = 20     # anonymous page size limit


def slug(s: str, n: int = 40) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:n] or "sound"


def api_get(params: dict) -> dict:
    """One Openverse request, cached for 24 h; waits out a 429 once, then gives up with the limit it hit."""
    q = urllib.parse.urlencode(params)
    CACHE.mkdir(parents=True, exist_ok=True)
    cf = CACHE / (hashlib.sha1(q.encode()).hexdigest()[:20] + ".json")
    if cf.exists() and time.time() - cf.stat().st_mtime < CACHE_S:
        return json.loads(cf.read_text())
    req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": UA, "Accept": "application/json"})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode())
                left = r.headers.get("x-ratelimit-available-anon_sustained")
                if left is not None and int(left) < 20:
                    print(f"note: {left} Openverse requests left today (anonymous limit 200/day)", file=sys.stderr)
                cf.write_text(json.dumps(data))
                return data
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 1:
                wait = int(e.headers.get("Retry-After") or 60)
                if wait > 120:
                    raise SystemExit(f"Openverse rate limit: retry in {wait} s (anonymous: 20/min, 200/day)")
                print(f"Openverse rate limit, waiting {wait} s…", file=sys.stderr)
                time.sleep(wait)
                continue
            raise SystemExit(f"Openverse error {e.code}: {e.read()[:200]!r}")
    raise SystemExit("Openverse: no answer")


def licences(arg: str) -> list[str]:
    out = []
    for lic in (x.strip().lower() for x in arg.split(",") if x.strip()):
        if lic in REFUSED:
            raise SystemExit(f"--license {lic}: refused ({REFUSED[lic]}). Allowed: cc0, pdm, by")
        if lic not in ALLOWED:
            raise SystemExit(f"--license {lic}: unknown. Allowed: cc0, pdm, by")
        out.append(lic)
    return out


def search(query: str, lic: list[str], n: int, min_s: float, max_s: float, source: str | None) -> list[dict]:
    """Up to n results that pass the duration window, best first (Openverse's relevance order)."""
    found, page = [], 1
    while len(found) < n and page <= 3:
        params = {"q": query, "license": ",".join(lic), "page_size": PAGE_MAX, "page": page, "filter_dead": "true",
                  "mature": "false"}
        if source:
            params["source"] = source
        d = api_get(params)
        for r in d.get("results", []):
            dur = (r.get("duration") or 0) / 1000
            if r.get("license") not in lic or not (min_s <= dur <= max_s) or not r.get("url"):
                continue
            found.append(r)
        if page >= (d.get("page_count") or 1):
            break
        page += 1
    return found[:n]


def sidecar(r: dict, query: str) -> dict:
    return {"openverse_id": r["id"], "title": r.get("title"), "creator": r.get("creator"),
            "creator_url": r.get("creator_url"), "license": r.get("license"),
            "license_version": r.get("license_version"), "license_url": r.get("license_url"),
            "credit_required": r.get("license") == "by", "attribution": r.get("attribution"),
            "landing_url": r.get("foreign_landing_url"), "file_url": r.get("url"), "source": r.get("source"),
            "duration_s": round((r.get("duration") or 0) / 1000, 3), "bit_rate": r.get("bit_rate"),
            "query": query, "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def table(rows: list[dict]) -> None:
    print(f"{'#':>2}  {'dur s':>6}  {'licence':7}  {'source':10}  {'creator':18}  title")
    for i, r in enumerate(rows, 1):
        print(f"{i:>2}  {(r.get('duration') or 0) / 1000:6.2f}  {r.get('license', ''):7}  {r.get('source', ''):10}  "
              f"{(r.get('creator') or '')[:18]:18}  {(r.get('title') or '')[:60]}")


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)


def cmd_search(a) -> None:
    rows = search(a.query, licences(a.license), a.n, a.min_s, a.max_s, a.source)
    if not rows:
        sys.exit(f"No {a.license} results for {a.query!r} between {a.min_s} and {a.max_s} s")
    table(rows)


def cmd_get(a) -> None:
    rows = search(a.query, licences(a.license), a.n, a.min_s, a.max_s, a.source)
    if not rows:
        sys.exit(f"No {a.license} results for {a.query!r} between {a.min_s} and {a.max_s} s")
    a.out.mkdir(parents=True, exist_ok=True)
    files = []
    for r in rows:
        ext = (r.get("filetype") or Path(urllib.parse.urlparse(r["url"]).path).suffix.lstrip(".") or "mp3").lower()
        dest = a.out / f"{slug(r.get('title') or a.query)}_{r['id'][:8]}.{ext}"
        if not dest.exists():
            try:
                download(r["url"], dest)
            except Exception as e:  # noqa: BLE001 - one dead file shouldn't stop the batch
                print(f"skip {r['id'][:8]}: download failed ({e})", file=sys.stderr)
                continue
        dest.with_suffix(".json").write_text(json.dumps(sidecar(r, a.query), indent=1))
        files.append(dest)
    print(f"{len(files)} candidate(s) in {a.out}")
    table(rows)
    if a.rank and files:
        args = ["rank", a.rank, *map(str, files)]
        try:
            res = run_json(args, a.out / "rank.json")
        except RuntimeError as e:
            sys.exit(f"earshot rank failed: {e}")
        print(f"\nearshot rank vs {a.rank!r} (best first; a 'strong' verdict is the right kind of sound ~98% of the "
              "time on earshot's held-out test, but listen before the final mix):")
        for i, it in enumerate(res.get("ranked") or res.get("results") or [], 1):
            name = Path(it.get("path") or it.get("file") or "?").name
            print(f"{i:>2}. {name}  {it.get('verdict', '')}  z {it.get('z', '')}  sounds like: {it.get('sounds_most_like', '')}"[:200])
        print(f"→ {a.out / 'rank.json'}")


def cmd_keep(a) -> None:
    src = a.candidate
    meta_f = src.with_suffix(".json")
    if not src.exists() or not meta_f.exists():
        sys.exit(f"{src}: need the file and its .json sidecar (from `get`)")
    meta = json.loads(meta_f.read_text())
    if meta.get("license") not in ALLOWED:
        sys.exit(f"{src.name}: licence {meta.get('license')} isn't allowed")
    dest_dir = a.dest
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{slug(a.name, 60)}.wav"
    if dest.exists() or dest.with_suffix(".json").exists():
        sys.exit(f"{dest} exists: assets are shared between reels, so pick another --name")
    cmd = ["ffmpeg", "-v", "error", "-nostdin"]
    if a.start is not None:
        cmd += ["-ss", f"{a.start:.3f}"]
    cmd += ["-i", str(src)]
    if a.end is not None:
        cmd += ["-t", f"{a.end - (a.start or 0):.3f}"]
    cmd += ["-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", str(dest)]
    subprocess.run(cmd, check=True)
    meta.update({"kept_as": dest.name, "kept_from": src.name, "trim_s": [a.start, a.end],
                 "kept_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    dest.with_suffix(".json").write_text(json.dumps(meta, indent=1))
    print(f"✓ {dest} ({meta['license']}{', credit required' if meta['credit_required'] else ''})")
    print(f"  next: ./.venv/bin/python scripts/sfx_prep.py {dest.relative_to(ROOT) if dest.is_relative_to(ROOT) else dest}"
          " -o projects/<reel>/sfx")


def sidecar_for(f: Path) -> Path | None:
    """The sidecar of a kept file or of its sfx_prep.py copy (same stem, looked up in assets/sfx/openverse)."""
    for cand in (f.with_suffix(".json"), KEEP_DIR / f"{f.stem}.json"):
        if cand.exists() and cand.name != "sfx_prep.json":
            return cand
    return None


def cmd_credits(a) -> None:
    files: list[Path] = []
    for p in a.paths:
        files += sorted(x for x in p.iterdir() if x.suffix.lower() in {".wav", ".mp3", ".flac", ".ogg"}) if p.is_dir() else [p]
    need, thanks, unknown = [], [], []
    for f in files:
        sc = sidecar_for(f)
        if not sc:
            unknown.append(f.name)
            continue
        m = json.loads(sc.read_text())
        line = f"\"{m.get('title')}\" by {m.get('creator')} ({m.get('license', '').upper()} {m.get('license_version') or ''}".rstrip() \
            + f", {m.get('landing_url')})"
        (need if m.get("credit_required") else thanks).append(line)
    if need:
        print("Credit REQUIRED (CC BY): put these in the Instagram caption or the first comment:")
        print("\n".join(f"  {ln}" for ln in dict.fromkeys(need)))
    if thanks:
        print("CC0 / public domain: no credit needed (courtesy line for project.md):")
        print("\n".join(f"  {ln}" for ln in dict.fromkeys(thanks)))
    if unknown:
        print(f"No Openverse sidecar (studio starter pack, earshot bank or the director's own): {', '.join(unknown)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("search", "get"):
        s = sub.add_parser(name)
        s.add_argument("query")
        s.add_argument("--license", default="cc0,pdm", help="cc0, pdm, by (comma-separated); default cc0,pdm")
        s.add_argument("-n", type=int, default=10 if name == "search" else 6)
        s.add_argument("--min-s", type=float, default=0.1)
        s.add_argument("--max-s", type=float, default=30.0)
        s.add_argument("--source", help="e.g. freesound or wikimedia_audio (default: all)")
        if name == "get":
            s.add_argument("-o", "--out", type=Path, required=True)
            s.add_argument("--rank", metavar="DESCRIPTION", help="rank the downloads with earshot against this description")
    k = sub.add_parser("keep")
    k.add_argument("candidate", type=Path)
    k.add_argument("--name", required=True)
    k.add_argument("--from", dest="start", type=float)
    k.add_argument("--to", dest="end", type=float)
    k.add_argument("--dest", type=Path, default=KEEP_DIR)
    c = sub.add_parser("credits")
    c.add_argument("paths", nargs="+", type=Path)
    a = ap.parse_args()
    {"search": cmd_search, "get": cmd_get, "keep": cmd_keep, "credits": cmd_credits}[a.cmd](a)


if __name__ == "__main__":
    main()
