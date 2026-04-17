---
description: Daily summary — EOD snapshot, day P&L, phase P&L, email recap
---

Local-mode daily summary. No commit-and-push at the end.

STEP 1 — Read memory:
- tail of memory/TRADE-LOG.md (find most recent EOD snapshot)
- Count TRADE-LOG entries dated today
- Count trades Mon-today this week

STEP 2 — Pull final state:
  bash scripts/alpaca.sh account
    bash scripts/alpaca.sh positions
      bash scripts/alpaca.sh orders

      STEP 3 — Compute:
      - Day P&L ($ and %) = today_equity - yesterday_equity
      - Phase cumulative P&L ($ and %) = today_equity - starting_equity
      - Trades today, trades this week

      STEP 4 — Append EOD snapshot to memory/TRADE-LOG.md (matching H.2 format).

      STEP 5 — Send ONE Gmail message (always, even on no-trade days):
        bash scripts/gmail.sh "EOD $DATE" <<EOF
          Portfolio: \$X (±X% day, ±X% phase)
            Cash: \$X
              Trades today: <list or none>
                Open positions: ...
                  Tomorrow: <one-line plan>
                    EOF
                    
