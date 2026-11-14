# CR-20261021-uski-aankhein-multi-project-premiere

| Field | Value |
|---|---|
| From reel | `projects/uski-aankhein/` |
| Arch version | 0.6.0 |
| Type | rule · skill · harness |
| Severity | workaround (near-miss on another reel's project) |
| Status | open |

## What happened
1. **Several projects open, one "active" project.** Premiere had pujo-ki-asolei-sobar.prproj, uski-aankhein.prproj and puja-night-2.prproj open together. `app.project` and every QE call (`qe.project.getActiveSequence()`, `addVideoEffect`, transitions) act on whichever project's sequence was last in front. Between two of my calls, a few minutes apart, it flipped from uski to Pujo. My first QE "add Lumetri" script would have added a Lumetri to a **Pujo** clip; its guard (`app.project.path != PROJP` → throw) stopped it.
2. **Manual Lumetri steps can land in another reel.** The skill's "load the .cube by hand" step assumes the right clip is selected. The director ran it while no uski clip was selected, so the Look went somewhere else (they think onto a Pujo clip). Nothing in the panel says which project or sequence it is editing. A script can't set the Look either: `Lumetri.properties[34].setValue(path)` throws `Illegal Parameter type`.
3. **Fixing it by computer use:** teach mode wasn't available in this session. Premiere ran full-screen in its own Space, so `app_bring_to_current_space` failed, and switching to it needed a Finder grant (Dock click). After that the load took 6 actions: select the V3 clip, expand Creative, open the Look dropdown, Browse, Cmd+Shift+G + path, Return.

4. **`projectItem.refreshMedia()` on a re-rendered overlay** (same name, same frame count, ProRes) returned true, but Premiere then rendered that V2 Screen layer wrongly: frame luma 0.376 vs 0.242 with the layer disabled, versus 0.249 expected. The same refresh on the V1 file was fine.

## Workaround used in the reel
- Every uski ExtendScript starts by checking `app.project.path` against the reel's own `.prproj` and re-activates its own project with `P.openSequence(seq.sequenceID)`, which reliably switched the active project.
- The `.cube` was loaded by screen control (with the director's OK) after selecting the uski V3 clip. Verified by an exported still against the local previz (luma within 0.012).
- Sent a cross-session warning to the Pujo session to check its clips' Creative > Look.

- Overlay re-renders get a new file name (`_v2`) and a fresh import + re-place instead of `refreshMedia()`. Always followed by an `export_frame` check against a local reference frame.

## Proposed change
- **Reality doc + skill Phase 1:** "one reel = one open project" is the safe default. Before Premiere work, close other reels' projects or ask the director to. If they must stay open, every script guards on `app.project.path` and calls `openSequence` first. QE never runs without that guard.
- **Skill Phase 4, manual LUT step:** the steps must start with "click the Adjustment Layer clip on V3 in the `Reel_<name>` timeline. Effect Controls must show `Reel_<name> * Adjustment Layer` at its top". Add a render check right after (Rule 2a) that the Look actually changed the picture.
- **Template:** a shared `_es_guard.jsx` header (proj(), activate(), save()) in `scripts/` so every reel's scripts start the same way.
- **Harness note:** computer use can do the `.cube` load in about a minute, but needs Premiere + Finder grants and full-screen approval. Mention it as the fallback when the director would rather not click.
