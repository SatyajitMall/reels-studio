# CR-20261111-could-not-go-home-diwali-scan-window

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.10.2 |
| Type | script |
| Severity | workaround (a false FAIL; typed around it, about 10 min to diagnose) |
| Status | open |

## What happened
On v3c, pregate FAILed with `frame_scan blur_dip 01_C049_auto 0.08–0.24 s (0.45)`. 01 is now real time (no longer a step-print), so no designed span covered the flag.

The picture wasn't soft. I measured Laplacian sharpness on the v3c export, frames 0–38, each value relative to the shot's median:

| Region | Frames 0–4 | From frame 8 |
|---|---|---|
| Whole frame | 0.36–0.42 | ≈ 1.00 |
| Picture window (y 505–1315) | 1.27 → 1.07 (sharpest at the start) | ≈ 1.00 |
| Caption band below the window (absolute) | 0.08 | 5.4 |

The first letter line fades in at 0.20 s. That adds sharp text edges to the whole frame, so every frame before it scores as a "dip".

v3b had the same flag at 0.08–0.24 s. It was hidden inside the 01 step-print span, and review_v3b explained it as "the letter line fading in". Once the step-print went, the flag surfaced.

## Workaround used in the reel
Typed the span as a title: `--designed 0-0.32:title`. That is honest, since the flag comes from a title-type overlay fading in, but it also excuses any real blur in the picture during those 8 frames.

The reviewer still judged the hook strip at full rate.

## Proposed change
1. **`frame_scan.py`** takes pregate's `--window` and measures sharpness, frozen runs and luma jumps **inside the picture window**. Today only motion_audit and the strips use it.
   - In windowed reels, overlay type outside the window shouldn't move the picture metrics.
   - Text and graphics can be scanned separately, as a black or frozen check on the bands.
2. Failing that, `blur_dip` uses the shot's median over **frames where the overlay set is the same**, so a line fading in doesn't count as the picture going soft.
3. **Pregate output:** when a blur_dip is mostly outside `--window`, say so in the FAIL line (for example "dip is outside the picture window: overlay?"), so the editor doesn't have to measure it by hand.

## Added 2026-11-12 (v7): the same gap with the frozen check, the other way round
- **What happened:** v7's new 12 is a locked-off stock close-up, a hand lighting a diya with a flickering flame, src 26.80–28.76 s. Pregate FAILed it: `frozen 12_S32_home_diya 17.12–18.76 s (0.22)`.
- **The rule:** frozen fires on 4+ frames whose mean change is under 0.35/255, measured over the **whole 1080×1920 frame**. The 16:9 window is 608/1920 = 32 % of it, and the rest is black, so the picture's own change is diluted about 3×. Measured on the source and scaled to the window:
  - the close-up changes about 0.6–0.7/255 per frame inside the picture;
  - that reads as about 0.20 over the whole frame.
- **Where the blur_dip case gave a false FAIL, this one tightened the bar 3×.** A calm tripod shot inside a window can't pass, though it would pass full-frame.
- **Workaround:** picked a different stretch, 12.96–14.92 s, where the camera still rises (0.49, a margin over the floor). It's the same close-up. I didn't type a `freeze` span: it isn't a freeze.
- **Cost:** about 15 min (a whole-clip scan, a sheet, a fix script, a re-export and a re-run of the pregate).
- **Adds to proposal 1:** measure frozen runs inside `--window`, at the same 0.35 floor, so the floor means the same thing in windowed and full-frame reels.

## HQ decision
<!-- HQ fills this in. -->

### More evidence (2026-11-13, v10d)
- **The reviewer made the same mistake frame_scan makes.** It measured whole-window Laplacian-variance sharpness and read each letter line's 3-frame text fade-in as a 7-frame "focus-in blur" on the picture, and FAILED v10d on it. The probe (`projects/could-not-go-home-diwali/analysis/v10_notes/linestart_blur_probe.md`) disproved it:
  - track-mute renders: with the text track off, the picture is flat;
  - with the text pixels masked out, all six line-start shots are flat.

  The reviewer re-measured and withdrew the finding (PASS). Cost: about 35 min and a second review pass.
- **Proposed in addition:**
  - `frame_scan` and the reviewer's sharpness checks mask the type, using the V5 overlay alpha or a text mask from the line PNGs, before computing blur;
  - review-gate.md: a "blur" finding must hold with the type masked, or on a render with the text track muted.
