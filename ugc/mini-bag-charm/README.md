# Mini Bag Charm, burgundy (Grace), 2026-10-26
Status: 2026-10-27 round 4 (Grace: 'still way too big', 'it changes the design'): real listing charm composited at true size on S4/S7/S8/S9 (tools/composite.py), scarf-only edits S1/S5a; Seedance redraws the tiny charm, so S7/S8 are real-charm paste-backs (tools/track_paste.py), S5a trimmed clean. WAITING on Ralph: paste-back OK + S1/S4/S9 fix ($0.73 rec. / $0.41). Kie job $7.36 of $7.37 OK'd. Review https://claude.ai/artifact/Uns9WGWdYcjDBsdbbeCezb
Format: hands + hand-free AI over Grace's cloned voice, 9 shots, ~26 s, no text. Model: @the_little_beannn 331K.
Files: BOOK.md (plan), scripts.md, shots.json + build_prompts.py -> prompts/, refs/product_sheet.png (make_sheet.py), product_truth.json, research/, rooms/ (SOURCES.md), GATES.md, REMOVED.md, review/ (build_review.py).
Run (after --approve-book): `python3 run.py stills S1 S2 ...`; S3 Seedance; product clips = Flow kits first, Kie Omni fallback `python3 run.py omni S5`.
