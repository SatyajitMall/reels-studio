# CR-20261019-puja-night-2-beat-transitions

| Field | Value |
|---|---|
| From reel | `projects/puja-night-2/` |
| Arch version | 0.5.3 |
| Type | script · skill (effects-playbook.md §D) |
| Severity | workaround |
| Status | open |

## What happened
Round 6 director note: "think about better cinematic transitions that match the beat". Premiere's own transitions didn't fit:
- a Film Dissolve across Warp-stabilised clips rendered Warp's "analysing" banner during the transition (the handles aren't analysed);
- built-in zoom / whip presets can't be keyed to a frame-exact beat by script, and they're graded by the V3 look twice when placed above it.

Also, a 0.01-speed frame hold on a Warp-stabilised clip (C089) jumped ≈ 25 px, because the hold piece isn't stabilised.

## Workaround used in the reel
Reel-local `projects/puja-night-2/tools/beat_transitions.py`:
- renders short full-frame overlays (default 4 frames before + 4 after the cut) from an export of the graded reel **with the overlay track hidden**, so they match the grade exactly and need no handles;
- types: `zoom` (zoom-through with radial blur), `whip` (directional blur + slide, left / right / up / down), `leak` (warm gold light leak sweeping across the cut, replaces white flashes), `dip` (soft dip through warm dark, the outro dissolve that works over Warp clips);
- `--spec` JSON of `{type, cut, dir?, n?}`, `--prefix` to keep names unique in the bin, writes a manifest with each overlay's start time;
- placed on the top video track (V6, above the look and the titles) at cut − n/25.

Used at 3.80 (intro → reel), 20.24 (the lift), 22.76 / 24.00 / 27.80 (pans meeting on beats), 40.44 (the reveal) and 50.52 (into the ending). The C089 hold is the same idea: the stabilised last moving frame baked from the graded body, on V6.

Cost to know: any change to a shot that an overlay touches (grade, framing, swap) means re-exporting the body and re-baking that overlay. In round 6 two overlays were re-baked twice.

## Proposed change
1. Promote the tool to `scripts/beat_transitions.py` with the four types, plus a `hold` type (freeze the last frame of a stabilised shot).
2. `effects-playbook.md` §D: list these as the default way to do beat transitions on Warp-stabilised or graded footage, with when to use each (zoom-through on section changes, whip where two pans meet on a beat, leak on a reveal, dip into an outro; hard cuts everywhere else; 3–4 per 30 s).
3. Skill Phase 5 step: "bake transitions last, after colour and framing are final; keep a list of overlay → shots it touches; re-bake any overlay whose shots changed".
4. Optional: a `--from-premiere` helper that exports the body with the overlay track hidden (`_es_export_seq6.jsx` pattern) so the bake is one command.

## HQ decision
<!-- HQ fills this in. -->
