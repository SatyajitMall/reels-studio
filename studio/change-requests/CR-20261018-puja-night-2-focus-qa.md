# CR-20261018-puja-night-2-focus-qa

| Field | Value |
|---|---|
| From reel | `projects/puja-night-2/` |
| Arch version | 0.5.0 |
| Type | script · skill |
| Severity | workaround (2 review-gate loops, ≈ 1 h, spent on soft footage that could have been screened in Phase 1) |
| Status | open |

## What happened
The director's night footage (phone + Blackmagic Cam app) hunts focus a lot. Several clips are **out of focus for most of their length** and snap sharp for a second or two: C081 (sharp only 4.40–5.64 of 5.64 s), C089 (soft before 2.80), C139 (soft until 9.52 of 12.48), C137, C078–C082 (soft throughout).
- `selects_score.py` scores sharpness per 1 s window **relative to the clip/shoot**, so it still listed moments from these clips.
- `frame_scan.py` flags a blur **dip relative to the shot median**: when most of a shot is soft, the median is soft and nothing is flagged (the reviewer noted this explicitly on v1b).
- My own first check ran at **half resolution** (540×960) and called C139 sharp from 7.68; at full resolution it was soft until 9.52 (Laplacian variance ≈ 40 vs 195–320). The reviewer caught it in loop 2.
- Each fix needed a rebuild (remove + re-place + re-apply Lumetri, scale/rotation, keys, Warp, transitions, A1 levels), about 15 min per loop, because there is no verified trim-in-place recipe.

## Workaround used in the reel
- Full-resolution, absolute per-frame Laplacian variance on every candidate source range (`ffmpeg … scale=1080:1920,format=gray` → numpy), printed every frame around suspected snaps to find the exact snap frame; same pass on the export per shot ("frames below 50 % of the shot median, outside transitions").
- Picked in-points at the focus snap; re-timed or replaced shots (C130, C092, C107 in; C105, C093 out; C089 slowed 6 % with optical flow to reach a bar).

## Proposed change
1. **New Phase 1 check, `scripts/focus_map.py`** (or a mode of `selects_score.py`): per clip, full-res absolute sharpness per frame, detect focus snaps (≥ 3× jump within 2 frames) and output **"sharp windows"** (start, end, length) to `analysis/focus.md`. Selects and the EDL may only use sharp windows; the brief's clip table lists each shot's sharp window.
2. **`frame_scan.py`**: add an absolute floor per shot (e.g. flag frames below 35 % of the reel's 75th-percentile sharpness, with a lower floor for intentionally dark shots), not only dips relative to the shot median.
3. **Reality doc: trim-in-place recipe** for trackItem start/end/inPoint/outPoint (with and without speed changes), so gate fixes don't need full rebuilds; verify on 26.5.2.
4. Skill Phase 7b: when the editor fixes after the last gate loop, re-run the same per-frame check on the new export and record the numbers (done here: `analysis/review_v1c/`).

## Follow-up (round 5): full-shoot shot pool
- **What happened:** round 5 (a dramatic cut) needed ~30 short moments instead of 17 long shots. `selects_score.py` keeps only the top 3 one-second windows per clip and ranks them by relative sharpness.
- **Workaround:** reel-local `projects/puja-night-2/tools/shot_pool.py`, ~4 min with 4 workers.
  - Per-frame Laplacian sharpness at 1080 × 1920 (centre 80 %), motion (frame difference at 270 × 480) and luma for all 62 clips, saved as `analysis/shot_pool.json`.
  - Calibrated against known focus points (C081 snaps into focus at 4.40, C139 at 9.52): an absolute floor of 120 separates sharp from soft on this shoot.
  - Sharp runs of ≥ 0.6 s found 17 unused clips with usable material.
  - A per-shot check sheet (first / middle / last frame, rotated where needed) caught orientation and phones before placement.
- **Proposed change:** a studio `scripts/shot_pool.py` (or a `--all-windows` mode in `selects_score.py`) with an absolute sharpness floor calibrated per shoot and a run list per clip. Add skill Phase 2 guidance: for fast cutting, plan from the pool, not from the top-3 selects.
- Round 5 addendum: C097 measured a high Laplacian (245–320) during a fast pan whose frames are heavy horizontal smear; streak texture fools the metric. `shot_pool.py` / `frame_scan.py` need a motion-blur check (directional gradient anisotropy, or sharpness vs frame difference) next to the Laplacian.
- Round 6 addendum (gate loop 2): **a camera zoom can stutter while the translation jitter reads clean.** C087's forward move stepped unevenly in the source (CFR 25 fps; frame-difference cadence 0.16 vs ≤ 0.03 on smooth shots). My per-shot QA measured phase-correlation translation only, which a zoom barely moves. Proposed: report a **cadence index** per shot (std / mean of frame differences, ignoring the first and last 2 frames) in `frame_scan.py` or `shake_report.py`, flag outliers against the reel's other moving shots (threshold to calibrate: smooth shots here measured 0.02–0.12 on 270 × 480 grey), and run it on the source range of every candidate before placement.
