#!/usr/bin/env python3
"""Generate a short AI video shot with Google Veo 3.1 (Gemini API), inside the studio's budget and policy.

Policy (director, 2026-10-18; studio/director-profile.md):
  - Generated footage ONLY for shots the director's own footage can't provide. Every run must say
    why (--why), and the shot is labelled "AI-generated" in the reel's brief.
  - The director approves generated shots per reel at Checkpoint 1, with their cost.
Budget: studio/ai-budget.json (monthly limit, default $10). Every paid call is logged to
studio/ledger/ai-spend.jsonl, and a call that would exceed the month's remaining budget is refused.

Prices (official, ai.google.dev/gemini-api/docs/pricing, checked 2026-10-18; per second, paid tier):
  lite      veo-3.1-lite-generate-preview   720p $0.05   1080p $0.08
  fast      veo-3.1-fast-generate-preview   720p $0.10   1080p $0.12   (default)
  standard  veo-3.1-generate-preview        720p $0.40   1080p $0.40
1080p requires 8 s. Videos carry Google's SynthID AI watermark and are deleted from Google's
servers after 2 days, so this script downloads immediately.

Usage (dry run first: prints the cost and the remaining budget, spends nothing):
  ./.venv/bin/python scripts/gen_video.py --reel <reel> --name <shot> --why "<why footage can't>" \
      --prompt "<prompt>" [--model fast|lite|standard] [--res 720p|1080p] [--duration 4|6|8] \
      [--negative "<avoid>"] [--image first_frame.png]
  ... then add --yes to actually generate (and pay).
Needs GEMINI_API_KEY in the environment or in .env (Google AI Studio key with billing on).
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://generativelanguage.googleapis.com/v1beta"
MODELS = {"lite": "veo-3.1-lite-generate-preview", "fast": "veo-3.1-fast-generate-preview",
          "standard": "veo-3.1-generate-preview"}
PRICE = {("lite", "720p"): 0.05, ("lite", "1080p"): 0.08, ("fast", "720p"): 0.10, ("fast", "1080p"): 0.12,
         ("standard", "720p"): 0.40, ("standard", "1080p"): 0.40}
BUDGET_FILE = ROOT / "studio" / "ai-budget.json"
LEDGER = ROOT / "studio" / "ledger" / "ai-spend.jsonl"


def api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "")
    env = ROOT / ".env"
    if not key and env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    return key


def month_spend() -> float:
    if not LEDGER.exists():
        return 0.0
    month = dt.date.today().strftime("%Y-%m")
    total = 0.0
    for line in LEDGER.read_text().splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("time", "").startswith(month):
            total += float(e.get("cost_usd", 0))
    return round(total, 2)


def log(entry: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reel", required=True, help="reel name (folder under projects/)")
    ap.add_argument("--name", required=True, help="shot name, used for the file name")
    ap.add_argument("--why", required=True, help="why the director's footage can't provide this shot (policy)")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--negative", default="", help="what to avoid (negative prompt)")
    ap.add_argument("--model", choices=list(MODELS), default="fast")
    ap.add_argument("--res", choices=["720p", "1080p"], default="1080p")
    ap.add_argument("--duration", type=int, choices=[4, 6, 8], default=8)
    ap.add_argument("--aspect", choices=["9:16", "16:9"], default="9:16")
    ap.add_argument("--image", type=Path, help="optional first-frame image (image-to-video)")
    ap.add_argument("--yes", action="store_true", help="actually generate and pay (default: dry run)")
    args = ap.parse_args()

    if args.res == "1080p" and args.duration != 8:
        sys.exit("1080p requires --duration 8 (Google's rule).")
    reel_dir = ROOT / "projects" / args.reel
    if not reel_dir.is_dir():
        sys.exit(f"No reel folder {reel_dir}")
    budget = json.loads(BUDGET_FILE.read_text()) if BUDGET_FILE.exists() else {"monthly_limit_usd": 10}
    limit = float(budget["monthly_limit_usd"])
    cost = round(PRICE[(args.model, args.res)] * args.duration, 2)
    spent = month_spend()
    print(f"Model {MODELS[args.model]} · {args.res} · {args.duration}s · {args.aspect}")
    print(f"Cost ≈ ${cost:.2f}  ·  spent this month ${spent:.2f} of ${limit:.2f}  ·  remaining ${limit - spent:.2f}")
    if spent + cost > limit + 1e-9:
        sys.exit(f"✗ Refused: this would exceed the monthly AI budget (${limit:.2f}). Ask the director.")
    if not args.yes:
        print("Dry run: nothing generated. Re-run with --yes once the director has approved this shot and cost.")
        sys.exit(2)
    key = api_key()
    if not key:
        sys.exit("✗ GEMINI_API_KEY isn't set (environment or .env).")

    instance: dict = {"prompt": args.prompt}
    if args.image:
        mime = "image/png" if args.image.suffix.lower() == ".png" else "image/jpeg"
        instance["image"] = {"bytesBase64Encoded": base64.b64encode(args.image.read_bytes()).decode(), "mimeType": mime}
    params = {"aspectRatio": args.aspect, "resolution": args.res, "durationSeconds": str(args.duration)}
    if args.negative:
        params["negativePrompt"] = args.negative
    headers = {"x-goog-api-key": key, "Content-Type": "application/json"}
    entry = {"time": dt.datetime.now().isoformat(timespec="seconds"), "reel": args.reel, "shot": args.name,
             "model": MODELS[args.model], "res": args.res, "duration_s": args.duration, "why": args.why,
             "prompt": args.prompt, "cost_usd": 0.0, "status": "started"}

    r = requests.post(f"{BASE}/models/{MODELS[args.model]}:predictLongRunning", headers=headers,
                      json={"instances": [instance], "parameters": params}, timeout=60)
    if r.status_code != 200:
        entry.update(status=f"rejected {r.status_code}", error=r.text[:500])
        log(entry)
        sys.exit(f"✗ Google rejected the request ({r.status_code}): {r.text[:500]}")
    op = r.json()["name"]
    print(f"… generating ({op}); Google says 11 s to 6 min", flush=True)
    deadline = time.time() + 600
    while True:
        s = requests.get(f"{BASE}/{op}", headers=headers, timeout=60).json()
        if s.get("done"):
            break
        if time.time() > deadline:
            entry.update(status="timeout", operation=op)
            log(entry)
            sys.exit(f"✗ Timed out after 10 min. Operation {op} may still finish; Google keeps it for 2 days.")
        time.sleep(10)
    if "error" in s:
        entry.update(status="failed", error=json.dumps(s["error"])[:500])
        log(entry)
        sys.exit(f"✗ Generation failed (not charged): {s['error']}")
    try:
        uri = s["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
    except (KeyError, IndexError):
        entry.update(status="no video", error=json.dumps(s)[:500])
        log(entry)
        sys.exit(f"✗ No video in the response (often a safety filter): {json.dumps(s)[:400]}")

    out_dir = reel_dir / "renders" / "gen"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = out_dir / f"{args.name}_{stamp}.mp4"
    with requests.get(uri, headers={"x-goog-api-key": key}, stream=True, timeout=300) as dl:
        dl.raise_for_status()
        with out.open("wb") as f:
            for chunk in dl.iter_content(1 << 20):
                f.write(chunk)
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height,r_frame_rate:format=duration",
                            "-of", "json", str(out)], capture_output=True, text=True).stdout
    entry.update(status="ok", cost_usd=cost, output=str(out.relative_to(ROOT)), probe=json.loads(probe or "{}"))
    log(entry)
    (out.with_suffix(".json")).write_text(json.dumps({**entry, "label": "AI-generated (Veo 3.1, SynthID watermark)",
                                                      "negative": args.negative, "parameters": params}, indent=1))
    print(f"✓ {out.relative_to(ROOT)}  (${cost:.2f}; month total ${month_spend():.2f} of ${limit:.2f})")


if __name__ == "__main__":
    main()
