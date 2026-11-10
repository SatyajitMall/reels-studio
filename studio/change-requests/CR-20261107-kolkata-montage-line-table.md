# CR-20261107-kolkata-montage-line-table

| Field | Value |
|---|---|
| From reel | `projects/kolkata/` |
| Arch version | 0.9.0 |
| Type | skill · rule |
| Severity | workaround |
| Status | partly done (v0.9.1) |

## What happened
- **KOLKATA got the same note three times.**
  - Round 2, on v1b: "the frames didn't follow a story".
  - Round 3: Amar Shohor "does not match the storyline and the footage".
  - Round 4, on v3b_M3, which had passed the review gate: "the footage still does not match the song or the story, no story is coming out properly".
- **The story lived only in the brief.** Each shot carried a story-beat label (river morning, the roads, where we gathered …), but those were time-of-day buckets.
- **Shots went into beat slots by priority and energy.** The reel-local `tools/audition_edl.py` filled the slots that way, which is close to the skill's Phase 2 method for music-montage.
- **Result:**
  - 9 of 16 shots were empty places;
  - the order ran Pujo night → morning → night;
  - nothing on screen showed someone away, arriving or leaving.
- **Why the process missed it.** Skill Phase 2.3's **line table** (`line | shot | what in the frame shows it`) and the "search the whole pool per line" rule apply to **VO and dialogue reels only**. A music montage has no spoken lines, so it never gets a line table. The review gate checks pacing, framing, beats and colour against the brief. It doesn't check whether the shots tell the brief's story in order, so v3b_M3 passed.
- **Beat grid.** The beat tracker's downbeats on Mayabee sat on unplayed beats about half the time (onset about 1.5× median, against 4–16× on played beats). The reviewer caught five such cuts as minors.

## Workaround used in the reel
- **Story question.** The director was asked a multiple-choice story question with a shot spine per option, and picked "Home for Pujo".
- **Line table first,** in `project.md` Round 4: song moment → story line → shot → what in the frame shows it. The pool was searched for each line on upright sheets (`analysis/pool_v3/sheet_*.jpg`). Six clips no cut had used before carry the story: scooter POV, Howrah walkway crowd, façade ride, taxi with a person, football, Dashami ghat.
- **Reel-local EDL writer.** `projects/kolkata/tools/story_edl.py` writes the EDL from that table and reuses the reviewed shot settings. Cuts go only on played beats: onset ≥ 4× median, measured with librosa onset strength in the song window.

## Proposed change
1. **Skill Phase 2.3:** the line table applies to **every** reel type.
   - For music-montage, write it as `song moment | story line | shot | what in the frame shows it`, before any EDL.
   - The energy arc sets the shot lengths; the line table sets which shot goes where.
   - At most a third of the shots may be empty places, unless the brief says otherwise.
2. **Review gate (`review-gate.md` / `reel-reviewer`):** add a **story check**.
   - Read the brief's story and the line table.
   - Say, per shot, whether the frame shows its line, and whether the order reads as that story with the sound off.
   - A cut that is a list of places fails, even if every frame is clean.
3. **`scripts/gemini_audio_and_beat_analyzer.py` / the beat grid:**
   - mark each beat **played / unplayed** (onset strength against the median in a ±3-frame window);
   - make "cuts land on beats" mean played beats.

## HQ decision (v0.9.1, 2026-11-08)
- **Director profile done:** "the picture shows the word being said" now covers sung lyrics and montages.
- **(1, 2) Accepted for v0.11:** the line table for every reel type (`song moment | story line | shot | what in the frame shows it`, at most a third empty places), and a story check in `review-gate.md` / `reel-reviewer`.
- **(3) Accepted for v0.12:** played / unplayed beats in the beat grid; cuts land on played beats.
