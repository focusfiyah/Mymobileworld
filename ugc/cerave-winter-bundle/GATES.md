# Gates: CeraVe Winter Skin Bundle, plan stage (2026-11-02)

OWNS: ugc/cerave-winter-bundle/**

Scope: the plan Ralph approves before any spend: script gate passed, 5 linted prompts with real references, a spoken script for later, BOOK.md with one total, sent on a review page with push + email.

- [ ] G1: script gate passes (all PLAYBOOK §4 proofs newer than the script)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/cerave-winter-bundle
  EXPECT: GATE OK
  EVIDENCE: pending

- [ ] G2: every still and clip prompt passes the lint
  CHECK: cd /home/user/Mymobileworld && python3 grace/prompt_check.py lint ugc/cerave-winter-bundle/shots.json
  EXPECT: PROMPT_LINT_OK
  EVIDENCE: pending

- [ ] G3: every shot shows all four products and every reference file exists
  CHECK: cd /home/user/Mymobileworld/ugc/cerave-winter-bundle && python3 -c "import json,os;S=json.load(open('shots.json'));bad=[r for s in S for r in s['still_refs']+s['clip_refs'][1:] if not os.path.exists(r)];miss=[s['id'] for s in S if not all(w in s['still'] for w in ['Hydrating Facial Cleanser','AM Facial Moisturizing Lotion','Intensive','Healing Lip Balm'])];print(len(S),bad,miss);print('REFS_OK' if len(S)==5 and not bad and not miss else 'REFS_BAD')"
  EXPECT: REFS_OK
  EVIDENCE: pending

- [ ] G4: spoken script readability grade <= 6
  CHECK: cd /home/user/Mymobileworld/ugc/cerave-winter-bundle && python3 ../../.claude/skills/tiktok-shop-coach/scripts/tiktok.py readability scripts.md
  EXPECT: Grade level \(Flesch-Kincaid\): [0-5]\.
  EVIDENCE: pending

- [ ] G5: BOOK.md has one TOTAL line and a Sent to Ralph line with a link
  CHECK: cd /home/user/Mymobileworld/ugc/cerave-winter-bundle && grep -c -E "^TOTAL: \$[0-9.]+$|^Sent to Ralph: https" BOOK.md
  EXPECT: ^2$
  EVIDENCE: pending

- [ ] G6: review page shows the storyboard, script, product sheet, room and hand sheet; Ralph notified by push + email
  EVIDENCE: pending
