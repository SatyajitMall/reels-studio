# CR-20261020-pujo-ki-asolei-sobar-reference-grade-match

| Field | Value |
|---|---|
| From reel | `projects/pujo-ki-asolei-sobar/` |
| Arch version | 0.5.3 |
| Type | skill · script |
| Severity | workaround |
| Status | rejected in part (v0.8.0) |

## What happened
The brief's look came from the director profile's default (Warm Film, then a "one warm-neutral target" at luma 0.36, B/G 0.90) instead of the reference reel the director supplied. After two cuts the director asked: "the cinematic effect and colour grading as shown in the reference should come out." Measured, the reference sat far from that target: luma 0.25, warm-olive shadows (B/G 0.53), amber mids (B/G 0.65). `analyze_footage.py --reference` reports pacing and a single warm/cool number, but nothing per tone band.

## Workaround used in the reel
- `projects/pujo-ki-asolei-sobar/tools/ref_look.py`:
  - **measure:** frames of the reference → luma mean / p02 / p50 / p98, crushed %, clipped %, saturation, and R/G + B/G per band (shadows < 0.2, mids, highlights > 0.6);
  - **look:** per-clip normalise → low-key filmic tone curve + 3-way channel gains + saturation trim (pixelwise, exported as a 33³ `.cube`) → halation + vignette (optical; not in the LUT);
  - **check:** the same stats on our graded stills against the reference medians. Three tuning passes landed within ~0.03 on every measure.
- The LUT is `grade/pujo_reference_look_v1.cube`. It loads by hand in Lumetri (it can't be loaded by script).

## Proposed change
- **Skill Phase 1:** when a reference exists, "measure its grade" is a required step, with numbers written to `brief.md` §3 (per-band ratios, luma, crush, saturation, optics such as shallow focus or halation). The look is designed to hit those numbers, then checked with the same metric at Phase 4.
- **Promote `ref_look.py`** to `scripts/` (split into `measure_grade.py` and `build_look_lut.py`), and add a `--reference` comparison mode to `colour_report.py`.
- **Playbook §A3:** add "Match Reference (measured)" with this recipe, and note that profile looks are only the default when there is no reference.

## Follow-up 2026-10-23 (rounds 9–10): per-shot trims need person-gated skin protection
Holding skin to one anchor while correcting a shot's cast fails when the protection is hue-based: Pujo walls (orange sodium, pink-brown pandal cloth) fall in the skin hue band (10–45°). So the cast and saturation corrections skipped exactly the surfaces that made shots read warm / cool, and two blind reviews flagged the alternation. The fix in the reel is `projects/pujo-ki-asolei-sobar/tools/shot_trim.py`:
- `protect: person`: skin inside a person matte (hyperframes remove-background, cached);
- `face_lift`: exposure on faces only;
- `floor`: a shared black floor.

**Proposed:** promote it to `scripts/`. In the colour phase, use person-gated skin protection whenever a correction must not move faces.

## HQ decision (v0.8.0, 2026-11-01)
**Designing the grade to hit the reference's numbers is rejected.** Pujo's reference-matched level (luma 0.25–0.36) read "too dark" on the phone in round 13, and the studio default is now camera-true (effects-playbook §A0). Measuring the reference with `teardown.py` stays. Person-gated skin protection is deferred, together with CR skin-qa.
