# Trade Log

## Day 0 — EOD Snapshot (pre-launch baseline)
**Portfolio:** $10,000.00 | **Cash:** $10,000.00 (100%) | **Day P&L:** $0 | **Phase P&L:** $0

No positions yet. Bot launches tomorrow.

## 2026-04-23 — Market Open

| Date | Ticker | Side | Shares | Entry | Stop | Thesis | Target | R:R |
|------|--------|------|--------|-------|------|--------|--------|-----|
| 2026-04-23 | XLE | BUY | 75 | $56.63 | 10% GTC trail (stop $51.09) | Energy YTD leader, WTI bid on Iran, data-center power demand | +15% (~$65.12) | ~1.5:1 |

- Cost basis: $4,247.25 (~5% equity) — starter size, cold-start exception
- Trailing stop verified: `type=trailing_stop`, `time_in_force=gtc`, `trail_percent=10`
- Weekly trade count: 1/3

## 2026-04-28 — Midday Scan

| Date | Ticker | Side | Shares | Entry | Exit | UPL | UPL% | Notes |
|------|--------|------|--------|-------|------|-----|------|-------|
| 2026-04-28 | FN | SELL | 10 | $723.55 | queued (mkt sell at next open) | -$675.50 | -9.34% | Cut at -7% per rule (actual -9.34%) |

- Cancelled trailing stop GTC (id 69d64c4e-9fb4-41bf-9f33-10524d2dd329) at 11:19:00 UTC.
- Submitted market sell DAY (id 219d83ff-4920-48e3-a8b7-b3b0ddf3a80a) at 11:19:05 UTC; market was closed (pre-market 7:19 ET) — order queued for 9:30 ET open.
- Mark price at decision: $656.00 (last close bid in pre-market $650 / ask $686).
- Reason: -9.34% breaches -7% manual cut threshold per TRADING-STRATEGY sell-side rules. JPM cut to neutral last week added thesis pressure but not the trigger; -7% rule is the trigger.
- Realized P&L will be confirmed after 9:30 ET fill; addendum to be appended by next routine.
- Position count after: 4/6. Weekly trade count: confirm against live count (TRADE-LOG was stale prior to this entry).

