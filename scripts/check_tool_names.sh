#!/usr/bin/env bash
# Check that every Premiere MCP tool name the studio rules mention exists in the installed server.
# Lists tools over MCP stdio (Premiere doesn't need to be running). Run after upgrading adobe-premiere-pro-mcp.
# Usage: scripts/check_tool_names.sh        exit 1 if a rule names a tool the server doesn't have
set -euo pipefail
cd "$(dirname "$0")/.."
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

( printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"studio-check","version":"0"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'; sleep 6 ) \
  | PREMIERE_MCP_TOOLSET=full PREMIERE_MCP_TELEMETRY=0 PREMIERE_TEMP_DIR=/tmp/premiere-mcp-bridge \
    premiere-pro-mcp 2>/dev/null > "$TMP/out.jsonl" || true

python3 - "$TMP/out.jsonl" CLAUDE.md .claude/skills/cinematic-reel/SKILL.md .claude/skills/cinematic-reel/effects-playbook.md <<'EOF'
import json, re, sys
from pathlib import Path
tools = set()
for line in open(sys.argv[1]):
    try:
        msg = json.loads(line)
    except ValueError:
        continue
    if msg.get("id") == 2:
        tools = {t["name"] for t in msg["result"]["tools"]}
if not tools:
    sys.exit("✗ Couldn't list tools: is premiere-pro-mcp on PATH?")
# Our own scripts, files and resources share the snake_case shape; they aren't MCP tools.
ours = {p.stem for p in Path("scripts").iterdir()} | {
    "audio_summary", "takes_packed", "timeline_view", "pack_transcripts", "get_instructions"}
# Look ids from the film-stock table (effects-playbook §A3) are defined in look_preview.py
ours |= set(re.findall(r'^\s+"([a-z0-9_]+)": \(', Path("scripts/look_preview.py").read_text(), re.M))
missing = {}
for f in sys.argv[2:]:
    for name in set(re.findall(r"`([a-z]+(?:_[a-z0-9]+)+)`", Path(f).read_text())):
        if name not in tools and name not in ours:
            missing.setdefault(name, []).append(f)
print(f"server: {len(tools)} tools")
for name, files in sorted(missing.items()):
    print(f"✗ {name}  ({', '.join(files)})")
if missing:
    sys.exit(1)
print("✓ every tool name in the rules exists")
EOF
