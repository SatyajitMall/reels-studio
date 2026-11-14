# Song research method (KOLKATA prototype, 2026-11-06)

**Why this exists.** The director rejected two songs on the same ground: "the song does not match the storyline and the footage".
1. The reference's *Pyaasa* song was borrowed with the reference.
2. "Amar Shohor" was picked from a list I wrote in one pass.

The studio has no song-research step. Skill Phase 0 only asks "your file, or mood + BPM for me to suggest", and every audio tool (`gemini_audio_and_beat_analyzer.py`, `teardown.py`) analyses a song **after** it's chosen. Running this method in the reel folder is the workaround; CR-20261106-kolkata-song-research asks HQ to make it a studio step.

**Principles**
1. **Story first, song second.** The song must carry a story that the footage can show, line by line (director profile: "the picture shows the word being said").
2. **The reference lends qualities, never the choice.** We measure what its music *does* (tempo, density, mood, how cuts sit on it) and keep those as ranges. We never take its song, title card or quote, and the shortlist must not be "the same kind of song from the same era".
3. **Show, don't name.** Shortlisted songs are auditioned as offline previews cut from our own pool. The director picks on the phone, not from a table.
4. **Availability is a gate, not a score.** If the song isn't in Instagram's audio library, or there's no licensed copy, it's out.

## Stage 1: Reference music DNA (measured, then abstracted)
Source: `analysis/teardown/TEARDOWN.md`, `analysis/audio_summary.md` (the guide), and the 1 fps watch sheets.

| Quality | The reference | What we keep (as a range) | What we must NOT copy |
|---|---|---|---|
| Tempo / feel | 95.7 BPM, rubato, slow | Unhurried: 70–105 BPM, or a half-time feel over a faster track | The song itself, its era-specific orchestration |
| Vocal density | 3 sung lines in 35 s; the vocal enters at 3.7 s | Sparse vocal: ≤ 1 line per 2–3 shots, so pictures breathe | – |
| Mood | Melancholic longing, a love song | Nostalgic, warm, bittersweet | Heartbreak / romance as the theme (says nothing about Kolkata) |
| Pictures ↔ music | Lines universal, not literal; a cut per bar on line onsets | Cuts on line onsets and bars; but **our** lines should name things we can show | – |
| Arc | Flat, low → mid, fade out | A gentle lift into a payoff, then a soft ending | – |
| Type | "Frames of Calcutta" + a quote | A title card only | Their title wording, their quote, their card layout |

## Stage 2: Footage DNA (what our pool can actually say)
Source: `analysis/orientation.json`, `analysis/pool_unused.jpg`, `analysis/selects.md`, `analysis/motion.json`, `analysis/pujo_picks/PICKS.md`.
- **Subjects we can show literally:**
  - river, boats, boatmen;
  - bridges (Howrah walkway, Vidyasagar Setu; stock Howrah ×2);
  - ghats;
  - College Street books and booksellers, the Coffee House;
  - yellow Ambassador taxis, trams (parked, interior);
  - Maidan football at dusk, St Paul's, Victoria (stock);
  - the Academy at night, the Uttam Kumar mural;
  - scooter rides past red heritage façades;
  - chai on the boil;
  - Pujo nights (Dashami ghat, dancers, dhakis, lit gates).
- **Time of day:** strong day and dusk; night thin (Academy, Pujo; Nov 1 is too dark).
- **Motion:** mostly steady holds of 2.5–5 s; a few moving POVs (scooter, walkway).
  - So the song's bar or line length should allow 2–4 s shots.
  - A very fast song (≥ 140 BPM full-time) forces 1-bar cuts on handheld footage, which is what read as "rushed" before.
- **Gaps:** few faces in close-up; no family or home interiors; no rain; no rickshaw-puller close-up (one Pujo rickshaw).

## Stage 3: Story spines (the director picks one; the song is chosen *for* it)
Each spine is 5–7 beats, and every beat must have shots in Stage 2. A song whose lyrics don't touch the beats fails Stage 5.

## Stage 4: Song criteria (written from Stages 1–3 before searching)
For the chosen spine:
- theme words the lyrics should touch (and that the footage can show);
- mood;
- tempo band;
- energy shape over the reel length;
- vocal density;
- language and era;
- recognisability for Bengalis at home and abroad;
- licence route.

## Stage 5: Long-list → scored shortlist
- **Long-list (15–25)**, across categories: Bengali film songs (classic and new), adhunik, band / Bangla rock, Rabindrasangeet / Nazrulgeeti, Hindi film songs set in Calcutta, instrumental / folk (sarod, bansuri, baul), and songs the director already loves.
- Sources: published lists (e.g. Wikipedia's *List of songs about Kolkata*), press features, the director.
- **Gate:** the director checks the top ~8 in Instagram's audio picker (the studio can't see the library).
- **Score (0–5 each, weights in brackets):**
  - story fit, lyrics ↔ beats (×3);
  - footage fit, the lyric nouns we can literally show (×3);
  - arc fit, the best continuous section vs the target energy shape (×2);
  - tempo fit vs our hold lengths (×1);
  - audience resonance (×2);
  - distinct from the reference (×1);
  - a clean continuous section at the target length (×1).
- Scored **from the lyrics' meaning**, summarised, never quoted.

## Stage 6: Audition (top 3)
1. The director supplies a copy of each (cutting guide only; `projects/<reel>/music/`).
2. `tools/song_fit.py` measures each: BPM, bar length, vocal line onsets (local Whisper), the best continuous section for the target length and arc, and how many shots of our median hold fit.
3. A **line table per song** (line → shot that shows it), searched across the whole pool.
4. An **offline preview per song** from the same pool (`preview_edl.py`). The director watches all three on the phone and picks.

## Stage 7: Lock
Record in the brief and `project.md`: the song, the section (start / end, IG start timecode), the line table and the licence route. Then `edl_vN.json`.
