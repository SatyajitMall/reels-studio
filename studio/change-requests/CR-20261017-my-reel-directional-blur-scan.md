# CR-20261017-my-reel-directional-blur-scan

| Field | Value |
|---|---|
| From reel | `projects/my-reel/` |
| Arch version | 0.5.0 |
| Type | script |
| Severity | workaround |
| Status | open |

## What happened
In v10 the outro shot C011 went back to its original clip, a camera pan. At 49.0–49.4 it showed a heavy horizontal motion smear: double edges, the face unreadable. `scripts/frame_scan.py` and my source profile, both based on Laplacian sharpness, rated those frames normal or even sharp (1.12 of median).

A one-directional blur kills the edges across the motion, but keeps the edges along it, so the Laplacian energy stays high. The v9 blind reviewer had flagged C011 as smeared, but the scan only caught a 0.12 s piece of it.

## Workaround used in the reel
A directional check: per frame, the ratio of horizontal-gradient energy to vertical-gradient energy, `mean(diff(g, axis=1)²) / mean(diff(g, axis=0)²)`, relative to the shot median. Flag it when it goes below 0.6 or above 1/0.6 for ≥ 2 frames. This found C011's smear at source 4.0–4.75, 5.25 and 6.25 (`analysis/v10_src/C011_dir.json`).

## Proposed change
1. `frame_scan.py`: add a `dir_blur` flag using the gradient ratio above, next to `blur_dip`.
2. `selects_score.py` / any source profiling: score the window's worst frame on both sharpness and the directional ratio.
3. Reviewer checklist: on any pan, zoom into the subject at full size for streaking, as well as softness.
4. The reviewer also notes that frame_scan misses a whole-frame blur straddling a cut (e.g. a 0.2 s whip), since it ignores the first and last 2 frames of each shot. Check designed whips by eye, or scan transition spans separately.
