# GATES: JIYU Cleansing Polish Pads (Grace), 2026-10-24

- [ ] G1: Script gate passes (proofs newer than the script, override recorded)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/jiyu-polish-pads 2>&1
  EXPECT: GATE OK
- [ ] G2: Product sheet + logo close-ups built from JIYU's real photos
  CHECK: test -s refs/product_sheet.png && test -s refs/closeup_jiyu_front.png && test -s refs/closeup_lid_top.png && test -s refs/closeup_pad_texture.png && echo SHEET_OK
  EXPECT: SHEET_OK
- [ ] G3: Production Book approved by Ralph before any paid call
  CHECK: python3 -c "import json;c=json.load(open('checklist.json'));print('BOOK_OK' if c.get('book_ok') else 'NO')"
  EXPECT: BOOK_OK
- [ ] G4: 10 stills exist and passed QC (jar = real pink lid/mint/blue JIYU, half face only, grip)
  CHECK: ls stills/S*.png | wc -l | sed "s/^10$/STILLS_10/"
  EXPECT: STILLS_10
- [ ] G5: Voiceover passes the echo gate (<= 150 ms)
  CHECK: cd /home/user/Mymobileworld && python3 grace/voice/echo.py ugc/jiyu-polish-pads/vo/vo_final.wav 2>&1
  EXPECT: PASS
- [ ] G6: Final cut exists, 1080x1920, AI finish applied
  CHECK: ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0 out/jiyu_v1.mp4
  EXPECT: 1080,1920
- [ ] G7: Cut gate (compare vs winner, no text) passes
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/jiyu-polish-pads --stage cut 2>&1
  EXPECT: GATE OK
- [ ] G8: QC report: 2x edges, first second, no eyes/mouth, REMOVED.md checked on every frame
  EVIDENCE: pending
- [ ] G9: Drive folder "JIYU Polish Pads (Grace)" has CURRENT video + script doc, link in README
  EVIDENCE: pending
