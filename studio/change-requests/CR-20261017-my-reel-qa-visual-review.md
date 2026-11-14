# CR-20261017-my-reel-qa-visual-review

| Field | Value |
|---|---|
| From reel | `projects/my-reel/` |
| Arch version | 0.4.1 |
| Type | skill · script · rule |
| Severity | workaround |
| Status | open |

## What happened
After approving v8, the director asked: "Are we not QAing videos for correctness and accuracy [with] reasoning?" Their other note was that the glittery AE looks were "cringe and less production grade".

QA up to v8 was metric-only: luma, colour, shake, Warp-banner scans and a few spot frames. Two kinds of fault got through.
- **Taste.** The light leaks, CC Light Rays and bokeh embers all passed the luma checks, but they looked cheap. Premiere's *Light Leaks* transitions also strobed (luma +0.15 then −0.16 within 4 frames), and nothing checks frame-to-frame jumps.
- **Correctness.** C073 (in the reel since v6) has two source camera jerks with smeared frames, down to 0.51 of the shot's median sharpness. Warp hid the shake, so `shake_report.py` passed it. Selects scoring ranks windows on mean sharpness and never looks at the worst frame. On C076 the source is blurred near the out-point, and Timewarp at 60 % stretched it over 5 frames with ghosting.

## Workaround used in the reel
Reel-local scripts (scratchpad, recipes in `projects/my-reel/analysis/`):
- luma-jump scan (every frame, |Δ| > 0.05);
- repeated-frame scan;
- black and white frame scan;
- cut-to-beat offsets;
- blur dips: Laplacian variance per frame < 60 % of the shot's median → `analysis/qa_v8_auto.json`, `qa_v8_blur.json`.

Then a written per-shot review with a pass/fail and a reason for each shot (`analysis/qa_v8_report.md`).

## Proposed change
1. **`scripts/qa_reel.py <export> --edl <edl/json> [--beats beats.json]`.** Writes `analysis/qa_<ver>.json`, plus a contact strip of every flagged frame. It runs these checks:
   - repeated frames;
   - luma jumps;
   - black and white frames;
   - blur dips per shot;
   - cut-to-beat offsets;
   - Warp-banner scan.
2. **Skill, QA phase.** Before every export goes to the director, write `analysis/qa_<ver>_report.md`: one row per shot (time, shot, pass/fail, reason), plus the root cause of each fail. A fail on a designed moment (a transition or a fade) gets marked as intended, with the reason.
3. **Selects.** Score windows on their *minimum* sharpness as well as the mean (reject a window if min < 0.7 × median). Check source blur near the out-point before any slow-mo op.
4. **Playbook, taste rule.** On handheld night footage, avoid:
   - stacked decorative AE looks (leaks + rays + particles);
   - Premiere's *Light Leaks* transition (it strobes).

   Judge any added look by eye, at 100 % and in motion. Never judge it by luma alone. Default to film dissolve, cut, dip or flash.
