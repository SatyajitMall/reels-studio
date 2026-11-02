# CR-20261023-pujo-ki-asolei-sobar-correction-stacking

| Field | Value |
|---|---|
| From reel | `projects/pujo-ki-asolei-sobar/` |
| Arch version | 0.5.3 |
| Type | skill (colour phase) · script (QA) |
| Severity | workaround (the director called v10 "over-processed, not natural" after 10 rounds of fixes) |
| Status | partly done (v0.8.0) |

## What happened
Each director note and review finding added one more correction on top of the last, and each one passed on its own metric. By v10 every shot went through:
- heavy temporal denoise;
- clarity + local contrast (+ a sharpen on one shot);
- per-shot auto-levels to one target;
- near-full white balance and a forced cast match to one colour;
- the cine look at 100 %;
- a skin anchor in the render plus a skin post-pass;
- deflicker;
- face lifts and shadow toe lifts.

The director: "why does everything look so over-processed and not natural". Side by side with the camera original (`projects/pujo-ki-asolei-sobar/analysis/look_n1/compare.jpg`), the problems were plain:
- the blue night street had turned orange;
- whites had gone cream;
- skin looked waxy;
- edges had halos.

No studio check compares a render against its camera original. All the QA (`colour_report.py`, the skin metrics, frame_scan, the review gate) compares shots with each other or with targets.

## Workaround used in the reel
- `shot_render_v5.py --natural` / `--natural-matched`: every correction at partial strength (white balance 45–60 %, levels 50–65 %, cast 0.35–0.6, look 60–75 %, skin anchor ^0.5–0.75), light denoise, no clarity, no face lifts.
- Shown to the director as a 3-column sheet (original / current / proposed) before re-rendering. The director picked "natural, but warmer and matched".

## Proposed change
- **Colour QA:** a `vs_original` sheet (camera original / graded, same frame, 3–4 shots) is mandatory at every Checkpoint 2, and the reviewer gets it too. Add to `reel-reviewer.md`: "flag a grade that departs from the original's light without a brief reason (night turned day-warm, whites shifted, waxy skin, halos)".
- **Playbook §A2:** default corrections at partial strength. Full-strength auto-levels and forced cast matching only where the brief asks for a stylised match.
- **Skill rule:** before adding a correction to fix a note, list the stack already applied to that shot. If it is over ~5 steps, rebalance instead of adding one more.

## Follow-up 2026-10-24 (round 13)
On a phone the final v12 read "too dark" (mean luma 0.25–0.36 per shot, the reference-matched level). The director chose +½ stop (×1.25 mean luma by a power curve). **Proposed:** a phone-viewing brightness floor in colour QA (mean luma ≥ ≈ 0.32 per shot unless the brief asks for a dark look), and a phone check before Checkpoint 2.

## HQ decision (v0.8.0, 2026-11-01)
**Partly accepted, with the director's go-ahead on Batch A of the v0.8 plan.**
- Done: camera-true grading as the default (effects-playbook §A0). Each shot is corrected toward its own camera file and checked by `scripts/camera_fidelity.py`. The absolute floors (≥ 0.32 here, 0.40 / 0.30 on goddess) are reported only: on goddess they burnt night shots. The phone viewing check is the `encode_master.py --phone` review copy.
- Still open: a cap on stacked corrections per clip, and the person-matte skin metric (CR skin-qa).
