# CR-20261024-pujo-ki-asolei-sobar-skin-qa

| Field | Value |
|---|---|
| From reel | `projects/pujo-ki-asolei-sobar/` |
| Arch version | 0.5.3 |
| Type | script (colour_report.py) · skill (colour phase, playbook §A2) |
| Severity | workaround (skin was judged "not on point" by the director in round 5; two later rounds hit skin side-effects) |
| Status | open |

## What happened
1. **Round 5:** colour QA measured only neutrals and global stats. Skin tone, which is what viewers judge, wasn't measured until the director's 5th colour note ("colour corrections still not on point"). The faces sat at hue 23–40° across shots.
2. A colour-only skin mask (a YCbCr box) also catches warm objects: a yellow shirt, orange walls, pink cloth, jars. So the measurement and the correction both went to the wrong pixels.
3. **Round 10:** skin protection by hue alone also protected orange and pink walls (they sit in the 10–45° skin band). Two rounds of cast trims never reached them, and two blind reviews flagged warm / cool alternation between shots.
4. **Round 12:** fixing one face (a pink jewellery bounce, 16.7°) with `skin_post.py`'s global channel gains pulled red out of the whole frame. The stall turned mint-green and the review flagged a warm → cool → warm swing.

## Workaround used in the reel
- **Skin metric:**
  - pixels = person matte (hyperframes remove-background) ∩ skin colour box ∩ HSV window (hue 0–42°, sat 0.15–0.75);
  - robust median over 5 frames per shot;
  - target hue 28°, sat 0.45.
  - `tools/skin_post.py`, `tools/skin_report.py`.
- **Final reel:** person-gated skin hue 22–37°, sat 0.43–0.50 across 13 shots.
- **`tools/shot_trim.py`:**
  - `protect: person` (grade changes skip skin inside the person matte only);
  - `skin_gain` (correct skin inside the person matte only, luminance kept);
  - `face_lift` (exposure on faces only).

  Mattes are cached per render.

## Proposed change
- **`colour_report.py`:** add a person-gated skin hue / saturation line per shot, flagging any shot more than ±5° from the reel median. Make it part of every Checkpoint 2.
- **Playbook §A2 (shot match):** anchor skin first; never move skin with global channel gains when only the face is off (use a face / person-matte correction); gate any "protect skin" on a person matte, never on hue alone.
- **Promote** `skin_post.py` (metric) and `shot_trim.py`'s `protect: person` / `skin_gain` / `face_lift` to `scripts/`. They need hyperframes remove-background, which the studio already has.
