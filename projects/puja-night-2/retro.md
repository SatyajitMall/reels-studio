# Retro — written by the editor at the end of the reel

| Field | Value |
|---|---|
| Reel | puja-night-2 (Durga Puja night, second pilot) |
| Reel type | music-montage |
| Arch version | 0.5.0 at the start; 0.5.1 adopted at round 2; 0.5.3 at round 3; `verify_render.py` (0.6.0) used for the final file check |
| Rounds to approval | 6 (v1c → v2 → v3c → v4c → v5c → v6d), 17 sequence versions, 11 blind-review runs (all FAIL; rounds 1 and 3–6 hit the 2-loop limit, round 2 was superseded after 1 loop). Instagram package approved on the first try |
| Final runtime | 55.60 s on *Shondhatara* section D (1:45.6–2:41.2) · DURGA intro 3.80 s + 27 shots · avg 1.92 s · 7 baked beat transitions · v1 was 59.80 s, 14 shots, avg 4.27 s |

## What worked (keep doing)
- **Mocks before builds.** Round 5's intro went out as two 4-second renders ("inside the letters" vs "behind the letters") and round 6's transitions as one mock with the song. The director chose from renders, not descriptions, and nothing was rebuilt because of a misunderstanding.
- **A full-shoot shot pool.** `tools/shot_pool.py` (per-frame sharpness at 1080 × 1920, motion and luma for all 62 clips, ≈ 4 min) found 17 unused clips with usable moments. It made round 5's 28-shot dramatic cut possible and answered round 6's "check what you discarded" with numbers.
- **Transitions baked from the graded body.** `tools/beat_transitions.py` renders zoom-through / whip / light-leak / dip overlays from an export with the overlay track hidden, so they match the grade and land on the frame. It also replaced a Film Dissolve that burned Warp's banner, and gave a clean frame hold (C089) from the stabilised last frame.
- **Text-mask intro from the reel's own grade** (`tools/durga_intro.py`). The director's "Marvel-style DURGA" idea was built from the director's own footage, beat-timed, in one round.
- **Music section chosen by numbers + preview renders.** Round 4 compared sections A and D by level and bar energy and gave the director both to hear; switching took one round, with the whole cut re-timed to the grid.
- **Blind review on a different model.** Every one of the 11 runs found something real, including things my metrics passed: upside-down clips (C085 / C086 blockers), phones and faces, a stutter that lives in the source (C087), and a soft nest upscale (C132).
- **Top-anchored reframes instead of masks.** Scaling a 4K clip to 115–138 % and anchoring the top pushes phones, faces and shop signs into IG's bottom UI band. It's quicker and cleaner than a tracked mask (which round 4 still needed for C088).
- **Measure-then-decide on stability.** Source jitter and cadence per clip decided Warp vs. no Warp vs. a steadier stretch vs. drop. Warp on steady clips made them worse (C096 judder).
- **Facts-only Instagram copy.** Clip count, phone, camera app and times came from the metadata; no invented pandal names. Approved as written.

## Friction (from the friction log, ranked by time lost)
| # | Phase | What happened | Workaround | Time lost |
|---|---|---|---|---|
| 1 | 7b gate | 11 blind-review runs at ≈ 25–42 min each, all FAIL; five rounds ended at the loop limit with editor-verified fixes. Most majors were classes a script could catch before the reviewer (orientation, phones / faces, soft focus, stutter, tone outliers) | Fixed each, verified by numbers and stills, reported the gate status honestly | ≈ 5 h wall clock; the director noticed ("running for quite a while") |
| 2 | 5 stability | Warp analysis can't be started by script: QE-added Warp never analyses, MCP `stabilize_clip` started 7 of 25. v6 was abandoned; 18 clips needed the Analyze button; the director's clicks didn't register, the editor pressed them via screen control | Rebuilt v6b with `stabilize_clip`, then full-screen control | ≈ 75 min + 1 director round-trip |
| 3 | 1 / 7b focus | Phone night footage hunts focus; relative-sharpness selects passed clips that are soft for most of their length (C081, C089, C139) | Absolute per-frame Laplacian floor (120 on this shoot) before the EDL → `shot_pool.py` | ≈ 60 min (2 gate loops) |
| 4 | 1 / 5 orientation | ≈ 18 clips recorded upside down; I missed C087 (round 3) and C085 / C086 (round 5), all caught as blockers | Per-clip orientation from readable cues (text, ground), logged before placement | ≈ 45 min over 3 loops |
| 5 | all | Premiere sessions: two projects open, the adjustment layer took 4 rounds, an Auto-Save copy reopened after a bridge drop, an Import Files dialog hung the bridge twice, exports time out at 45 s but finish | One project open; imports alone; poll `_es_out.txt` after exports | ≈ 50 min + 6 director round-trips |
| 6 | 7b fixes | No trim-in-place recipe until round 4 (remove + re-place + re-apply everything per fix) | `trackItem.inPoint` / `outPoint` are writable; `transition.remove` works | ≈ 15 min per loop, rounds 1–3 |
| 7 | 6 round 6 | Source-level defects surfaced only in the last gate loop: C087's camera zoom steps unevenly (my jitter metric measures translation only), the nest-then-Warp recipe made C132's 128 % reframe an upscale, swapped clips kept scale 100 % | Removed C087; rebuilt C132 from 4K with Optical Flow; base scale in every placement script | ≈ 40 min (1 extra loop) |
| 8 | 3 overlays | A baked clip placed on V1 rendered transparent; same media on V2 fine | V2 overlay | ≈ 20 min |
| 9 | 0 music | The song came as a YouTube link (commercial, unlicensed for sync) | Director's own copy as a cutting guide only; IG library audio at upload; `_IG` export with the music muted | ≈ 10 min + an open rule |
| 10 | 0 | ElevenLabs key 401; no local Whisper | Chroma cross-correlation proved the reference has no voiceover | ≈ 10 min |

