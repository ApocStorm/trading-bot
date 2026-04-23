# Trading Strategy

## Mission
Beat the S&P 500 over the challenge window. Stocks only — no options, ever.

## Capital & Constraints
- Starting capital: ~$10,000
- Platform: Alpaca (paper to start)
- Instruments: Stocks ONLY
- PDT limit: 3 day trades per 5 rolling days (account < $25k)

## Core Rules
1. NO OPTIONS — ever.
2. 75-85% deployed
3. 5-6 positions at a time, max 20% each
4. 10% trailing stop on every position as a real GTC order
5. Cut losers at -7% manually
6. Tighten trail: 7% at +15%, 5% at +20%
7. Never within 3% of current price; never move a stop down
8. Max 3 new trades per week
9. Follow sector momentum
10. Exit a sector after 2 consecutive failed trades
11. Patience > activity

## Entry Checklist
- Specific catalyst?
- Sector in momentum?
- Stop level (7-10% below entry)
- Target (min 2:1 R:R)

## Buy-side Gate (programmatic, before every order)
Every single check must pass. If any fail, skip the trade and log the reason.
- Total positions after fill <= 6
- Trades placed this week (including this one) <= 3
- Position cost <= 20% of account equity
- Position cost <= available cash
- Pattern-day-trader count leaves room (< 3 on sub-$25k account)
- A specific catalyst is documented in today's RESEARCH-LOG entry
- The instrument is a stock (not an option, not anything else)

## Sell-side Rules
Evaluated at the midday scan and opportunistically.
- If unrealized loss is -7% or worse, close immediately.
- If the thesis has broken (catalyst invalidated, sector rolling over, news
  event), close, even if not yet at -7%.
- If up +20% or more, tighten trailing stop to 5%.
- If up +15% or more, tighten trailing stop to 7%.
- If a sector has two consecutive failed trades, exit all positions in that
  sector.

## Cold-Start Entry Exception
When cash > 50% of equity AND no positions have been held for > 1 trading day,
the normal "pullback-and-reclaim" filter is relaxed:

- A ticker is eligible for entry if it is within 5% of its 20-day simple
  moving average (not in clear chase territory near a recent extension high).
- Up to 2 positions at starter size (3-5% equity each) may be taken per
  market-open run from the top-ranked ideas in today's RESEARCH-LOG, provided
  all other buy-side gates pass: catalyst documented, PDT room
  (daytrade_count < 3), stock only (no options, ever), weekly trade count
  after fill <= 3.
- 10% GTC trailing stop is placed immediately after fill, same as normal flow.
- This exception auto-disables once the account holds any position for a full
  trading day. After that, normal rules apply.
- Rationale: a cold-start bot should build a base. Idle cash is not
  discipline, it is absence from the market. Research that identifies real
  catalysts should produce at least a starter position unless every candidate
  is in chase territory.

## Stop Hygiene
Every position MUST have a live GTC trailing-stop sell order at the trail %
required by the ratchet rule (10% default → 7% at +15% gain → 5% at +20%).
This is enforced by the stops watchdog cron, but every routine that places
a stop also has to do its part:

1. After placing any stop, **verify the response**: it must come back as
   `type=trailing_stop` AND `time_in_force=gtc`. Anything else (a fixed
   stop, a day-TIF order, an OTO child stop submitted before fill, a
   PDT-blocked fallback that got accepted as a fixed stop) is a *partial*
   stop that needs to be converted later.

2. **Tag every partial stop in TRADE-LOG.md** on its own line, with this
   exact format so the watchdog and grep can find it:
