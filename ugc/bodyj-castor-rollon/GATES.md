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

- [x] G4: Every claim in the scripts is in product_facts.md with a listing source, unbacked claims flagged
  EVIDENCE: research/product_facts.md claims table: every spoken claim (rose quartz roller, USDA organic, cold pressed, hexane free, old link gone) has a listing or Ralph source

- [x] G5: Still storyboard (one still per shot, real product pasted back) shown to Ralph with ONE total cost before any video spend
  EVIDENCE: preview/storyboard.jpg shown; Ralph tapped 'Yes, start' on 'Start the clips with this storyboard for $1.64?' (2026-10-17 06:29Z)

- [x] G6: Ralph approved the plan and cost in his own words
  EVIDENCE: Ralph 2026-10-17 05:16Z: "Option a, and ok with Kie. use these two reference sheets for the product."

- [x] G7: Final cut 1080x1920, length within 20-40 s
  CHECK: python3 check_scripts.py --cut out/bodyj_castor.mp4
  EXPECT: CUT_OK
  EVIDENCE: CUT_OK on out/bodyj_castor_rollon_r1_final.mp4 (1080x1920, 31.97 s), 2026-10-17 07:00Z

- [x] G8: Cut-stage gate passes (compare vs the winner, no text overlay)
  CHECK: python3 ../../grace/gate.py . --stage cut
  EXPECT: GATE OK
  EVIDENCE: GATE OK (--stage cut), compare proof research/compare/notes.md, no text drawn by cut.py

- [x] G9: QC report: real product unchanged, no shimmer, whole wrists, hands from frame edge, 2x edge zoom, first second, AI finish applied, REMOVED.md checked
  EVIDENCE (2026-10-17): qc/check_cut.py ALL OK (cuts between words, no freeze/black, -13.7 LUFS); 2x edge zooms qc/cut_zoom.jpg clean; first second qc/S1r2_*; nails/skin hold (S1 r2); AI finish applied; REMOVED.md checked. Real label pasted on S1 S5 S7 S8 S9 (+ real box on S9). OPEN: S4 and S6 show the AI's own small label (tracker could not fit it, bottle turned/small): letters soft/warped there. Raised with Ralph; he approved r1 with it (2026-10-17 07:30Z: "Approved").

- [x] G10: Drive: CURRENT - files in one BodyJ4You (Grace) folder in Grace Tiktok assets, link in README; Ralph emailed
  EVIDENCE: Drive 'CURRENT - BodyJ castor roll-on (Grace AI video r1, 2026-10-17).mp4' in folder 19jUSElPjnXIC0f3DFoiaxA1Kl9333_nk, size 82087212 matches; email + push sent
