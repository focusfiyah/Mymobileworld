# GATES: Vans sequin V12 recreation (Grace), 2026-10-24

- [x] G1: Script gate passes (all proofs, banned phrases)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/vans-sequin-v12 2>&1
  EXPECT: GATE OK
- [x] G2: Every logo close-up the clips need exists (insole, side tab, heel label) + sheet + place photo
  CHECK: test -s refs/product_sheet.png && test -s refs/real_insole_logo.jpg && test -s refs/real_vans_tab.jpg && test -s refs/real_heel_label.jpg && test -s refs/ground_herringbone.jpg && echo REFS_OK
  EXPECT: REFS_OK
- [x] G3: Production Book approved by Ralph before any paid call
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/vans-sequin-v12 2>&1
  EXPECT: BOOK: approved
- [x] G4: 6 stills exist and passed QC (2 shoes max, grip, five fingers, logos vs close-ups, no turn set up)
  CHECK: python3 -c "import os;print('STILLS_6' if all(os.path.exists(f'stills/S{i}.png') for i in range(1,7)) else 'NO')"
  EXPECT: STILLS_6
- [x] G5: 6 clips exist (Flow takes or approved Kie fallback)
  CHECK: python3 -c "import os;print('CLIPS_6' if all(os.path.exists(f'clips/S{i}.mp4') for i in range(1,7)) else 'NO')"
  EXPECT: CLIPS_6
- [x] G6: Final cut is 1080x1920
  CHECK: ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0 out/vans_v12.mp4
  EXPECT: 1080,1920
- [x] G7: Cut gate (compare vs the ref, no text) passes
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/vans-sequin-v12 --stage cut 2>&1
  EXPECT: GATE OK
- [x] G8: QC report: 2x edges, first second, no held-shoe turn, max 2 shoes, logos vs close-ups, REMOVED.md
  EVIDENCE: qc/QC.md + qc/check.py CHECK_OK on out/V12_final.mp4 (2026-10-25); Ralph caught S1's wrong shoe of the pair on Flow take 1, fixed with a fresh still
- [x] G9: Drive "Vans sequin (Grace)" has CURRENT - Vans V12 + caption doc line, link in README
  EVIDENCE: https://drive.google.com/drive/folders/1sCPZmn3mSM_BazNZxNxVFibniSqUOE-_ (CURRENT - Vans V12.mp4 14,209,875 bytes = local; CURRENT - Vans captions with the V12 line, old doc in Older versions as v2 (2026-10-22))
