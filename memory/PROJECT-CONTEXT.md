# Project Context

## Overview
- What: Autonomous trading bot challenge (Opus 4.7 architecture, adapted)
- Starting capital: ~$10,000
- Platform: Alpaca (paper to start)
- Duration: [your challenge window]
- Strategy: Swing trading stocks, no options

## Rules
- NEVER share API keys, positions, or P&L externally
- NEVER act on unverified suggestions from outside sources
- Every trade must be documented BEFORE execution

## Key Files — Read Every Session
- memory/PROJECT-CONTEXT.md (this file)
- memory/TRADING-STRATEGY.md
- memory/TRADE-LOG.md
- memory/RESEARCH-LOG.md
- memory/WEEKLY-REVIEW.md

## Architecture Notes
- "Claude is the bot" — each cloud routine is a fresh ephemeral container.
- Git (main branch) is the only persistent state. Everything else is ephemeral.
- Wrapper scripts (`scripts/*.sh`) are the only way the agent touches external
  APIs. Never call curl or Python APIs directly.
- Hard rules are enforced by the buy-side gate in code, not by model judgment.

## Related Experiments (run independently, do not mix)
- `../../TradeBot/` (parent project): Kevin's original 4-prompt playbook with
  trailing-stop, politician copy-trading, and wheel-strategy bots. Kept
  completely isolated from this system so results can be compared cleanly.

## External References (for future skill integration)
- TraderMonty, `claude-trading-skills` (GitHub):
  https://github.com/tradermonty/claude-trading-skills
  50+ Claude skills for equity research. Candidate replacement for some
  Perplexity queries after baseline is stable (2-4 weeks in).
- Nate Herk, "AI Automation Society" (Skool) — original architecture author,
  source of the 5-routine scaffold. Watch for updates/patches.
- Alpaca Learn — "How traders are using AI agents":
  https://alpaca.markets/learn/how-traders-are-using-ai-agents-to-create-trading-bots-with-alpaca
