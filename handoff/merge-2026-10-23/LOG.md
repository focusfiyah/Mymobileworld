# Branch merge, 2026-10-23 (Ralph: "Go ahead")

branch_sync.py listed 15 Mymobileworld session branches never merged into main (Dayone-ai and claude-skills: SYNC_OK).
Method: for every branch, every line it added that main lacks was listed (`missing.txt` method: added lines vs
main's current file) and judged. 90-99% of each branch's files were already identical on main.

## Decisions
| What the branches had that main lacks | Decision |
|---|---|
| Older Grace voice wording ("Grace" / Grace C / Grace B notes), grace.json, grace_c.json, clean.py `--tries` loop | Superseded: main has "Grace cloned" (2026-10-21), its grace.json, and clean.py with `--tries` + `--first` |
| Older wordings in CLAUDE.md, PLAYBOOK, the 4 handoff memory files (Kling for hand-free, session name "<Client>: <Product>", Drive, budget, Composio gemini "not run") | Superseded by main's newer dated rules (no Kling 2026-10-21, product-only names, Composio confirmed 2026-10-22, budget + BOOK 2026-10-22) |
| "A paid quote includes one likely redo" (memory files) | Covered: main CLAUDE.md (product reference sheet line) + PLAYBOOK §6 (4) |
| "never heads up" (GLOBAL_MEMORY) | Covered: banned phrase in grace/gate.py |
| omni_clip.py / youtheory kie.py gate lines, spend.py price lines, spend.json | Superseded: main's versions add the BOOK/budget lock and the same price logic |
| Winners tracker: BodyJ 3 sales (2026-10-20) | Superseded: main has 5 sales, 2,126 views (2026-10-22) |
| BodyJ 2026-10-17 plan files (claude/project-thread-qrybpv) | Superseded: main holds the made and approved BodyJ videos |
| Vans r11/r12 code + REMOVED.md | Already on main (cut.py lines checked) |
| Vans README r11/r12 status | PORTED to main's Vans README |

Each branch is then recorded as merged with `git merge -s ours` (main's tree kept), so branch_sync.py prints SYNC_OK.
