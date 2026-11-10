#!/usr/bin/env python3
"""Generate a short AI video shot inside the studio's cost structure. Default: OpenRouter → Google Veo 3.1 Lite, no audio.

POLICY (director, 2026-10-18; widened 2026-11-10; studio/director-profile.md, motion-and-ai.md §3)
  - The LAST step of the bad-footage ladder (motion-and-ai.md §3): for a shot the director's footage can't provide, or
    whose footage and free stock are unusable after the free fixes. --why is required and says which.
  - May show the reel's subjects (people, the idol) since 2026-11-10. Still never proof, never words put in someone's
    mouth. Labelled "AI-generated" in brief.md; approved per shot at Checkpoint 1, and each paid run by the director.
  - No raw footage is ever sent: at most a first and a last still (--first-frame / --last-frame).
  - Claude (Fable 5.2 included) writes text and code only: it plans, prompts and checks the shot; the frames come from here.

COST STRUCTURE (studio/ai-budget.json)
  draft  720p · 4 s · no audio · Veo 3.1 Lite  ≈ $0.12   (try the idea cheaply)
  final  1080p · 8 s · no audio · Veo 3.1 Lite ≈ $0.40   (only after a draft is approved)
  omni   Gemini Omni 1.2 Flash (--model omni): 3–15 s, and the frames BETWEEN two stills (give --first-frame and
         --last-frame). It bills sound on every clip (≈ $0.07/s 720p, $0.10/s 1080p, upscaled); the estimate uses that.
  caps   per shot: 3 drafts + 1 final · per reel: $4, 4 final shots, 24 s of generated footage
         per month: $20. Every call is checked against all caps BEFORE it's sent.
  Audio is off by default: reels use the director's music, and audio costs ~60 % more on Lite.
Prices are read live from OpenRouter's public model list on every run, so they never go stale.
Every paid call is logged to studio/ledger/ai-spend.jsonl with the provider's actual charged cost.

PROVIDER
  OpenRouter only (OPENROUTER_API_KEY in .env). POST /api/v1/videos → poll → /content. The Google Gemini API fallback
  was removed in v0.10.0: its Veo "-preview" models were shut down on 2026-10-22.

USAGE (always dry-run first: prints the cost and every cap; spends nothing)
  ./.venv/bin/python scripts/gen_video.py --reel <reel> --shot <name> --why "<why the footage can't>" \
      --prompt "<prompt>" [--mode draft|final] [--first-frame still.png] [--last-frame still.png] \
      [--negative "<avoid>"] [--model lite|fast|standard|omni|<openrouter slug>] [--duration S] [--audio]
  ... then add --yes once the director has approved (the shot, and for a final the chosen draft).
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
BUDGET_FILE = ROOT / "studio" / "ai-budget.json"
LEDGER = ROOT / "studio" / "ledger" / "ai-spend.jsonl"
OR_BASE = "https://openrouter.ai/api/v1"
ALIASES = {"lite": "google/veo-3.1-lite", "fast": "google/veo-3.1-fast", "standard": "google/veo-3.1",
           "omni": "google/gemini-omni-1.2-flash"}
MODES = {"draft": {"res": "720p", "duration": 4}, "final": {"res": "1080p", "duration": 8}}
DEFAULT_BUDGET = {"monthly_limit_usd": 20, "per_reel_usd": 4, "max_final_shots_per_reel": 4,
                  "max_generated_seconds_per_reel": 24, "max_drafts_per_shot": 3, "max_finals_per_shot": 1}


def env_key(name: str) -> str:
    key = os.environ.get(name, "")
    env = ROOT / ".env"
    if not key and env.exists():
        for line in env.read_text().splitlines():
            if line.startswith(name + "="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    return key


def ledger() -> list[dict]:
    if not LEDGER.exists():
        return []
    out = []
    for line in LEDGER.read_text().splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def log(entry: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def openrouter_price(model: str, res: str, audio: bool) -> tuple[float | None, dict, bool]:
    """Per-second price from OpenRouter's public video model list (live). Returns (price, model_info, sound_billed).

    A model with no silent price (Gemini Omni bills sound on every clip) is priced with sound, and sound_billed is True.
    """
    try:
        data = requests.get(f"{OR_BASE}/videos/models", timeout=30).json().get("data", [])
    except (requests.RequestException, ValueError):
        return None, {}, audio
    info = next((m for m in data if m.get("id") == model), None)
    if not info:
        return None, {}, audio
    skus = info.get("pricing_skus") or {}
    suffix = "" if res == "1080p" else "_" + res.lower()
    a = "with_audio" if audio else "without_audio"
    for key in (f"duration_seconds_{a}{suffix}", f"duration_seconds{suffix}"):
        if key in skus:
            return float(skus[key]), info, audio
    if not audio and f"duration_seconds_with_audio{suffix}" in skus:
        return float(skus[f"duration_seconds_with_audio{suffix}"]), info, True
    return None, info, audio


def image_part(path: Path) -> tuple[str, str]:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return mime, base64.b64encode(path.read_bytes()).decode()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reel", required=True)
    ap.add_argument("--shot", required=True, help="shot name; caps are counted per shot")
    ap.add_argument("--why", required=True,
                    help="why the director's footage can't provide this shot, or why its footage and free stock are unusable (policy)")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--mode", choices=list(MODES), default="draft")
    ap.add_argument("--model", default="lite", help="lite | fast | standard | omni | any OpenRouter video model slug")
    ap.add_argument("--res", choices=["720p", "1080p"], help="override the mode's resolution")
    ap.add_argument("--duration", type=int, help="override the mode's duration (s)")
    ap.add_argument("--aspect", default="9:16")
    ap.add_argument("--audio", action="store_true", help="generate audio too (costs more; reels use the director's music)")
    ap.add_argument("--first-frame", type=Path, help="a still from the director's own footage to start from")
    ap.add_argument("--last-frame", type=Path)
    ap.add_argument("--negative", default="")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--yes", action="store_true", help="actually generate and pay (default: dry run)")
    args = ap.parse_args()

    model = ALIASES.get(args.model, args.model)
    res = args.res or MODES[args.mode]["res"]
    duration = args.duration or MODES[args.mode]["duration"]
    audio = bool(args.audio)
    if not (ROOT / "projects" / args.reel).is_dir():
        sys.exit(f"No reel folder projects/{args.reel}")
    budget = {**DEFAULT_BUDGET, **(json.loads(BUDGET_FILE.read_text()) if BUDGET_FILE.exists() else {})}

    price, info, sound_billed = openrouter_price(model, res, audio)
    if info and duration not in (info.get("supported_durations") or [duration]):
        sys.exit(f"{model} supports durations {info['supported_durations']}, not {duration}.")
    if info and res not in (info.get("supported_resolutions") or [res]):
        sys.exit(f"{model} supports {info['supported_resolutions']}, not {res}.")
    kinds = info.get("supported_frame_images") or ["first_frame", "last_frame"]
    for path, kind in ((args.first_frame, "first_frame"), (args.last_frame, "last_frame")):
        if path and kind not in kinds:
            sys.exit(f"{model} doesn't take a {kind.replace('_', ' ')} (it takes: {', '.join(kinds)}).")
        if path and not path.is_file():
            sys.exit(f"No still at {path}")
    est = round(price * duration, 2) if price is not None else None
    # Veo takes a negative prompt as a Vertex parameter; models without it (Gemini Omni) get it written into the prompt.
    neg_param = "negativePrompt" in (info.get("allowed_passthrough_parameters") or ["negativePrompt"])
    prompt = args.prompt if neg_param or not args.negative else f"{args.prompt.rstrip()} Avoid: {args.negative}"

    # Caps, all checked before anything is sent.
    month = dt.date.today().strftime("%Y-%m")
    paid = [e for e in ledger() if e.get("status") == "ok"]
    month_spent = round(sum(float(e.get("cost_usd", 0)) for e in paid if e.get("time", "").startswith(month)), 2)
    reel_paid = [e for e in paid if e.get("reel") == args.reel]
    reel_spent = round(sum(float(e.get("cost_usd", 0)) for e in reel_paid), 2)
    reel_finals = [e for e in reel_paid if e.get("mode") == "final"]
    final_shots = {e.get("shot") for e in reel_finals}
    final_secs = sum(int(e.get("duration_s", 0)) for e in reel_finals)
    shot_drafts = sum(1 for e in reel_paid if e.get("shot") == args.shot and e.get("mode") == "draft")
    shot_finals = sum(1 for e in reel_paid if e.get("shot") == args.shot and e.get("mode") == "final")

    print(f"openrouter: {model} · {args.mode} · {res} · {duration}s · {args.aspect} · audio {'on' if audio else 'off'}"
          + (" (sound is billed anyway: this model has no silent price)" if sound_billed and not audio else "")
          + (" · first frame" if args.first_frame else "") + (" · last frame" if args.last_frame else ""))
    if args.negative and not neg_param:
        print("Negative prompt: this model takes none, so it's added to the prompt as \"Avoid: …\"")
    print(f"Cost ≈ {'$%.2f' % est if est is not None else 'UNKNOWN (no live price)'}")
    print(f"Month ${month_spent:.2f}/${budget['monthly_limit_usd']} · reel ${reel_spent:.2f}/${budget['per_reel_usd']} · "
          f"reel finals {len(final_shots)}/{budget['max_final_shots_per_reel']} shots, {final_secs}/{budget['max_generated_seconds_per_reel']} s · "
          f"this shot: drafts {shot_drafts}/{budget['max_drafts_per_shot']}, finals {shot_finals}/{budget['max_finals_per_shot']}")
    problems = []
    if est is None:
        problems.append("no live price for this model/resolution/audio, so it can't be checked against the budget")
    else:
        if month_spent + est > budget["monthly_limit_usd"] + 1e-9:
            problems.append(f"monthly budget ${budget['monthly_limit_usd']} would be exceeded")
        if reel_spent + est > budget["per_reel_usd"] + 1e-9:
            problems.append(f"per-reel budget ${budget['per_reel_usd']} would be exceeded")
    if args.mode == "draft" and shot_drafts >= budget["max_drafts_per_shot"]:
        problems.append(f"this shot already used {shot_drafts} drafts (max {budget['max_drafts_per_shot']})")
    if args.mode == "final":
        if shot_finals >= budget["max_finals_per_shot"]:
            problems.append(f"this shot already has a final (max {budget['max_finals_per_shot']})")
        if args.shot not in final_shots and len(final_shots) >= budget["max_final_shots_per_reel"]:
            problems.append(f"reel already has {len(final_shots)} generated final shots (max {budget['max_final_shots_per_reel']})")
        if final_secs + duration > budget["max_generated_seconds_per_reel"]:
            problems.append(f"reel would exceed {budget['max_generated_seconds_per_reel']} s of generated footage")
    if problems:
        sys.exit("✗ Refused: " + "; ".join(problems) + ". Ask the director.")
    if not args.yes:
        print("Dry run: nothing sent. Re-run with --yes once the director has approved this shot and its cost.")
        sys.exit(2)

    key = env_key("OPENROUTER_API_KEY")
    if not key:
        sys.exit("✗ OPENROUTER_API_KEY isn't set (environment or .env).")
    entry = {"time": dt.datetime.now().isoformat(timespec="seconds"), "reel": args.reel, "shot": args.shot, "mode": args.mode,
             "provider": "openrouter", "model": model, "res": res, "duration_s": duration, "audio": audio, "sound_billed": sound_billed,
             "first_frame": str(args.first_frame) if args.first_frame else None,
             "last_frame": str(args.last_frame) if args.last_frame else None,
             "why": args.why, "prompt": prompt, "estimate_usd": est, "cost_usd": 0.0, "status": "started"}
    out_dir = ROOT / "projects" / args.reel / "renders" / "gen"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{args.shot}_{args.mode}_{dt.datetime.now():%Y%m%d-%H%M%S}.mp4"

    hdr = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    body: dict = {"model": model, "prompt": prompt, "duration": duration, "resolution": res,
                  "aspect_ratio": args.aspect, "generate_audio": audio}
    frames = []
    for path, kind in ((args.first_frame, "first_frame"), (args.last_frame, "last_frame")):
        if path:
            mime, b64 = image_part(path)
            frames.append({"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}, "frame_type": kind})
    if frames:
        body["frame_images"] = frames
    if args.seed is not None:
        body["seed"] = args.seed
    if args.negative and neg_param:
        body["provider"] = {"options": {"google-vertex": {"parameters": {"negativePrompt": args.negative}}}}
    r = requests.post(f"{OR_BASE}/videos", headers=hdr, json=body, timeout=60)
    if r.status_code not in (200, 201, 202):
        entry.update(status=f"rejected {r.status_code}", error=r.text[:500]); log(entry)
        sys.exit(f"✗ OpenRouter rejected the request ({r.status_code}): {r.text[:500]}")
    job = r.json()
    poll = job.get("polling_url") or f"{OR_BASE}/videos/{job['id']}"
    print(f"… generating (job {job.get('id')}); typically 30 s to a few minutes", flush=True)
    deadline, s = time.time() + 900, {}
    while time.time() < deadline:
        s = requests.get(poll, headers=hdr, timeout=60).json()
        if s.get("status") in ("completed", "failed", "cancelled", "expired"):
            break
        time.sleep(20)
    if s.get("status") != "completed":
        entry.update(status=s.get("status", "timeout"), error=str(s.get("error"))[:500], job=job.get("id")); log(entry)
        sys.exit(f"✗ Generation {s.get('status', 'timed out')}: {s.get('error')}")
    url = (s.get("unsigned_urls") or [f"{OR_BASE}/videos/{job['id']}/content?index=0"])[0]
    with requests.get(url, headers={"Authorization": f"Bearer {key}"}, stream=True, timeout=300) as dl:
        dl.raise_for_status()
        with out.open("wb") as f:
            for chunk in dl.iter_content(1 << 20):
                f.write(chunk)
    cost = float((s.get("usage") or {}).get("cost", est or 0))
    entry.update(job=job.get("id"), generation_id=s.get("generation_id"))

    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration",
                            "-of", "json", str(out)], capture_output=True, text=True).stdout
    entry.update(status="ok", cost_usd=round(cost, 4), output=str(out.relative_to(ROOT)), probe=json.loads(probe or "{}"))
    log(entry)
    out.with_suffix(".json").write_text(json.dumps({**entry, "label": f"AI-generated ({model})" + ("; Google SynthID watermark" if model.startswith("google/") else ""),
                                                    "negative": args.negative}, indent=1))
    print(f"✓ {out.relative_to(ROOT)}  charged ${cost:.2f} (estimate ${est})")


if __name__ == "__main__":
    main()
