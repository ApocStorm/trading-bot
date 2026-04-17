---
description: Friday weekly review — week stats, what worked/didn't, letter grade
---

Local-mode weekly review. No commit-and-push at the end.

STEP 1 — Read memory:
- memory/WEEKLY-REVIEW.md (match existing template)
- ALL this week's entries in memory/TRADE-LOG.md
- ALL this week's entries in memory/RESEARCH-LOG.md
- memory/TRADING-STRATEGY.md

STEP 2 — Pull week-end state:
  bash scripts/alpaca.sh account
    bash scripts/alpaca.sh positions

    STEP 3 — Compute the week's metrics: starting portfolio, ending portfolio,
    week return ($/%), S&P 500 week return, trades W/L/open, win rate, best/worst,
    profit factor.

    STEP 4 — Append full review section to memory/WEEKLY-REVIEW.md (H.4 format).

    STEP 5 — If a rule needs to change (proven out for 2+ weeks or failed badly),
    update memory/TRADING-STRATEGY.md too.

    STEP 6 — Send ONE Gmail message (<=15 lines):
      bash scripts/gmail.sh "Weekly review — week ending $DATE" <<EOF
        ...
          EOF
          
