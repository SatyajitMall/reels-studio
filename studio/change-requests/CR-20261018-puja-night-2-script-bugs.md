# CR-20261018-puja-night-2-script-bugs

| Field | Value |
|---|---|
| From reel | `projects/puja-night-2/` |
| Arch version | 0.5.0 |
| Type | script · harness |
| Severity | workaround |
| Status | partly done (v0.9.0) |

## What happened
1. **`scripts/shake_report.py` crashes on the director's Blackmagic Cam `.mov` files:** `ValueError: could not convert string to float: '1,'` in `fps_of()`. ffprobe's `csv=p=0` output for these files ends in a trailing comma (`25/1,`).
2. **`scripts/link_footage.sh` reference-folder skip pattern** `*ref*rence*` doesn't match the director's spelling `Reffernce` (my-reel's was `Refference`, which does match). A re-run of the b-roll link would have pulled the reference reel in as footage (not hit, because the reference was added after linking).
3. **Upside-down clips again (2nd reel → studio rule).** 18 of 62 clips are recorded inverted (phone held upside down at night). `analyze_footage.py` still doesn't flag orientation, already raised in `CR-20261016-my-reel-footage-overview`. The cut uses C139 rotated 180°.
4. **Beat analyser "Candidate cuts" rank by energy only.** All its 45 s and 60 s picks were high-energy stretches. This reel's brief is calm / nostalgia, so the section was picked by hand from the per-bar table, and 3 candidate MP3 previews were rendered with ffmpeg for the director's ear. The director chose the recommended one.
5. **Environment:** the `ELEVENLABS_API_KEY` in `.env` is rejected (`401 invalid_api_key`), and no local Whisper is installed (`mlx_whisper`, `faster_whisper`, `whisper` all missing). Transcription is impossible on this machine right now. That wasn't blocking for a montage, but it was needed to check whether the reference had a voiceover (solved by chroma cross-correlation against the song instead).

## Workaround used in the reel
1. Cut each shot's source range to a 540×960 25 fps H.264 proxy in the scratchpad and ran `shake_report.py` on those.
2. Linked the reference separately with role `references`.
3. Listed inverted clips by eye from the overview sheets; rotated in Premiere.
4. Manual section pick + ffmpeg previews (`projects/puja-night-2/music/previews/`).
5. Chroma cross-correlation (librosa) of reference audio vs the song: matched 2:06.4–2:51.5 at 0.97–0.99 per 4 s window, level within ±1.7 dB → no voiceover.

## Proposed change
1. `shake_report.py` `fps_of`: `out.strip().rstrip(',')` (or parse with `-of default=nw=1:nk=1`). Check `motion_holds.py` / `selects_score.py` for the same pattern.
2. `link_footage.sh`: match any folder whose name starts with `ref` (case-insensitive), e.g. `-iname 'ref*'`.
3. Orientation: per-clip "inverted?" check (face/sky-up heuristic, or a 180°-rotated vs upright sharpness/horizon score), listed in `summary.md`; and a skill rule: **rotate and score inverted clips, never drop them** (my-reel R8 + this reel).
4. Beat analyser: add `--mood calm|build|energetic` (calm = prefer a quiet entry and a single lift; penalise flat-high stretches) and `--previews` to write MP3 previews of the top candidates for the director.
5. `setup.sh` / README: verify the ElevenLabs key at setup and offer `pip install mlx-whisper` as the local fallback.

## Follow-up (round 3)
- A clip I added late (C087) was recorded upside down and went into v3 unrotated; the blind reviewer flagged it as a **blocker**. This is the third time orientation bit the studio (my-reel R8, puja-night-2 Phase 1, v3). Proposal stands (orientation check in `analyze_footage.py`), plus: the reviewer's checklist and skill Phase 3 should say "check orientation of every clip added in a later round" (the editor checked sharpness and shake for C087, not orientation).

## Follow-up (round 5): orientation, 4th time
- C085 and C086 (forge pandal, the same camera minute as the upside-down C087) went into v5 upside-down. The blind reviewer caught both as blockers in gate loop 2; loop 1 missed them. The editor's check sheet showed abstract content (hanging nuts, red spikes) that looked plausible either way; the deciding cues were stall signage (text reads only when rotated) and where the ground and garlands sit.
- **Stronger proposal:**
  1. `analyze_footage.py` should flag orientation per clip and group clips by recording time. Neighbours of a known-inverted clip get flagged "check".
  2. The skill should require an **orientation table in the brief** (clip → upright / 180°, with the cue used: text, ground, people, light direction) before any placement.
  3. The reviewer's checklist should say: "verify orientation of every clip from a readable cue; abstract shots too".

## HQ decision (v0.9.0, 2026-11-04)
- **(5) Transcription without a working ElevenLabs key: done.** Local Whisper (faster-whisper in `.venv`, installed by `setup.sh`) is the default; the key is optional (`transcribe_reel.sh --scribe`).
- Everything else stays open.
