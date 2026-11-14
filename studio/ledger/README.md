# Spend ledgers (local only)

Append-only logs of paid AI generation, written by scripts and hooks, never by hand:

| File | Written by | What it records |
|---|---|---|
| `ai-spend.jsonl` | `scripts/gen_video.py` | Every OpenRouter video job (Veo 3.1 Lite / Gemini Omni): reel, shot, model, the provider's charged cost, prompt, why |
| `higgsfield-credits.jsonl` | reel sessions, after each Higgsfield MCP job (`.claude/skills/cinematic-reel/motion-and-ai.md`) | Credits spent and the balance after |

The caps they're checked against are in `studio/ai-budget.json`.

The `.jsonl` files are git-ignored: they hold one person's spend, prompts and account balance. A fresh clone starts with none, and the scripts create them on first use.
