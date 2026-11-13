# Gates: Scripts for Grace's 5 selling videos (2026-11-13)

OWNS: ugc/sales-scripts-1113/**, grace/winners/**

Scope: for each of the 5 products Grace sold with (Haiti flag, ili case, meat sticks + jerky, Bobbi Brown Prep and Brighten Duo, Asvivid mock neck sweatshirt), a voiceover script and a talk-to-camera script built through the full Grace script gate, logged in her sales tracker, delivered as a Google Doc in each product's Drive folder and on Telegram.

- [x] G1: every product has a Voiceover and a Talk-to-camera script, library hook word for word, orange cart close, no banned phrase or price
  CHECK: python3 ugc/sales-scripts-1113/check.py scripts
  EXPECT: SCRIPTS_OK
  EVIDENCE: 2026-11-13 20:00 UTC ran by hand: SCRIPTS_OK (5 products, 10 scripts)

- [x] G2: all 5 jobs pass the Grace script gate (playbook, coach, viral board, facts, audience, RESEARCH.md, hooks, humanizer, readability <= 6, line sources, line audit)
  CHECK: python3 ugc/sales-scripts-1113/check.py gates
  EXPECT: ALL_GATES_OK
  EVIDENCE: 2026-11-13 20:00 UTC ran by hand: ALL_GATES_OK (grace/gate.py GATE OK x5)

- [x] G3: the 5 videos are in the sales tracker with every judgment field filled
  CHECK: python3 grace/winners/check.py fields
  EXPECT: PASS fields 13
  EVIDENCE: 2026-11-13 20:00 UTC ran by hand: PASS fields 13; Drive sheet 17qkOy... rewritten A1:Y14 and read back (14 rows)

- [x] G4: one Google Doc "Scripts - <product>" per product in its Drive folder in Grace Tiktok assets (Bobbi Brown folder new + Originals, anyone-with-link editor), no PDF
  EVIDENCE: Docs created + read back (Haiti): 1nOQRFOx..., 1-CHmpNG..., 1Gt_CG7o..., 1go6oMpg..., 1AV48BDK... each in its product folder (search parentId); Bobbi folder 1l2ibq62... + Originals 1kcw9UFu... anyoneWithLink writer (permissions read back); 4 other folders shared anyoneWithLink writer; no PDF

- [x] G5: Grace got one Telegram message per product with its folder link, Ralph got one line; Telegram ack for msg 493 sent first
  EVIDENCE: Ack msg 493 sent first (ok true); msgs 499-503 to Grace (ok true, one per product, folder link, ✅); Ralph private line ok true; msg 496 answered

- [x] G6: Brain updated and the brain check passes
  CHECK: python3 tools/brain/check.py --terms "Haiti flag,Bobbi Brown,selling videos scripts"
  EXPECT: BRAIN_OK
  EVIDENCE: 2026-11-13 ran by hand: BRAIN_OK (428 notes, terms found); vault pushed 22cd73f
