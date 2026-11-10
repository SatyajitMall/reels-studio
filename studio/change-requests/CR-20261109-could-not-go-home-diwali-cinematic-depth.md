# CR-20261109-could-not-go-home-diwali-cinematic-depth

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.9.1 |
| Type | script · rule |
| Severity | workaround |
| Status | done (v0.9.2) |

## What happened
The director shot the whole Diwali pool (18 of 19 clips) in **Blackmagic Cam's Cinematic mode** on the iPhone 17 (f/2, 26 mm Main, 25 fps, 1/50). Their aim was the shallow depth of field. The files are Apple **Cinematic Video**:
- format tag `com.apple.quicktime.cinematic-video-intent=1`;
- besides the HEVC picture, a disparity track (`dish`, handler "Core Media Auxiliary Picture") and two focus-metadata tracks (`mebx`);
- the f-number (here f/2) is a rendering setting, not baked in.

**The blur only exists when an Apple framework renders it at playback** (Photos, iMovie, Final Cut). Premiere, ffmpeg and every studio script read the stored picture, which is sharp front to back. The director noticed this and raised it with HQ as "a problem" with the footage.

Nothing in the studio detects it:
- `ingest_report.py` reports codec, fps, white balance and so on, but not the cinematic intent or the disparity track;
- `analyze_footage.py`, `preview_edl.py`, `look_preview.py` and Premiere all show the sharp picture.

## Workaround used in the reel
Reel-local `projects/could-not-go-home-diwali/tools/cine_bake.swift` (compiled with the Command Line Tools: `swiftc -O -o tools/cine_bake tools/cine_bake.swift`). It uses Apple's **Cinematic framework** (macOS 14+):
- reads the video, disparity and metadata tracks with `AVAssetReader`;
- builds `CNRenderingSession.FrameAttributes(sampleBuffer:)` from each metadata sample, which carries the recorded focus decisions and f-number (`--fnumber` overrides it);
- renders with `CNRenderingSession.encodeRender(... destinationImage:)` at `.export` quality;
- writes ProRes 422 HQ, BT.709-tagged, with the **source's rotation tag kept**, so the output drops in for the camera file (same size, fps, timing and orientation).

Verified on C050 / C054 / C062 / C047 / C063 (`analysis/cinematic/depth_sheet.jpg`): background and far planes soften, subjects stay sharp, no visible edge halos at review size. Speed: about 1 s per second of 4K footage on this Mac. Size: ~88 MB/s (ProRes HQ 4K), so the tool runs per shot on the shortlist with handles, not on the whole card.

The director chose "bake f/2 as shot" and left per-shot depth calls to the editor.

### Later in the reel: focus pulls and f/1.4 (2026-11-09)
- `cine_bake --rack` can pull focus between two screen regions (median disparity per frame), or end on the camera's recorded focus (a width-0 rect, for a moving subject). It works technically.
- **The director rejected it:** on p1b, the three pulls (at f/1.4) read as "in and out focus".
- The **recorded** focus is steady on every clip measured (range ≤ 0.11 in a shot), so a plain bake at the shot's f-number doesn't pump.
- Hands and tools moving through the focal plane at f/2 shimmer once slow motion interpolates them. f/2.8 on those shots.

## Proposed change
1. **`scripts/cine_bake.swift`** (+ a build line in `setup.sh`): promote the reel tool. Add `--start/--dur` handles from an EDL, `--audio` passthrough, and a batch mode that reads `analysis/edl_v<N>.json` and writes `raw/baked/<clip>_f<N>.mov`.
2. **`ingest_report.py`:** flag `cinematic` when `com.apple.quicktime.cinematic-video-intent=1` or a `dish` track is present, with the recorded f-number, and say "depth is not in the picture: bake with cine_bake before previews, look sheets and Premiere".
3. **Skill Phase 1 step 3 / CLAUDE.md §5:** one line saying Cinematic-mode clips are baked before anything else reads them. `preview_edl.py` and the Premiere build then point at the baked files, and `camera_fidelity.py` compares against the baked frames (the director's intended picture).
4. **`studio/shooting-guide-blackmagic-cam.md`:** note that Cinematic mode is fine (the depth is recoverable), records 8-bit HEVC, and that the f-number can be changed after the shoot.
5. **Effects playbook:** focus pulls from Cinematic depth only when the director asks for them; default to the recorded focus.
6. **Director profile → Camera:** "Shoots Blackmagic Cam Cinematic mode at f/2–3.8, 26–56 mm, for depth (Diwali, 2026-11-09)."

## HQ decision
**v0.9.2, 2026-11-10: done**, with the director's go-ahead ("Promote now").

| # | Proposed | Done |
|---|---|---|
| 1 | `scripts/cine_bake.swift` + `setup.sh` build line, handles, `--audio`, EDL batch mode | ✅ `scripts/cine_bake.swift` (built to `scripts/bin/cine_bake`) and `scripts/cine_bake.py --edl / --check`. Batch writes `raw/baked/<camera stem>_f<F>_<start>-<end>.mov`, `bake_map_<edl>.json` and `<edl>_baked.json`. Fixed on the way: `--audio` hung (0-byte file) because sound was read after all the video, and `--start` now snaps to the camera frame |
| 2 | `ingest_report.py` `cinematic` flag with the f-number | ✅ flag plus advice; aperture in the Lens column |
| 3 | Skill Phase 1 / CLAUDE.md §5 line; previews, Premiere and `camera_fidelity.py` on the bakes | ✅ via `edl_v<N>_baked.json`, which every downstream tool already reads, so no tool changes |
| 4 | Shooting-guide note | ✅ Cinematic mode row |
| 5 | Playbook: focus pulls only when asked | ✅ effects-playbook §B (plus f/2.8 for slowed hands and tools) |
| 6 | Director profile → Camera | ✅ |

The reel keeps `tools/cine_bake` (same rendering) and can switch to `scripts/cine_bake.py` at its next bake.
