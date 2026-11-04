# CR-20261019-pujo-ki-asolei-sobar-external-vo-audio

| Field | Value |
|---|---|
| From reel | `projects/pujo-ki-asolei-sobar/` |
| Arch version | 0.5.3 |
| Type | reel-type · rule · skill · script |
| Severity | workaround |
| Status | partly done (v0.9.0) |

## What happened
1. In Round 1, the director said "no speech, music only" (→ `music-montage`). In Round 2, asked for music, they supplied a **reference reel and asked to use its audio, VO included**, as the whole soundtrack (a Hindi voiceover over a soft bed, 35.8 s; posted later with IG's audio). This is a common Instagram pattern ("use this audio" with a trending VO). It fits none of the three reel types cleanly: there's no speech in our footage, yet a VO drives the timing.
2. **Transcription failed:** `.vendor/video-use/helpers/transcribe.py` → `Scribe returned 401 … "Invalid API key"`. The ElevenLabs key in `.env` is set but rejected. `scripts/gemini_transcribe_fallback.py` then has no backend: no `mlx_whisper` / `faster_whisper` / `whisper` installed, and no Gemini SDK in `.venv` despite the script's name.
3. `transcribe_reel.sh` only reads `raw/a-roll/`, so it can't take an external audio or reference file.
4. `gemini_audio_and_beat_analyzer.py` on VO + bed returned "117.5 BPM" and accents that follow the speech. That's meaningless as a cut grid, but nothing warns about it.

## Workaround used in the reel
- Typed as `hybrid`, with the external VO as the timing source. Every cut sits in a VO pause.
- `projects/pujo-ki-asolei-sobar/tools/vo_timing.py`: line timings from (a) changes in the reference's burned-in subtitles (a yellow-text mask on the bottom band) and (b) pauses in a 300–3400 Hz speech-band envelope. 10 lines; the two methods agree within 0.1 s.
- Audio extracted to `audio/ref_audio_vo.wav` as a **cutting guide** (not in `assets/music/`). `_mix` + `_IG` exports per version, following CR-20261018-puja-night-2-commercial-music-ig.
- The English subtitles are the editor's translation, for the director to check.

## Proposed change
- **ARCHITECTURE §6 / CLAUDE.md §4:** add a sub-case of `hybrid` (or a type `voiceover`): "external VO track as the soundtrack". Timing source: VO phrase pauses (word level when transcription works). Captions: subtitles of the VO. Audio: guide only, IG audio at upload.
- **Skill Phase 0, round 1, Q1:** ask "Is the soundtrack an existing audio (a song, or a reel's audio with a VO)?" alongside "Is anyone speaking?".
- **`transcribe_reel.sh`:** accept a file argument (`--file references/x.mp4`), not only `raw/a-roll/`.
- **Setup:** fix or flag the invalid ElevenLabs key (director action). Install `faster-whisper` in `.venv` so the fallback works offline, and add a `setup.sh` check that runs one 1 s test call.
- **Beat analyzer:** warn when the track contains speech (e.g. high speech-band energy ratio), saying the beat grid is unreliable.
- Promote `tools/vo_timing.py` (subtitle-change + pause detection) to `scripts/` as the no-API fallback for references that have burned-in subtitles.

## Follow-up (end of reel, 2026-10-21)
- **Cut placement rule for VO-driven montage (cost: 3 director rounds).** I put cuts inside VO pauses (CLAUDE.md §4b's dead-air logic). The director wants **pictures to change on the words**: on the first word of each sentence or clause, never mid-pause. v1b had cuts up to 28 frames early. Proposed rule for §4b / hybrid: "cut on the measured onset of a sentence or clause (0 to −2 frames); a pause belongs to the outgoing shot."
- **Onset detection:** a plain "end of pause" rule fires on breaths (3–4 f early). A peak-relative rule (first 5 ms frame within 8 dB of the word's peak) matched the reviewer's independent measurement. Promote `tools/vo_timing.py` + that rule as `scripts/vo_onsets.py`.
- **Depiction:** each shot must depict its line literally. The working device was one man per voice: a young drummer for "the first man" at every mention, a tea seller for "the second". Reviewers flagged three different "first men" as major.
- `hyperframes transcribe` (local Whisper / Parakeet word timestamps) exists. It would have covered the dead ElevenLabs key; add it as the transcription fallback (Hindi needs large-v3 or Parakeet).

## Follow-up 2026-10-27 (round 14, at posting)
**"Add the reference audio in Instagram at upload" failed.** The reference reel's IG audio is a licensed library song ("Jaago", Lifafa). The creator spoke his voiceover over it, so **Use audio** gives only the song, without the voice the cut and subtitles follow. Nobody checked this until the director was posting.

**Workaround:**
1. The director recorded the lines himself in a reel-local browser recorder (`tools/vo_recorder`: guide video + mic, takes saved into the reel). It had a record-along guide (`tools/record_guide.py`: teleprompter, slot bars, CLAP sync).
2. The phrases were placed on their cuts (`tools/vo_build.py`).
3. The voice was matched to the reference: Praat PSOLA pitch / formant shift and a half-octave match EQ (`tools/vo_gentle.py`).
   - A WORLD-vocoder full match (`tools/vo_match.py`) was rejected by the director as "synthetic".
   - A jagged per-band match EQ was heard as "nasal".
4. The subtitle cards were re-worded to his words (`tools/sub_card.py`, `tools/sub_patch.py`).
5. The music bed is added from IG's library at upload.

**Proposed:**
- **At Phase 1, open the reference's audio page in IG.** If it names a song, the voice is not in the IG audio. Then decide early: get the creator's permission and bake in his voice, or re-record (own voice), or go music only.
- **Promote the recorder, the guide and the PSOLA + smooth-EQ matcher to `scripts/`.**
- **Record the VO on a close phone or lav mic, never the laptop mic.** The laptop mic's nasal resonance couldn't be fully processed out.
- **Studio rule:** never clone a real person's voice with AI without consent; matching pitch, pace and tone of one's own voice is fine.

**Resolution (same day):** the creator gave permission. The voice was split from the song with demucs (htdemucs two-stem, 40 dB separation, about 20 s on CPU), baked into the video, and the song was re-added from IG's library. **Proposed:** add a `scripts/stem_split.py` (demucs) to the studio for exactly this case: creator voice yes, song from IG's library. Ask for the creator's permission at Phase 1, not at posting.

## HQ decision (v0.9.0, 2026-11-04)
**Transcription, the Round 1 question and the cut rule accepted, v0.9.0.**
- `transcribe_reel.sh` takes files (an external VO or a reference) and uses local Whisper by default (`scripts/transcribe_local.py`, faster-whisper in `.venv`; `--model large-v3-turbo --language hi` for Hindi). Scribe is `--scribe`.
- SKILL Round 1 question 7: is the soundtrack existing audio? Phase 1 checks its Instagram page and the creator's OK.
- "Pictures change on the words" and literal depiction, one subject per line: director profile, CLAUDE.md §4b, the Phase 2 line table and a reviewer check.
- **Still open (backlog):** promote `tools/vo_timing.py` with the peak-relative onset rule; the beat analyser's warning on speech; a `voiceover` sub-type of `hybrid`.