## Change the studio (each one becomes a CR)
| # | Change | File / section | CR id |
|---|---|---|---|
| 1 | Pre-gate checks by script (orientation sheet, phones / faces in the frame, absolute focus floor, cadence, tone vs neighbours) so the blind reviewer spends its loops on taste, not on defects; a short third "fix-verification" loop limited to changed shots | `review-gate.md`, `scripts/` | CR-20261019-puja-night-2-review-gate (new) |
| 2 | Promote beat-matched baked transitions (zoom-through, whip, light leak, warm dip) and the stabilised frame hold to a studio script; rule: bake from the graded body with the overlay track hidden, re-bake any overlay that touches a changed shot | `scripts/`, `effects-playbook.md` §D | CR-20261019-puja-night-2-beat-transitions (new) |
| 3 | Warp: Analyze can't be scripted (plan a click pass), banner check before export, no reframing a nest above 100 %, Optical Flow by QE `setTimeInterpolationType(2)`, base scale after `overwriteClip`, trim-in-place recipe | `premiere-mcp-reality.md` | CR-20261018-puja-night-2-extendscript-notes (items 1–29) |
| 4 | Full-shoot shot pool with an absolute focus floor; streak-smear guard; cadence per shot | `scripts/selects_score.py` / `frame_scan.py`, skill Phase 1 | CR-20261018-puja-night-2-focus-qa |
| 5 | Orientation decided per clip from readable cues and logged before placement; `shake_report.py` ffprobe crash; `link_footage.sh` skip pattern; beat analyser candidate cuts by energy only | `scripts/`, skill Phase 1 | CR-20261018-puja-night-2-script-bugs |
| 6 | One Premiere project per reel session; Auto-Save recovery; imports in their own call; export timeouts | skill Phase 1, `premiere-mcp-reality.md` | CR-20261018-puja-night-2-premiere-session-setup |
| 7 | A route for commercial songs added from IG's library at upload (guide copy, `_IG` export, start timecode in the package) | CLAUDE.md §4c | CR-20261018-puja-night-2-commercial-music-ig |
| 8 | Text-mask intro, tracked phone mask, tracked text-behind; ProRes alpha 0.97 renders ≈ 0.87 | `motion-and-ai.md`, `scripts/` | CR-20261018-puja-night-2-motion-ai |

## Director's notes pattern
What the director asked for in more than one round. These are likely candidates for new defaults.
- **Stability, twice** (round 2: "C099 jerks, stabilise it"; round 6: "pan out and pan in … are jumpy"). The studio default already says stabilise moving handheld shots; I skipped it in v5. Measure every moving shot before the first cut, not after notes.
- **Distractions in the frame** (round 2: C090 bald head and phone; gate rounds 3–6: phones, faces, a shop awning). Screen every shot for phones / faces / signage before the EDL; prefer the top-anchored reframe.
- **One tone** (round 2: "desaturate the red a little", "push the chandelier to gold"; round 6: "all shots need cinematic tone"). Match every shot to its neighbours by numbers (luma, warmth, saturation), not only to the montage median.
- **Drama follows the music** (round 4: "slower, longer holds", then round 5: "a slideshow, not cinematic cuts; the music is dramatic, the cuts aren't"). A calm brief on a dramatic song reads as a slideshow: flashes on hits, hero holds on the peaks, designed transitions on section changes. Now in the `cinematic-montage` playbook (0.6.0).
- **Visible craft from the director's own footage** (round 3 text-behind, round 5 Marvel-style intro, round 6 beat transitions). The director wants designed moments, as long as they're built from the shoot, never stock.

## Tool reality check
Premiere MCP tools that failed, behaved unexpectedly or needed a different name than the docs say.
- QE `addVideoEffect("Warp Stabilizer")` never starts analysis; MCP `stabilize_clip` started it on 7 of 25 clips. Warp property 31: 201 = not analysed, 408 / 708 = analysed. Smoothness set by script (100) can leave a permanent "extreme cropping" error frame.
- MCP `set_time_interpolation` only calls QE `setFrameBlend(bool)`. QE `trackItem.setTimeInterpolationType(2)` sets Optical Flow (readback 2). The DOM TrackItem has no interpolation call.
- `speed_change` keeps the clip's timeline duration and stretches the source range (1.5× on 2.52 s → source 0.12–3.90); `inPoint` / `outPoint` then read back speed-scaled.
- `track.overwriteClip` places 4K clips at scale 100 % in a 1080 × 1920 sequence.
- `add_track {position: "below"}` inserts at index 0 and renumbers the audio tracks.
- `exportAsMediaDirect` through the bridge times out at 45 s or reports "bridge not running" but finishes; poll the result file.
- `app.project.importFiles` inside a larger script can open the Import Files dialog and hang the bridge.
- `trackItem.inPoint` / `outPoint` are writable; DOM `transition.remove(false, false)` works.
- ExtendScript `File.write` writes 0 bytes with non-ASCII text unless `encoding = "UTF-8"`.
- `color_correct` also writes temp / tint into Lumetri's HSL Secondary (idx 101 / 102).
- `export_frame` needs a `.png` path and an existing folder.
- Premiere composites a ProRes 4444 pixel with alpha 0.97 at ≈ 0.87.
