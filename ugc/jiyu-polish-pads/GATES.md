# GATES: JIYU Cleansing Polish Pads (Grace), 2026-10-24

- [x] G1: Script gate passes (proofs newer than the script, override recorded)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/jiyu-polish-pads 2>&1
  EXPECT: GATE OK
- [x] G2: Product sheet + logo close-ups built from JIYU's real photos
  CHECK: test -s refs/product_sheet.png && test -s refs/closeup_jiyu_front.png && test -s refs/closeup_lid_top.png && test -s refs/closeup_pad_texture.png && echo SHEET_OK
  EXPECT: SHEET_OK
- [x] G3: Production Book approved by Ralph before any paid call
  CHECK: python3 -c "import json;c=json.load(open('checklist.json'));print('BOOK_OK' if c.get('book_ok') else 'NO')"
  EXPECT: BOOK_OK
- [x] G4: 10 current stills exist and passed QC (jar = real pink lid/mint/blue JIYU, half face only, grip, five digits)
  CHECK: python3 -c "import json,os;c=json.load(open('stills/current.json'));print('STILLS_10' if sum(os.path.exists(f'stills/{v}.png') for v in c.values())==10 else 'NO')"
  EXPECT: STILLS_10
- [x] G5: Voiceover passes the echo gate (<= 150 ms)
  CHECK: cd /home/user/Mymobileworld && python3 grace/voice/echo.py ugc/jiyu-polish-pads/vo/vo_final.wav 2>&1
  EXPECT: PASS
- [x] G6: Final cut exists, 1080x1920, AI finish applied
  CHECK: ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0 out/jiyu_v2.mp4
  EXPECT: 1080,1920
- [x] G7: Cut gate (compare vs winner, no text) passes
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/jiyu-polish-pads --stage cut 2>&1
  EXPECT: GATE OK
- [x] G8: QC report: 2x edges, first second, no eyes/mouth, REMOVED.md checked
  EVIDENCE: qc/QC.md + qc/check.py CHECK_OK on out/jiyu_v2.mp4 (2026-10-24); Ralph caught S3 six fingers in v1, fixed in v2
- [x] G9: Drive folder "JIYU Polish Pads (Grace)" has CURRENT video + script doc, link in README
  EVIDENCE: https://drive.google.com/drive/folders/1huj4iFB4i2zXqIDHB7WuEiBvI6sygjbH (CURRENT - JIYU V1.mp4 82,351,211 bytes = local; CURRENT - JIYU script + caption)
