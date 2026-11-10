# CR-20261107-kolkata-lyric-shot-skill

| Field | Value |
|---|---|
| From reel | `projects/kolkata/` |
| Arch version | 0.9.0 |
| Type | skill |
| Severity | workaround |
| Status | accepted (v0.11) |
| Requested by | **the director**, in the reel session (2026-11-07): "Try and understand the lyric and determine the shots, post it create that skill" |

## What happened
- **The ask.** KOLKATA is cut to a song with a spoken intro (*Kolkata*, from *Praktan*). Six rounds of notes on it said one thing: the shots don't show what the song is saying.
- **The notes that showed the gap:**
  - **Unexplained people.** In a stock clip of wall writing, a woman and a passer-by blocked the wall. On "explorer", a stock girl on a Metro platform made the director ask "why is that there".
  - **Unreadable frames.** A forge-themed pandal (giant spanners framing Durga) didn't read at phone size: "I couldn't find a clue what that pandal is".
  - **Off-meaning frames.** The director called the "city of surprises" frames ("doesn't match") and the Coffee House frame (a pan with no subject) bad.
  - **Too much of one subject.** The steadiest replacements came from the Pujo pool, and Pujo crept up to 8 of 30 shots: "too many pooja shots".
  - **A spoken line the director didn't want.** The guide's name was in the line, and he wanted only "I am your guide": "why that part is there, chop it".
- **The lyrics were never understood.**
  - The song's Bengali verse was transcribed by Whisper large-v3-turbo with `--language bn` and came out garbled. Sung Bengali with a music bed is hard for it.
  - The English part of the spoken intro was transcribed separately in `en`, which also turned the Bengali half-line "ami … apnader guide" into English.
  - No step in the skill asks what each sung line *means* before shots are picked. For music the line table (CR-20261107-kolkata-montage-line-table) uses song sections, not the words.
- **What worked in round 6:**
  - Whisper large-v3 (not turbo) on the verse alone, with no initial prompt, gave usable Bengali. An initial prompt made turbo hallucinate the prompt's words.
  - A speech-band envelope (20 ms RMS, 300–3400 Hz) located the spoken words more reliably than the word timestamps.
  - Each line was summarised in a sentence before any shot was chosen.

## Workaround used in the reel
- `projects/kolkata/tools/guide_edl_v6.py`: the line table is in the code. Each line is (song time, what the line means, one shot), with the meanings summarised, never quoted.
- `projects/kolkata/tools/song_edit_v6.py`: cuts the name from the spoken intro.
  - The cut is exactly 5 beats (2.553 s at 117.5 BPM), so the music bed stays on its grid, with a 30 ms centred equal-power crossfade.
  - Verified by re-transcribing the edited line, and by checking for a click at the join.
- **Subject mix by hand:**
  - Pujo down to 3 shots of 26;
  - no stock person whose presence the line doesn't explain;
  - every frame readable at phone size without context.

## Proposed change: a new skill `lyric-shots` (draft below)
Add `.claude/skills/lyric-shots/SKILL.md`. Call it from `/cinematic-reel` Phase 2 for any reel whose soundtrack has words (sung or spoken), before the EDL. Wire its checks into the review gate's story check (CR-20261107-kolkata-montage-line-table item 2).

````markdown
---
name: lyric-shots
description: Understand a song's words line by line and choose one shot per line that shows what the line means. Use in Phase 2 of /cinematic-reel for any reel cut to a song or VO with words, before writing the EDL.
---

# /lyric-shots

The director's rule: the picture follows what the song is saying. Understand every line first, then pick shots.

## 1. Get the words right (never quote them in any output)
- Split the song into spoken and sung stretches, and stretches by language. Find the boundaries by ear-proxy: a
  speech-band envelope (300–3400 Hz RMS at 20 ms) and Whisper's language guess per 10 s chunk.
- Transcribe each stretch in its own language:
  - spoken: large-v3-turbo is fine;
  - sung: use large-v3 (turbo garbles sung Bengali/Hindi under music);
  - no initial prompt (it makes Whisper repeat the prompt's words);
  - pass audio as a 16 kHz numpy array (faster-whisper's own decoder has failed on WAV paths).
- Word timestamps drift on sung and mixed-language audio. Place every cut on the envelope (the clause onset 0–2
  frames before the energy rise), not on the timestamp.
- Write `analysis/lyrics_meaning.md` with one row per line: song time | language | what the line MEANS, in your own words, one sentence.
  - Never reproduce lyrics in any file or message.
  - Flag lines you couldn't understand, and ask the director about those only.

## 2. Line table (before any EDL)
`song time | reel time | meaning | the image it asks for | shot | what in the frame shows it | steadiness | source`
- **The image it asks for:** literal (Coffee House for "culture"), metaphor (a boat drifting in for "a stranger
  arrives"), or the feeling (slow motion on a walk for "come and see"). Write which.
- **One line = one shot by default.** A long sung line may hold one shot. Split only on a downbeat the band plays.
- **Search the whole pool for each line** (own footage first), then free stock only for lines the pool can't show.

## 3. Hard checks per shot (each one has failed a real reel)
1. **Readable at phone size in under 1 s with no context.** If the subject needs explaining (a theme pandal whose
   material you can't make out), it fails.
2. **No unexplained people.** A person who is the subject must be someone the line is about. A stranger looking
   around, a passer-by blocking the subject, or anyone looking into the lens fails.
3. **Steady:** `shake_report.py` jit_rms ≤ 3 px and no swoops (pan > 300 px/s), unless the line asks for movement.
4. **It matches its neighbours:** time of day and light flow, unless the line is the turn (a night shot dropped
   between dusk and day reads as a mistake).
5. **Subject mix:** no subject over about a third of the shots unless the brief is about it (a city reel went to 8/30
   Pujo shots and the director called it).

## 4. Editing the words
If the director wants words removed (a name, a filler line):
- cut a length that is a whole number of beats, so the bed stays on the grid;
- use a ~30 ms equal-power crossfade centred on the cut points;
- re-transcribe the edited line to confirm the words are gone, and check the join for a click;
- warn that Instagram's library audio can't carry the edit, so it lives only in the baked `_mix`.

## 5. Hand-off
- Show the director the meaning column and the shot column together with the storyboard and the preview.
- Every note on a shot gets its row's "what in the frame shows it" rewritten before a new pick.
````

## HQ decision (v0.9.1, 2026-11-08)
- **Accepted for v0.11**, as the director asked: a `lyric-shots` skill, called from SKILL Phase 2 for any reel whose soundtrack has words, with its checks wired into the review gate's new story check (CR-20261107-kolkata-montage-line-table). The draft in this CR is the starting point; HQ will test the transcription route (large-v3 for sung lines, no initial prompt, the speech-band envelope) on the kolkata song before shipping.
- Director profile already carries the rule in v0.9.1: sung lyrics and montages get one shot per line that shows what it means.
