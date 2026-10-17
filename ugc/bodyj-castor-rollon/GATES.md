# Gates: BodyJ4You castor oil roll-on, AI hands-only ad (Grace), 2026-10-17

OWNS: ugc/bodyj-castor-rollon/**

Scope: one AI video for Grace answering "I think we all need castor oil" on her cradle cap video, plan-stage first (scripts, storyboard, one total cost, Ralph's approval), then the cut, QC and Drive delivery.

- [x] G1: Script gate passes at plan stage (all 9 proofs, banned phrases clean)
  CHECK: python3 ../../grace/gate.py .
  EXPECT: GATE OK
  EVIDENCE: GATE OK, 2026-10-17 01:20Z (9/9 proofs)

- [x] G2: Every script option mentions cradle cap at most once, in the first two lines, and ends with "It's in the orange cart."
  CHECK: python3 check_scripts.py
  EXPECT: SCRIPTS_OK
  EVIDENCE: SCRIPTS_OK

- [x] G3: Every script reads at grade 6 or lower
  CHECK: python3 check_scripts.py --grade
  EXPECT: GRADE_OK
  EVIDENCE: GRADE_OK (A 3.6, B 3.3, C 2.6)

- [ ] G4: Every claim in the scripts is in product_facts.md with a listing source, unbacked claims flagged
  EVIDENCE: pending

- [ ] G5: Still storyboard (one still per shot, real product pasted back) shown to Ralph with ONE total cost before any video spend
  EVIDENCE: pending

- [ ] G6: Ralph approved the plan and cost in his own words
  EVIDENCE: pending

- [ ] G7: Final cut 1080x1920, length within 20-40 s
  CHECK: python3 check_scripts.py --cut out/bodyj_castor.mp4
  EXPECT: CUT_OK
  EVIDENCE: pending

- [ ] G8: Cut-stage gate passes (compare vs the winner, no text overlay)
  CHECK: python3 ../../grace/gate.py . --stage cut
  EXPECT: GATE OK
  EVIDENCE: pending

- [ ] G9: QC report: real product unchanged, no shimmer, whole wrists, hands from frame edge, 2x edge zoom, first second, AI finish applied, REMOVED.md checked
  EVIDENCE: pending

- [ ] G10: Drive: CURRENT - files in one BodyJ4You (Grace) folder in Grace Tiktok assets, link in README; Ralph emailed
  EVIDENCE: pending
