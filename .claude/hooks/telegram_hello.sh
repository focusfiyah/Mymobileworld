#!/bin/bash
# Ralph 2026-11-05: "I want you also to respond if I start a new session": one Telegram line per new session.
# Never prints or stores the token. Skips quietly if the token or session id is missing, or if already sent.
[ -n "$TELEGRAM_BOT_TOKEN" ] || exit 0
SID="${CLAUDE_CODE_REMOTE_SESSION_ID:-}"
[ -n "$SID" ] || exit 0
MARK="/tmp/.tg_hello_$SID"
[ -e "$MARK" ] && exit 0
touch "$MARK"
REPO="$(basename "${CLAUDE_PROJECT_DIR:-session}")"
(timeout 15 curl -sS -o /dev/null -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d chat_id=7628331161 --data-urlencode "text=Azariah here: a new session just started in ${REPO}. I'm ready." >/dev/null 2>&1 &)
exit 0
