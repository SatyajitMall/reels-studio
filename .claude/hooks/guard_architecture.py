#!/usr/bin/env python3
"""Studio harness guard: only the HQ session may edit architecture files.

Wired in .claude/settings.json for two events:
- UserPromptSubmit: a prompt starting with /studio-hq claims HQ for that session
  (writes its session_id to .claude/state/hq_session).
- PreToolUse (Edit|Write|MultiEdit|NotebookEdit): denies edits to HQ-owned paths
  from any other session, pointing it at studio/change-requests/ instead.

Shell writes (Bash) are not intercepted; CLAUDE.md §0.1 covers those by rule.
See studio/ARCHITECTURE.md for the ownership table.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2]).resolve()
MARKER = ROOT / ".claude/state/hq_session"

# HQ-owned: files and folder prefixes, relative to ROOT.
PROTECTED_FILES = {"CLAUDE.md", "README.md", "setup.sh", ".mcp.json"}
PROTECTED_DIRS = (".claude/", "scripts/", "studio/", "projects/_template/")
# Carve-outs inside protected dirs that reel sessions may write.
ALLOWED_DIRS = ("studio/change-requests/", "studio/retros/")


def hq_session() -> str:
    try:
        return MARKER.read_text().strip()
    except OSError:
        return ""


def is_protected(path: str) -> bool:
    try:
        rel = Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return False  # outside the studio
    if rel.startswith(ALLOWED_DIRS):
        return False
    return rel in PROTECTED_FILES or rel.startswith(PROTECTED_DIRS)


def main() -> None:
    data = json.load(sys.stdin)
    event = data.get("hook_event_name")
    session = data.get("session_id", "")

    if event == "UserPromptSubmit":
        if data.get("prompt", "").lstrip().startswith("/studio-hq") and session:
            MARKER.parent.mkdir(parents=True, exist_ok=True)
            MARKER.write_text(session + "\n")
        return

    if event == "PreToolUse":
        inp = data.get("tool_input", {})
        path = inp.get("file_path") or inp.get("notebook_path") or ""
        if not path or not is_protected(path) or session == hq_session():
            return
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"{path} is HQ-owned studio architecture. Reel sessions don't edit it. "
                "Work around it inside projects/<reel>/ and file a change request in "
                "studio/change-requests/ (see _TEMPLATE.md) for the HQ session to apply."
            ),
        }}))


if __name__ == "__main__":
    main()
