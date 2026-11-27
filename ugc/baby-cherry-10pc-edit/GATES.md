# Gates: Baby Girl Floral Cherry 10-Piece Set edit (Grace, 2026-11-25)

OWNS: ugc/baby-cherry-10pc-edit/**

Scope: two edits of Grace's own HD footage (V1 silent up to 29 s per her msg 843 (was 7-20 s, msg 764) showing all 10 pieces + features; V2 a cut sized to a voiceover script she records) plus the V2 script through the Grace script gate, reviewed by Ralph, CURRENT in Drive, done messages sent.

- [x] G1: Grace's original video(s) are in the Originals folder and downloaded at full resolution (Drive size = local size, not the Telegram copy)
  EVIDENCE: 2026-11-27 9 files IMG_0921-0930 (no 0922) downloaded, every size = Drive size (51,757,680 ... 43,999,410 B); h264 1080x1920 (rot -90) 30 fps, 6.7-26.4 s, no talking

- [x] G2: The V2 script passes the Grace script gate (all PLAYBOOK §4 proofs newer than the script, no banned phrase, line audit, research)
  CHECK: python3 grace/gate.py ugc/baby-cherry-10pc-edit
  EXPECT: GATE OK
  CWD: ../..
  EVIDENCE: 2026-11-27 GATE OK (ran by hand)

- [x] G3: V1 is 1080x1920, silent, 7-29 s, within 0.15 s of plan, no black frames
  CHECK: python3 check.py v1 7 29
  EXPECT: CUT_OK v1
  EVIDENCE: 2026-11-27 ran by hand: CUT_OK v1 24.00s (unlazy --approve not run: needs Ralph's say)

- [x] G4: V1 has every planned cut, no stray/flash frame, mean brightness >= 110
  CHECK: python3 cuts.py v1
  EXPECT: CUTS_OK
  EVIDENCE: 2026-11-27 CUTS_OK cuts=9 stray=[] yavg=129

- [x] G5: V2 is 1080x1920, silent (Grace adds her VO), length fits the script read at her pace (within 15-35 s), no black frames
  CHECK: python3 check.py v2 15 35
  EXPECT: CUT_OK v2
  EVIDENCE: 2026-11-27 CUT_OK v2 22.93s

- [x] G6: V2 has every planned cut, no stray/flash frame, mean brightness >= 110
  CHECK: python3 cuts.py v2
  EXPECT: CUTS_OK
  EVIDENCE: 2026-11-27 CUTS_OK cuts=10 stray=[] yavg=137; distinct.py DISTINCT_OK

- [x] G7: Both cuts viewed on frame sheets: V1 shows all 10 pieces and the features (soft, stretchy, breathable...), V2 shots follow the script lines; V1 and V2 use different shots/order; same room per video; REMOVED.md checked; earshot skipped with reason (silent cuts)
  EVIDENCE: 2026-11-27 qc/v1_3fps.jpg, qc/v2_3fps.jpg, v1_end.jpg viewed; all 5 sets in both; stretch shots in both; one bed, same hands; 1.5x flips jumped -> 1.25x; opener moved off the duplicate leopard; V1 end trimmed off the messy pile; REMOVED.md empty; earshot skipped (silent, Grace adds music/VO)

- [x] G8: Cuts + script on the review page; Ralph told (push + email); Grace answered on Telegram (no ✅/"done" while pending)
  EVIDENCE: 2026-11-27 review https://claude.ai/artifact/7qnDEKVrL8U43p9dKnxKBd; push requested; email 1a21a6cc0ea88a23; Grace group msgs 845-848 (script + hooks, <pre>), 855 (with Ralph, no ✅)

- [ ] G9: After Ralph's OK on those exact cuts: "CURRENT - Cherry Set V1.mp4", "CURRENT - Cherry Set V2.mp4" and the script Google Doc in the product folder, Drive size = local, nothing loose
  EVIDENCE: pending

- [ ] G10: "✅ Baby Girl Floral Cherry 10-Piece Set V1 (HD) is done and in Drive: <link>" (and V2) sent to Ralph on Telegram, and to Grace in the group
  EVIDENCE: pending

- [ ] G11: Brain job note + session log written, Active work line removed, BRAIN_OK; media packed MEDIA_OK
  EVIDENCE: pending
