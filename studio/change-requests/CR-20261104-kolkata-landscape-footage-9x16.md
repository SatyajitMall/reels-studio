# CR-20261104-kolkata-landscape-footage-9x16

| Field | Value |
|---|---|
| From reel | `projects/kolkata/` |
| Arch version | 0.9.0 |
| Type | rule · script |
| Severity | workaround |
| Status | partly done (v0.9.1) |

## What happened
- **KOLKATA2026 was shot mostly with the phone held landscape**, but Blackmagic Cam tagged every file the same way: 3840×2160 with display rotation −90, so all 101 clips show as 2160×3840 portrait. 57 of the 84 usable clips are landscape pictures lying on their side: 46 need Premiere Rotation −90 and 11 need +90. 3 are upside down (180°). Nothing in the file says which.
- `ingest_report.py` reports `rotation = -90` for all 101 and can't tell them apart. `analyze_footage.py`'s overview sheets show them sideways, and the skill says orientation "isn't detected automatically". Sorting 101 clips by eye from the sideways overview wasn't reliable. Edge-brightness ("sky is on top") guessing was too weak.
- **CLAUDE.md §3 (V1) and effects-playbook §B require ≥ 80 % of the camera width in 9:16** (Scale ≤ 62.5 on vertical 4K). That assumes vertical footage. A landscape shot full-bleed in 9:16 keeps 32 % of the width, so the rule can't be met without bars.
- `look_preview.py` squashes a portrait still into the first still's landscape tile when portrait and landscape stills are mixed (C100 on the kolkata sheet).

## Workaround used in the reel
- A both-rotations sheet in the scratchpad: each sideways clip's mid-frame turned +90° and −90°, side by side. I picked the upright one by eye, about 2 minutes for 70 clips. The result is `projects/kolkata/analysis/orientation.json` (lists per rotation + unusable clips with reasons).
- **Framing:** the director was shown A full-bleed (32 % width) · B 16:9 film frame (100 %) · C 4:5 window (45 %) on their own stills with the IG UI bands (`projects/kolkata/analysis/framing/framing_sheet.jpg`). They picked **C, a 1080×1350 window centred in the safe area (y ≈ 910)** for every shot, vertical clips included. Recorded as a brief override of the 80 % rule.

## Proposed change
1. `scripts/ingest_report.py` (or `analyze_footage.py --orientation`): a both-rotation contact sheet for every clip (as is · +90 · −90 · 180), plus an `orientation.json` the editor fills in. Optionally a horizon or face detector could pre-pick the rotation.
2. CLAUDE.md §3 V1 and effects-playbook §B: add "landscape-held footage: choose with the director between full-bleed (states the % of width kept), a 16:9 film frame, or a 4:5 window". Then the 80 % rule reads "of the camera width, for vertical footage".
3. `studio/shooting-guide-blackmagic-cam.md`: if Blackmagic Cam's orientation lock is on, landscape shots record as rotated portrait. Ask the director to unlock it, or note it on the slate.
4. `scripts/look_preview.py`: keep each still's own aspect per row (pad, don't stretch).
5. `scripts/storyboard.py` / `preview_edl.py`: support a windowed frame (a framing `window: [w, h, y_centre]` key in the EDL) so the 4:5 window shows in previews. Workaround in use: a full-frame matte PNG as an overlay (`projects/kolkata/renders/overlays/window_matte.png`). Both scripts handle `rotation` correctly.
6. **`scripts/camera_fidelity.py` (and so `pregate.py`) ignore the EDL's `rotation` and the window.** On kolkata p1 every shot FAILs:
   - the window's black bars (29.7 % of the frame) read as "crushed 29.5 % vs 0.1 %" and drag the luma down 0.1–0.26;
   - the "camera at the render's framing" column searches the **unrotated** camera frame, so hue, match and width are wrong. C061 hue reads −72°, C007 reads +36°, C030 finds no framing at all. The render itself is correct (checked on the fidelity sheet and the storyboard).

   Proposed:
   - apply `rotation` before the framing search;
   - take an `--window x,y,w,h` (or read the EDL `window` key) and measure inside it only. `--exclude-band` takes one band; a window needs two.

   Until then, the kolkata pregate is judged on `verify_render` + `frame_scan` + the fidelity sheet by eye, noted in its `project.md`.
7. **Orientation picked by eye on mid-frames got 4 of 101 clips wrong** (found in round 3, after the director's note "they can be upside down or ill-oriented, make sure they are fixed and used").
   - C017, C018 and C025 were labelled portrait but display sideways.
   - C109 was marked unusable ("railing blur") when it was only sideways; it has two clean windows of one of the best frames in the shoot.
   - Workaround: every clip rendered upright at its best steady moment (selects windows + motion holds), in the reel's framing window, on one sheet (`projects/kolkata/analysis/pool_v3/`). Wrong ones stand out at once.
   - Proposed: `ingest_report.py` or `analyze_footage.py` writes that sheet, and Phase 1 orientation is confirmed on it rather than on mid-frames. An "unusable" verdict is re-checked against the clip's best window, not its middle.

8. **How to get the upright camera frame on this footage** (from the v3c_M1 reviewer, who rebuilt the camera check by hand):
   - the files carry a portrait display matrix, which ffmpeg honours by default, and the EDL's `rotation −90` cancels it;
   - so the upright picture of a −90 clip is the raw 3840×2160 frame decoded with `-noautorotate`;
   - a true portrait (e.g. Oct21:C035) is the auto-rotated frame at 50 %.

   Item 6's fix in `camera_fidelity.py` should decode this way. With that and the window rows (235–1584), the reviewer's crops matched the export at ncc 0.87–0.99.

## HQ decision (v0.9.1, 2026-11-08)
- **(2) Done.** The 80 % width rule now reads "for vertical footage" (CLAUDE.md §3 V1, effects-playbook §B, SKILL Phase 3). Landscape footage takes the framing the director picks in the brief: A full-bleed (state the % kept), B a 16:9 film frame, C a 4:5 window.
- **(3) Done.** Shooting guide: a "Holding the phone landscape" row (avoid it; check the orientation lock is off, or note "landscape" on the slate). The lock is the likely cause, not a confirmed one.
- **(4) Done.** `look_preview.py` keeps each still's own aspect per row (tested: a landscape row 152 px and a portrait row 480 px on one sheet).
- **(7) Done as a rule.** SKILL Phase 1: confirm rotation on frames turned both ways at each clip's best steady moment, record it in `analysis/orientation.json`, and re-check "unusable" clips at their best window. Director profile notes the KOLKATA2026 tagging.
- **(1, 5, 6, 8) Accepted for v0.12:** the upright orientation sheet in the analysers, an EDL `window` key in `preview_edl.py` / `storyboard.py`, and `camera_fidelity.py` decoding the upright frame (`-noautorotate` for a −90 clip, per item 8) and measuring inside the window.
