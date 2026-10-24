# GATES: PRITECH black face scrubber (Grace), 2026-10-23

- [ ] G1: Script gate passes (proofs newer than the script, override recorded)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/pritech-cleansing-brush 2>&1
  EXPECT: GATE OK
- [ ] G2: Production Book approved by Ralph before any paid call
  CHECK: python3 -c "import json;c=json.load(open('checklist.json'));print('BOOK_OK' if c.get('book_ok') else 'NO')"
  EXPECT: BOOK_OK
- [ ] G3: Product sheet built from real photos
  CHECK: test -s refs/product_sheet.png && echo SHEET_OK
  EXPECT: SHEET_OK
- [ ] G4: 9 approved stills exist
  CHECK: ls stills/S?.png | wc -l | sed "s/^9$/STILLS_9/"
  EXPECT: STILLS_9
- [ ] G5: Flow trial logged (both S6 takes, credits, Ralph's pick)
  CHECK: grep -c "pritech" /home/user/Mymobileworld/grace/flow/RESULTS.md | sed 's/^[1-9].*/FLOW_LOGGED/'
  EXPECT: FLOW_LOGGED
- [ ] G6: Voiceover passes the echo gate (<= 150 ms)
  CHECK: cd /home/user/Mymobileworld && python3 grace/voice/echo.py ugc/pritech-cleansing-brush/vo/vo_final.wav 2>&1
  EXPECT: PASS
- [ ] G7: Final cut exists, 9:16, AI finish applied
  CHECK: ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0 out/pritech_v1.mp4
  EXPECT: 1080,1920
- [ ] G8: Cut gate (compare vs winner, no text) passes
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/pritech-cleansing-brush --stage cut 2>&1
  EXPECT: GATE OK
- [ ] G9: (manual) QC: 2x edges + first second, no eyes/mouth on screen, product matches the sheet in every clip, REMOVED.md checked
- [ ] G10: (manual) Spend within BOOK TOTAL + approved extras (grace/spend.py)
- [ ] G11: (manual) Drive folder "PRITECH Face Scrubber (Grace)" with CURRENT video + script doc; link sent
