# Hybrid Trade Log

Nate's Hybrid bot trade log — isolated from Samin's memory/TRADE-LOG.md.
Same strategy doc (memory/TRADING-STRATEGY.md), different Alpaca paper account (~$85k).

## Open Positions

| Ticker | Qty | Entry | Cost basis | Stop type | Stop floor | HWM | Stop order |
|---|---|---|---|---|---|---|---|
| XLE | 75 | $56.63 | $4,247.25 | GTC trailing 10% | $51.417 | $57.13 | c7682c8e-b399-497a-8660-b1a0fbb54907 |

## History

## 2026-04-23  XLE  BUY  75 @ $56.63

- **Thesis:** Cold-Start Entry Exception — first deployment for Hybrid bot on a fresh ~$85k paper account. Energy sector ETF (XLE) chosen as a defensive opening salvo while the strategy's full pre-market candidate engine wasn't yet wired.
- **Sizing:** $4,247.25 cost basis = **~5.0%** of $85k equity (well inside the 20% per-position cap; conservative first-trade size).
- **Order:** market buy filled 2026-04-23 14:32:55 UTC (10:32:55 ET) at $56.63.
- **Stop:** GTC trailing_stop 10% placed 2026-04-23 14:33:12 UTC (18 sec after fill). Order ID `c7682c8e-b399-497a-8660-b1a0fbb54907`. Initial stop floor $50.97 (10% off entry).
- **As of 2026-04-26 (Sun, log seed):** XLE last $56.87, unrealized **+$18.00 (+0.42%)**, HWM $57.13, stop floor ratcheted to **$51.417**. Headroom −9.59%. Still in 10%-trail tier (not at +15% ratchet to 7%).
- **Skill / route:** Cold-Start Entry Exception (manual, not via pre-market routine — pre-market candidate engine not yet running for Hybrid as of this trade).

---

## Migration note

This entry was seeded 2026-04-26 (Sun, pre-Monday-soft-launch audit) from Alpaca order history + position state, since the original log entry on 2026-04-23 went into the shared `memory/TRADE-LOG.md` (Samin's log) before the Hybrid log isolation was set up on 2026-04-24. Authoritative current state still comes from `bash scripts/alpaca.sh positions` and `... orders` — this file is the rationale/ratchet history that Alpaca alone can't provide.

---

### Apr 28 — Hybrid EOD Snapshot (Day 4, Tuesday)
**Portfolio:** $85,078.75 | **Cash:** $80,752.75 (94.9%) | **Day P&L:** +$68.25 (+0.080%) | **Phase P&L:** +$78.75 (+0.093%)

| Ticker | Shares | Entry | Close | Day Chg | Unrealized P&L | Stop |
|---|---|---|---|---|---|---|
| XLE | 75 | $56.63 | $57.68 | +1.60% | +$78.75 (+1.85%) | $51.417 (10% trail) |

**Trades today:** none. **Trades this week:** 0 of 3 used.
**Notes:** Quiet day. Sole holding XLE (energy-sector ETF) drifted up about 1.6% with a positive pre-open print, lifting equity by $68 from yesterday's close of $85,010.50. Trailing stop sits at $51.42 — well below the current $57.68, so no risk of an automatic sale today. Cash remains ~95% of the book; no candidate cleared the entry filters this morning so the bot stayed flat. Stop ratchet still in the 10% tier (XLE not yet up 15% from cost). Note: this snapshot was written by the scheduled summary run at 10:55 UTC (06:55 ET), before regular-session open — the "close" prices reflect Alpaca's most-recent quote (pre-market) rather than the formal 4 PM ET close.
