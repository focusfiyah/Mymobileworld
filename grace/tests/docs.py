"""G4: the 2026-10-22 rule is written where sessions and chats read it."""
from pathlib import Path

R = Path(__file__).resolve().parents[2]; D = R.parent / "Dayone-ai"
need = {R / "CLAUDE.md": "BOOK.md", R / "grace/PLAYBOOK.md": "BOOK.md",
        R / ".claude/skills/ugc-product-ad/SKILL.md": "BOOK.md",
        R / ".claude/skills/ugc-product-ad/templates/plan-message.md": "TOTAL: $__"}
for base in (R, D):
    for f in ("REMEMBER_ME.txt", "REMEMBER_ME_paste.txt", "GLOBAL_MEMORY.md", "CLAUDE_PREFERENCES.txt", "MEMORY_SHORT.txt"):
        need[base / "handoff" / f] = "BOOK.md"
bad = [str(f) for f, w in need.items() if w not in f.read_text()]
short = [len((b / "handoff/MEMORY_SHORT.txt").read_text()) for b in (R, D)]
if max(short) > 2000: bad.append(f"MEMORY_SHORT too long {short}")
print("DOCS OK" if not bad else f"MISSING: {bad}")
