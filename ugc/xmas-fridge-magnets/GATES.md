# Gates: Christmas Fridge Magnets, plan stage

OWNS: ugc/xmas-fridge-magnets/**

Scope: research, script, storyboard and Production Book for Grace's Christmas Fridge Magnets toddler-activity video, sent to Ralph for his OK, with no spend.

- [ ] G1: script gate passes on the current script and proofs
  CHECK: python3 grace/gate.py ugc/xmas-fridge-magnets
  EXPECT: GATE OK
  CWD: ../..
  EVIDENCE: pending

- [ ] G2: every still and clip prompt lints clean
  CHECK: python3 grace/prompt_check.py lint ugc/xmas-fridge-magnets/shots.json
  EXPECT: PROMPT_LINT_OK
  CWD: ../..
  EVIDENCE: pending

- [ ] G3: BOOK.md names the review page it was sent on and one TOTAL line
  CHECK: python3 -c "t=open('BOOK.md').read(); import re; assert re.search(r'Sent to Ralph: https://claude.ai/code/artifact/\S+', t); assert len(re.findall(r'(?m)^TOTAL: \$\d', t))==1; print('BOOK_FIELDS_OK')"
  EXPECT: BOOK_FIELDS_OK
  EVIDENCE: pending

- [ ] G4: no paid task was started in this job (plan stage)
  CHECK: python3 -c "import os; assert not os.path.exists('paid_tasks.json'); print('NO_SPEND_OK')"
  EXPECT: NO_SPEND_OK
  EVIDENCE: pending

- [ ] G5: Ralph was notified (email sent; push tool not found this session) and asked with tap questions
  EVIDENCE: pending

- [ ] G6: Grace's Telegram photo is in Drive "Telegram Assets (Azariah)" with the same size and an index line
  EVIDENCE: pending
