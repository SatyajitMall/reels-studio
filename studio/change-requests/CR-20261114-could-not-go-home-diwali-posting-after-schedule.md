# CR-20261114-could-not-go-home-diwali-posting-after-schedule

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.9.1 (studio at v0.11.0 at posting) |
| Type | skill (cinematic-reel Phase 8, `ig-posting-reality.md`) · harness (iPhone Mirroring, AirDrop) |
| Severity | workaround (a fix found after scheduling couldn't be swapped in before the post went out) |
| Status | open |

## What happened
1. **Music changed at posting.** The cut was timed to the reference's guide (152 BPM, "Telephones" by Vacations). At posting the director asked for "something Indian" picked "based on analytics and probability of a hit". Instagram's audio search shows no reel counts, and its Trending chart was off-story Bhojpuri originals. I picked "Maa Trending Version" (Shankar Mahadevan) for its trend label and topic fit. The cut was never checked against it beyond the director's ear.
2. **The reel was scheduled** (Fri 13 Nov, 19:00 IST) through iPhone Mirroring. I stopped before Schedule and the director tapped it.
3. **After the upload, the director watched the reel on the phone** and rejected shot 01's synthetic motion blur, which had passed two review gates and their approval. v10d fixed it in about 2 h and passed the gate at 16:47, before the 19:00 post.
4. **The swap could not be done before the post went out:**
   - Instagram can't replace the video in a scheduled reel. The only route is to delete the scheduled post and set it up again: music, section, volume, fade, cover, caption, location, AI label, quality and the schedule.
   - Re-opening iPhone Mirroring showed "iPhone Mirroring Is Locked. Enter the Mac login…". Only the director can enter it.
   - AirDrop needs Finder's Share menu, and Finder access was declined this time. The director did the same transfer the day before.
   - The director then reported "The reel is already posted". Which file went out wasn't stated.

## Workaround used in the reel
None. The director handled posting. v10d is in `deliver/`, and project.md records that the posted file isn't confirmed.

## Proposed change
1. **`ig-posting-reality.md`:**
   - Instagram can't swap a scheduled reel's video. A fix after scheduling means deleting the post and setting it up again.
   - Before deleting, copy the scheduled caption on the phone. That keeps the emoji the director added, which Mirroring can't type.
   - Re-opening Mirroring after a lock or a restart asks for the Mac login, which is the director's. Ask for it together with the AirDrop step, in one message.
2. **cinematic-reel Phase 8, before the director taps Share or Schedule:**
   - Ask the director to play Instagram's own preview on the phone, full screen, once. The upload is the first time the reel is seen at phone size with the real song.
   - Any effect the director flags there is cheaper to fix before the post exists.
3. **Music decided at posting:**
   - If the song changes from the one the cut was timed to, say so in one line.
   - Run `gemini_audio_and_beat_analyzer.py` on a preview of the new song if one can be extracted. If not, ask the director to check the two cuts PACKAGE.md names.
   - Better still, settle the posting song in Phase 1 (CLAUDE.md §4c already says to check the audio's Instagram page then).

## HQ decision
<!-- HQ fills this in. -->
