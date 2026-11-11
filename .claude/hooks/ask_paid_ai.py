#!/usr/bin/env python3
"""PreToolUse hook: every Higgsfield MCP tool call asks the director first (studio v0.10.3).

Higgsfield deducts credits on every generation made through MCP, on any plan, and the studio's AI ledger
(studio/ledger/ai-spend.jsonl) only counts OpenRouter dollars. So no session, in any permission mode that honours
hooks, may call a Higgsfield tool without the director's yes in the permission prompt. Backs up the
`permissions.ask` rule in .claude/settings.json. Rule: motion-and-ai.md §3 ("Higgsfield (MCP)").
"""
import json
import sys

try:
    event = json.load(sys.stdin)
except Exception:
    event = {}
tool = str(event.get("tool_name", ""))
if tool.startswith("mcp__higgsfield"):
    args = json.dumps(event.get("tool_input", {}), ensure_ascii=False)
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": (
            f"Higgsfield tool {tool.removeprefix('mcp__higgsfield__')} may spend credits. Director's yes needed for "
            f"every call (motion-and-ai.md §3). Input: {args[:300]}"),
    }}))
sys.exit(0)
