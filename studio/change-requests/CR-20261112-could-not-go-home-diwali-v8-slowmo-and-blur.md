# CR-20261112-could-not-go-home-diwali-v8-slowmo-and-blur

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.10.3 |
| Type | script + skill |
| Severity | workaround (five gaps hit in one round; about 70 min of the round went on them) |
| Status | open |

## What happened
On v7b the director asked for three things:
- slow the diya close-up (12, Pexels stock, 25 fps) and the AI cracker shot (19, Veo, 24 fps);
- extend the reel if needed;
- "add motion blur outside the auto" on the opening shot (01, a stabilised back-seat shot of the driver).

v8 delivers all three. Five gaps came up on the way.

### 1. Pregate has no slow-motion span type
- 12 at 50 % is a near-still close-up. `frame_scan` FAILed it as "frozen" (17.12–19.88 s, mean change 0.28 < 0.35).
- The span types are fade, end-card, title, step-print, flash, transition and freeze. None is "deliberate slow motion".
- **Workaround:** typed it `17.04-20.56:freeze`, so the reviewer gets full-rate strips and must judge every frame. That's honest about the control, but it's the wrong word.
- **Proposed:** add a `slowmo` type to `SPAN_FLAGS` that allows `frozen` and keeps the full-rate strip. Then a stall inside a real-time shot still FAILs, and a requested slow-mo is labelled as one.
- This compounds CR-20261111-could-not-go-home-diwali-scan-window: in a 16:9 window the frozen floor is about 3× stricter.

### 2. `ae_roundtrip.py` time_remap ignores `"ease": 0`
- I wanted a constant 50 % Frame Mix retime of 19, to compare against Timewarp on sparks, so I set `points [[0,0],[3.2,1.6]]`, `ease 0` and `blend mix`.
- The output followed an S-curve. Output frame 4 = source 22, frame 36 = 35, frame 48 = 54 (a constant retime gives 24, 40, 46).
- **Proposed:** `ease: 0` sets linear keys (`KeyframeInterpolationType.LINEAR`), or a `"interp": "linear"` field. Also add a `framemix` option to the `timewarp` op, since Frame Mix is a valid choice for particles.

### 3. No route for motion blur on part of the frame
- Nothing in the studio adds motion blur to a region: no RSMB, no masked op in `ae_roundtrip.py`, and no OpenCV in the venv for optical flow. A reel session may not install packages.
- **Workaround, reel-local `tools/blur_01_v8.py`:**
  1. Trace the openings as polygons on the clip's median frame. Subtract the subject's silhouette (the dark region connected to a seed point, dilated 7 px) and feather.
  2. `minterpolate` ×8 (mci, aobmc, bidir) at half size, then `tmix` over N sub-frames centred on each frame: 8 = 360°, 48 = a 6-frame shutter.
  3. Merge into the full-size ProRes in native yuv422p10le, so the interior is untouched within ProRes rounding (2–4/1023).
- **Measured:** at 360° nothing showed on an already-defocused cinematic-mode background; it took a 4–6 frame shutter to read. A statistical mask (temporal std) took in the pillars and left holes in uniform areas, so traced polygons won.
- **Proposed:** promote it as `scripts/region_motion_blur.py` (polygons + seed for the silhouette, `--shutter-frames`), or add AE's Pixel Motion Blur with a track-matte PNG to `ae_roundtrip.py`. Timewarp also has "Enable Motion Blur" with a shutter angle, which would give AE's vector blur at 100 % speed.

### 4. ffmpeg 7 converts levels when output colour tags are set
- Conforming the untagged Veo H.264 to ProRes with `-color_range tv -colorspace bt709 …` squeezed the codes from 4–253 to 14–241 (mean −3).
- Without the tags the codes match (error 0.4).
- **Proposed:** a line in the `ffmpeg-color-grading-chromakey` skill and in `conform_clip.py`'s notes: tag the input (before `-i`) or not at all. Never tag only the output of an untagged source.

### 5. Replacing an audio clip drops its level and fades
- Removing and re-placing the A3 guide lost the clip's Level (−1.2 dB) and end fade, so the mix peaked at −0.3 dBTP. The pregate caught it.
- **Proposed:** a reality-doc note, plus a helper in the shared jsx snippets that snapshots Volume/Level keys before `remove()` and restores them, shifted.

## HQ decision
<!-- HQ fills this in. -->

### More evidence (2026-11-13, after the upload)
- **The masked region blur was rejected after it shipped.** The op is minterpolate ×8 + tmix over 48 sub-frames inside a traced, feathered mask (`tools/blur_01_v8.py`). It passed two review gates (v8 8/10, v8b 8.5) and the director's approval. On the phone, after the scheduled upload, the director called shot 01:
  - "very weird and blurry, not straight-line motion blur";
  - "the man's face and the motion blur get mixed up";
  - "the subsequent auto shots now don't match the first".
- **Measured.** minterpolate's block motion plus a long tmix gives a soft haze, not directional streaks: lights smear into mush and the bus edges go. The mask feather halos the subject's outline. The neighbouring shots carry the camera's own depth (round bokeh), so the blurred shot stands out.
- **Fix:** v10d puts 01 back on the stabilised camera footage. It needed a re-upload on the day the post was scheduled.
- **Proposed in addition to item 3 (a masked region-blur op):**
  - don't build it on minterpolate + tmix. Use a real directional blur along measured optical-flow vectors, with streak length capped by the shutter. Or prefer the camera's own motion blur: shoot at 1/50 and move.
  - The gate must judge a blurred shot next to its neighbours at phone size (a 3-shot strip at 1080 px wide).
  - Check the mask edge against the subject on every frame (a halo test).
- **render_diff missed the change again.** v10c → v10d reported "no picture change" while 0–1.56 s changed (masters: mean |diff| 1.19, the rest identical). Its threshold skips a low-frequency change like a removed blur. That makes three misses on this reel → CR-20261111-could-not-go-home-diwali-render-diff-text.
