# Opus 4.7 Trading Bot — Kevin's build

Autonomous, cloud-scheduled, stateless swing-trading agent. Based on Nate Herk's
"Opus 4.7 Trading Bot" setup guide, with two local adaptations:

1. **Gmail SMTP replaces ClickUp Chat** for notifications (reuses Kevin's
   existing Gmail App Password setup).
2. **Perplexity is optional.** Without a key, the wrapper exits 3 and the agent
   falls back to native WebSearch for research.

"Claude is the bot." Each scheduled run is a fresh ephemeral Claude Code
container that clones this repo, reads memory, places orders, writes new
memory, commits, and pushes. The only persistent state is Git (the `main`
branch).

## Repository layout

```
trading-bot/
├── CLAUDE.md          # Agent rulebook (auto-loaded every session)
├── README.md          # This file
├── env.template       # Template for local .env file
├── .gitignore         # Excludes .env
├── .claude/
│   └── commands/      # Ad-hoc slash commands for local use
│       ├── portfolio.md
│       ├── trade.md
│       ├── pre-market.md
│       ├── market-open.md
│       ├── midday.md
│       ├── daily-summary.md
│       └── weekly-review.md
├── routines/          # Cloud routine prompts (the prod path)
│   ├── README.md
│   ├── pre-market.md
│   ├── market-open.md
│   ├── midday.md
│   ├── daily-summary.md
│   └── weekly-review.md
├── scripts/           # API wrappers (the only way to touch the outside world)
│   ├── alpaca.sh
│   ├── perplexity.sh
│   └── gmail.sh
└── memory/            # Agent's persistent state (committed to main)
    ├── TRADING-STRATEGY.md
    ├── TRADE-LOG.md
    ├── RESEARCH-LOG.md
    ├── WEEKLY-REVIEW.md
    └── PROJECT-CONTEXT.md
```

## Two execution modes

**Local mode.** Invoke slash commands like `/portfolio` or `/pre-market`
interactively inside Claude Code. Credentials come from a local `.env`.
Good for testing and ad-hoc. No commit-and-push in these commands — that's
the point; nothing local touches main.

**Cloud mode.** Claude Code cloud routines fire the five `routines/*.md`
prompts on a cron. Credentials come from the routine's environment variables.
**No `.env` file in the cloud.** This is the production path.

## Five cron schedules (America/Chicago)

```
Pre-market:     0 6  * * 1-5     (6:00 AM weekdays)
Market-open:   30 8  * * 1-5     (8:30 AM weekdays, market opens 8:30 AM CT)
Midday:         0 12 * * 1-5     (noon weekdays)
Daily-summary:  0 15 * * 1-5     (3:00 PM weekdays, market closes 3:00 PM CT)
Weekly-review:  0 16 * * 5       (4:00 PM Fridays only)
```

## Setup — first-time (replication checklist)

1. **Create a new private GitHub repo** called e.g. `trading-bot`. Leave it empty.
2. **Copy this whole `trading-bot/` folder into the new repo and push to `main`.**
3. **Sign up for Alpaca** (paper to start). Save API key and secret.
4. **(Optional) Sign up for Perplexity** and save the API key. Skip and the
   agent falls back to WebSearch.
5. **Create a Gmail App Password.** Google Account → Security → 2-Step
   Verification → App passwords. 16-character string. Save it.
6. **Local smoke test.**
   ```
   cp env.template .env
   # edit .env, paste ALPACA_API_KEY, ALPACA_SECRET_KEY, GMAIL_APP_PASSWORD
   chmod +x scripts/*.sh
   bash scripts/alpaca.sh account
   bash scripts/alpaca.sh positions
   bash scripts/gmail.sh "Smoke test" <<< "If you see this, SMTP works."
   ```
   Expect: your Alpaca paper account JSON, an empty positions array, and an
   email in your Gmail inbox. If any fail, fix before proceeding.
7. **Install the Claude GitHub App** on your trading-bot repo (least privilege —
   grant only this repo).
8. **Create the first cloud routine (pre-market).** In Claude Code cloud:
   - Routines → New Routine
   - Name: "Trading bot pre-market"
   - Repository: your trading-bot repo
   - Branch: `main`
   - Environment variables: paste all required vars (see below)
   - Toggle ON: **"Allow unrestricted branch pushes"** (this is the #1 reason
     first-time setups break)
   - Cron: `0 6 * * 1-5`, timezone `America/Chicago`
   - Prompt: paste `routines/pre-market.md` **verbatim** (do not paraphrase)
   - Save → click "Run now" to test
