# CR-20261108-kolkata-footage-catalogue

| Field | Value |
|---|---|
| From reel | `projects/kolkata/` |
| Arch version | 0.9.0 |
| Type | script · skill |
| Severity | workaround |
| Status | partly done (v0.9.1) |

## What happened
On v6c the director (2026-11-08) asked for shots by content, from memory:
- "the tram line video or the bus depot video that I have";
- "the bus stop that I have captured";
- "the picture where people are dancing on the streets during bhashan".

The director's footage is shared across reels:
- Pujo, Oct 15–21: about 800 clips in `~/Documents/Video /`, used by five reels;
- KOLKATA2026: 101 clips.

No catalogue says what is in each clip, so I had to search for them:
- grepped five reels' notes (`repick_v2/*.md`, `PICKS.md`, `rounds.md`), which use different words ("Bhashan", "immersion", "Dashami", "procession");
- re-read the goddess reel's `survey_oct21_*.jpg` sheets;
- built new contact sheets for 30 candidates.

This took about 35 minutes for three lookups. "Dancing on the streets during bhashan" was never written down for any clip. The candidates turned out to be:
- C035, the women dancing at the ghat, already in this reel;
- C047 25–27 s, a woman dancing by the dhakis: 7.6 px jitter even locked;
- C025, men hauling Ma up the steps: this looks like dancing at 2 fps but isn't.

Two script problems got in the way:
- **`scripts/shake_report.py` still crashes** on the camera's rotation-tagged files:
  - `ValueError: could not convert string to float: '7319,'` in `fps_of` (line 40);
  - this is the bug already filed in CR-20261107-kolkata-preview-fx;
  - it cost a proxy transcode of 16 clips before measuring.
- **Phase correlation measures subject motion as shake.** A big subject crossing the frame reads as camera movement:
  - a bus driving at a locked camera measured 13.9 px;
  - the dancer measured 10–17 px.

  Both needed a by-eye check of the background.

## Workaround used in the reel
- `analysis/round6d_bus_tram_pool.jpg` and `analysis/round6d_options.jpg`: labelled frames per candidate, through the 4:5 window. Each candidate got its shake measured on an upright H.264 proxy (`ffmpeg -vf scale=540:-2`, which drops the rotation side data).
- The picks were made by eye on the background, not by the jitter number, where a big subject moves.

## Proposed change
1. **`scripts/footage_catalogue.py`** writes `studio/footage/<shoot>.md` (one row per clip, shared by every reel), built once per shoot. Each row has:
   - shoot date and time, GPS place (reverse-geocoded name), fps, duration, orientation;
   - a one-line content description;
   - 3 thumbnails;
   - steady windows (from `motion_holds.py`);
   - tags: subject / event / people / vehicle / landmark.

   The descriptions come from a vision pass over the overview sheets: the editor writes them once, and reels add to them.
2. **Skill Phase 1:** read `studio/footage/` before searching a pool, and add the reel's own findings (for example "C025 = hauling, not dancing") back into it. Reel sessions may write to `studio/footage/` (append-only), like `studio/ledger/`.
3. **`shake_report.py`:**
   - fix `fps_of` (`avg_frame_rate.split(",")[0]`), as already proposed;
   - add `--background top|edges`: track only the top band or the four edge strips, so a big moving subject doesn't count as shake;
   - print a warning when the quadrants disagree by more than 3×.

4. **`scripts/ae_roundtrip.py` `time_remap`: add Pixel Motion.**
   - **The gap:** the op re-times by frame repeats only. A 100 → 40 % ramp (KOLKATA's dhakis) would stutter at 40 %, so the build had to use the reel-local ffmpeg-minterpolate pre-render at 1080×1920.
   - **The fix:** set `layer.frameBlendingType = FrameBlendingType.PIXEL_MOTION` and `comp.frameBlending = true` when the op asks for `"blend": "pixel"`, or use Timewarp's "Source Frame" mode with keys.
5. **Premiere builds: a shared "place, read back, correct" helper.**
   - **The gap:** in the v6 build, `setInPoint(T(frames))` + `overwriteClip` landed 1 frame early on 2 of 26 video clips (C082, C089) and on the tram-bell MP3. KOLKATA v2/v3 had the same on a WAV.
   - **Workaround:** each reel's build script reads `trackItem.inPoint` back and corrects it (`trackItem.inPoint = T(want)`, then re-sets start/end).
   - **The fix:** one studio snippet in `premiere-mcp-reality.md` (or a script helper) would stop every build from rediscovering this.

## HQ decision (v0.9.1, 2026-11-08)
- **(3, the crash) Done** with the shared `fps_of` (see CR film-emulation-first-use).
- **(4) Done.** `ae_roundtrip.py` `time_remap` takes `"blend": "pixel"` (or `"mix"`). The blending has to sit on the footage layer inside the nested source comp: on the outer layer alone, a 100 → 40 % ramp rendered 21 of 37 slow frames as exact repeats; with it inside, 0 of 37 (tested on a kolkata clip in `projects/_hqtest/`).
- **(5) Done.** Reality doc: a row for the 1-frame-early `setInPoint` + `overwriteClip`, and the in-point read-back snippet from `projects/kolkata/tools/swap_v7.py`. Batch C's ExtendScript library will carry it as a function.
- **(1, 2) Need the director's decision** (reel sessions appending to a shared `studio/footage/`, an ARCHITECTURE change); planned for v0.12 if approved.
- **(3, `--background`) Accepted for v0.12.**
