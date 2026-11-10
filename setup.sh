#!/usr/bin/env bash
# One-time setup for Cinematic Reels Studio (macOS, Apple Silicon or Intel).
# Run from this folder:   bash setup.sh
# Safe to re-run: each step skips itself if already done.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(pwd)"

ok()   { printf "\033[32m✓\033[0m %s\n" "$*"; }
warn() { printf "\033[33m!\033[0m %s\n" "$*"; }
step() { printf "\n\033[1m▸ %s\033[0m\n" "$*"; }

step "1/6  Checking prerequisites"
if ! command -v brew >/dev/null; then
  warn "Homebrew not found. Install it from https://brew.sh then re-run this script."; exit 1
fi
command -v node >/dev/null || brew install node
NODE_MAJOR=$(node -p 'process.versions.node.split(".")[0]')
[ "$NODE_MAJOR" -ge 20 ] || { warn "Node $NODE_MAJOR found, need 20+. Run: brew upgrade node"; exit 1; }
ok "node $(node -v)"
command -v ffmpeg >/dev/null || brew install ffmpeg
ok "ffmpeg $(ffmpeg -version | head -1 | awk '{print $3}')"
command -v python3 >/dev/null || brew install python
ok "python $(python3 --version | awk '{print $2}')"
# Apple Cinematic depth bake (Cinematic-mode footage: scripts/cine_bake.py). Needs macOS 14+ and the Command Line Tools.
if command -v swiftc >/dev/null; then
  mkdir -p scripts/bin
  if swiftc -O -o scripts/bin/cine_bake scripts/cine_bake.swift; then ok "cine_bake built (Cinematic depth bake)"
  else warn "cine_bake didn't build (needs macOS 14+). Only Cinematic-mode footage needs it."; fi
else
  warn "swiftc not found: run  xcode-select --install  then re-run, to build cine_bake (Cinematic-mode footage only)"
fi

step "2/6  Premiere Pro MCP server + CEP bridge (hetpatel-11/Adobe_Premiere_Pro_MCP)"
if ! command -v premiere-pro-mcp >/dev/null; then
  npm install -g adobe-premiere-pro-mcp
fi
ok "premiere-pro-mcp $(premiere-pro-mcp --version 2>/dev/null || echo installed)"
# Installs the CEP panel into Premiere, enables CEP debug mode,
# and registers the server with Claude Desktop / Claude Code if found.
premiere-pro-mcp --install-cep || warn "CEP install reported a problem — see output above."

step "3/6  video-use (cut inspection) + local Whisper (word-level transcripts)"
if [ ! -d .vendor/video-use/.git ]; then
  git clone --depth 1 https://github.com/browser-use/video-use .vendor/video-use
else
  git -C .vendor/video-use pull --ff-only || true
fi
python3 -m venv .venv
./.venv/bin/pip install -q --upgrade pip
./.venv/bin/pip install -q requests librosa matplotlib pillow numpy faster-whisper
mkdir -p .claude/skills
ln -sfn ../../.vendor/video-use .claude/skills/video-use
ok "video-use ready (Python env in .venv)"

step "4/6  Agent skills: Premiere MCP, HyperFrames, Instagram"
npx -y skills add hetpatel-11/Adobe_Premiere_Pro_MCP --skill premiere-pro-mcp -a claude-code -y \
  || warn "premiere-pro-mcp skill: install manually with  npx skills add hetpatel-11/Adobe_Premiere_Pro_MCP"
npx -y skills add heygen-com/hyperframes -a claude-code -y \
  || warn "hyperframes skills: install manually with  npx skills add heygen-com/hyperframes"
npx -y skills add sergebulaev/instagram-skills -a claude-code -y \
  || warn "instagram skills: install manually with  npx skills add sergebulaev/instagram-skills"

# Starter LUTs / SFX / grain (regenerable, git-ignored). Skipped if the director already has LUTs.
ls assets/luts/*.cube >/dev/null 2>&1 || ./.venv/bin/python scripts/gemini_generate_starter_pack.py

step "5/6  API keys"
if [ ! -f .env ]; then cp .env.example .env; warn "Created .env (API keys are optional: transcripts use local Whisper)."; fi
# video-use looks for .env in its own folder too
ln -sfn ../../.env .vendor/video-use/.env
grep -q '^ELEVENLABS_API_KEY=.\+' .env && ok "ElevenLabs key present (optional: transcribe_reel.sh --scribe)" || ok "No ElevenLabs key: transcripts use local Whisper"

step "6/6  Health check"
premiere-pro-mcp --doctor || warn "Doctor found issues — usually fixed by opening Premiere and starting the bridge (below)."
chmod +x scripts/*.sh

cat <<'EOF'

────────────────────────────────────────────────────────────
 Almost done — finish inside Premiere Pro (one time):
   1. Premiere Pro > Settings > Plugins > enable "UXP developer mode", restart Premiere.
   2. Window > Extensions > MCP Bridge (CEP)
   3. Temp Directory = /tmp/premiere-mcp-bridge  →  Save Configuration
   4. Start Bridge  →  Test Connection
 Then fully quit and reopen the Claude app (and/or start `claude` in this folder).

 Start a reel:   scripts/new_reel.sh my-first-reel
────────────────────────────────────────────────────────────
EOF
