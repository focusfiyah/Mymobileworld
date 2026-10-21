# Gates: Shnuggle toddler tub, "the next bath" (Grace)

OWNS: ugc/shnuggle-next-bath/**

Scope: One 25-35 s hands-only AI video for Grace on the brief's angle (toddler's next bath after the infant tub), product locked to the real tub, QC'd, AI-finished, in Drive, Ralph notified.

- [ ] G1: Script gate passes (all PLAYBOOK §4 proofs newer than the script)
  CHECK: python3 ugc/shnuggle-next-bath/qc/gates_check.py plan_gate
  EXPECT: plan_gate PASS

- [ ] G2: Shot mix is a third to a half hand-free
  CHECK: python3 ugc/shnuggle-next-bath/qc/gates_check.py shot_mix
  EXPECT: shot_mix PASS

- [ ] G3: Product lock: the real-photo product sheet exists and every tub still and hand clip is made from it (ref mode, no pasted label)
  CHECK: python3 ugc/shnuggle-next-bath/qc/gates_check.py product_lock
  EXPECT: product_lock PASS

- [ ] G4: Ralph approved one plan with the script choice, every shot and one total cost before any paid call; every redo asked with its cost
  EVIDENCE:

- [ ] G5: Voiceover says the approved script word for word (STT = script = shots.json)
  CHECK: python3 ugc/shnuggle-next-bath/qc/gates_check.py vo_match
  EXPECT: vo_match PASS

- [ ] G6: New footage only, no clip shared with the R1/R2 Shnuggle videos
  CHECK: python3 ugc/shnuggle-next-bath/qc/gates_check.py different
  EXPECT: different PASS

- [ ] G7: Final cut exists, 25-35 s, AI finish applied as the last step
  CHECK: python3 ugc/shnuggle-next-bath/qc/gates_check.py finals
  EXPECT: finals PASS

- [ ] G8: QC report ALL CLEAR (tub unchanged vs the sheet, grip, whole wrist from frame edge, 2x edge zoom + first second, no shimmer, no text, no child, no plug, REMOVED.md checked)
  CHECK: python3 ugc/shnuggle-next-bath/qc/gates_check.py qc_report
  EXPECT: qc_report PASS

- [ ] G9: Cut-stage gate passes (coach compare vs the top winner)
  CHECK: python3 ugc/shnuggle-next-bath/qc/gates_check.py cut_gate
  EXPECT: cut_gate PASS

- [ ] G10: In Drive "Grace Tiktok assets/Shnuggle Toddler Tub (Grace)" as CURRENT (older Shnuggle files untouched or versioned), sizes match, link sent; Ralph emailed + pushed at each review point
  EVIDENCE:
