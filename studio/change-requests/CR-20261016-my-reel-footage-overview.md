# CR-20261016-my-reel-footage-overview

| Field | Value |
|---|---|
| From reel | `projects/my-reel/` |
| Arch version | 0.2.5 |
| Type | script |
| Severity | workaround |
| Status | done v0.3.0 |

## What happened
`scripts/analyze_footage.py` on 77 B-roll clips writes 77 separate `contact.png` files (12 frames each) plus `summary.md`. For a music-montage the job is picking ~20 hero moments out of 77 clips; there is no single overview to look at. Also:
- the "Read" column judges exposure against a talking-head norm (0.40–0.50), so 70/77 night clips read "underexposed" and the flag stops meaning anything;
- clips recorded upside down (C008, C018, C022, C023, C032; all clips share the same −90° rotation tag) are not flagged — found only by eye;
- this machine's ffmpeg has no `drawtext` filter, so labelled thumbnails can't be made with ffmpeg alone.

## Workaround used in the reel
Extracted a mid-frame per clip with ffmpeg, labelled and tiled them with PIL (`.venv` python) into 4 sheets of 20, plus a 2-column mosaic of the candidate clips' contact sheets. Took ~4 min of ad-hoc scripting.

## Proposed change
In `scripts/analyze_footage.py`:
1. Write `analysis/overview_<n>.jpg`: labelled mid-frame thumbnails, 20 per sheet (PIL, not ffmpeg drawtext).
2. `--night` / per-reel-type norm: for music-montage or night shoots, report exposure relative to the shoot's median instead of the talking-head band.
3. Optional upside-down heuristic (e.g. compare brightness of top vs bottom third against the shoot's majority, or face/horizon detection) → "maybe inverted" in Read.
Skill Phase 1: "Look at `overview_*.jpg` first, then contact sheets of candidates."

## HQ decision
**Partly accepted, done in v0.3.0.** (1) The overview sheets are in. (2) `--norm auto` judges dark shoots relative to their median. (3) Auto upside-down detection is **rejected**: the brightness and detail heuristics didn't separate your 5 known clips, and the metadata is identical. Use the overview sheets instead; they show 3 more likely upside-down clips: C014, C015, C020. The skill Phase 1 step is updated.
