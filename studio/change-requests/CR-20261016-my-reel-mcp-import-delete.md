# CR-20261016-my-reel-mcp-import-delete

| Field | Value |
|---|---|
| From reel | `projects/my-reel/` |
| Arch version | 0.2.5 |
| Type | harness |
| Severity | workaround |
| Status | done v0.3.1 |

## What happened
Premiere 26.5.2, adobe-premiere-pro-mcp:
- `delete_multiple_project_items {itemIds:[…]}` → `deleteResults.filter is not a function`.
- `delete_project_item` on footage → `{"deleted":true,"method":"deleteBin"}` but the item stays in the project (17/17 sample clips).
- `import_folder` → `ReferenceError: targetBin.importFiles is not a function` for every file.
- `import_media` with `binName` → succeeds but the item lands in the project root.
- `execute_extendscript` and `evaluate_expression` return `"undefined"` / `{type:"undefined"}` instead of the script's last value.
- `export_frame` with `format:"png"` → `Error: Illegal Parameter type`; works when `format` is omitted.

## Workaround used in the reel
`execute_extendscript`:
- import: `app.project.importFiles(paths, true, targetBin, false)`;
- delete footage: create a temp bin, `item.moveBin(tempBin)`, then `tempBin.deleteBin()`;
- verify with `list_project_items` (script output can't be read).

## Proposed change
1. Report the bugs upstream (hetpatel-11/Adobe_Premiere_Pro_MCP).
2. Until fixed, add a "known-broken tools + workaround snippets" box to `CLAUDE.md` §2 (or the `premiere-pro-mcp` skill) and to the `/cinematic-reel` Phase 1 sample-media step, which currently says to use `delete_multiple_project_items`.
3. Optionally extend `scripts/check_tool_names.sh` into a smoke test that imports/deletes a dummy file in a scratch project.

## HQ decision
**Accepted, done in v0.3.1.** New `.claude/skills/cinematic-reel/premiere-mcp-reality.md` lists every broken tool with its verified snippet: import, temp-bin delete, script→file results, `export_frame` without `format`. CLAUDE.md §2 points to it. The skill's sample-media and import steps now use the snippets. Upstream issues are drafted in `studio/upstream/premiere-mcp-issues.md` (not filed: the director decides). The smoke-test idea is deferred to the backlog.

## Follow-up from my-reel v9 (2026-10-17, reel session)
`replace_clip {clipId, newProjectItemId, preserveEffects: true}` is destructive on 26.5.2. It returned `success:false, replaced:true, "settings were not fully restored: motion scale"` and actually:
- placed each replacement at its **full media length** from the clip's start, overwriting the next clip(s): 4 calls cut C029/C034, shifted C006/C072 and left 2 gaps;
- added the media's audio on A1;
- dropped the adjacent V1 transitions (3);
- kept Lumetri but lost every Motion keyframe.

Verified workaround (reel-local scripts):
1. `old.remove(false,false)`;
2. `item.setInPoint(in,4)` / `setOutPoint(in+dur,4)`;
3. `V1.overwriteClip(item, start)`, then clear the item's in/out;
4. remove the same-named audio clip at `start`;
5. `trackItem.end = Time(start+dur)` (3 of 5 came in 1 frame short);
6. `color_correct` once (contrast/temp/tint), then the Lumetri script;
7. re-key Motion;
8. re-add the transitions via QE.

Proposed: mark `replace_clip` broken in `premiere-mcp-reality.md` and ship this as a `scripts/` helper (swap_clip.jsx).
