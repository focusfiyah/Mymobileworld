# Gates: Scripts for Grace's 5 selling videos (2026-11-13)

OWNS: ugc/sales-scripts-1113/**, grace/winners/**

Scope: for each of the 5 products Grace sold with (Haiti flag, ili case, meat sticks + jerky, Bobbi Brown Prep and Brighten Duo, Asvivid mock neck sweatshirt), a voiceover script and a talk-to-camera script built through the full Grace script gate, logged in her sales tracker, delivered as a Google Doc in each product's Drive folder and on Telegram.

- [ ] G1: every product has a Voiceover and a Talk-to-camera script, library hook word for word, orange cart close, no banned phrase or price
  CHECK: python3 ugc/sales-scripts-1113/check.py scripts
  EXPECT: SCRIPTS_OK
  EVIDENCE: pending

- [ ] G2: all 5 jobs pass the Grace script gate (playbook, coach, viral board, facts, audience, RESEARCH.md, hooks, humanizer, readability <= 6, line sources, line audit)
  CHECK: python3 ugc/sales-scripts-1113/check.py gates
  EXPECT: ALL_GATES_OK
  EVIDENCE: pending

- [ ] G3: the 5 videos are in the sales tracker with every judgment field filled
  CHECK: python3 grace/winners/check.py fields
  EXPECT: PASS fields 13
  EVIDENCE: pending

- [ ] G4: one Google Doc "Scripts - <product>" per product in its Drive folder in Grace Tiktok assets (Bobbi Brown folder new + Originals, anyone-with-link editor), no PDF
  EVIDENCE: pending

- [ ] G5: Grace got one Telegram message per product with its folder link, Ralph got one line; Telegram ack for msg 493 sent first
  EVIDENCE: pending

- [ ] G6: Brain updated and the brain check passes
  CHECK: python3 tools/brain/check.py --terms "Haiti flag,Bobbi Brown,selling videos scripts"
  EXPECT: BRAIN_OK
  EVIDENCE: pending
