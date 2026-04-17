#!/usr/bin/env bash
# Notification wrapper. Sends an email via Gmail SMTP.
# Usage: bash scripts/gmail.sh "<message>"
#        echo "body" | bash scripts/gmail.sh "<subject>"
#
# Replaces the original guide's scripts/clickup.sh so notifications land in
# Kevin's Gmail inbox instead of ClickUp Chat.
#
# If credentials are unset, appends to DAILY-SUMMARY.md as a fallback and exits 0
# (mirrors the original clickup.sh behavior — the agent never crashes on
# missing notification creds).

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"
FALLBACK="$ROOT/DAILY-SUMMARY.md"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

if [[ $# -gt 0 ]]; then
  subject="$1"
else
  subject="Trading Bot Alert"
fi

if [[ ! -t 0 ]]; then
  body="$(cat)"
else
  body="$subject"
fi

if [[ -z "${body// /}" ]]; then
  echo "usage: bash scripts/gmail.sh \"<subject>\" < body-on-stdin  OR  bash scripts/gmail.sh \"<message>\"" >&2
  exit 1
fi

stamp="$(date '+%Y-%m-%d %H:%M %Z')"

if [[ -z "${GMAIL_USER:-}" || -z "${GMAIL_APP_PASSWORD:-}" || -z "${GMAIL_TO:-}" ]]; then
  printf "\n---\n## %s (fallback — Gmail not configured)\n%s\n\n" "$stamp" "$body" >> "$FALLBACK"
  echo "[gmail fallback] appended to DAILY-SUMMARY.md"
  echo "$body"
  exit 0
fi

SUBJECT="$subject" BODY="$body" \
  GMAIL_USER="$GMAIL_USER" GMAIL_APP_PASSWORD="$GMAIL_APP_PASSWORD" GMAIL_TO="$GMAIL_TO" \
  python3 <<'PY'
import os, smtplib, ssl
from email.message import EmailMessage

msg = EmailMessage()
msg["From"]    = os.environ["GMAIL_USER"]
msg["To"]      = os.environ["GMAIL_TO"]
msg["Subject"] = "[TradingBot] " + os.environ["SUBJECT"]
msg.set_content(os.environ["BODY"])

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as s:
    s.login(os.environ["GMAIL_USER"], os.environ["GMAIL_APP_PASSWORD"])
    s.send_message(msg)
print("[gmail] sent to", os.environ["GMAIL_TO"])
PY
