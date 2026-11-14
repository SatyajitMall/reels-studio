# CR-20261018-puja-night-2-commercial-music-ig

| Field | Value |
|---|---|
| From reel | `projects/puja-night-2/` |
| Arch version | 0.5.0 |
| Type | rule · skill |
| Severity | workaround |
| Status | open |

## What happened
The director asked for a commercial song (*Shondhatara*, Coke Studio Bangla) and gave it as a **YouTube link**. CLAUDE.md §4c says music must be licensed and in `assets/music/`, and "if the director plans to add IG audio at upload, cut to a stand-in track at the same BPM". Neither fit cleanly:
- the editor must not download from YouTube (unlicensed copy, platform terms);
- a same-BPM stand-in can't give the song's real accents and phrases, so the cut would drift from the real song at upload;
- the director then supplied their own copy (from their Music library), which isn't a licensed sync copy and doesn't belong in the shared `assets/music/` library.

Also learned: **Instagram's audio picker takes one continuous stretch of a song**, so a music edit (joining intro + main section, as in my-reel) is impossible on this route.

## Workaround used in the reel
- Director's own copy symlinked as a **cutting guide** in the reel folder: `projects/puja-night-2/music/shondhatara_GUIDE.mp3`, not in `assets/music/`.
- Section chosen as one continuous stretch (3:31.88–4:31.70), from 3 rendered previews.
- Two exports per version: `<reel>_vN_mix.mp4` (guide music, for review and archive) and `<reel>_vN_IG.mp4` (music track muted, ambience only) for posting with IG's library song started at the same timecode.
- The brief records the start timecode for the IG picker.

## Proposed change
In CLAUDE.md §4c and skill Phase 0/1, add a "**commercial song via Instagram's library**" route:
1. The editor never downloads from streaming links. Ask the director for a copy they own, used **only as a cutting guide** in `projects/<reel>/music/` (never `assets/music/`).
2. Pick one continuous section (no music edits); record the IG start timecode in the brief.
3. Export `_mix` (review) and `_IG` (music muted) every version.
4. At Checkpoint 3, remind the director to add the song in IG from the recorded timecode, and to check that IG's version matches the guide (masters can differ by a few hundred ms).
Keep the same-BPM stand-in only for when the director has no copy at all.
