# CR-20261107-kolkata-film-emulation-first-use

| Field | Value |
|---|---|
| From reel | `projects/kolkata/` |
| Arch version | 0.9.0 |
| Type | skill · script |
| Severity | polish |
| Status | done (v0.9.1) |

## What happened
`film-emulation-prompts` asks the first reel that uses it to report back: the prompt, the draft's numbers against its anchor, and whether a re-prompt was needed. KOLKATA is that reel.

- **The shot.** The director wanted "the tram actually running on the line with a clear front end view" (round 6b). I checked and found none:
  - Pexels: 267 Kolkata clips, and 175 tram clips;
  - Pixabay;
  - Wikimedia Commons;
  - own footage: only retired, parked trams (C025–C027).

  The director chose an AI shot: `tram_front`, a draft at $0.12 (2026-11-07). There's no first frame, so no real people get animated. The light was matched to the next shot, C101: a daylight street with tram lines and a taxi.
- **Prompt:**
  - the shot, followed by the skill's light block;
  - light: "Soft daylight under light cloud, a hazy pale sky, soft shadows";
  - negative: the skill's list, plus people close to the camera, faces, crowd, modern/articulated/European tram, double-decker, bus, logos.
- **What Veo got right.** The tram drives straight at the camera along grooved rails. It has:
  - a white body with a blue band;
  - orange window frames;
  - a headlight;
  - overhead wires;
  - green-shuttered colonial houses.

  The motion is clean, and there's no baked look (p02 0.000, no bars, no grain).
- **What it got wrong:**
  1. **Prompt words became text in the frame.** "a route number board" came out as a board that literally reads "ROUTE", with invented numbers "26.10" and "26.16".
  2. **"a yellow Ambassador taxi" became a New York checker cab** (a roof "TAXI" sign, a checker band). Veo doesn't know the Hindustan Ambassador by name.
  3. **"Soft daylight under light cloud" came out as bright sun with a blue sky and white clouds.**
- **The draft against its anchor, by numbers** (`colour_report.py`; draft from 1 s, C101 0.5–2.6 s):

  | | luma | p02 | p98 | crush % | clip % | sat | R−B |
  |---|---|---|---|---|---|---|---|
  | draft | 0.489 | 0.000 | 0.987 | 8.6 | **15.9** | 0.192 | 0.068 |
  | C101 (anchor) | 0.391 | 0.046 | 0.943 | 1.0 | 0.06 | 0.225 | 0.097 |

  Luma is +0.10 (the tolerance is ±0.04). The sky is blown (15.9 % clipped). Warmth is −0.03, at the edge of the tolerance. `conform_clip.py --match` pulled the colour much closer on the sheet.
- **Script bug:** `scripts/colour_report.py` crashes on the director's camera files:
  - error: `ValueError: could not convert string to float: '1,'` in `fps_of` (line 43);
  - cause: the same rotation-tagged `avg_frame_rate` trailing comma as `shake_report.py` (CR-20261107-kolkata-preview-fx).

## Workaround used in the reel
- **Measuring the anchor:** I measured C101 from a temporary H.264 copy of the range (no rotation side data).
- **Draft 2 / the final get a re-prompt:**
  - no taxi in the prompt (the next shot is the real Ambassador);
  - "a plain destination board" instead of "route number board";
  - light: "a hazy overcast afternoon, no direct sun, a soft white-grey sky";
  - negative: + "bright sunshine, blue sky, hard shadows, readable words, the word ROUTE, New York taxi, checkered taxi, taxi roof sign".
- **The preview (v6b):** uses the draft, conformed (`--start 0.25 --match C101`) and slowed to 0.85 by the reel-local fx pre-render to fill the 4.08 s line.

## Re-prompt result (draft 2, same day)
The prompt v2 changes (listed under the workaround) fixed all three faults in one draft: the board is plain, there's no taxi, and the sky is hazy and overcast.

| | luma | p02 | p98 | crush % | clip % | sat | R−B |
|---|---|---|---|---|---|---|---|
| draft 2 | 0.493 | 0.045 | 0.992 | 0.3 | 16.0 | 0.117 | 0.001 |
| C101 (anchor) | 0.391 | 0.046 | 0.943 | 1.0 | 0.06 | 0.225 | 0.097 |

- **What it fixed:** the blacks now match the anchor.
- **What's left:** "overcast" gives a large white, clipped sky and neutral, pale colour, where our late-afternoon haze is warm and saturated. A text prompt alone doesn't match a warm anchor. The conform `--match` nudge and the Premiere primary have to close it.
- **Proposed rule:** when the anchor is warm haze, describe the light as "late-afternoon haze, the sky a small pale strip between treetops". This is untested, so mark it as a candidate.

## Proposed change
1. **`film-emulation-prompts` SKILL.md, a new "Words Veo takes literally" section:**
   - never name a sign, board or label's content ("route board", "shop sign"): Veo writes the word;
   - ask for "plain" or "blank" boards, and add "readable words" to `--negative`.
   - Regional objects (Hindustan Ambassador, a Kolkata tram's trolley pole) need a visual description, not a name. Better still, leave them out and let the real next shot carry them.
2. **Same skill, Daylight street row:** "soft daylight under light cloud" read as sunny. For an overcast anchor, say "hazy overcast, no direct sun, soft white-grey sky", and add "bright sunshine, blue sky, hard shadows" to `--negative`. Mark the row verified once the final confirms it (this CR's update).
3. **`scripts/colour_report.py` `fps_of`:** parse `avg_frame_rate.split(",")[0]`, the same fix as `shake_report.py`. It would be better as one shared helper.

## HQ decision (v0.9.1, 2026-11-08)
- **(1) Done.** `film-emulation-prompts` rule 6, "Words Veo takes literally": never name a sign's content (ask for a plain board, add "readable words" to `--negative`); describe regional objects, or leave them to the real neighbouring shot.
- **(2) Done.** Daylight street row: sunny and overcast wordings, with the overcast negatives, marked as fixed in one draft; the warm-haze wording is listed as an untested candidate.
- **(3) Done.** `scripts/media_info.py` `fps_of` (ffprobe JSON, avg → r_frame_rate fallback) replaces the csv parsers in `colour_report.py`, `shake_report.py`, `frame_scan.py` and `render_diff.py`. All four were verified crashing on a kolkata camera file (`ValueError: '1,'`) and now run on it.
