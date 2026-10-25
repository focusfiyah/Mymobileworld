# GATES: OQQ wide-leg pants (black + brown) AI recreation of @krunch.7 (Grace), 2026-10-25

- [x] G1: Script gate passes (all proofs, banned phrases)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/oqq-wide-leg-pants 2>&1
  EXPECT: GATE OK
- [x] G2: Inspo beat table exists with every look, move and a setting row
  CHECK: python3 -c "t=open('research/inspo_beats.md').read().lower();print('BEATS_OK' if all(k in t for k in ['| time','setting','camera','money move']) else 'NO')"
  EXPECT: BEATS_OK
- [x] G3: Refs exist: real-photo product sheet, pocket close-up, Vans sequin close-ups, Grace body sheet, room photo
  CHECK: test -s refs/product_sheet.png && test -s refs/real_pocket.jpg && test -s refs/real_vans_tab.jpg && test -s refs/grace_body_sheet.jpg && test -s refs/room.jpg && echo REFS_OK
  EXPECT: REFS_OK
- [x] G4: Production Book approved by Ralph before any paid call
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/oqq-wide-leg-pants 2>&1
  EXPECT: BOOK: approved
- [x] G5: Every planned still exists and passed QC at 2x (stills/QC.md lists each one PASS)
  CHECK: python3 -c "import json,os;s=json.load(open('shots.json'))['shots'];q=open('stills/QC.md').read() if os.path.exists('stills/QC.md') else '';print('STILLS_OK' if s and all(os.path.exists('stills/%s.png'%x['id']) and ('%s PASS'%x['id']) in q for x in s) else 'NO')"
  EXPECT: STILLS_OK
- [x] G6: Every planned clip exists
  CHECK: python3 -c "import json,os;s=json.load(open('shots.json'))['shots'];print('CLIPS_OK' if s and all(os.path.exists('clips/%s.mp4'%x['id']) for x in s) else 'NO')"
  EXPECT: CLIPS_OK
- [x] G7: Final cut is 1080x1920
  CHECK: ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0 out/oqq_final.mp4
  EXPECT: 1080,1920
- [x] G8: Cut gate (compare vs the inspo, no text) passes
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/oqq-wide-leg-pants --stage cut 2>&1
  EXPECT: GATE OK
- [x] G9: QC report: 2x edges, first second, pants colour/seam/pocket vs real photos, shoes vs Vans close-ups, solid (not sheer) fabric, REMOVED.md, AI finish
  EVIDENCE: qc/QC.md (2026-10-25): cuts on boundaries only, hands 2x, S4 logo painted out, S2 dropped, REMOVED.md rows checked
- [ ] G10: Drive folder "OQQ Wide Leg Pants (Grace)" has CURRENT video + script/caption doc, link in README
  EVIDENCE: (manual) Drive link
