#!/usr/bin/env python3
"""
gov-watch.py - Weekly Gov-Watch watchlist generator (production).

Pulls the most recent Congressional STOCK Act disclosures from Quiver
Quantitative, filters to top-performing-legislator stock BUYS with fresh
dates, runs the 'post-disclosure spike now flattened' price filter, and
writes a ranked watchlist that pre-market.md can consume the next morning.

Schedule (proposed):  Sunday 18:00 America/Chicago   (0 18 * * 0)
Env vars required:    QUIVER_API_KEY  (in .env, sourced by wrapper)
Output:               memory/GOV-WATCHLIST.md
"""

import os
import sys
import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Config
def _load_env_var(name):
    """Env var first; fall back to ../.env k=v lookup."""
    v = os.environ.get(name)
    if v:
        return v
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

QUIVER_API_KEY     = _load_env_var("QUIVER_API_KEY")
TELEGRAM_BOT_TOKEN = _load_env_var("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = _load_env_var("TELEGRAM_CHAT_ID")

def tg_notify(text):
    """Send a Telegram message; swallow failures so the main run still
    finishes. Stays silent if Telegram creds are not configured."""
    if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID):
        print(f"[gov-watch] telegram not configured; would have sent: {text}", file=sys.stderr)
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": text[:4000],
                  "parse_mode": "Markdown", "disable_web_page_preview": "true"},
            timeout=10,
        )
    except Exception as e:
        print(f"[gov-watch] telegram send failed: {e}", file=sys.stderr)

if not QUIVER_API_KEY:
    msg = "🔴 ERROR — gov-watch: QUIVER_API_KEY not set in env or .env"
    print(msg, file=sys.stderr)
    tg_notify(msg)
    sys.exit(1)

QUIVER_BASE = "https://api.quiverquant.com/beta"
HEADERS     = {"Authorization": f"Token {QUIVER_API_KEY}"}

TOP_COHORT = {
    # Historical 2025 return leaders (media-sourced)
    "Nancy Pelosi", "Josh S. Gottheimer", "Josh Gottheimer",
    "Ro Khanna", "Warren Davidson", "Donald Norcross",
    "Terri A. Sewell", "Terri Sewell",
    "Bryan Steil", "Alex Padilla", "Nicholas A. LaLota",
    "Nick LaLota", "Rick Scott", "Michael Guest",
    "Dwight Evans", "Tommy Tuberville",
    # Added per Kevin's Quiver watchlist review (2026-04-23)
    "Cleo Fields", "Daniel Meuser",
    # Most-active recent BUYERS in live data (>=20 purchases this window)
    "Gilbert Cisneros", "John Boozman", "Markwayne Mullin",
    "Maria Elvira Salazar", "April Mcclain Delaney",
    "Angus King", "David J. Taylor",
}

DISCLOSURE_FRESH_DAYS = 60
MIN_TRADE_DAYS        = 5

