"""Write Ralph's user-level Claude Code hooks into ~/.claude/settings.json (idempotent). Run by the cloud environment's
setup script (Ralph 2026-11-14 weekly audit): sessions that open across all repos (/home/user) skip each repo's own
SessionStart hooks, so playwright, camofox, broll and the Telegram hello never ran there. In-repo sessions keep using
the repo hooks (the command exits at once there, so nothing runs twice).

  python3 Mymobileworld/tools/env/user_hooks.py     -> USER_HOOKS_OK
"""
import json, os

HOOKS = "/home/user/Mymobileworld/.claude/hooks"
WANT = {
    "UserPromptSubmit": f'f={HOOKS}/context_watch.py; [ -f "$f" ] && python3 "$f" || true',
    "SessionStart": ('case "$CLAUDE_PROJECT_DIR" in /home/user/Mymobileworld*|/home/user/Dayone-ai*) exit 0;; esac; '
                     'for h in browser_setup camofox_setup broll_setup telegram_hello; do '
                     f'f={HOOKS}/$h.sh; [ -f "$f" ] && CLAUDE_PROJECT_DIR=/home/user/Mymobileworld bash "$f"; done; true'),
}
p = os.path.expanduser("~/.claude/settings.json")
os.makedirs(os.path.dirname(p), exist_ok=True)
d = json.load(open(p)) if os.path.exists(p) else {}
for event, cmd in WANT.items():
    groups = d.setdefault("hooks", {}).setdefault(event, [])
    if cmd not in [h.get("command") for g in groups for h in g.get("hooks", [])]:
        groups.append({"hooks": [{"type": "command", "command": cmd}]})
json.dump(d, open(p, "w"), indent=2)
print("USER_HOOKS_OK")
