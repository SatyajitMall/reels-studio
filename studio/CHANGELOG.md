# Studio Changelog

## 0.2.2 — 2026-10-16
Found while preparing the first pilot (`my-reel`: 77 iPhone 17 / Blackmagic Cam clips, mostly 25 fps).
- **Rule: sequence frame rate matches the footage** (CLAUDE.md §3, skill Phase 3).
  - The most common frame rate in the footage wins.
  - Outlier clips are conformed with `speed_change`.
  - This replaces the old "30 fps default", which would have made 25 fps footage stutter.
- **New: `scripts/link_footage.sh <reel> <dir> [a-roll|b-roll]`.**
  - Symlinks footage that lives outside the studio into `raw/` and records it in `raw/SOURCES.md`.
  - Originals are never copied or moved.
  - Skips macOS `._*` files and camera `Proxy/` folders.
  - Safe to re-run.
- **Fix: `analyze_footage.py` skips `._*` metadata files** when scanning a folder.

## 0.2.1 — 2026-10-16
- **New: `scripts/check_tool_names.sh`.** It lists the Premiere MCP server's tools over stdio and fails if any tool name in `CLAUDE.md` or the cinematic-reel skill and playbook doesn't exist. Premiere doesn't need to be running. Result today: all 52 names are valid against server 1.2.9 (283 tools).
- **Gemini review triage.**
  - G4 (move graphics above the grade): rejected by the director.
  - G5 (wrong tool names): rejected; the check above shows the claim is false.
- Guard hook installed (`.claude/settings.json`).

## 0.2.0 — 2026-10-15
- **HQ / reel-session split.**
  - Each reel is its own sub-project, edited in its own session.
  - One HQ session owns the architecture (`studio/ARCHITECTURE.md`).
- **Guard hook.** `.claude/hooks/guard_architecture.py` blocks edits to HQ-owned files from reel sessions. The hook is staged in `studio/harness/settings.json`. It becomes active once installed into `.claude/settings.json`.
- **Change requests.** Reel sessions file them in `studio/change-requests/`, and HQ triages them with `/studio-hq`.
- **Pilot programme.**
  - Every pilot reel keeps a friction log.
  - Every pilot reel writes a `retro.md`, copied to `studio/retros/`.
- **Reel types.** `talking-head`, `music-montage` and `hybrid` are now defined. Music-montage cuts on the music's beat grid and skips transcription.
- **`project.md` fields.** The template now records the architecture version, reel type and pilot flag. `new_reel.sh` fills in the version.

## 0.1.0 — 2026-10-15
- Initial bootstrap. Covers:
  - `CLAUDE.md` contract;
  - `/cinematic-reel` skill and effects playbook;
  - analysis and transcription scripts;
  - Premiere MCP setup.
