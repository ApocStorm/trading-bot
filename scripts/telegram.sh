#!/usr/bin/env bash
# Notification wrapper. Sends a message via Telegram Bot API.
# Usage: bash scripts/telegram.sh "<subject>" "<body>"
#        echo "body" | bash scripts/telegram.sh "<subject>"
#
# Runs alongside scripts/gmail.sh for dual-channel alerts.
# Graceful fallback: if TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing,
# appends to DAILY-SUMMARY.md and exits 0.

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
            shift || true
            else
              subject="Trading Bot Alert"
              fi

              if [[ $# -gt 0 ]]; then
                body="$*"
                elif [[ ! -t 0 ]]; then
                  body="$(cat)"
                  else
                    body="$subject"
                    fi

                    if [[ -z "${body// /}" ]]; then
                      echo "usage: bash scripts/telegram.sh \"<subject>\" \"<body>\"" >&2
                        exit 1
                        fi

                        stamp="$(date '+%Y-%m-%d %H:%M %Z')"

                        if [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_CHAT_ID:-}" ]]; then
                          printf "\n---\n## %s — %s (fallback — Telegram not configured)\n%s\n\n" "$stamp" "$subject" "$body" >> "$FALLBACK"
                            echo "[telegram fallback] appended to DAILY-SUMMARY.md"
                              echo "$body"
                                exit 0
                                fi

                                full_msg="*[TradingBot] ${subject}*

                                ${body}"

                                if (( ${#full_msg} > 4000 )); then
                                  full_msg="${full_msg:0:3990}
                                  …[truncated]"
                                  fi

                                  TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" TELEGRAM_CHAT_ID="$TELEGRAM_CHAT_ID" MSG="$full_msg" \
                                    python3 <<'PY'
                                    import json, os, sys, urllib.request, urllib.parse

                                    token = os.environ["TELEGRAM_BOT_TOKEN"]
                                    chat  = os.environ["TELEGRAM_CHAT_ID"]
                                    text  = os.environ["MSG"]

                                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                                    data = urllib.parse.urlencode({
                                        "chat_id": chat,
                                            "text": text,
                                                "parse_mode": "Markdown",
                                                    "disable_web_page_preview": "true",
                                                    }).encode()

                                                    req = urllib.request.Request(url, data=data)
                                                    try:
                                                        resp = urllib.request.urlopen(req, timeout=10)
                                                            body = json.loads(resp.read())
                                                                if body.get("ok"):
                                                                        print(f"[telegram] sent to chat {chat}")
                                                                            else:
                                                                                    print(f"[telegram] api error: {body}", file=sys.stderr)
                                                                                            sys.exit(1)
                                                                                            except Exception as e:
                                                                                                print(f"[telegram] send failed: {e}", file=sys.stderr)
                                                                                                    sys.exit(1)
                                                                                                    PY
                                                                                                    
