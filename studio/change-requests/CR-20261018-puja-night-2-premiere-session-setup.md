# CR-20261018-puja-night-2-premiere-session-setup

| Field | Value |
|---|---|
| From reel | `projects/puja-night-2/` |
| Arch version | 0.5.0 |
| Type | skill · template · harness |
| Severity | workaround (≈ 25 min lost, 4 director round-trips) |
| Status | open |

## What happened
1. **Two projects open.** `create_project` opened `puja-night-2.prproj` *alongside* `my-reel.prproj` (the previous reel's session had left it open). `get_project_info` on the new project still reported my-reel's `Reel_my-reel_v10` as the active sequence, so any call relying on "active sequence" could have edited the finished pilot.
2. **Adjustment layer took 4 attempts.**
   - The director's File › New › Adjustment Layer landed in **my-reel.prproj** (that project's panel had focus).
   - After closing my-reel (director's OK, without saving), the director's next two attempts left nothing: the menu item is **disabled until a Project panel has focus**, and Premiere was on another macOS Space while the director's Space was a full-screen app.
   - From the editor side, `app_menu ["File","New","Adjustment Layer..."]` → "disabled"; a background `app_click` on the Project panel didn't give it focus; `app_bring_to_current_space` → "The user's current Space is a full-screen app, and a window can't be moved into a full-screen Space".
3. `export_frame` failed with `Illegal Parameter type` even **without** `format` until the output path ended in `.png` **and** `renders/stills/` existed. `projects/_template/renders/` has no `stills/`.

## Workaround used in the reel
- Every script finds the sequence by ID (`app.project.sequences[i].sequenceID`), never `activeSequence`; sets `app.project.activeSequence` before QE calls.
- Closed my-reel via `app.projects[i].closeDocument(0,0)` after the director confirmed (its file stayed at its last save).
- Editor made the adjustment layer with **full-screen control**: `request_full_control` → `request_access ["Finder"]` (needed to click the Dock) → click Premiere's Dock icon (switches Space) → click an empty spot in the Project panel → File › New › Adjustment Layer… → OK. About 3 minutes once done this way.
- Created `renders/stills/`; always pass a `.png` path to `export_frame`.

## Proposed change
- **Skill Phase 1, new step 0 "Premiere session":** list `app.projects`; if another reel's project is open, ask the director to close it (save first if it's theirs to decide) before `create_project` / `open_project`. Then all scripts address the reel's sequence by ID.
- **Skill Phase 4 step 3 / reality doc "Adjustment layer":** make it the *editor's* step, done once at reel setup right after the sequence exists, via the full-screen recipe above. Keep the director's manual click as the fallback, but its text must start with "Click an empty spot in the Project panel of `<reel>.prproj` first; the menu item is greyed out otherwise".
- **`projects/_template/renders/stills/.gitkeep`** and a reality-doc line: `export_frame` needs an existing folder and a `.png` path.

## Follow-up (round 4): bridge drop and an auto-save copy reopened
- **What happened:** the MCP Bridge heartbeat stopped at 11:41, during a 42-minute blind review, with no editor activity. `verify_premiere_connection` reported `bridge_unavailable` with Premiere running. After the director restarted the panel, the open project was `Adobe Premiere Pro Auto-Save/puja-night-2--…-11-38-31.prproj`, not `puja-night-2.prproj` (probably a crash recovery). Saving there would have forked the project.
- **Workaround:**
  1. Compared file times: the main file was saved 11:41:52, after the v4b export; the auto-save was from 11:38:31.
  2. `app.openDocument(main)`, then closed the auto-save copy with `closeDocument(0,0)`.
  3. Every script checks the project path.
- **Proposed change:** in the reality doc and skill Phase 1, after any reconnect, check `app.project.path`. If it's under `Adobe Premiere Pro Auto-Save/`, compare its time with the main file and reopen the main project (ask the director if the auto-save is newer). `verify_premiere_connection` could also warn when the open project's path is an auto-save copy.

## Follow-up (round 5): import dialog hang
- **What happened:** `app.project.importFiles([...mov], true, bin, false)` with suppressUI = true still opened Premiere's **Import Files** progress dialog. The dialog never finished, and the bridge timed out with no result. Premiere was in a full-screen Space the editor can't reach, so it took the director's screenshot to find the dialog. After the director clicked Cancel, the same import run alone in a tiny script finished in seconds.
- **Proposed change:** in the reality doc, put imports in their own small script call (never in the same call as placement, stills or save), and on a bridge timeout ask the director to look for an Import / Export / Save dialog first. Consider a `verify_premiere_connection` extension that reports "Premiere has a modal dialog open".
