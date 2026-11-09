# CR-20261107-kolkata-preview-fx

| Field | Value |
|---|---|
| From reel | `projects/kolkata/` |
| Arch version | 0.9.0 |
| Type | script · skill |
| Severity | workaround |
| Status | partly done (v0.9.1) |

## What happened
- **The director's round 5b note on preview v5:** "a few of my shots need stabilisation and cinematic effect, the swooping shots don't make it good". An earlier note said the same about effects on their own footage: "no slow motion, no anything".
- **The offline preview can't show the moves.** Since v0.9, pace, picks and framing are settled on `scripts/preview_edl.py` previews, but four kinds of effect can't appear in them:
  - Stabilisation isn't available at all.
  - Slow motion on 25 fps footage repeats frames. Its header says "the final uses AE Timewarp".
  - Speed ramps are faked by splitting a shot into a fast and a normal piece. That gives a step, not a ramp.
  - Whip pans and light leaks show as hard cuts, or don't show at all.
- **Result:** the director judged v5 as if those effects weren't planned. Half the effects in the brief (the whip, step-print, every slow-mo on our own shots) were invisible in the preview.
- **Nothing ranks shots by shake before the cut.** `scripts/shake_report.py` works on exports and previews. On camera `.mov` files it crashes:
  - error: `ValueError: could not convert string to float: '7319,'`;
  - cause: `fps_of` reads ffprobe `avg_frame_rate` with `csv=p=0`. On every rotation-tagged camera file (all of the director's footage) the output gains a trailing comma: `25/1,`, or `7319,` in the error above.
  - The round 5b picker worked around it with a wrapper that only swaps in a robust `fps_of()`. Measuring 47 clips that way found locked replacements (0.08–1.05 px).
- **The swooping shots were only found after the director saw them.** The v5 preview's shake ranking was clear:
  - C097 façade ride: 56 px jit_rms, 701 px/s;
  - C094 scooter POV: 20–32 px;
  - locked shots: 0.3–1.2 px.

## Workaround used in the reel
- **Reel-local `projects/kolkata/tools/fx_prerender.py`** pre-renders each treated shot's exact window to ProRes 422, at half the camera's display size. In the EDL the shot then points at the render, with `src_in` 0, `rate` 1 and Scale ×2, and its `note` keeps the camera in-point, rate and treatment for the Premiere build. The treatments:
  - **stabilise:** a similarity tracker (phase correlation on 4 quadrants: shift, roll, zoom), a Gaussian-smoothed or locked path, the horizon levelled, then a 5–6 % zoom. On the C082 walkway it halved translation and roll jitter (shake_report 2.6 → 1.2 px).
  - **slow:** ffmpeg `minterpolate` (mci, aobmc, bidir). The dhakis' in-between frames showed no doubled limbs at 1:1.
  - **speed_keys:** an eased ramp: 4× minterpolate in-betweens, sampled at the integrated camera time.
  - **whip_in / whip_out:** a horizontal box-blur smear plus a slide, easing out of or into the cut.
  - **interpret:** 24/30 fps stock used frame for frame, as Premiere's interpretation does.
- **Reel-local `tools/make_leak.py`:** a procedural warm light leak, rendered twice:
  - `_screen.mov` for Premiere V4 in Screen;
  - `_alpha.mov` (alpha = brightness) for the preview, listed before the window matte so the bands stay black.
- **`tools/guide_edl_v5b.py`** writes the EDL and the fx jobs file together, so their durations can't drift. Each job is the shot's length + 0.12 s.
- **The build still uses the studio routes:** Warp Stabilizer in Premiere (skill Phase 5) and AE Timewarp (after-effects.md). The preview renders are a stand-in for judging the cut.

## Proposed change
1. **`scripts/preview_edl.py`:** add optional per-shot keys, or a pre-pass script `scripts/preview_fx.py` modelled on the reel-local tool:
   - `stabilise: "smooth" | "lock"` (+ `sigma`, `zoom`);
   - `slow_interp: true` (motion-compensated slow-mo instead of repeated frames);
   - `speed_keys` (an eased ramp);
   - `whip_in` / `whip_out`;
   - overlay `blend: "screen"` (for leaks and grain, so the preview matches V4).
2. **`scripts/shake_report.py`:** parse fps robustly (`split(",")[0]`), so it runs on camera files. Then add a Phase 1/2 step: rank every planned window's shake from the EDL before the first preview, and flag jit_rms > 3 px or pan > 300 px/s (swoops) for stabilisation or another pick.
3. **Skill Phase 2.5 / review-gate:** for any reel whose brief lists slow-mo, ramps or whips, the preview must show them (pre-rendered), so the director doesn't judge a cut with its effects missing.

## HQ decision (v0.9.1, 2026-11-08)
- **(2, the crash) Done.** `shake_report.py` uses the shared `media_info.fps_of` and runs on rotation-tagged camera files (verified on a kolkata clip).
- **(1, 3) and (2, the shake ranking step) accepted for v0.11:** `scripts/preview_fx.py` promoted from `projects/kolkata/tools/fx_prerender.py` (stabilise, motion-compensated slow-mo, eased ramps, whips, Screen-blend overlays), the rule that a preview shows the brief's planned effects, and a shake ranking of every planned window before the first preview (with Batch C's pre-screen).