def fetch_quiver_congress_trading():
    r = requests.get(f"{QUIVER_BASE}/live/congresstrading", headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

def in_cohort(rec):   return rec.get("Representative") in TOP_COHORT
def is_purchase(rec): return rec.get("Transaction", "").lower().startswith("purchase")
def is_stock(rec):    return rec.get("TickerType") == "ST"
def has_ticker(rec):  return bool(rec.get("Ticker"))

def recent(rec, days=DISCLOSURE_FRESH_DAYS):
    try:
        td = datetime.strptime(rec["TransactionDate"], "%Y-%m-%d")
        return (datetime.now() - td).days <= days
    except Exception:
        return False

def passes_filter(rec):
    return (in_cohort(rec) and is_purchase(rec)
            and is_stock(rec) and has_ticker(rec) and recent(rec))

def analyze(rec):
    tkr = rec["Ticker"]
    disc = pd.to_datetime(rec["TransactionDate"])
    start = (disc - timedelta(days=15)).strftime("%Y-%m-%d")
    end = datetime.now().strftime("%Y-%m-%d")
    try:
        df = yf.download(tkr, start=start, end=end, progress=False, auto_adjust=True)
        if df.empty or len(df) < MIN_TRADE_DAYS:
            return {"ticker": tkr, "error": "insufficient price history"}
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        post = df.loc[df.index >= disc]
        if post.empty:
            return {"ticker": tkr, "error": "disclosure after history"}
        disc_price = float(post.iloc[0]["Close"])
        peak_price = float(post["High"].max())
        cur_price  = float(df.iloc[-1]["Close"])
        peak_ret   = (peak_price / disc_price - 1) * 100
        cur_ret    = (cur_price / disc_price - 1) * 100
        pullback   = (cur_price / peak_price - 1) * 100
        rec_20     = df.tail(20)
        rng_20     = (float(rec_20["High"].max()) / float(rec_20["Low"].min()) - 1) * 100
        return {
            "ticker":     tkr,
            "legislator": rec["Representative"],
            "party":      rec.get("Party", ""),
            "chamber":    rec.get("House", ""),
            "disc_date":  rec["TransactionDate"],
            "report_date": rec.get("ReportDate", ""),
            "range":      rec.get("Range", ""),
            "disc_price": round(disc_price, 2),
            "peak_price": round(peak_price, 2),
            "peak_ret":   round(peak_ret, 1),
            "cur_price":  round(cur_price, 2),
            "cur_ret":    round(cur_ret, 1),
            "pullback":   round(pullback, 1),
            "rng_20d":    round(rng_20, 1),
        }
    except Exception as e:
        return {"ticker": tkr, "error": str(e)}

def score(r):
    if "error" in r: return -999
    spike = min(r["peak_ret"], 50) if r["peak_ret"] > 0 else 0
    pb = r["pullback"]
    if   -10 <= pb <= -3: pb_s = 25
    elif -15 <= pb < -10: pb_s = 15
    elif  -3 <  pb <= 0:  pb_s = 10
    else:                 pb_s = 0
    rng_s = max(0, 25 - r["rng_20d"])
    return round(spike + pb_s + rng_s, 1)

def main():
    print("[gov-watch] fetching from Quiver...", file=sys.stderr)
    raw = fetch_quiver_congress_trading()
    print(f"[gov-watch] {len(raw)} total records", file=sys.stderr)
    seen, dedup = set(), []
    for rec in raw:
        key = (rec.get("Representative"), rec.get("Ticker"), rec.get("TransactionDate"), rec.get("Transaction"))
        if key in seen: continue
        seen.add(key)
        dedup.append(rec)
    filtered = [r for r in dedup if passes_filter(r)]
    print(f"[gov-watch] {len(filtered)} pass filter", file=sys.stderr)
    analyzed = []
    for rec in filtered:
        a = analyze(rec)
        if "error" not in a:
            a["score"] = score(a)
            analyzed.append(a)
    analyzed.sort(key=lambda x: x["score"], reverse=True)
    top = analyzed[:10]

    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append("# Gov-Watch Watchlist")
    lines.append("")
    lines.append(f"**Generated:** {today} (live from Quiver Quantitative)  ")
    lines.append(f"**Source:** GET api.quiverquant.com/beta/live/congresstrading - Hobbyist tier  ")
    lines.append(f"**Filter:** Top-cohort stock PURCHASES in last {DISCLOSURE_FRESH_DAYS} days  ")
    lines.append(f"**Universe:** {len(raw)} records -> {len(filtered)} pass filter -> {len(analyzed)} scored")
    lines.append("")
    lines.append(f"## Top {len(top)} candidates")
    lines.append("")
    lines.append("| # | Ticker | Legislator | Disc Date | Amount | Peak % | Pullback | 20d Range | Score |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(top, 1):
        lines.append(
            f"| {i} | **{r['ticker']}** | {r['legislator']} ({r['party']}) "
            f"| {r['disc_date']} | {r['range']} "
            f"| +{r['peak_ret']}% | {r['pullback']}% "
            f"| {r['rng_20d']}% | **{r['score']}** |"
        )
    lines.append("")
    lines.append("## All analyzed")
    lines.append("")
    for r in analyzed:
        lines.append(
            f"- **{r['ticker']}** - {r['legislator']} ({r['chamber']}, {r['party']}) "
            f"disc {r['disc_date']} [{r['range']}]: "
            f"peak +{r['peak_ret']}%, pullback {r['pullback']}%, "
            f"20d range {r['rng_20d']}%, score **{r['score']}**"
        )
    lines.append("")
    lines.append("## Pre-market consumption")
    lines.append("")
    lines.append("On Monday morning, STEP 3 of routines/pre-market.md reads this")
    lines.append("file and folds the top-ranked tickers into its Perplexity")
    lines.append("research queries. Each candidate must still clear the existing")
    lines.append("guardrails (-7% stop, 20% sizing, 3-trades/week cap).")
    md = "\n".join(lines) + "\n"
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "memory", "GOV-WATCHLIST.md"))
    with open(path, "w") as f:
        f.write(md)
    print(md)
    print(f"\n[gov-watch] Wrote {path}", file=sys.stderr)

    # Telegram 🟢 WIN with the top picks so Kevin sees them without opening the file.
    if top:
        bullets = "\n".join(
            f"• *{r['ticker']}* — {r['legislator']} (score {r['score']}, pullback {r['pullback']}%)"
            for r in top[:5]
        )
        tg_notify(
            f"🟢 WIN — gov-watch: {len(top)} Quiver picks refreshed ({today})\n\n"
            f"Top {min(5, len(top))}:\n{bullets}\n\n"
            f"Monday pre-market will fold these into Perplexity research. "
            f"Full list: memory/GOV-WATCHLIST.md"
        )
    else:
        tg_notify(
            f"🟡 ISSUE — gov-watch: refresh ran but produced 0 qualifying picks "
            f"({len(raw)} raw, {len(filtered)} passed filter). "
            f"Check GOV-WATCHLIST.md."
        )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        tg_notify(f"🔴 ERROR — gov-watch: {type(e).__name__}: {e}")
        raise
