#!/usr/bin/env python3
"""UserPromptSubmit hook: tell Ralph when the session context is about half full so he can compact.

Reads the newest assistant usage from the session transcript (input + cache tokens = what the
model just saw), compares it with CONTEXT_WINDOW_TOKENS (default 1,000,000), and at 50%, 70%
and 85% adds one instruction for Claude to open its reply with a compact request (Ralph
2026-10-30). Each level is announced once per session. Silent below 50%.
"""
import json, os, sys

WINDOW = int(os.environ.get("CONTEXT_WINDOW_TOKENS", "1000000"))
LEVELS = (50, 70, 85)


def used_tokens(path):
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        f.seek(max(0, size - 400_000))
        tail = f.read().decode("utf-8", "ignore").split("\n")
    for line in reversed(tail):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        u = (d.get("message") or {}).get("usage") if d.get("type") == "assistant" else None
        if u:
            return u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
    return 0


def main():
    try:
        data = json.load(sys.stdin)
        used = used_tokens(data["transcript_path"])
    except Exception:
        return
    pct = 100 * used // WINDOW
    hit = max((l for l in LEVELS if pct >= l), default=0)
    state = f"/tmp/context_watch_{data.get('session_id', 'x')}"
    try:
        done = int(open(state).read())
    except Exception:
        done = 0
    if hit <= done:
        return
    open(state, "w").write(str(hit))
    msg = (f"CONTEXT WATCH: this session is about {pct}% full ({used:,} of {WINDOW:,} tokens). "
           f"Start your reply with one plain line telling Ralph the context reached {hit}% and asking him to compact the "
           "session so work can continue; then answer his message as usual. Do not repeat this line later unless told again.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": msg}}))


main()
