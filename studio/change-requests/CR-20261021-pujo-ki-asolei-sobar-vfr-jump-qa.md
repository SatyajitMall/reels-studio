# CR-20261021-pujo-ki-asolei-sobar-vfr-jump-qa

| Field | Value |
|---|---|
| From reel | `projects/pujo-ki-asolei-sobar/` |
| Arch version | 0.5.3 |
| Type | script (frame_scan.py, analyze_footage.py) |
| Severity | workaround (a jump inside a shot reached a near-final export) |
| Status | partly done (v0.7.1) |

## What happened
Blackmagic Cam clip C004 is variable-frame-rate (`r_frame_rate` 30/1, `avg_frame_rate` 29.285: 612 frames in 20.9 s). Around 12.50 s the camera moved during a dropped-frame gap, so the shot snaps to a new framing mid-shot. It was placed as shot 5 in v1e. **`frame_scan.py` reported 0 flags** on that export. I caught it by eye on a 10 fps strip: a frame difference of 41 against a median of 3.5. Another clip (C028, 30.003 fps) and many 30.00x clips have the same VFR signature.

## Workaround used in the reel
- Moved shot 5's in-point past the jump (12.55 s); the placed window's max frame diff is now 6.7 against a median of 3.3.
- Shot renders resample anything between 28 and 31 fps onto an exact 30 grid (`fps=30`).

## Proposed change
- **`analyze_footage.py`:** flag VFR clips (avg ≠ r_frame_rate by more than 0.1 %, or frame count ≠ duration × fps), and list **content discontinuities**: frame-to-frame diff above ~6× the clip median, with timestamps. Write them into `summary.md`, so the EDL can avoid those windows.
- **`frame_scan.py`:** add a `jump` check inside each shot (same diff-spike rule, excluding the shot's own cut frames), so a mid-shot snap is flagged like a flash.
- **Added 2026-10-23 (round 9, review gate):** `frame_scan.py` also gave **0 flags on a half-second full-frame optical-flow smear** (ffmpeg `minterpolate` slow-mo across two passers-by crossing the lens; translucent doubled heads, duplicated edges, 3 frame-difference peaks in 9 frames). The blind reviewer caught it. Proposed: a `ghost` check that flags frames whose edge map is the average of the two neighbours' (double edges: high gradient energy at two offsets), plus a rule in `motion-and-ai.md` / effects-playbook "Slow-mo B-roll": never interpolate across an occluder crossing the lens; cut around it or keep that stretch at 1×.
- **Added 2026-10-23 (round 9, gate loop 2):** `frame_scan.py` also missed a **48 px whole-frame translation jump** in one frame (a same-framing cut that read as a camera jerk). Proposed: a `translation` check (phase-correlation shift between consecutive frames, flag > 8 px inside a shot), sharing the `jump` rule above. Studio rule for the playbook: a cut between two moments of the same take with near-identical framing reads as a glitch. Either make it a clear cut-in / change of size, or hide it under motion.

- **Added 2026-10-24 (retro), synthesised slow motion limits:** (a) on soft, low-light handheld 30 fps footage, `minterpolate` mci warps faces and hands below ~0.6×; frame blend ghosts thin fast objects (drumsticks) at any speed. (b) Never interpolate across an occluder crossing the lens, or a fast hand turn; play that stretch at 1× and ease the speed after it. (c) An abrupt 1× → slow step reads as a glitch; ease over 10–15 frames. (d) Two takes in this reel (dhaki, young balloon seller) failed every slow-mo variant over 4 blind reviews and ended at real speed. Shoot 60 fps for anything that may be slowed (director-profile CR).

## HQ decision
**Partly accepted, v0.7.1 (2026-10-27).**
- **Done on the raw clips:** `scripts/ingest_report.py` flags variable frame rate (average vs nominal > 0.1 %). With `--scan` it lists dropped-frame gaps (from packet times) and isolated picture jumps (frame difference > 6× the clip median and > 3× both neighbours, so pans don't count), with times. Verified on C004: 15 dropped frames, one jump at 12.53 s, the one this reel found by eye. Phase 1 now says to keep placed windows clear of those times.
- **Deferred to the backlog:** the `jump`, `ghost` and `translation` checks in `frame_scan.py` (exports), and the slow-motion rules in `motion-and-ai.md` / the effects playbook.