9. **Verify the run** writes `memory/RESEARCH-LOG.md`, commits it, and pushes.
   Check GitHub for the new commit.
10. **Repeat step 8-9 for the other four routines** (market-open, midday,
    daily-summary, weekly-review) with their respective crons and prompts.
11. **Seed Day 0 snapshot.** `memory/TRADE-LOG.md` already contains a Day 0
    snapshot. Tomorrow's daily-summary will compute Day P&L off it.
12. **Monitor the first week closely.** Read every commit the agent makes.
    Adjust only after 2 full weeks of evidence.

## Required environment variables

Set these on the cloud routine itself (NOT in a `.env` file in the cloud):

```
ALPACA_API_KEY            (required)
ALPACA_SECRET_KEY         (required)
ALPACA_ENDPOINT           (optional; default https://paper-api.alpaca.markets/v2)
ALPACA_DATA_ENDPOINT      (optional; default https://data.alpaca.markets/v2)
PERPLEXITY_API_KEY        (optional; without it, agent falls back to WebSearch)
PERPLEXITY_MODEL          (optional; defaults to 'sonar')
GMAIL_USER                (required for notifications)
GMAIL_APP_PASSWORD        (required for notifications — 16-char Google App Password)
GMAIL_TO                  (required for notifications)
```

## Gmail SMTP swap — how it differs from the original guide

The original Opus 4.7 guide uses a `clickup.sh` wrapper to post to a ClickUp
Chat channel. This build replaces it with `gmail.sh` that sends via Gmail's
SMTP (`smtp.gmail.com:465`, SSL) using a 16-character Google App Password.

- Uses the same "graceful fallback" pattern: if any Gmail env var is missing,
  the message is appended to `DAILY-SUMMARY.md` and the script exits 0. The
  agent never crashes on missing notification creds.
- Subject line prefix is `[TradingBot]` so you can filter or label in Gmail.
- All six routine and slash-command prompts reference `scripts/gmail.sh`
  instead of `scripts/clickup.sh`. No other changes.

## Priors from the field

`memory/TRADING-STRATEGY.md` ends with a "Priors from the Field (2026)"
section citing lessons from publicly documented Claude-Code trading
experiments (ji_ai's 15-strategy backtest, the harness-layer principle,
the options-wipeout case, citation discipline). These are starting biases,
not rules — the weekly review should challenge or confirm them as actual
performance data accrues.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Repository not accessible" / clone fails | Claude GitHub App not installed | Install it, grant access to the specific repo |
| `git push` fails with proxy/permission error | "Allow unrestricted branch pushes" toggle is off | Enable it in the routine's environment |
| `ALPACA_API_KEY not set in environment` | Env var missing from routine env | Add it in the routine config, not a `.env` |
| Agent creates a `.env` anyway | Prompt was paraphrased and lost the "DO NOT create .env" block | Re-paste from `routines/*.md` exactly |
| Yesterday's trades missing from today's run | Previous run didn't commit+push | Check `git log origin/main`. Re-verify STEP N |
| Push fails "fetch first" / non-fast-forward | Another run pushed between this one's clone and push | Prompt handles with `git pull --rebase`. If looping, check for merge conflict |
| Gmail didn't arrive | One of GMAIL_USER / GMAIL_APP_PASSWORD / GMAIL_TO missing | Script falls back to local file. Add the missing vars |
| Perplexity calls didn't happen | PERPLEXITY_API_KEY missing | Script exits 3, agent falls back to WebSearch. Add the key or accept fallback |
| Alpaca rejects stop with PDT error | Same-day stop on same-day buy | Prompt's fallback ladder: trailing_stop → fixed stop → queue for tomorrow AM |

## Notification philosophy

Most bots are chatty. This one is not.

- **Pre-market:** silent unless genuinely urgent.
- **Market-open:** only if a trade was placed.
- **Midday:** only if action was taken.
- **Daily-summary:** always sends, one email, under 15 lines.
- **Weekly-review:** always sends, one email, headline numbers.

Cost of a missed notification is low (you can always check the portfolio
ad-hoc). Cost of a chatty bot is high — you stop reading the messages, and
then you miss the one that mattered.
