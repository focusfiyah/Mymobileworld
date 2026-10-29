# GATES: Vans sequin V13-V17, 5 AI videos on Grace's own VO (Grace), 2026-10-29

OWNS: ugc/vans-vo5/**

Scope: five ~27.6 s hands + feet AI videos of the Vans Premium Authentic sequin checkerboard, each cut to Grace's own
voiceover from https://www.tiktok.com/t/ZPLDRH7Rk (her post 7699252578239925535), visuals matched line by line, every
video with its own places, outfits, shots, order and framing; QC'd, AI-finished, in Drive.

## Phase 1: plan (before any spend)
- [x] G1: Grace's voice separated from the music bed, full length, clone sample logged
  CHECK: python3 tools/check.py vo
  EXPECT: VO_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=dee052ae24accdea54444b273337a6138133e4d1f90021ae41c4a1f36b99700d; exit=0; EXPECT=matched; output-sha256=c651e0e60d97ae4bedaf887e198570412ffa116e6d4b7eb1ce21dee303f32da4; output-bytes=6; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/vans-vo5; path=7f4fb4b02918/15 entries
- [x] G2: Product truth written from the real photos (facts + forbid, every photo exists)
  CHECK: python3 tools/check.py truth
  EXPECT: TRUTH_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=fab52754468f436515907dbd757dd77b5d72b05277cce57dcc194b88b963260a; exit=0; EXPECT=matched; output-sha256=be3a515e39e9388a549ac4fdfd9834edfef39a978001a2cbcd008c643382692e; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/vans-vo5; path=7f4fb4b02918/15 entries
- [x] G3: shots.json = 5 videos x 11 shots covering 0-27.6 s with no gap, each still <= 8 refs, every ref file exists, own place photos per video, no two videos share a shot idea
  CHECK: python3 tools/check.py shots
  EXPECT: SHOTS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=2f448f048f48aaef23acf8de39746f7fad87e3066c1e15ef17237069009b6939; exit=0; EXPECT=matched; output-sha256=700c872acf04d834a37cb04f99353c2a855be2097154d9e9c53a93be6ca69ab4; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/vans-vo5; path=7f4fb4b02918/15 entries
- [x] G4: Every still and clip prompt passes prompt_check lint (image numbers, toe direction, framing, effect words, forbid list)
  CHECK: cd /home/user/Mymobileworld && python3 grace/prompt_check.py lint ugc/vans-vo5/shots.json 2>&1
  EXPECT: PROMPT_LINT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=ee5e7bdc7aa40b962e723625c474aecce39adffb10f4d00882a0a8a704abf32b; exit=0; EXPECT=matched; output-sha256=5c4f728c7c01f694f1f5cd0ff2c5c73b84f583e2b6210c48e82bf87254d8a796; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/vans-vo5; path=7f4fb4b02918/15 entries
- [x] G5: Script gate passes (proofs + banned phrases; verbatim-VO note recorded)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/vans-vo5 2>&1
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=d6da9593a2a440722f1c28084fea35e68c57f62ab01e78f5e1daab3b868c855f; exit=0; EXPECT=matched; output-sha256=1ab5a5adbb0010e574a4c4b6e3fa82b85e63f529e242414ffd1d560bd8fe1372; output-bytes=154; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/vans-vo5; path=7f4fb4b02918/15 entries
- [x] G6: BOOK.md has one TOTAL line and a Sent to Ralph line with the review page link
  CHECK: python3 tools/check.py book
  EXPECT: BOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=c814749f19890f0b756713843e24bb93656345aec45dcba92219716b5b1f3df2; exit=0; EXPECT=matched; output-sha256=9e3343135cc993ebad1c7063868498f46d4d79987594dbe5fd96d7c1283ddd4a; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/vans-vo5; path=7f4fb4b02918/15 entries
- [x] G7: Review page published with the plan, places and Grace's VO playable; Ralph told by push + email
  EVIDENCE: https://claude.ai/artifact/SK6yEMLyJ45i2UcoofCJ5s v1 (video + mp3 + 10 place photos + 55 shot rows + 110 prompts); PushNotification "Mobile push requested"; Gmail id 1a185b34ad0fa812 sent 2026-10-29

## Phase 2: make (after Ralph's OK on BOOK.md)
- [ ] G8: Production Book approved by Ralph before any paid call
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/vans-vo5 2>&1
  EXPECT: BOOK: approved
- [ ] G9: 55 stills exist and passed QC (2 shoes max, grip, five fingers, correct side of the pair, logos vs close-ups)
  CHECK: python3 tools/check.py stills
  EXPECT: STILLS_OK
- [ ] G10: 55 clips exist
  CHECK: python3 tools/check.py clips
  EXPECT: CLIPS_OK
- [ ] G11: 5 final cuts, 1080x1920, length within 0.2 s of the VO, audio = Grace's VO
  CHECK: python3 tools/check.py cuts
  EXPECT: CUTS_OK
- [ ] G12: Cut gate (compare vs Grace's post, no text) passes
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/vans-vo5 --stage cut 2>&1
  EXPECT: GATE OK
- [ ] G13: QC on every cut: 2x edges, first second, no held-shoe turn or flip, max 2 shoes, logos vs close-ups, REMOVED.md, verify_fix (flash, sync, levels)
  EVIDENCE: pending
- [ ] G14: Drive "Vans sequin (Grace)" has CURRENT - Vans V13..V17 + captions, sizes match, link in README
  EVIDENCE: pending
