# CR-20261016-my-reel-conform-by-interpretation

| Field | Value |
|---|---|
| From reel | `projects/my-reel/` |
| Arch version | 0.2.5 |
| Type | rule |
| Severity | polish |
| Status | done v0.3.1 |

## What happened
CLAUDE.md §3 says to conform outlier frame rates (24 fps clips in a 25 fps sequence) with `speed_change`. Applied after placement, a speed-up shortens the clip and opens a gap; the source span then has to be pre-computed ×1.0417 and the clip re-trimmed, with QE frame quantisation on top.

## Workaround used in the reel
`set_override_frame_rate {projectItemId, frameRate: 25}` on the 4 used 24 fps clips (Modify > Interpret Footage). Every frame plays once, durations are exact, and source in-points are just ×0.96. Verified with `get_footage_interpretation` and `get_timeline_gaps` (0 gaps).

## Proposed change
CLAUDE.md §3 and skill Phase 3: "Conform outliers by interpreting them at the sequence rate (`set_override_frame_rate`) **before** placing them. Scale source times by original_fps / sequence_fps. Use `speed_change` only for creative speed." Audio on interpreted clips shifts pitch ~4 %, which is fine when natural sound is muted (music-montage); for dialogue clips, flag it.

## HQ decision
**Accepted, done in v0.3.1.** CLAUDE.md §3 now conforms outliers with `set_override_frame_rate` before placement and scales source times by original/sequence fps, with a pitch note for dialogue. Skill Phase 1 step 6 does it at import time.
