# Retro — written by the editor at the end of the reel

| Field | Value |
|---|---|
| Reel | uski-aankhein ("Uski Aankhein / if her eyes were music"), pilot |
| Reel type | music-montage, playbook cinematic-montage (soundtrack: the reference reel's audio, IG audio added at upload) |
| Arch version | 0.6.0 at the start (studio is at 0.7.1 at the end) |
| Rounds to approval | 5 director rounds to approval, then a 6th after the iPhone check (v10/v10b, 2026-10-29), 2026-10-20 → 10-28 (Checkpoint 2 on v1c, v2c, v3b, the v5 preview, v9c). 8 blind review-gate runs (v1, v1b, v2, v2b, v3, v3b, v9, v9b); the last one passed |
| Final runtime | 22.0 s (550 frames at 25 fps), 3 shots, 2 blink transitions |

## What worked (keep doing)
- **Baking V1 outside Premiere.** Eye-lock, pushes, blinks, AI upscale, deflicker and clarity were all done in Python/ffmpeg. Premiere only held the look, grain, type and mix. The Premiere export matched the local preview at 1.8–1.9 % median frame difference every round, so previews were a reliable stand-in for approvals.
- **The blind review gate on a second model.** Every run found something real that my own number QA had passed:
  - eye-lines 30–200 px off;
  - a shrine in the IG bottom zone;
  - the double-exposure veil and the esraj neck between her eyes;
  - the AI-drawn nath;
  - regional flicker at ~1.5 %.
- **Measuring the reference frame by frame.** Once the director pointed at it, per-frame luma plus a strip showed the reference's only transitions are two 6-frame blinks. That took 10 minutes, after three rounds of guessing.
- **Real-ESRGAN with a denoise first, one AI still under a push for static idols.** This cleared "very bad image quality" without the shimmer that per-frame AI gave (v7).
- **Path-guarded ExtendScript.** Every script checks `app.project.path` and calls `openSequence` first. Premiere was shared with other reel sessions for the whole pilot, with no damage to another project.
- **Cloning the sequence carries the hand-loaded `.cube`.** v9b and v9c needed no second on-screen look load.
- **A designed cover sheet** (4 options plus the grid crop) settled "Use a better cover" in one question.

## Friction (from the friction log, ranked by time lost)
| # | Phase | What happened | Workaround | Time lost |
|---|---|---|---|---|
| 0 | 9 | **After approval, the director found the file "very poor" on the iPhone** (soft, plastic faces, blocky darks). Every check had been made at 2 fps / Mac size. The causes were the AI upscale + strong denoise on 1.65–2.5× enlargements, and Premiere's H.264 preset (Main, 9.5 Mb/s). | Real-frame stacks (2× shift-and-add for B), framing ≤ 1.42×, ProRes master + x264 High; review loop 1 caught B still soft | ~3 h, plus a round after approval (CR items 30–31) |
| 1 | 2–5 | Each note was executed literally (more footage, one place, minimal idols, tighter, eyes as the subject). The sum drifted from the reference's calm two-shot idea. Image quality fell below the source's limits (2.4–3.4× crops), until the director called v5 "very off from the concept". | Re-brief to the reference's structure; AI upscaler; enlargement limits | ~2 rounds (v2–v5) |
| 2 | 1–4 | `teardown.py` reports cut counts, not transition types. I designed dissolves, eye-match dissolves and a ghost for three rounds before the director said "look at the reference video to understand the transitions". | Per-frame luma + strip found the blink | ~3 rounds of transition notes |
| 3 | 1, 4 | Survey of 262 clips over 5 shoots, with no shared index and no place grouping ("one house" was three houses). | Background-agent surveys (~34 + ~33 min) | ~70 min + "too many places" notes |
| 4 | 7 | Review v1: the eye-lock pinned hand-estimated eye points, 30–200 px off; review v2: an `eye_ref` outside the slot was clamped silently. | Measured pupils; tracker fix | ~45 + ~20 min |
| 5 | 2 | No licensable footage of the reference's esraj player; reverse image search needed a JS file injection. | AI-generated esraj (director-approved, $0.52) | ~40 min |
| 6 | 3, 5 | Custom `.cube` loads: the director's manual load landed in another project. Computer use needed full-screen approval, a Finder grant, and the keyboard in the XPC Open panel. | Screen control after selecting the clip by script | ~25 min + a near-miss on pujo |
| 7 | 7 | v9's full-frame Screen double exposure veiled shot A (p10 0.20 vs 0.07), and the neck sat between her eyes. | Placed / weighted / de-veiled ghost + level match (`bake_r9b.py`) | ~40 min |
| 8 | 5, 7 | Per-frame AI + motion interpolation shimmered (v7). AI drew the nath as blobs and gave the silver a waxy texture (v9). | One AI still + push; AI 55 % / 20 % on jewellery | ~1 round + ~20 min |
| 9 | 3, 7 | Bake bugs: a hard-coded last shot, manifests keyed by file name, a `setdefault` chain left `ey` unset, minterpolate dropped end frames. | Fixed in the reel's bakers | ~30 min of re-bakes |
| 10 | 7 | A global deflicker left ~1.2–1.6 % anti-phase flicker on the clay face's cheeks. | Regional gain field (`bake_r9c.py`) | ~20 min |
| 11 | 1 | Small tool gaps: `teardown --ours`, the beat analyser can't read .mp4, no `drawtext`, no `cv2`, `verify_render --fix-loudness` skips true-peak-only fails. | Local workarounds | ~20 min total |

## Change the studio (each one becomes a CR)
| # | Change | File / section | CR id |
|---|---|---|---|
| 1 | Footage location, clip-id collisions across shoots, stock as a default not a ban, reference audio as the director's habit; a per-round "concept anchor" check | `studio/director-profile.md`, skill Phase 6 | CR-20261020-uski-aankhein-director-profile |
| 2 | One open project per reel, or path-guarded scripts; manual LUT steps start by selecting the V3 clip; a shared `_es_guard.jsx`; the `refreshMedia()` caveat; computer use as the `.cube` fallback | reality doc, skill Phases 1/4, `scripts/` | CR-20261021-uski-aankhein-multi-project-premiere |
| 3 | 29 script and tool items. Highlights:<ul><li>teardown should classify transitions (18);</li><li>the survey should group by place (19);</li><li>a reframe/eye-lock tool with measured eye points (4, 11, 16, 21);</li><li>an enlargement cap (22);</li><li>adopt Real-ESRGAN (23) with blend defaults (28);</li><li>regional deflicker (26);</li><li>a double-exposure recipe (27);</li><li>a subject-vs-IG-UI check (17);</li><li>designed covers by default (29);</li><li>`verify_render` true-peak fix (10);</li><li>previz range tags (24);</li><li>custom-look loading (25).</li></ul> | `scripts/`, skill, playbooks, `motion-and-ai.md` | CR-20261020-uski-aankhein-script-gaps |
| — | Shared survey index across shoots | `scripts/`, `studio/` | CR-20261019-pujo-ki-asolei-sobar-pool-survey (already filed) |
| — | Reference grade match | `scripts/` | CR-20261020-pujo-ki-asolei-sobar-reference-grade-match (already filed) |

## Director's notes pattern
What the director asked for in more than one round. These are likely candidates for new defaults.
- **The director judges on the phone.** "Very poor quality" came after approval, from the AirDrop copy. Default: check at 100 % before every checkpoint, and make the delivery encode from a ProRes master.
- **"Like the reference", literally** (rounds 1, 3, 4, 5): the same structure, the same transition language (here a blink), the same calm pace. Default: measure the reference's transitions and structure in Phase 1, and treat the reference as a concept anchor each round.
- **Image quality and stability** (rounds 1, 5, 5c): "unstable", "very bad image quality", "stabilisation and video enhancement", "light flickering". The director sees softness, jitter and flicker on a phone. Defaults: an enlargement cap, a denoise before any enlargement, a stability and flicker check before every preview.
- **Cinematic colour** (rounds 1, 2, 5c): warm gold with deep shadows ("Gold & Shadow", then "Rich and deep"). Default: start from the G2 family for night puja footage.
- **Fewer, stronger subjects** (rounds 3, 4, 5b): "too many places", "minimal idols", then "one idol per shot". Default: few shots, each held longer, one subject per shot.
- **A designed cover** (Checkpoint 3 here and on pujo-ki-asolei-sobar): a frame grab isn't enough.

## Tool reality check
Premiere MCP tools that failed, behaved unexpectedly or needed a different name than the docs say.
- Lumetri Look can't be set by script: `properties[34].setValue(path)` throws `Illegal Parameter type`. `add_adjustment_layer` and `apply_lut` are broken, as the reality doc says.
- `app.project` and QE follow whichever open project's sequence was last in front, and it flipped between calls with 3 projects open.
- `execute_extendscript` returns `"undefined"` for `$.evalFile` scripts: always write results to `analysis/_es_out.txt` and read the file.
- Calls that worked:
  - `seq.clone()` creates `"<name> Copy"`; rename it, then `P.openSequence(id)`. The clone keeps the V3 Lumetri with its custom `.cube`.
  - `seq.exportAsMediaDirect(path, "Match Source - H.264 High Bitrate.epr", ENCODE_IN_TO_OUT)` (in/out set to 0–22.0 s), with A3 mute toggled for the `_IG` copy.
  - Motion `Position.setValue([0.5, 0.375], true)` moved the V5 end card up 240 px; verified by render.
- `projectItem.refreshMedia()` on a re-rendered Screen overlay rendered it wrong (V1 refresh was fine): re-import under a new name instead.
- Computer use: Premiere's own full-screen Space blocks background clicks. The macOS Open panel (XPC) can't be clicked, but the keyboard works.
