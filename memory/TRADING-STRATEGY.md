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

## Priors from the Field (2026)
These are starting biases informed by publicly documented Claude-Code trading
experiments. They are not rules — they are starting beliefs the weekly review
should challenge or confirm.

- **Fewer trades tend to beat more trades.** In one 15-strategy backtest by
  "ji_ai" on 90 days of 5-minute data, the only surviving strategy was EMA
  momentum — which also had the fewest trades of any candidate. Treat the
  "Max 3 new trades/week" cap as a ceiling, not a target. A week with zero
  trades is often the right answer.
- **The harness, not the model, keeps the bot safe.** The buy-side gate above
  is the single most important piece of code in this repo. Never bypass it
  "just this once."
- **Single options trade can undo a month of gains.** This is why rule #1 is
  absolute. If a future idea ever involves derivatives, the strategy doc
  must be changed first, in a separate commit, before any such order.
- **Claude's pre-market research is only as good as the citations.** Every
  trade idea in RESEARCH-LOG must name the source of its catalyst. No
  anonymous hunches.
