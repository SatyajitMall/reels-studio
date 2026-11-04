# CR-20261019-pujo-ki-asolei-sobar-pool-survey

| Field | Value |
|---|---|
| From reel | `projects/pujo-ki-asolei-sobar/` |
| Arch version | 0.5.3 |
| Type | script · skill |
| Severity | workaround |
| Status | partly done (v0.9.0) |

## What happened
1. **Pool survey before selection.** The director keeps footage in a pool folder (`~/Documents/Media`, 97 clips over 4 shoot days, plus earlier reels' folders) and wanted to **choose clips together before anything entered the reel**. Skill Phase 1 assumes the footage is already decided: `link_footage.sh` links a whole folder, and `analyze_footage.py` runs on `raw/`.
2. **Copy vs link.** The director chose to **copy** the 41 picks into `raw/b-roll/` (self-contained reel folder). `link_footage.sh` has no copy mode and no "only these clip ids" mode.
3. **No pick sheet or storyboard tool.** The overview sheets show one mid-frame per clip. That's fine for spotting junk, but too thin to choose by story role (for example, C188's mid-frame showed a passer-by; its real subject is two girls selling toys). Nor is there a Checkpoint 1 storyboard (in / mid / out frames per EDL row). The one built here caught a bad source range on the payoff shot before the director saw it.

## Workaround used in the reel
- `analyze_footage.py ~/Documents/Media -o projects/<reel>/analysis/media_survey` (97 clips, ~7 min, 4.5 s per 4K HEVC clip; it doesn't recurse, so the camera's `Proxy/` folder was skipped automatically).
- `projects/pujo-ki-asolei-sobar/tools/picksheet.py`: grouped sheets with 4 frames per clip from each `contact.png`, plus duration/fps and a role note. Three sheets (spectacle / edges / turn and themes) went to the director; they approved the 41-clip shortlist in one question.
- Copy: `cp -pn` loop over clip ids, plus a line in `raw/SOURCES.md`.
- `projects/pujo-ki-asolei-sobar/tools/storyboard.py <reel> analysis/edl_v1.json out.jpg`: 3 frames per EDL row, colour-coded by look group, with VO line / role labels.

## Proposed change
- **Skill Phase 0/1:** add a "footage pool" path. If the director names a pool folder (or says "we'll choose"), survey it into `analysis/media_survey/`, propose a shortlist as grouped pick sheets, and bring in only the approved ids.
- **`scripts/link_footage.sh`:** add `--copy` and `--only C143,C145,…` (clip-id filter). Keep link as the default.
- **New `scripts/pick_sheet.py`** (from the reel's `tools/picksheet.py`) and **`scripts/storyboard.py`** (from `tools/storyboard.py`, reading the EDL json). Make the storyboard a Checkpoint 1 deliverable in the skill: it's how the director sees the plan, and it catches bad in/out points early.

## Follow-up (end of reel, 2026-10-21)
- **Search every shoot folder by name pattern before shortlisting.** The director's Pujo footage was in 6 folders (`~/Documents/Video /Puja…`, `Pujo…`, two with trailing spaces in the name, which broke plain paths). I surveyed only the one folder named first. The shots the narration needed (a young drummer, a tea seller) were in a folder found 3 rounds later. Proposed: `scripts/find_footage.sh <pattern>` (glob-safe, trailing spaces) lists every matching folder with clip counts, and the skill runs it in Phase 1.
- **Quantise the EDL to sequence frames** before `add_to_timeline_batch`: times like 2.21 s (66.3 f) left 1-frame gaps at 7 of 19 cuts. Plan in frames (`startF` / `endF`) and convert once.
- **Storyboard should print each clip's fps and flag non-sequence rates** (25 fps C143 / C145 slipped into a 30 fps plan unnoticed in a 41-row table).
- Pick sheets and storyboards were the director's main decision surface, used at every round (`tools/picksheet.py`, `tools/storyboard.py`).

- **Added 2026-10-24 (retro):** `tools/storyboard.py` (reel-local) should print each clip's fps and flag any that differ from the sequence rate. Two 25 fps clips (C143/C145) slipped into a "30 fps" brief in round 1 and were caught only while re-planning.

## HQ decision (v0.9.0, 2026-11-04)
**Pick sheets and storyboard accepted, v0.9.0.**
- New `scripts/pick_sheet.py` (6 frames per clip with camera times, `--all` for the whole analysed pool, labels after `=`) and `scripts/storyboard.py` (from this reel's and goddess's versions: in / mid / out per EDL shot through its framing, fps and speed flags, the line and role, Instagram UI bands). Both are Checkpoint 1 deliverables in SKILL Phase 2, with the offline preview.
- The EDL is now planned in frames: `preview_edl.py` rounds every time to the reel's frame grid and rejects overlaps.
- **Copy mode (`link_footage.sh --copy --only …`):** Batch C item 19, with the reference-skip fix. The director profile says to copy the shortlist by hand until then.
- **Still open:** the "footage pool" path in Phase 0/1 beyond `pick_sheet.py --all`, and the search of every shoot folder (Batch C item 19).
