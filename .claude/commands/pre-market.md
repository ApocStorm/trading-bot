---
description: Pre-market research — account snapshot, market context, trade ideas, risk factors, decision
---

Local-mode pre-market research. No commit-and-push (you're on the main branch
locally; commit yourself if you want the entry saved).

Resolve today's date: DATE=$(date +%Y-%m-%d).

STEP 1 — Read memory for context:
- memory/TRADING-STRATEGY.md
- tail of memory/TRADE-LOG.md
- tail of memory/RESEARCH-LOG.md

STEP 2 — Pull live account state:
  bash scripts/alpaca.sh account
    bash scripts/alpaca.sh positions
      bash scripts/alpaca.sh orders

      STEP 3 — Research market context via Perplexity:
        bash scripts/perplexity.sh "WTI and Brent oil price right now"
          bash scripts/perplexity.sh "S&P 500 futures premarket today"
            bash scripts/perplexity.sh "VIX level today"
              bash scripts/perplexity.sh "Top stock market catalysts today $DATE"
                bash scripts/perplexity.sh "Earnings reports today before market open"
                  bash scripts/perplexity.sh "Economic calendar today CPI PPI FOMC jobs data"
                    bash scripts/perplexity.sh "S&P 500 sector momentum YTD"
                      bash scripts/perplexity.sh "News on <each currently-held ticker>"

                      If Perplexity exits 3, fall back to native WebSearch.

                      STEP 4 — Write a dated entry to memory/RESEARCH-LOG.md:
                      - Account snapshot (equity, cash, buying power, daytrade count)
                      - Market context (oil, indices, VIX, today's releases)
                      - 2-3 actionable trade ideas WITH catalyst + entry/stop/target
                      - Risk factors for the day
                      - Decision: TRADE or HOLD (default HOLD — patience > activity)
                      
