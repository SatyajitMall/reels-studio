# CR-20261108-kolkata-late-round-edits

| Field | Value |
|---|---|
| From reel | `projects/kolkata/` |
| Arch version | 0.9.0 |
| Type | script · skill |
| Severity | workaround |
| Status | partly done (v0.9.1) |

## What happened
Rounds 7 and 8 changed single shots, the title and the look on a sequence that was already built and reviewed. The studio's tools assume a full build:
- the reel's `build_v6.py` clears V1/V2/V4/V5/V7 and A1–A3, and disables the V3 look layer;
- a rebuild would have wiped everything done by hand after the build: the review-gate dissolve, in-point corrections, Warp on four shots, the title keys, and the director's look.

So every change was a hand-written script. Problems found on the way:
1. **Swapping a shot also breaks its edges.**
   - The 10-frame Cross Dissolve on the shot's edge has to be re-made after the swap.
   - When the new clip has no picture after its out-point, Premiere silently makes a shorter one-sided dissolve: 5–6 frames, ending on the cut.
   - Warp has to be re-applied, because effects don't move with the media.
2. **Pregate false positives after a title change.**
   - `frame_scan`'s blur-dip check compares each frame with the shot's own median sharpness.
   - A bigger title raised the median, so the shot's untouched frames before the title appears (5.76–7.40 s) were flagged as "soft".
   - The title's designed focus-pull was flagged too.
   - Both had to go in `--designed` spans.
3. **`render_diff` scope.** `pregate.py --prev` diffs against the previous *export*, not the last *reviewed* one. After an unreviewed intermediate (v8), the scope it reported to the reviewer missed the title change. The reviewer caught it by diffing against v7b themselves.

## Workaround used in the reel
- `projects/kolkata/tools/swap_v7.py` replaces named shots in place:
  - remove the V1 clip (no ripple), then place the new source frame for frame, interpreting non-25 fps sources;
  - read the in-point back and correct it;
  - set Rotation, Position and Scale keys, and remove the linked camera sound;
  - re-make edge dissolves read before the swap.
  - Flags: `--base`, `--out`, `--seq-id`, `--seq-name`.
- `analysis/_es_title_v8.jsx` swaps a V5 still and copies its Opacity / Scale / Gaussian Blur keys, relative to the still's in-point (3599.96 s).
- Warp re-applied with `stabilize_clip`; analysis read back from `AnalysisStatusCounter` (408 = done) and the "Auto-scale (x %)" label.

## Proposed change
1. **`scripts/premiere_swap.py`** (promote `swap_v7.py`), the "late-round edit" helper:
   - swap a shot, a V5 still or an overlay, keeping keys and effects where Premiere allows;
   - re-make edge transitions, and **warn when one comes back shorter than asked**;
   - re-apply Warp and wait for `AnalysisStatusCounter = 408`;
   - write the new EDL as the shot map.
   - Document it in `premiere-mcp-reality.md` next to the in-point read-back (CR-20261108-kolkata-footage-catalogue item 5).
2. **`frame_scan.py` blur dips:** measure sharpness on the picture only, masking V5 overlay regions (from the EDL's overlays and their alpha). Or compare against the previous version's same frame when `--prev` is given, so unchanged frames can't be flagged.
3. **`pregate.py --reviewed <export>`:** the last export that passed the gate, used for the scope and `diff.json` (default: the latest `review_*.md` with PASS).

## HQ decision (v0.9.1, 2026-11-08)
- **(3) Done.** `pregate.py --reviewed <export> --reviewed-map <map>`: the last version that **passed** the gate (`--prev` / `--prev-map` remain as old names), with `review-gate.md` updated. Explicit, not auto-detected from `review_*.md`, because reels name those files differently.
- **(1, partly) Done in the reality doc:** the one-sided shorter transition and the Warp status codes (104 running, 408 done).
- **(1) `scripts/premiere_swap.py` and (2) `frame_scan.py` ignoring overlays: accepted for v0.11**, with Batch C's ExtendScript library. Reproduced (2) on kolkata v8c: without designed spans the title raises 5.76–7.6 s blur-dip flags.
