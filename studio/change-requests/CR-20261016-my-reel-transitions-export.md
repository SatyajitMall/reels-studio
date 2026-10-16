# CR-20261016-my-reel-transitions-export

| Field | Value |
|---|---|
| From reel | `projects/my-reel/` |
| Arch version | 0.2.5 |
| Type | harness · skill |
| Severity | workaround (transitions, volume) · blocker-ish (export audio) |
| Status | done v0.3.1 |

## What happened
Premiere 26.5.2, adobe-premiere-pro-mcp, Phases 5–7:
1. `add_transition {clipId1:A, clipId2:B}` puts the transition at the END of B (one cut late); `add_transition_to_clip {clipId:X, position:"end"}` puts it at the end of the clip BEFORE X. Both return `accepted_unverified`. Looks like a QE item-index off-by-one.
2. Opacity keyframes on a clip interpreted 24→25 fps (C011) didn't render; Motion keyframes on the same clip did.
3. `slip_edit` only works with `deltaSeconds`; `offset` is silently ignored (`deltaSeconds:0`).
4. `set_clip_volume {volumeDb:-16}` → Level 0 (silent). Premiere's Level is linear: 0.17783 = 0 dB; dB = 20·log10(v) + 15.
5. `get_encoder_presets` finds nothing (no user presets). `seq.exportAsMediaDirect(out, epr, 0)` with Premiere's `IngestPresets/Transcode/Match Source - H.264 High Bitrate.epr` and AME's `00 - Match Source - High bitrate.epr` both produce correct picture but **silent AAC (−91 dB)**, with all audio tracks unmuted and clip levels verified.
6. `razor_timeline_at_time {videoTrackIndices:[0], audioTrackIndices:[]}` still cut all audio tracks (empty array treated as "all").

## Workaround used in the reel
- Transitions: remove with `videoTracks[i].transitions[j].remove(true,true)`, add with QE `qe.project.getActiveSequence().getVideoTrackAt(t).getItemAt(k).addTransition(qe.project.getVideoTransitionByName(name), atStart, "00;00;00;FF")` — note `true` = start, `false` = end. Verify with `track.transitions[j].start/end`.
- Fades: Dip to Black transitions instead of opacity keyframes.
- Volume: `Level = 10^((dB−15)/20)` set by script.
- Export audio: rebuilt the mix in ffmpeg from the EDL (music section + SFX at timeline times/levels, limiter −1 dBFS) and muxed it with `-c:v copy` onto Premiere's picture.

## Proposed change
1. Report 1–6 upstream.
2. Skill Phase 7: ship a known-good 1080×1920 H.264 `.epr` in `assets/presets/` (or document the built-in path), and add an audio check after every export: `ffmpeg -af volumedetect` must show max_volume > −20 dB, else stop.
3. Add `scripts/mix_from_edl.py` (music + SFX list → ffmpeg mix + mux) as the sanctioned fallback, reading SFX placements from project.md or a JSON the reel writes.
4. Playbook §D: transitions via QE snippet until the MCP is fixed; §F: Level formula.
5. Investigate the silent export (sequence created via `create_sequence_from_clips`, MP3 music, mono/stereo mapping?) — maybe a new Premiere 26 audio-conform issue.

## HQ decision
**Accepted, done in v0.3.1 (apart from 5).** The QE transition snippet and Dip-to-Black fades are in playbook §D and the reality doc. The Level formula is in §F. Built-in `.epr` paths are documented (verified to exist) instead of shipping one. There's a mandatory audio check after every export (skill Phase 7). New `scripts/mix_from_edl.py`, tested on this reel's silent Premiere export: 41.28 s, max −3 dB. **Deferred (backlog):** finding the root cause of the silent export (upstream draft #15, needs a minimal repro).
