# HQ Backlog

Architecture work not yet done. HQ triages it at the start of each `/studio-hq` session. Change requests from reels are linked here when deferred.

## Untriaged: external review (`GEMINI_ARCHITECTURE_REVIEW.md`, added 2026-10-15 by another tool)
Each item needs to be verified before it's adopted. The scripts it ships (`scripts/gemini_*.py`) haven't been reviewed yet.

| # | Claim | Verify by | Status |
|---|---|---|---|
| G1 | `assets/` is empty, so the LUT / SFX / grain steps have nothing to use. A starter pack generator is offered | Already true: assets are empty. Decide between a generated starter pack and real licensed assets | **done** v0.2.3: starter pack adopted, with 2 LUT fixes. Real licensed assets can be added alongside it at any time |
| G2 | `transcribe.py` exits when there's no ElevenLabs key. A local Whisper fallback is offered | Read `.vendor/video-use/helpers/transcribe.py`. Test the fallback on a talking-head pilot | open |
| G3 | There's no loudness or beat-grid measurement. A librosa analyser is offered | Review the script, then run it on the first music-montage pilot | **partly adopted** v0.2.0: the beat grid was reviewed and tested on a 120 BPM click track (read 117.5 BPM, beats placed within about 1 frame). Used by §4c. The loudness half hasn't been reviewed |
| G4 | HyperFrames graphics on V2 sit under the V3 grade and get discoloured | Valid concern. Decide on a track layout change (graphics above the grade) | **rejected** 2026-10-16 by the director. Graphics stay on V2, under the grade |
| G5 | `set_clip_opacity` / `speed_change` / `reverse_clip` may not exist as tools | Grep the tool registry in the installed `adobe-premiere-pro-mcp` package | **rejected** 2026-10-16. Claim is false. All 52 tool names in the rules exist in server 1.2.9 (283 tools), including the 3 named. Rerun `scripts/check_tool_names.sh` after any MCP upgrade |
| G6 | Premiere tone-maps iPhone HLG before grading, so a Log LUT blows it out | Check on the first iPhone HDR clip in a pilot | open. `my-reel` footage is Rec.709 SDR, so it isn't tested there |
| G7 | `scripts/gemini_setup_premiere_mcp.sh` (added 2026-10-16): setup with an npm fallback for a root-owned `/usr/local`, plus CEP debug mode for CSXS 9–16 (doctor covers 10–12) | Fold its npm-prefix fallback into `setup.sh`. Enable more CSXS versions only if the panel doesn't show in Premiere | open. File left untracked |

## From the my-reel retro (deferred)
- Template `.prproj` with a pre-made 1080×1920 adjustment layer and sequence presets. This would remove the one manual step (CR color-tools 3b).
- Root cause of the silent Premiere export (upstream draft #15). Needs a minimal repro project.
- Map built-in Lumetri presets for Teal & Orange, Moody Desat, Clean Bright and Mono Drama (playbook §A3) as reels verify them.
- MCP smoke test: extend `check_tool_names.sh` to import and delete a dummy file in a scratch project, so tool regressions are caught after upgrades.
- File the upstream issues (the director decides).

## Known gaps
- Music-montage runs on CLAUDE.md §4c rules, which haven't been tested in Premiere yet. The first pilot validates them.
- The guard hook was installed 2026-10-16. Its deny path hasn't been confirmed from a real reel session yet. The first pilot should hit it once, on purpose.
