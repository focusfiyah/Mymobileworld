# Gates: Shnuggle toddler tub response videos (Grace)

OWNS: ugc/shnuggle-response/**

Scope: Two AI hands-only response videos (R1 "over priced", R2 "just the right size") on Grace's scripts word for word, QC'd, AI-finished, delivered to Drive, Ralph notified.

- [x] G1: Spoken lines in shots.json equal Grace's scripts word for word for both videos
  CHECK: python3 ugc/shnuggle-response/qc/gates_check.py vo_match
  EXPECT: vo_match PASS
  EVIDENCE: vo_match PASS (2026-10-16 23:55)

- [x] G2: Script gate passes (all PLAYBOOK §4 proofs, override recorded for R2 readability)
  CHECK: python3 ugc/shnuggle-response/qc/gates_check.py plan_gate
  EXPECT: plan_gate PASS
  EVIDENCE: plan_gate PASS

- [x] G3: Listing claims flagged to Ralph, not edited (research/product_facts.md) and plan with storyboard and one total cost approved by Ralph before any paid call
  EVIDENCE: product_facts.md flags sent in the plan; Ralph approved the $7.56 plan ("Yes") before any paid call; each redo asked with its cost

- [x] G4: R1 and R2 use different footage (no shared plate or clip)
  CHECK: python3 ugc/shnuggle-response/qc/gates_check.py different
  EXPECT: different PASS
  EVIDENCE: different PASS

- [x] G5: Both finals exist, over 30 s, AI finish applied as the last step
  CHECK: python3 ugc/shnuggle-response/qc/gates_check.py finals
  EXPECT: finals PASS
  EVIDENCE: finals PASS (45.67 s / 39.53 s, ai finish inline in cut.py)

- [x] G6: QC report all clear for both cuts (hands: birthstone rings only, no bracelet or watch, whole wrist from frame edge, grip; 2x edge zoom; first second; product unchanged; no text; no child; REMOVED.md checked)
  CHECK: python3 ugc/shnuggle-response/qc/gates_check.py qc_report
  EXPECT: qc_report PASS
  EVIDENCE: qc_report PASS; QC.md review 2 ALL CLEAR (plug removed, dense 0.45 s check)

- [x] G7: Cut-stage gate passes (coach compare vs the top winner)
  CHECK: python3 ugc/shnuggle-response/qc/gates_check.py cut_gate
  EXPECT: cut_gate PASS
  EVIDENCE: cut_gate PASS

- [x] G8: Drive folder "Shnuggle Toddler Tub (Grace)" in Grace Tiktok assets holds CURRENT R1 + R2 + script doc, link sent; Ralph emailed at each review point
  EVIDENCE: Drive folder 1eXtI8h9xioVSJlxg53pI7j96jLvN_3O3: CURRENT R1 70904893 B + R2 61447249 B (= local) + script doc; emails sent at each review point; Ralph approved 2026-10-16 23:58
