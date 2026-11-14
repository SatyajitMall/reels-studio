# Stage 6: song audition (KOLKATA round 3, 2026-11-07)

**Director's pick for the audition:** Shantiniketan · Chiltey Roud · Mayabee.

**How the cuts were made.** Each song is cut from the same pool, the 20-shot "Bengali far from home" spine (`tools/audition_edl.py`), so the song is the only thing that changes.
- **Cuts:** every one lands on that song's own beat, and on a bar downbeat where possible.
- **Shot length** follows the song's energy (quiet bars ≈ 5 s, loud ≈ 2.2 s). The open is slower and the end softer, whatever the energy.
- **Dropped shots:** when a slow song has fewer slots, the lowest-priority shots go first (Uttam mural, flowers, dhakis, tram, façade, walkway).
- **Colour** is the camera's (offline preview), not the grade.

**Copies used.** The director's copies are the official music-video audio (`music/*.wav`, converted from `audio/`). Instagram's library version may start at a different point, so each IG cue below is a moment in the song, not a timecode.

## The three cuts

| | **Shantiniketan** (Anupam Roy) | **Chiltey Roud** (Arnob, Ripon) | **Mayabee** (Blue Touch) |
|---|---|---|---|
| Tempo | 103 BPM, 2.32 s bars | 92 BPM, 2.60 s bars | 123 BPM, played as half-time (3.9 s) |
| Section in our copy | 86.4–133.6 s | 8.0–54.4 s | 46.4–92.9 s |
| **IG start cue** | The pre-chorus lift, **23 s before the chorus** ("take me back" line) | Inside the bansuri intro, **23 s before the first sung line** | **13 s before the hook**, about 10 s before the drop |
| Runtime · shots | 47.2 s · 17 | 46.4 s · 14 | 46.5 s · 15 |
| Shot lengths | 1.9–4.6 s (median 2.5) | 2.5–5.2 s (median 3.2) | 2.0–5.0 s (median 3.0) |
| What plays under the pictures | Pre-chorus over the river and roads; the **chorus from 23 s** runs over the gathering places, the evening, Pujo and the night; its repeat lands on the lit ghat (39 s) | **23 s of bansuri and strings** over the river, roads and chai; the vocal enters at 23 s; the refrain at 32 s over Victoria at dusk, through Pujo and the night | Quiet open over the river; **the drop at 10 s** on the Setu title; the hook at 13 s and again at 25 s; continuous singing to the end |
| Vocals | Sparse to moderate | Sparse: 23 s instrumental, then one line every few seconds | Dense: about 8 words per 10 s, never more than 1.5 s without singing |
| Ends on | The last sung word at 45.8 s, then 1.4 s of tail on the Academy at night | The refrain's last word at 44.9 s, then 1.5 s on the Academy | The last word at 44.8 s, then 1.7 s on the Academy |
| Meaning (summary, from sources + machine transcript) | Wanting out of the crowd and noise; asks to be taken back to a remembered place where something was left unsaid. Homesickness. | Sunlight and pond imagery, then the folk refrain asking someone to come back, just once. Yearning across distance; a person, but placeless enough to read as home. | Sung to an enchanting "you", not seen for months; longing to have them back. A romance. |

## Scores (Stage 5 weights; 0–5 each, max 65)

| Song | Story ×3 | Footage ×3 | Arc ×2 | Tempo ×1 | Audience ×2 | Distinct ×1 | Section ×1 | **Total** |
|---|---|---|---|---|---|---|---|---|
| **Shantiniketan** | 5 | 4 | 4 | 5 | 4 | 5 | 4 | **57** |
| **Chiltey Roud** | 3 | 4 | 5 | 4 | 4 | 3 | 4 | **50** |
| **Mayabee** | 2 | 2 | 3 | 3 | 4 | 4 | 4 | **37** |

**What drives the scores**
- **Shantiniketan:** the only one whose words are literally "take me back"; a story score of 5. Unhurried. Anupam Roy is the 25–34 audience's Kolkata voice. Almost unused on IG (151 reels).
- **Chiltey Roud:** the best arc, a real quiet open that suits the river. It's from the same show (Coke Studio Bangla) as "Shondhatara" in the director's other reel.
- **Mayabee:** a romance, which was v1's failure. Its dense vocal never lets a picture breathe. Proven audio (18K reels).

These scores are a guide only: **the director picks on the phone** (method, principle 3).

## Files
- EDLs: `analysis/audition/edl_{shantiniketan,chiltey_roud,mayabee}.json`
- Previews: `renders/previews/kolkata_audition_<song>.mp4` and `_phone.mp4`
- Measurements: `research/fit_audition/SONG_FIT.md`, `song_fit.json`, `grids.json`, plus full transcripts in `research/fit_audition/full/` (timing only; never quoted)
