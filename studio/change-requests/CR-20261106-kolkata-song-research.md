# CR-20261106-kolkata-song-research

| Field | Value |
|---|---|
| From reel | `projects/kolkata/` |
| Arch version | 0.9.0 |
| Type | skill · script |
| Severity | workaround |
| Status | partly done (v0.9.1) |

## What happened
- KOLKATA has cost two full builds (v1/v1b, v2/v2b) to songs the director then rejected: "the song does not match the storyline and the footage".
  - v1 borrowed the reference reel's song (*Pyaasa*, 1957).
  - v2 used "Amar Shohor", picked from a 6-row list written in one pass.
- The studio has **no song-research step**:
  - skill Phase 0 Q7 only asks whether the soundtrack is existing audio;
  - Round 2 offers "your file · mood + BPM for you to suggest";
  - every audio tool (`gemini_audio_and_beat_analyzer.py`, `teardown.py`) analyses a song *after* it's chosen.
- So the song gets picked before the story is written, and the footage is then fitted to it.
- The director asked for an architecture for researching songs: built on the reference video, but using it only as a reference, never a copycat.

## Workaround used in the reel
`projects/kolkata/research/SONG_RESEARCH_METHOD.md`, a 7-stage method:
1. Reference music DNA, measured and abstracted into ranges, with an explicit "must not copy" column;
2. footage DNA (what the pool can literally show, hold lengths, gaps);
3. story spines (the director picks one);
4. song criteria written before searching;
5. a 15–25 long-list across categories, gated on Instagram-library availability (the director checks), scored on story fit, footage fit, arc, tempo, audience, distinctness and section availability;
6. an audition of the top 3 as offline previews cut from the same pool;
7. lock.

Plus reel-local tools for stage 6, both used for the 2026-11-07 audition:
- `tools/song_fit.py`: BPM, best 45 s window against the arc, vocal density by Whisper;
- `tools/audition_edl.py`: cuts one shot pool to each candidate on its own beat grid, energy-paced, dropping low-priority shots on slow songs. Output goes to `preview_edl.py`.

Intake note: director copies are often music-video rips, sometimes AAC under a `.mp3` name, which libsndfile rejects. Convert to WAV on intake, and give IG start cues as song moments, since a rip may not start where the library version does.

## Proposed change
1. **Skill Phase 0 / Phase 2:** for `music-montage` and `hybrid` reels without director-supplied music, run the song-research method **after the story spine is chosen and before the EDL**. Add a checkpoint "⏸ song audition" (three offline previews from the same pool).
2. **New doc** `.claude/skills/cinematic-reel/song-research.md`, from the reel's method (stages, scoring weights, "the reference lends qualities, never the choice").
3. **New script** `scripts/song_fit.py` (from `projects/kolkata/tools/song_fit.py` once it's proven). Input: several audio files + target length + target arc. Output: BPM, bars, vocal line onsets, the best continuous section per song, shots-that-fit vs the pool's median hold, and a comparison table.
4. **Director profile:** "the song must carry a story the footage can show; never borrow the reference's song as the default".

## HQ decision (v0.9.1, 2026-11-08)
- **(4) Done.** Director profile: "The song carries a story the footage can show; never default to the reference's song. Choose the story first, then research and audition songs."
- **(1–3) Accepted for v0.10** (process batch): the song-research step after the story spine, the "⏸ song audition" checkpoint, `song-research.md` from the reel's method, and `scripts/song_fit.py` promoted from `projects/kolkata/tools/song_fit.py` (with the WAV-on-intake note).
