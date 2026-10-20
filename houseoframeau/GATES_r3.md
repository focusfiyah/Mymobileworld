# Gates: looser wording as the default + House of Rameau AI/sales facts, 2026-10-20

OWNS: grace/hooks/HOOKS.md, grace/PLAYBOOK.md, handoff/**, houseoframeau/**, CLAUDE.md

Scope: make Grace's looser wording the standing default everywhere the word-for-word rule lives (repo docs + the 4 memory files in both repos), record which House of Rameau videos are our AI videos and that only Tiger Eye sold, and deliver the memory paste to Ralph.

- [ ] T1: no file outside history/results logs still says hooks are said word for word or verbatim
  CHECK: python3 houseoframeau/check_r3.py wording
  EXPECT: PASS wording
  EVIDENCE: pending

- [ ] T2: MEMORY_SHORT.txt <= 2000 chars, and the 5 handoff files are identical in Mymobileworld and Dayone-ai
  CHECK: python3 houseoframeau/check_r3.py handoff
  EXPECT: PASS handoff
  EVIDENCE: pending

- [ ] T3: videos.json marks exactly the 5 videos we made as AI (Tiger Eye, Restlex, arnica, Fungix x2) and records sales (Tiger Eye 1, others 0)
  CHECK: python3 houseoframeau/check_r3.py hor
  EXPECT: PASS hor
  EVIDENCE: pending

- [ ] T4: committed + pushed (Mymobileworld, Dayone-ai), REMEMBER_ME_paste.txt sent, Ralph emailed + pushed
  EVIDENCE: pending
