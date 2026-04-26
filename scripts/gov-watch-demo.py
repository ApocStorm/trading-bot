#!/usr/bin/env python3
"""
gov-watch-demo.py — Proof-of-concept for the Gov-Watch weekly module.

PURPOSE
    Simulates what the proposed Sunday-evening gov-watch routine would do:
    pull recent Congressional STOCK Act disclosures from top-performing
    legislators, apply the "post-disclosure spike now flattened" filter
    using real price data, and write a ranked watchlist that pre-market.md
    can consume the next morning.

DATA SOURCE
    Demo version: hardcoded list of real recent disclosures surfaced via
    Perplexity/WebSearch (no scraping, no subscription needed).
    Production version: replace DISCLOSURES with a call to Quiver's
    /beta/bulk/congresstrading endpoint (paid, ~$30/mo). The rest of the
    pipeline (filter / score / output) is unchanged.

PRICE DATA
    yfinance (free). Production can swap to Alpaca via scripts/alpaca.sh
    for consistency with the rest of the bot.

USAGE
    python3 scripts/gov-watch-demo.py
    -> writes memory/GOV-WATCHLIST.md
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# ============================================================
# 1. INPUT — recent real disclosures (demo data, verified via public trackers)
#    In production this list comes from Quiver API, filtered to:
#    - top-performing cohort (2025 return > 30% OR Pelosi/Gottheimer/Khanna)
#    - trade type = buy/stock (no options, no sells)
#    - filed within last 30 days
# ============================================================

DISCLOSURES = [
    # Gottheimer — active buyer through Q1 2026
    {"legislator": "Josh Gottheimer",  "ticker": "GEV",   "type": "stock", "disc_date": "2026-02-15", "amount_max": 250000,  "cohort": "active_buyer"},
    {"legislator": "Josh Gottheimer",  "ticker": "APD",   "type": "stock", "disc_date": "2026-04-02", "amount_max": 100000,  "cohort": "active_buyer"},
    {"legislator": "Josh Gottheimer",  "ticker": "MSFT",  "type": "stock", "disc_date": "2026-03-25", "amount_max": 750000,  "cohort": "active_buyer"},

    # Pelosi — top_20pct, AI/power/dividends tilt per Jan 2026 disclosure
    {"legislator": "Nancy Pelosi",     "ticker": "AB",    "type": "stock", "disc_date": "2026-01-20", "amount_max": 750000,  "cohort": "top_20pct"},
    {"legislator": "Nancy Pelosi",     "ticker": "AMZN",  "type": "stock", "disc_date": "2026-01-20", "amount_max": 500000,  "cohort": "top_20pct"},
    {"legislator": "Nancy Pelosi",     "ticker": "GOOGL", "type": "stock", "disc_date": "2026-01-15", "amount_max": 1000000, "cohort": "top_20pct"},

    # Khanna — top performer (+112% since 2024, AI-heavy)
    {"legislator": "Ro Khanna",        "ticker": "MAR",   "type": "stock", "disc_date": "2025-12-10", "amount_max":  50000,  "cohort": "top_performer"},
    {"legislator": "Ro Khanna",        "ticker": "ODFL",  "type": "stock", "disc_date": "2025-12-10", "amount_max":  50000,  "cohort": "top_performer"},
    {"legislator": "Ro Khanna",        "ticker": "DECK",  "type": "stock", "disc_date": "2025-12-10", "amount_max":  50000,  "cohort": "top_performer"},

    # 2025 top-10 performers (for breadth — would be continuously filtered in prod)
    {"legislator": "Warren Davidson",  "ticker": "NVDA",  "type": "stock", "disc_date": "2026-01-08", "amount_max":  250000, "cohort": "top10_2025"},
    {"legislator": "Terri Sewell",     "ticker": "NVDA",  "type": "stock", "disc_date": "2025-04-15", "amount_max":  100000, "cohort": "top10_2025"},
    {"legislator": "Alex Padilla",     "ticker": "META",  "type": "stock", "disc_date": "2026-02-10", "amount_max":  100000, "cohort": "top10_2025"},
]

# top-earner whitelist — only legislators in this set pass the cohort filter
TOP_COHORT = {
    "Nancy Pelosi", "Josh Gottheimer", "Ro Khanna",
    "Warren Davidson", "Donald Norcross", "Terri Sewell",
    "Bryan Steil", "Alex Padilla", "Nick LaLota",
    "Rick Scott", "Michael Guest", "Dwight Evans",
}

# ============================================================
# 2. FILTER
# ============================================================

def in_cohort(d): return d["legislator"] in TOP_COHORT
def is_stock(d):  return d["type"] == "stock"
def recent(d, days=120):
    return (datetime.now() - datetime.strptime(d["disc_date"], "%Y-%m-%d")).days <= days

filtered = [d for d in DISCLOSURES if in_cohort(d) and is_stock(d) and recent(d)]

# ============================================================
# 3. PRICE ANALYSIS
# ============================================================

def analyze(trade):
    tkr = trade["ticker"]
    disc = pd.to_datetime(trade["disc_date"])
    start = (disc - timedelta(days=15)).strftime("%Y-%m-%d")
    end = datetime.now().strftime("%Y-%m-%d")
    try:
        df = yf.download(tkr, start=start, end=end, progress=False, auto_adjust=True)
        if df.empty or len(df) < 5:
            return {"ticker": tkr, "error": "no price data"}
        # flatten multi-level columns if yf returns them
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        post = df.loc[df.index >= disc]
        if post.empty:
            return {"ticker": tkr, "error": "disclosure after price history"}

        disc_price   = float(post.iloc[0]["Close"])
        peak_price   = float(post["High"].max())
        cur_price    = float(df.iloc[-1]["Close"])
        peak_ret     = (peak_price / disc_price - 1) * 100
        cur_ret      = (cur_price / disc_price - 1) * 100
        pullback     = (cur_price / peak_price - 1) * 100
        recent_20    = df.tail(20)
        rng_20d      = (float(recent_20["High"].max()) / float(recent_20["Low"].min()) - 1) * 100

        return {
            "ticker": tkr,
            "legislator": trade["legislator"],
            "cohort": trade["cohort"],
            "disc_date": trade["disc_date"],
            "disc_price": round(disc_price, 2),
            "peak_price": round(peak_price, 2),
            "peak_ret":   round(peak_ret, 1),
            "cur_price":  round(cur_price, 2),
            "cur_ret":    round(cur_ret, 1),
            "pullback":   round(pullback, 1),
            "rng_20d":    round(rng_20d, 1),
        }
    except Exception as e:
        return {"ticker": tkr, "error": str(e)}

# ============================================================
# 4. SCORE — "spike then flattened" pattern
# ============================================================

def score(r):
    if "error" in r: return -999
    # reward big post-disclosure rally (but diminish above 50%)
    spike = min(r["peak_ret"], 50) if r["peak_ret"] > 0 else 0
    # reward mild pullback into consolidation (sweet spot -3% to -10%)
    pb = r["pullback"]
    if -10 <= pb <= -3:      pb_score = 25
    elif -15 <= pb < -10:    pb_score = 15
    elif -3 < pb <= 0:       pb_score = 10
    else:                    pb_score = 0
    # reward tight 20d range (consolidation)
    rng_score = max(0, 25 - r["rng_20d"])
    return round(spike + pb_score + rng_score, 1)

# ============================================================
# 5. BUILD WATCHLIST
# ============================================================

print(f"Analyzing {len(filtered)} disclosures...", file=sys.stderr)
results = [analyze(t) for t in filtered]
for r in results:
    r["score"] = score(r) if "error" not in r else None

errs = [r for r in results if "error" in r]
ok   = [r for r in results if "error" not in r]
ok.sort(key=lambda x: x["score"], reverse=True)
top  = ok[:5]

# ============================================================
# 6. OUTPUT
# ============================================================

today = datetime.now().strftime("%Y-%m-%d")
out = [
    "# Gov-Watch Watchlist",
    "",
    f"**Generated:** {today}  ",
    f"**Source:** STOCK Act disclosures (demo: free public sources; production: Quiver API)  ",
    f"**Filter:** Top-cohort legislator stock buys, filed within 120 days, 'post-disclosure spike now flattened' pattern",
    "",
    f"## Top {len(top)} candidates (ranked by score)",
    "",
    "| # | Ticker | Legislator | Disc Date | Disc $ | Peak $ | Peak % | Current $ | Pullback | 20d Range | Score |",
    "|---|---|---|---|---|---|---|---|---|---|---|",
]
for i, r in enumerate(top, 1):
    out.append(
        f"| {i} | **{r['ticker']}** | {r['legislator']} | {r['disc_date']} "
        f"| ${r['disc_price']} | ${r['peak_price']} | +{r['peak_ret']}% "
        f"| ${r['cur_price']} | {r['pullback']}% | {r['rng_20d']}% | **{r['score']}** |"
    )

out += [
    "",
    "## Scoring logic",
    "",
    "- **Spike (0–50):** max post-disclosure return, capped at 50. Big rally confirms the legislator's signal worked.",
    "- **Pullback (0–25):** 25 pts if currently -3% to -10% off peak (sweet spot = thesis intact + cheaper entry). 15 if -10% to -15% (deeper dip). 10 if -3% to 0% (no pullback yet). 0 otherwise (either still near highs or blown out).",
    "- **Range (0–25):** 25 − (20d high/low range %). Tight range = consolidation, not capitulation.",
    "",
    "## All analyzed candidates",
    "",
]
for r in ok:
    out.append(
        f"- **{r['ticker']}** ({r['legislator']}, disc {r['disc_date']}) — "
        f"peak +{r['peak_ret']}%, pullback {r['pullback']}%, 20d range {r['rng_20d']}%, "
        f"score **{r['score']}**"
    )
if errs:
    out += ["", "## Errors", ""]
    for e in errs:
        out.append(f"- {e['ticker']}: {e['error']}")

out += [
    "",
    "## How pre-market.md would consume this",
    "",
    "On Monday morning, STEP 3 of `routines/pre-market.md` reads this file and appends the top-ranked tickers to its Perplexity research queries:",
    "",
    "```",
    "bash scripts/perplexity.sh \"Is $TICKER near a technical entry today given market context?\"",
    "```",
    "",
    "Each candidate still has to clear the existing guardrails (-7% stop, 20% sizing, 3-trades/week cap) before any order is placed.",
]

md = "\n".join(out) + "\n"

# write to the bot's memory folder so pre-market.md can read it
watchlist_path = os.path.join(os.path.dirname(__file__), "..", "memory", "GOV-WATCHLIST.md")
watchlist_path = os.path.abspath(watchlist_path)
with open(watchlist_path, "w") as f:
    f.write(md)

print(md)
print(f"\n[gov-watch-demo] Wrote {watchlist_path}", file=sys.stderr)
