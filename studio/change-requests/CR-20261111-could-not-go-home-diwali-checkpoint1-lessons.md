# CR-20261111-could-not-go-home-diwali-checkpoint1-lessons

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.9.1 |
| Type | script · rule · template |
| Severity | workaround (nine preview rounds at Checkpoint 1, about 6 h; the retro's top friction) |
| Status | open |

## What happened
These are the "CR candidate" lines from the pilot's friction log, filed together at the retro (skill Phase 9, step 3). Each one cost at least one preview round.

1. **teardown.py read the reference wrong, twice.**
   - It counted in-camera motion blur (crowd streaks, whip pans) as cuts: 43 cuts/min reported, against 9 real shots.
   - It counted the reference's step-print as cuts too. I read the step-print as slow motion for three rounds (v1b–v2d).
2. **frame_scan missed a one-frame snap.** My preview stabiliser jumped 43 px at one frame inside a shot (C062, v2d), and nothing flagged it. I found it only after the director's note.
3. **The brief let "Time: none" through.** v1's Treatment said "none (25 fps, no slow-mo headroom)". That went against the director profile ("drama from holds and slow motion") and Kolkata's identical round-5 note. Then p1b over-corrected: interpolated slow motion on every shot, plus rack pulls nobody asked for.
4. **Inserts and motifs:**
   - Stock from other places and camera heights read as "unrelated", even when each clip fit its line.
   - I turned a found clip (the director's city, from GPS) into a symbol nobody asked for: "serves no purpose".
5. **GPS places weren't listed at ingest.** The clips' GPS showed the Diwali show was at the same venue, which nobody had noticed. Partly covered by CR-20261108-kolkata-footage-catalogue.

## Workaround used in the reel
1. I watched the reference's bursts frame by frame; the step-print became the reel's slow-down.
2. I measured per-frame global shifts with phase correlation by hand.
3. The director said "no slow motions, no cinematic effect" and I rebuilt (v1b, v1c).
4. Insert boards of the director's own topic footage plus topic stock went to the director before building. Stock was kept only for a different world (home, Maa's hands).
5. I read GPS with ffprobe (`com.apple.quicktime.location.ISO6709`).

## Proposed change
1. **`scripts/teardown.py`:**
   - merge "cuts" less than 0.2 s apart and report them as **motion bursts**;
   - report **step-print sections** (runs of near-duplicate frames with a hold of 2–4 frames) separately from cuts and from slow motion;
   - add both to `COMPARE.md`.
2. **`scripts/frame_scan.py`:** flag a **single-frame global shift** inside a shot, by phase correlation, when it's more than 8 px and the frames either side agree.
3. **Brief template, Treatment:** a per-shot **time and camera-move plan** (real time / step-print / interpolated slow motion / push / none). "None" for the whole reel needs the director's sign-off in the brief.
   - Rule (cinematic-montage): on 25 fps footage, interpolated slow motion only on calm human beats; hands and work stay real time; no focus pulls unless asked.
4. **cinematic-montage playbook, inserts:**
   - same people and same place first (macro crops of the 4K);
   - stock only for a world the footage can't show (home, memory);
   - never turn a found clip into a motif without asking.
5. **`scripts/ingest_report.py`:** list GPS per clip (reverse-geocoded or clustered by distance) so same-venue shots and "home" footage turn up in Phase 1. This could join CR-20261108-kolkata-footage-catalogue.

## HQ decision
<!-- HQ fills this in. -->
