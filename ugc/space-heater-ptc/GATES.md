# Gates: Antarctic Star 1500W PTC space heater (Grace), hands-only AI videos

OWNS: ugc/space-heater-ptc/**

Scope: ONE script (V1, Ralph 2026-10-19: 'just choose the best one'; V2/V3 dropped) + a hands-only AI video (Grace's hands with the gold bracelet and blue birthstone ring, Grace C VO), a different room per shot, lots of motion; my product reference sheet compared with Ralph's; free room plates first; plan + one total cost approved before any paid call; QC'd, AI-finished, in Drive, Ralph notified.

- [x] G1: My product reference sheet (real listing pixels only) and a side-by-side comparison with Ralph's sheet exist
  CHECK: python3 ugc/space-heater-ptc/qc/gates_check.py sheets
  EXPECT: sheets PASS
  EVIDENCE: sheets PASS (2026-10-19, ran directly; refs/product_sheet.png from refs/listing real pixels, refs/sheet_compare.jpg)

- [x] G2: At least 8 free room photos in rooms/, each with source URL and licence in rooms/SOURCES.md
  CHECK: python3 ugc/space-heater-ptc/qc/gates_check.py rooms
  EXPECT: rooms PASS
  EVIDENCE: rooms PASS (18 plates, Pexels/Pixabay, rooms/SOURCES.md)

- [x] G3: Three scripts, each opens with a different hook-library id said word for word and closes "It's in the orange cart."
  CHECK: python3 ugc/space-heater-ptc/qc/gates_check.py scripts
  EXPECT: scripts PASS
  EVIDENCE: scripts PASS (V1 H063, V2 H027, V3 H126, all close with the orange cart line)

- [x] G4: Script gate passes (all PLAYBOOK §4 proofs newer than the script, no banned phrase)
  CHECK: python3 grace/gate.py ugc/space-heater-ptc
  EXPECT: GATE OK
  EVIDENCE: GATE OK (2026-10-19)

- [x] G5: shots.json marks every shot HAND or HAND-FREE, a third to half hand-free per video, and no room plate is shared between videos
  CHECK: python3 ugc/space-heater-ptc/qc/gates_check.py shots
  EXPECT: shots PASS
  EVIDENCE: shots PASS (V1 5/10, V2 4/9, V3 4/9 hand-free; 6 own rooms per video)

- [x] G6: Plan with storyboard, sheet comparison and one total cost sent (review page + email + push) and approved by Ralph before any paid call
  EVIDENCE: Ralph approved V1 at $2.13 (2026-10-19, 'Approved, your default is fine'); review page https://claude.ai/artifact/Domjukqum8q4ee1X6AhqMG, email + push each stop

- [x] G7: Still storyboard (paid stills) shown and approved before any video spend
  EVIDENCE: Still stop kept (Ralph): r1-r3 + free fixes + 1 edit shown; Ralph's notes (S5 keep ring on thumb) applied before clips

- [x] G8: The V1 final exists, is 9:16, has audio and was AI-finished as the last step
  CHECK: python3 ugc/space-heater-ptc/qc/gates_check.py finals
  EXPECT: finals PASS
  EVIDENCE: finals PASS (out/heater_V1.mp4 30.09 s, 720x1280, audio, heater_V1.finish.json)

- [x] G9: QC report all clear on the V1 cut (hands from frame edge with bracelet + birthstone ring, grip, 2x edge zoom, first second, product unchanged, no text, REMOVED.md checked)
  EVIDENCE: qc/QC.md all clear (S8 tail cut, S3 top trim, S3 upside-down digits noted)

- [x] G10: Cut-stage gate passes (coach compare vs the top winner)
  CHECK: python3 grace/gate.py ugc/space-heater-ptc --stage cut
  EXPECT: GATE OK
  EVIDENCE: GATE OK --stage cut (research/compare/compare_V1.md)

- [ ] G11: Drive "Grace Tiktok assets" / one heater folder holds the CURRENT video + script doc, link sent, Ralph emailed + pushed at each review point
  EVIDENCE:
