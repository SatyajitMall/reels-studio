# CR-20261016-my-reel-montage-craft

| Field | Value |
|---|---|
| From reel | `projects/my-reel/` |
| Arch version | 0.3.0 |
| Type | skill · rule · script |
| Severity | workaround (cost 2 extra rounds) |
| Status | done v0.3.2 |

## What happened
v1 followed the studio rules (cuts on the beat grid, signature effects, kinetic type, 40 % grain) and was approved, then the director reopened it: too mechanical (one shot per bar), "jumps/shakes" (impact shakes + snap zoom on handheld), meaningless beat words, no opening, no slow-mo or speed play, too much grain. Round 3 asked for a frame-by-frame shake fix for unstable hands.

## Workaround used in the reel
- `analysis/motion.json`: per-clip pan/hold detection (phase correlation at 10 fps). Static holds ≥ 2 s were used for digital push/pull.
- Tempo arc from the v0.3.0 energy table: intro → rise → full → mid → outro, with the music edited (intro + main section joined on a downbeat).
- `analysis/shake_*.json`: per-frame translation of the export; shake = the >~3 Hz part of the trajectory; Warp Stabilizer on shots above ~0.3 px/frame RMS; re-measured after.
- Title + end card only; grain 12 %; Optical Flow slow-mo on calm shots.

## Proposed change
1. Skill Phase 2 (music-montage): the brief must include an **energy arc** (which song sections are up/down, where the shot length changes) and a **motion style** (handheld vs holds vs digital moves). Default arc: slow open → build → full → breath → payoff → outro.
2. Skill Phase 1: add `scripts/motion_holds.py` (pan/hold detection per clip) and `scripts/shake_report.py` (per-shot shake of a clip or export), from the scripts in this reel's analysis notes.
3. Playbook §B: no impact shake / snap zoom on handheld footage; prefer push/pull on holds. §C: Optical Flow slow-mo on calm shots is allowed at 25 fps if checked in motion. §A4: grain default 10–15 %.
4. Playbook §E / Round 2 questions: kinetic words only when the director supplies meaningful words; default to title + end card.
5. Skill Phase 4/5: Warp Stabilizer handheld moving shots by default (via a nest for speed/interpreted clips), then scan the export for Warp banners.
6. Skill Phase 4 colour QA: measure every frame of the export (crush % < 0.02, clip % > 0.98, saturation, R−B, G−M, mean midtone hue) and fix to targets before review: montage luma within ±0.03, crush < ~25 % except true-black skies, hue for 'gold' 30–45°, blue shots G−M ≈ 0. Warn in playbook §A3: Kodak 2393-style looks push red; correct with look-layer temperature + green tint, not by cooling clips (which turns orange pink). Add `scripts/colour_report.py`.
7. Skill Phase 1 selects: score every 1 s window of every clip (sharpness, colourfulness, highlight contrast, high-frequency shake, pan speed, exposure/crush), shortlist the top moments per clip and review them by eye before writing the EDL (`scripts/selects_score.py`). In the pilot this found better shots than mid-frame picking in Round 6.
8. Checkpoint 2: ask the director to watch full-screen with sound, and ask one "what would make it more cinematic?" question before accepting approval.

## HQ decision
**Accepted, done in v0.3.2.** All 8 items are in.
- Items 1, 4 and 8: skill Phase 2 energy arc + motion style; title + end card by default; full-screen review plus the "more cinematic?" question.
- Item 3: playbook §B/§C/§A4.
- Item 5: Warp-by-default with the nest recipe and banner scan.
- Item 6: `scripts/colour_report.py` plus the red-push warning in §A3.
- Items 2 and 7: `scripts/selects_score.py`, `scripts/motion_holds.py`, `scripts/shake_report.py`.

The scripts are generalised from your scratchpad versions: no hardcoded skips, fps read from the file. Tested on my-reel v6: the shake and colour numbers match your reports exactly.

Two deliberate differences:
- No fixed "shaky" threshold. The 0.3 px rule didn't fit this measure, because all 21 shots exceeded it. The report ranks shots and is meant for before/after comparison.
- Colour flags are prompts, not failures: approved v6 had 16/21 flagged, mostly by intent.
