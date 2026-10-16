# HQ Backlog

Architecture work not yet done. HQ triages it at the start of each `/studio-hq` session. Change requests from reels are linked here when deferred.

## Untriaged: external review (`GEMINI_ARCHITECTURE_REVIEW.md`, added 2026-10-15 by another tool)
Each item needs to be verified before it's adopted. The scripts it ships (`scripts/gemini_*.py`) haven't been reviewed yet.

| # | Claim | Verify by | Status |
|---|---|---|---|
| G1 | `assets/` is empty, so the LUT / SFX / grain steps have nothing to use. A starter pack generator is offered | Already true: assets are empty. Decide between a generated starter pack and real licensed assets | open |
| G2 | `transcribe.py` exits when there's no ElevenLabs key. A local Whisper fallback is offered | Read `.vendor/video-use/helpers/transcribe.py`. Test the fallback on a talking-head pilot | open |
| G3 | There's no loudness or beat-grid measurement. A librosa analyser is offered | Review the script, then run it on the first music-montage pilot | open: needed by music-montage |
| G4 | HyperFrames graphics on V2 sit under the V3 grade and get discoloured | Valid concern. Decide on a track layout change (graphics above the grade) | open |
| G5 | `set_clip_opacity` / `speed_change` / `reverse_clip` may not exist as tools | Grep the tool registry in the installed `adobe-premiere-pro-mcp` package | open |
| G6 | Premiere tone-maps iPhone HLG before grading, so a Log LUT blows it out | Check on the first iPhone HDR clip in a pilot | open |

## Known gaps
- Music-montage runs on CLAUDE.md §4b rules, which haven't been tested in Premiere yet. The first pilot validates them.
- The hook enforcement only works once `studio/harness/settings.json` is installed as `.claude/settings.json`.
