# Gates: Shnuggle slideshow test (Grace)

OWNS: ugc/shnuggle-slideshow/**

Scope: A 6-slide TikTok Shop photo slideshow of the Shnuggle Toddler Bath, no text, product true to the real photo with nothing added, caption options, review page, Drive, Ralph notified.

- [ ] G1: Script gate passes (PLAYBOOK §4 proofs for slides + captions)
  CHECK: python3 ugc/shnuggle-slideshow/qc/gates_check.py gate
  EXPECT: gate PASS
  EVIDENCE: pending

- [ ] G2: Ralph approved the plan and total cost before any paid call; each redo asked with its cost
  EVIDENCE: pending

- [ ] G3: Six distinct slides, each 1080x1920, none reused from the R1/R2 stills
  CHECK: python3 ugc/shnuggle-slideshow/qc/gates_check.py slides
  EXPECT: slides PASS
  EVIDENCE: pending

- [ ] G4: QC report all clear: tub matches the real photo (shape, rim, backrest, logo badge, grey feet), nothing added (no plug, water, toys, towel, hands, text), 2x edge zoom, bright neutral grade, REMOVED.md checked
  CHECK: python3 ugc/shnuggle-slideshow/qc/gates_check.py qc
  EXPECT: qc PASS
  EVIDENCE: pending

- [ ] G5: Kie spend within the approved cap
  CHECK: python3 ugc/shnuggle-slideshow/qc/gates_check.py spend
  EXPECT: spend PASS
  EVIDENCE: pending

- [ ] G6: Review page (Artifact) shows the slides in order + caption; Ralph notified by push and email
  EVIDENCE: pending

- [ ] G7: Drive: slides + caption doc in the Shnuggle Toddler Tub (Grace) folder as CURRENT, nothing loose; link in README
  EVIDENCE: pending

ABANDON: G2 Ralph stopped the test 2026-10-19 before the round 2 (true size) approval; handoff: lessons in grace/PLAYBOOK.md §6
ABANDON: G3 only 5 slides passed QC (S6 failed); test stopped by Ralph
ABANDON: G4 S6 open in qc/QC.md; test stopped by Ralph
ABANDON: G6 review page done (5NCFPRRD9Cxzp5Yq5zusAj) but Ralph never signed off; test stopped
ABANDON: G7 nothing uploaded to Drive; test stopped by Ralph
