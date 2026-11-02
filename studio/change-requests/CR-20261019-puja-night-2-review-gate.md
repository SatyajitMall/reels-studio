# CR-20261019-puja-night-2-review-gate

| Field | Value |
|---|---|
| From reel | `projects/puja-night-2/` |
| Arch version | 0.5.3 (gate from 0.5.0) |
| Type | skill (review-gate.md) · script |
| Severity | workaround (≈ 5 h of wall clock over 11 blind-review runs) |
| Status | partly done (v0.8.0) |

## What happened
puja-night-2 ran the review gate 11 times across 6 rounds (`analysis/review_v1.md` … `review_v6c.md`). Every run returned FAIL. Rounds 1 and 3–6 each ended at the 2-loop limit, so the director always saw a version whose last fixes only the editor had checked. Each run took ≈ 25–42 min; the director noticed one ("Review gate 2 has been running for quite a while").

The reviewer's findings were real every time. But most majors fell into a few classes that a script could have caught before the reviewer looked:

| Class | Examples | Times flagged |
|---|---|---|
| Orientation | C087 (round 3), C085 / C086 (round 5, blockers) | 3 |
| Phones / faces / signage in frame | C088, C090, C124, C116, C091, C132, C085 awning | 7+ |
| Soft focus (soft for most of the shot) | C081, C089, C139, C137, C132 nest upscale | 5 |
| Motion cadence / stutter | C087 (source zoom steps unevenly), C096 Warp judder, C089 hold jump | 3 |
| Tone outlier vs neighbours | C086, C085, C133 / C135 | 3 |

So the blind loops were spent finding defects, and the second loop was usually spent on defects the first loop's fixes introduced (new clips at the wrong scale, a nest upscale, a stutter in a replacement).

## Workaround used in the reel
- Measured before the gate where I could: `tools/shot_pool.py` (absolute focus floor), velocity jitter + frame-difference cadence per shot, `colour_report.py` per shot, a blue-band scan for Warp banners.
- After loop 2, fixed every finding and verified it by numbers and frames, and told the director plainly that no third blind review ran.

## Proposed change
1. **A pre-gate script** (`scripts/pregate.py <export> --shots shots.json`) that runs before the reviewer and blocks the gate on hard fails:
   - absolute sharpness floor per shot (calibrated per shoot from `shot_pool`), with a streak-smear guard;
   - cadence index per moving shot (std / mean of frame differences) and velocity jitter, outliers flagged against the reel's other moving shots;
   - tone vs **neighbouring** shots (luma, warmth R−B, saturation), not only vs the montage median;
   - Warp banner band scan;
   - a per-shot first / middle / last frame sheet for an **orientation + phones / faces** check by the editor, signed off in `project.md` before the reviewer runs.
2. **A third, narrow loop**: after loop 2, the reviewer re-checks only the shots changed by the loop-2 fixes (shot list from the fix script), with a fixed small budget. A loop-2 fix that introduces a new defect then gets caught before the director sees it.
3. **Gate scope in `review-gate.md`**: tell the reviewer that the pre-gate checks passed, so it spends its time on taste and brief fit (pacing, drama vs the music, story, transitions).
4. **Placement-change rule:** any clip swapped in during a fix gets the same pre-gate checks before the next loop (scale, orientation, focus, cadence).

## HQ decision (v0.8.0, 2026-11-01)
**Accepted in part, with the director's go-ahead on Batch A of the v0.8 plan.**
- **1, pre-gate: done as `scripts/pregate.py`.** It runs `verify_render`, `frame_scan`, `camera_fidelity` (tone against each shot's own camera, which covers the tone-outlier class) and `render_diff`, then `watch`, and blocks the gate on any FAIL. Not in it yet: the absolute sharpness floor, the cadence index, the banner scan and the orientation / phones sheet (planned in Batch C as a full-resolution pre-screen of the candidate windows).
- **2, narrow third loop: done.** After loop 2, one focused check of the shots the last fixes changed (`review-gate.md` step 6).
- **3, gate scope: done.** The reviewer is told the pregate passed, and gets the camera sheet.
- **4, placement changes: covered.** Every export runs the pregate again.
