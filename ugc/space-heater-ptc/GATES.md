# Gates: Antarctic Star 1500W PTC space heater (Grace), hands-only AI videos

OWNS: ugc/space-heater-ptc/**

Scope: 3 script angles + hands-only AI videos (Grace's hands with the gold bracelet and blue birthstone ring, Grace C VO), a different room per shot, lots of motion; my product reference sheet compared with Ralph's; free room plates first; plan + one total cost approved before any paid call; QC'd, AI-finished, in Drive, Ralph notified.

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

- [ ] G6: Plan with storyboard, sheet comparison and one total cost sent (review page + email + push) and approved by Ralph before any paid call
  EVIDENCE: SENT 2026-10-19: https://claude.ai/artifact/Domjukqum8q4ee1X6AhqMG, email 1a1530aa42c532dd, push requested. Waiting on approval.

- [ ] G7: Still storyboard (paid stills) shown and approved before any video spend
  EVIDENCE:

- [ ] G8: Each approved video's final exists, is 9:16, has audio and was AI-finished as the last step
  CHECK: python3 ugc/space-heater-ptc/qc/gates_check.py finals
  EXPECT: finals PASS

- [ ] G9: QC report all clear per cut (hands from frame edge with bracelet + birthstone ring, grip, 2x edge zoom, first second, product unchanged, no text, REMOVED.md checked)
  EVIDENCE:

- [ ] G10: Cut-stage gate passes (coach compare vs the top winner)
  CHECK: python3 grace/gate.py ugc/space-heater-ptc --stage cut
  EXPECT: GATE OK

- [ ] G11: Drive "Grace Tiktok assets" / one heater folder holds CURRENT videos + script doc, link sent, Ralph emailed + pushed at each review point
  EVIDENCE:
