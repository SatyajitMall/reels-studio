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
| G6 | Premiere tone-maps iPhone HLG before grading, so a Log LUT blows it out | Check on the first iPhone HDR clip in a pilot | open. `my-reel` footage is Rec.709 SDR, so it isn't tested there. Since v0.6.1: the ffmpeg route can't tone-map either (no `zscale` in this build), so Premiere is the only path for now |
| G7 | `scripts/gemini_setup_premiere_mcp.sh` (added 2026-10-16): setup with an npm fallback for a root-owned `/usr/local`, plus CEP debug mode for CSXS 9–16 (doctor covers 10–12) | Fold its npm-prefix fallback into `setup.sh`. Enable more CSXS versions only if the panel doesn't show in Premiere | open. File left untracked |

## From the my-reel retro (deferred)
- Template `.prproj` with a pre-made 1080×1920 adjustment layer and sequence presets. This would remove the one manual step (CR color-tools 3b).
- Root cause of the silent Premiere export (upstream draft #15). Needs a minimal repro project.
- Map built-in Lumetri presets for Teal & Orange, Moody Desat, Clean Bright and Mono Drama (playbook §A3) as reels verify them.
- MCP smoke test: extend `check_tool_names.sh` to import and delete a dummy file in a scratch project, so tool regressions are caught after upgrades.
- File the upstream issues (the director decides).

## After Effects (from v0.4.0)
- Option: `@kumoproductions/mcp-aftereffects` (MIT, released 2026-10-16, 1 contributor, no panel needed). It's a richer AE MCP; adopting it is a dependency call for the director. Revisit once it has more history.
- AE 26.5 ships Adobe's own MCP server (`Contents/Required/MCP Server.plugin`). It's disabled behind a beta gate; recheck in later AE builds.
- Paid plugins (director decides): Neat Video (much stronger denoise than Remove Grain), Twixtor, RSMB, Deep Glow.
- `aerender` starts a second AE per shot (about 4 min each). If render time hurts, try `-reuse` or rendering from AE's own queue.
- ProRes 422 HQ needs a custom output-module template made once in AE's UI; today we use "High Quality" (ProRes 422).

## Motion graphics / AI (from v0.5.1)
- Verify the Premiere import of a HyperFrames ProRes 4444 alpha MOV on V5 (first real use).
- ~~Verify the first real OpenRouter call~~: done 2026-10-18 ($0.12, `data:` URL first frame OK, 24 fps output). Still unverified: the Google fallback (its `predictLongRunning` vs `generateContent` note), if it's ever needed.
- Text behind the subject on moving shots needs motion tracking: either track the word to the subject, or limit it to holds (as now).
- Gemini Omni video-to-video restyle (the creator's "text behind the head"): not on Google's pricing page as of 2026-10-18. `text_behind.py` covers the need locally for free.
- A per-format motion-graphics kit (reusable title, end card and lower-third in the director's style) once v0.5.1-style formats exist.

## From v0.6.0 (playbooks + the WeAreNoCode kit)
- **Group B: talking-head tools (target v0.7.0):** an audio cut audit (clipped words at cut edges; his most important finding), a paper-cut script from the transcript, dead-air detection on the cut, a local transcription option (Parakeet / Whisper, see G2), and camera-move helpers for the `creator-explainer` rules. Build them before or during the first talking-head pilot.
- **`creator-explainer` needs its pilot.** Every rule is adapted from 16:9 YouTube; log every misfit as a CR.
- **Premiere lock:** three reel sessions contend for one Premiere. A lock file (session, reel, since) checked before mutating tools, released at wrap-up.
- **A final re-review step** after the review gate's last loop, so the fixes from loop 2 are seen by the reviewer too.
- `CR-20261017-my-reel-directional-blur-scan`: one-directional smear and blur straddling a cut in `frame_scan.py`.
- `colour_report.py`: exclude designed fades from the crushed-shadows count.
- `CR-20261017-my-reel-qa-visual-review` leftovers.
- After Effects ops still missing: `light_rays`, and handles on trimmed shots.
- ffmpeg build without libzimg (`zscale`) and freetype (`drawtext`). An ffmpeg with both would enable HDR → SDR tone-mapping and labelled sheets in one pass. That's an install the director decides on (it changes a system tool).
- Optional `scripts/look_preview.py`: if Round 2 look sheets get used on every reel, turn the tested recipe (ffmpeg tiles + Pillow labels) into a script.
- Instagram plugin: needs the director's Graph API token via `instagram:configure`. Read-only use (insights, comments) recommended; posting only with approval per post.

## Known gaps
- Music-montage runs on CLAUDE.md §4c rules, which haven't been tested in Premiere yet. The first pilot validates them.
- The guard hook was installed 2026-10-16. Its deny path hasn't been confirmed from a real reel session yet. The first pilot should hit it once, on purpose.
