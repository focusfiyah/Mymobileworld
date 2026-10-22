# Gates: Goth High-Low Skirt (Grace), V1 boots recreation

OWNS: ugc/goth-highlow-skirt/**

Scope: one ~15 s vertical AI video recreating the inspo (@jaquelineee809, adjustable-length mirror video) with boots instead of heels, the real NOVALL black skirt locked (Omni on Kie), approved by Ralph, delivered to Drive.

- [x] G1: Script gate passes on the current script
  CHECK: python3 grace/gate.py ugc/goth-highlow-skirt
  EXPECT: GATE OK
  EVIDENCE: 2026-10-22 GATE OK

- [x] G2: Product reference sheet exists, built only from real listing photos
  CHECK: python3 -c "from PIL import Image; im=Image.open('ugc/goth-highlow-skirt/refs/product_sheet.png'); print('SHEET_OK' if im.size==(1600,2400) else 'bad')"
  EXPECT: SHEET_OK
  EVIDENCE: 2026-10-22 SHEET_OK (make_sheet.py, listing photos 08/25/26/27/34)

- [x] G3: Ralph approved the one-message plan + total cost (and the open questions) before any paid call; his words quoted in README
  EVIDENCE: Ralph 2026-10-22 "Knee high boots, with bracelet, dark brown, no text, music only, Kie" (README)

- [x] G4: Test still S2 QC'd at full size + 2x edges (grip on cords, whole wrists, real skirt details, boots not heels), then the other stills; storyboard shown before any clip spend
  EVIDENCE: S2 r1 failed (fitted midi, no grip) -> r2 passed at 2x; storyboards r2/r6/r8 on the review page before clip spend; 5 looks BACK/S2/TOP/ONELEG/SHORT

- [x] G5: Test clip S2 (riskiest: the pull) QC'd frame by frame before the other clips
  EVIDENCE: pull tests S2 Omni, T2 Omni first+last, R1/R3 Seedance, V1 Veo each QC'd at 4 fps + 2x hem (qc/*_sheet.jpg); none shortened the skirt; Ralph chose the tug-cut

- [x] G6: Final cut exists, 9-18 s (tug-cut came to 11.7 s, in the 9-12 s winners' range), 1080x1920, every shot moving, no text, ai_finish applied last
  CHECK: python3 ugc/goth-highlow-skirt/qc/final_check.py
  EXPECT: FINAL_OK
  EVIDENCE: run by hand 2026-10-22: FINAL_OK (11.7s)

- [x] G7: Cut gate passes (coach compare vs the inspo done)
  CHECK: python3 grace/gate.py ugc/goth-highlow-skirt --stage cut
  EXPECT: GATE OK
  EVIDENCE: run by hand 2026-10-22: GATE OK (proof/compare.md)

- [ ] G8: Cut checked against REMOVED.md; on the review page; Ralph pushed + emailed; Ralph approved

- [ ] G9: In Drive "Grace Tiktok assets" product folder as CURRENT, link in README; Kie cost vs quote recorded; job branch merged to main
