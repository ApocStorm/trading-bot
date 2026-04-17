---
description: Midday scan — cut losers at -7%, tighten stops on winners, thesis check
---

Local-mode midday scan. No commit-and-push at the end.

STEP 1 — Read memory:
- memory/TRADING-STRATEGY.md (exit rules)
- - tail of memory/TRADE-LOG.md (entries, theses, stops)
  - - today's memory/RESEARCH-LOG.md entry
   
    - STEP 2 — Pull state:
    -   bash scripts/alpaca.sh positions
    -     bash scripts/alpaca.sh orders
   
    - STEP 3 — Cut losers. For every position where unrealized_plpc <= -0.07:
    -   bash scripts/alpaca.sh close SYM
    -     bash scripts/alpaca.sh cancel ORDER_ID
    - Log the exit to TRADE-LOG.
   
    - STEP 4 — Tighten trailing stops on winners:
    - - Up >= +20% -> trail_percent: "5"
      - - Up >= +15% -> trail_percent: "7"
        - Never within 3% of current price. Never move a stop down.
       
        - STEP 5 — Thesis check. If a thesis broke intraday, cut the position.
       
        - STEP 6 — Optional: bash scripts/perplexity.sh "<intraday query>"
        -          if something is moving sharply with no obvious cause.
       
        -      STEP 7 — Notification (only if action was taken):
        -    bash scripts/gmail.sh "Midday action $DATE" <<< "<summary>"
        -    
