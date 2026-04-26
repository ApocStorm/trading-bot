# Telegram message style — plain English, no trader jargon

Kevin is NOT a broker or active trader. Any Telegram message that asks
for or suggests his manual attention (strong-buy / strong-sell picks,
stop-triggered exits, mid-day actions, errors he needs to act on) MUST
be written in plain English.

The only exception is when Kevin explicitly requests a technical format
for a specific one-off purpose.

## Hard rules

1. **Always use the company's full name on first mention**, ticker
   in parentheses:
   - YES: "Fabrinet (ticker: FN)"
   - NO: "FN" or "$FN"

2. **Say what the company does** in one simple sentence. Kevin does not
   know what half these tickers are.
   - "Fabrinet makes parts for data-center computers."
   - "GE Vernova is a power-grid and electrification company."
   - "XLE is an exchange-traded fund that owns energy stocks."

3. **Translate every piece of trader shorthand**:
   | Jargon | Plain English |
   |---|---|
   | 10% trailing stop GTC | automatic sell order if the stock drops 10% from its highest price |
   | R:R 2:1 | if it works we make about twice what we'd lose if it doesn't |
   | Position cap / at 6/6 | your portfolio is full |
   | Max 3 trades/week | we've already used this week's trade quota |
   | unrealized P&L +$X | up $X on your cost basis |
   | "SWAP: Sell X → Buy Y" | Swap idea: if you want to make room, sell X and buy Y instead |
   | 50-MA breach | stock fell below its 50-day average (a warning sign) |
   | RS rank dropped | stock is underperforming the market recently |
   | VCP / CANSLIM / M-filter | (just omit — explain the conclusion, not the method) |
   | FTD fired | market trend turned favorable |
   | PDT / daytrade count | (omit — internal bookkeeping, not Kevin's problem) |
   | CPI / PPI / FOMC | (name the event plainly: "inflation data", "Fed meeting") |

4. **Start with what Kevin should do** (or that there's nothing to do):
   - "Nothing will happen automatically — these are just ideas."
   - "If you want to act, here's the top pick."
   - "Your portfolio is full, so these would require a swap."
   - "Heads up: we sold a position automatically — here's what and why."

5. **Use "up X%" / "down X%"**, not "+X%" / "-X%".

6. **End with a one-line account summary**: equity and what's cash vs
   invested.

7. **No emojis in the message body** — the leading 🟢 / 🟡 / 🔴 status
   flag is the only one. Don't decorate.

8. **Keep it under 15 lines where possible.** If the bot has more detail
   to share, put it in the log file and summarize in Telegram.

## Template — Strong-Rec pre-market message

```
🟢 <BOT NAME> — <weekday> picks

<One-line state: what Kevin needs to know up front. E.g.
"Your portfolio is full, so these are just ideas" or
"You have 4 open slots, so the bot can buy these Monday morning".>

TOP PICK TO BUY: <Company (ticker: SYM)>, about <price> a share.
<What the company does in one sentence.> <Why we like it in plain
English — catalysts, momentum, analyst upgrades, whatever matters.>
<If applicable: cost and % of account a normal-sized buy would use.>

SECOND PICK: <same format, shorter.>
THIRD PICK: <same format, shorter.>

SELL / TRIM IDEAS (omit this section if no positions held):
<For each held stock that's weakest, one plain-English line.
If at cap and a top pick is better than a held stock, say so as
a "Swap idea".>

Account: about $<equity>, <cash status>.
```

## Template — stop-triggered / mid-day exit message

```
🟡 <BOT NAME> — sold <Company (ticker: SYM)>

<Plain reason: "dropped below our auto-sell threshold" or "broke key
support" or "thesis changed".>
Bought at $X. Sold at $Y. <Profit or loss in dollars and percent.>

Account: about $<equity>, <cash position>.
```

## Template — error / issue message

```
🔴 <BOT NAME> — problem this morning

<Plain description of what went wrong — no stack traces, no API error
codes in raw form.> <What Kevin can/should do about it, or "I'll try
again on the next scheduled run".>
```

## Do-not-send policy

- If the run completed routine work (no trades, no alerts, no picks),
  stay silent. No "nothing to report" pings.
- Exception: the STRONG-REC pre-market Telegram ALWAYS fires, per
  Kevin's 2026-04-24 directive — even on days when caps block execution.
