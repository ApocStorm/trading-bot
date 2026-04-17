# Cloud Routines

These five markdown files are the **production** prompts. Paste each one
verbatim into its respective Claude Code cloud routine — do not paraphrase.
The env-var check block and the commit-and-push step are load-bearing.

| File              | Cron (America/Chicago) | Purpose                                         |
|-------------------|------------------------|-------------------------------------------------|
| pre-market.md     | `0 6 * * 1-5`          | 6:00 AM weekdays — research                     |
| market-open.md    | `30 8 * * 1-5`         | 8:30 AM weekdays — execute planned trades       |
| midday.md         | `0 12 * * 1-5`         | Noon weekdays — cut losers, tighten winners     |
| daily-summary.md  | `0 15 * * 1-5`         | 3:00 PM weekdays — EOD snapshot + email recap   |
| weekly-review.md  | `0 16 * * 5`           | 4:00 PM Fridays only — week stats + letter grade|

Each routine must have these env vars set **on the routine itself** (NOT in a
`.env` file in the repo):

```
ALPACA_API_KEY            (required)
ALPACA_SECRET_KEY         (required)
ALPACA_ENDPOINT           (optional; default paper URL)
ALPACA_DATA_ENDPOINT      (optional; default data URL)
PERPLEXITY_API_KEY        (optional; without it, agent falls back to WebSearch)
PERPLEXITY_MODEL          (optional; defaults to 'sonar')
GMAIL_USER                (required for notifications)
GMAIL_APP_PASSWORD        (required for notifications)
GMAIL_TO                  (required for notifications)
```
