# Nate's Hybrid — Cloud Routines

These five markdown files are Hybrid's **production** cloud-routine prompts.
Paste each one verbatim into its respective Claude Code cloud routine at
https://claude.ai/code/routines — do not paraphrase. The env-var checks and
commit-and-push steps are load-bearing.

| File              | Cron (America/New_York) | Purpose                                          | Status as of 2026-04-24 |
|-------------------|-------------------------|--------------------------------------------------|-------------------------|
| pre-market.md     | `0 7 * * 1-5`           | 7:00 AM weekdays — research (isolated logs)      | existing routine — re-paste with log-isolation text |
| market-open.md    | `30 9 * * 1-5`          | 9:30 AM weekdays — execute planned trades        | existing routine — re-paste with log-isolation text |
| midday.md         | `0 13 * * 1-5`          | 1:00 PM weekdays — cut losers, tighten winners   | NEW — create routine |
| daily-summary.md  | `0 16 * * 1-5`          | 4:00 PM weekdays — EOD snapshot + email recap    | NEW — create routine |
| weekly-review.md  | `0 17 * * 5`            | 5:00 PM Fridays only — week stats + letter grade | NEW — create routine |

All Hybrid routines write ONLY to `memory/hybrid/` — Samin continues to own
`memory/` at the top level. Both bots share:
- `memory/TRADING-STRATEGY.md` (shared rulebook, includes Cold-Start Entry Exception)
- `memory/GOV-WATCHLIST.md` (weekly Quiver Congressional-trade picks)

Env vars set **on the routine itself** (NOT in `.env`) — use the same
env as existing Hybrid routines, which has Alpaca keys locked to the ~$85k
paper account and Hybrid's Gmail app password.

Repo: `ApocStorm/trading-bot` (shared codebase with Samin; different Alpaca
keys per cloud-routine env gives each bot its own paper account).
