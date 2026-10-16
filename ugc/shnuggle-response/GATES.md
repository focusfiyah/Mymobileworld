# Gates: Shnuggle toddler tub response videos (Grace)

OWNS: ugc/shnuggle-response/**

Scope: Two AI hands-only response videos (R1 "over priced", R2 "just the right size") on Grace's scripts word for word, QC'd, AI-finished, delivered to Drive, Ralph notified.

- [ ] G1: Spoken lines in shots.json equal Grace's scripts word for word for both videos
  CHECK: python3 ugc/shnuggle-response/qc/gates_check.py vo_match
  EXPECT: vo_match PASS
  EVIDENCE: pending

- [ ] G2: Script gate passes (all PLAYBOOK §4 proofs, override recorded for R2 readability)
  CHECK: python3 ugc/shnuggle-response/qc/gates_check.py plan_gate
  EXPECT: plan_gate PASS
  EVIDENCE: pending

- [ ] G3: Listing claims flagged to Ralph, not edited (research/product_facts.md) and plan with storyboard and one total cost approved by Ralph before any paid call
  EVIDENCE: pending

- [ ] G4: R1 and R2 use different footage (no shared plate or clip)
  CHECK: python3 ugc/shnuggle-response/qc/gates_check.py different
  EXPECT: different PASS
  EVIDENCE: pending

- [ ] G5: Both finals exist, over 30 s, AI finish applied as the last step
  CHECK: python3 ugc/shnuggle-response/qc/gates_check.py finals
  EXPECT: finals PASS
  EVIDENCE: pending

- [ ] G6: QC report all clear for both cuts (hands: no jewellery, whole wrist from frame edge, grip; 2x edge zoom; first second; product unchanged; no text; no child; REMOVED.md checked)
  CHECK: python3 ugc/shnuggle-response/qc/gates_check.py qc_report
  EXPECT: qc_report PASS
  EVIDENCE: pending

- [ ] G7: Cut-stage gate passes (coach compare vs the top winner)
  CHECK: python3 ugc/shnuggle-response/qc/gates_check.py cut_gate
  EXPECT: cut_gate PASS
  EVIDENCE: pending

- [ ] G8: Drive folder "Shnuggle Toddler Tub (Grace)" in Grace Tiktok assets holds CURRENT R1 + R2 + script doc, link sent; Ralph emailed at each review point
  EVIDENCE: pending
