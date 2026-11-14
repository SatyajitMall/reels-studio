# CR-20261018-puja-night-2-motion-ai

| Field | Value |
|---|---|
| From reel | `projects/puja-night-2/` |
| Arch version | 0.5.3 |
| Type | script · skill (motion-and-ai.md) |
| Severity | workaround |
| Status | open |

## What happened (first real use of v0.5.1–0.5.3 features in a reel)
1. **HyperFrames alpha MOV → Premiere: verified ✅** (was "not yet verified" in `motion-and-ai.md` §1). ProRes 4444 `yuva444p12le`, 25 fps, imported with `app.project.importFiles`, placed on V5 with `overwriteClip`; transparency composites correctly over the graded picture (stills + export). Footage interpretation reads `alphaUsage 0` but the alpha is honoured. Render time ≈ 7 s for 3.4–3.7 s at 1080×1920.
2. **Text behind the subject on a non-static hold.** `text_behind.py` fixes the word to the screen. C095's "hold" drifts up to ~60 px/s (shake_report pan), so the word would slide against her head. Stills test (≈ 0.7 s/frame with `remove-background` on a PNG) worked well for choosing the shot: C095 ✅, C083 ⚠️ (face matte collapses after 2 s as the camera moves in), C089 ❌ (wide, mush), C139 ❌ (ornate close-up).
3. **Baked clip on V1 rendered transparent.** After trimming C095 on V1 (`trackItem.end`) and placing the baked clip in the freed slot, Premiere rendered nothing there (stills, QE `exportFramePNG` and a real export all showed only the V4 grain over black, mean 127). Same media on V2 rendered fine; re-placing fresh on V1, relinking to H.264 and removing effects didn't help. Cause unknown.
4. ffmpeg `prores_ks` ProRes 422 HQ from `text_behind.py` was suspected but ruled out (H.264 relink behaved the same); kept H.264 (`crf 8`, BT.709 tags) as the placed media anyway.

## Workaround used in the reel
- **Tracked bake:** reel-local `projects/puja-night-2/tools/text_behind_tracked.py` — anchors the word every frame to the subject's own matte (top of the subject + centre of its upper 300 px, 7-frame smoothing), fades the word in and out inside the bake, dark halo option. C095: subject top moved 732–876 px across 69 frames; word rides with her; `frame_scan` 0 flags.
- **Placement:** baked clip on **V2 over the untouched V1 shot** (same source frames underneath), graded with the same Lumetri values as the V1 clip, ending exactly when the word has faded out (so the V1 dissolve stays visible). No V1 surgery.

## Proposed change
1. `scripts/text_behind.py`: add `--track` (anchor to the matte per frame, smoothed) and `--fade-in/--fade-out`; add `--halo` colour (dark halo for calm reels). The reel-local tool is a working draft.
2. `motion-and-ai.md` §2: placement recipe = **V2 overlay over the original shot**, not a V1 replacement; grade it with the same Lumetri values; end it when the word is gone. Mark §1's Premiere alpha import as verified.
3. Add the stills-first shot test (as above) to §2 "How", with the per-shot results table extended.
4. Reality doc: note the V1 "transparent clip after `trackItem.end` trim + overwrite" symptom so the next session doesn't lose 20 min on codec theories.

## Follow-up (round 4, v4c): tracked phone-screen mask
- **What happened:** lit phone screens held up in the crowd (C088, the closing shot) were flagged in two gate loops. Cropping would cut the deities. v4b's static soft PNG on V2 with a 12-frame dissolve-in missed the screens for ~1.5 s (they drift with the camera pan and the hands), and a soft spot over a phone next to Ganesh punched a dark hole into the figure.
- **Workaround:** reel-local `projects/puja-night-2/tools/phone_mask_tracked.py`, ≈ 50 s for 134 frames:
  1. Decode the source range at the reel scale.
  2. Estimate the camera pan by phase correlation on the backdrop.
  3. Detect screens as cool-white pixels against the warm tungsten scene (Y > 55, B > 0.8 R) in a region of interest.
  4. Track each seeded phone (big screens follow their last detection; small ones use the pan as prediction).
  5. Render a 1080×1920 ProRes 4444 alpha overlay in reel space, applying the clip's Motion (scale keys).
  - Shape per phone: a tracked box where the phone is in front of dark crowd; the convex hull of the largest glass blob where it's next to bright set/stage (boxes and multi-blob hulls darkened the backdrop).
  - Black at full opacity, ramped with the cross-dissolve into the shot.
  - Rejected: inpainting the tiny screens (read as a soft smudge on the stage).
  - Verified in the export: screen luma under the mask p95 100–168 → 6–7.
- **Proposed change:**
  - `scripts/phone_mask.py` (or a `--track` mode in a studio masking tool) with this pipeline. Seeds come from a `--seeds` JSON (box per phone, `box|hull`) after a detection preview sheet.
  - A `motion-and-ai.md` section "Distracting lights / screens in a crowd": prefer this over cropping when the crop would cut the subject.
  - Note that Premiere under-applies partial alpha from ffmpeg ProRes 4444 (0.97 → ≈ 0.87), so mask cores should be 1.0.

## Follow-up (round 5): text-mask intro ("footage inside the letters")
- **What happened:** the director asked for a Marvel-style intro: the word DURGA with the reel's footage inside the letters. The studio has no text-mask title tool.
- **Workaround:** reel-local `projects/puja-night-2/tools/durga_intro.py`.
  - Modes: `fill` (footage inside the letters, pull-back 3.6× → 1×) and `behind` (solid letters landing one per beat over the footage).
  - Flips are beat-timed, then every half beat; subtitle under the word; white flash on the slam.
  - Tall letters: Impact stretched to 980 × 640 px, because a normal-proportion word is only ~170 px tall on 9:16.
  - Footage is sampled from the reel's graded render and placed above the look (V5), so the grade matches without double grading.
  - The director chose between 4.6 s previews of both modes with the song.
- **Proposed change:** a studio `scripts/text_mask_intro.py` (or a HyperFrames composition using an SVG text clip-path over video) taking a word, beat times and source picks. Add a motion-and-ai.md section: "for 9:16, stretch the word tall; a 16:9 Marvel layout reads as a thin strip on a phone".
