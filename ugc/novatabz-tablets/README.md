# NovaTabz Toothpaste Tablets (Grace), 2026-10-30

Status: PLAN SENT 2026-10-30, waiting on Ralph's OK + 5 answers (Flow vs Kie clips, Kie vs Gemini-app stills, hand sheet, hook text, product details). Spent $0. Book TOTAL $4.51 (about $1.99 with Flow). Review page https://claude.ai/artifact/6A88QRQeyEJyNgZWrPwsRe. Next: `python3 grace/gate.py ugc/novatabz-tablets --approve-book "<his words>"`, then all 12 stills at once -> still storyboard.

- Route: hands + hand-free AI over Grace cloned v5 VO, ~30 s, 12 shots (6 hand-free, 7 show the jar), no text.
- Product truth: `product_truth.json`, sheet `refs/product_sheet.png` (make_sheet.py, from Ralph's 3 photos), facts `research/product_facts.md` (Amazon B0GZX9TRT2).
- Script: `scripts.md`, `vo_lines.txt`; gate `python3 grace/gate.py ugc/novatabz-tablets` -> GATE OK.
- Shots/prompts: `make_shots.py` -> `shots.json` + `prompts/` (prompt-master, MARKED_OK). Rooms `rooms/SOURCES.md`.
- Review page: `build_review.py` -> `review/index.html`.
- Drive: not yet (job not delivered).
