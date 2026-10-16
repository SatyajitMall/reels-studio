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
