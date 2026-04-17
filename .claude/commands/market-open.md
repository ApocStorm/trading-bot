---
description: Market-open execution — validate today's plan, run buy-side gate, place trades + trailing stops
---

Local-mode market-open execution. No commit-and-push at the end (you push
manually).

STEP 1 — Read memory for today's plan:
- memory/TRADING-STRATEGY.md
- TODAY's entry in memory/RESEARCH-LOG.md (if missing, run /pre-market first)
- tail of memory/TRADE-LOG.md (for weekly trade count)

STEP 2 — Re-validate with live data:
  bash scripts/alpaca.sh account
    bash scripts/alpaca.sh positions
      bash scripts/alpaca.sh quote <each planned ticker>

      STEP 3 — Hard-check rules BEFORE every order. Skip any trade that fails:
      - Total positions after trade <= 6
      - Trades this week <= 3
      - Position cost <= 20% of equity
      - Position cost <= available cash
      - Catalyst documented in today's RESEARCH-LOG
      - daytrade_count leaves room
      - Instrument is a stock

      STEP 4 — Execute buys (day TIF market orders):
        bash scripts/alpaca.sh order '{"symbol":"SYM","qty":"N","side":"buy","type":"market","time_in_force":"day"}'

        STEP 5 — Immediately place 10% trailing stop GTC:
          bash scripts/alpaca.sh order '{"symbol":"SYM","qty":"N","side":"sell","type":"trailing_stop","trail_percent":"10","time_in_force":"gtc"}'
          PDT-blocked fallback: fixed stop 10% below entry.

          STEP 6 — Append each trade to memory/TRADE-LOG.md.

          STEP 7 — Notification (only if a trade was placed):
            bash scripts/gmail.sh "Market-open trades $DATE" <<< "<summary>"
            
