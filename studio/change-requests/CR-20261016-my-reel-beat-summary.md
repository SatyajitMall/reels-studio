# CR-20261016-my-reel-beat-summary

| Field | Value |
|---|---|
| From reel | `projects/my-reel/` |
| Arch version | 0.2.5 |
| Type | script |
| Severity | workaround |
| Status | done v0.3.0 |

## What happened
`scripts/gemini_audio_and_beat_analyzer.py --music assets/music/inhaleexhalestudio-dum-durga-530246.mp3`:
- `audio_summary.md` calls the every-4th-beat list "4-Bar Downbeats"; they are 1 bar apart (1.765 s at 136 BPM). JSON key `downbeats_every_4_s` is right, the label is wrong.
- Beats only between 12.49 s and 98.03 s; the beatless intro and outro aren't described, so you can't tell intro / build / drop / breakdown / outro from the summary.
- Choosing a 30–45 s section needs an energy map; none is produced.
- For a music-montage it still prints an empty "Dialogue Loudness" table.

## Workaround used in the reel
Computed a 2 s RMS energy curve with ffmpeg + numpy: intro 0–12 s, groove 12.5–37, lift at ~38, breakdown ~60, full energy 62–98, outro 98–103. Used it to offer the director 3 timecoded sections.

## Proposed change
In `scripts/gemini_audio_and_beat_analyzer.py`:
1. Rename the label to "Bar downbeats (every 4th beat)".
2. Add an "Energy / sections" table: RMS per bar, plus auto-labelled sections (intro, build, drop, breakdown, outro) with start/end.
3. Add "Candidate cuts for N s": for each target length (15/30/45/60), the best start downbeat so the first accent lands ≤ 3 s in and the end lands on an outro or a phrase end.
4. Skip the dialogue table when no `--dialogue` is passed.

## HQ decision
**Accepted, done in v0.3.0.** All 4 proposed changes are in `scripts/gemini_audio_and_beat_analyzer.py`. Sections are merged so the same label doesn't repeat back to back. Tested on the pilot track: the sections match your hand-made map, and the 30 s candidate list includes 61.88 s.
