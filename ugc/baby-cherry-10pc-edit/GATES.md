# Gates: Baby Girl Floral Cherry 10-Piece Set edit (Grace, 2026-11-25)

OWNS: ugc/baby-cherry-10pc-edit/**

Scope: two edits of Grace's own HD footage (V1 silent 7-20 s showing all 10 pieces + features; V2 a cut sized to a voiceover script she records) plus the V2 script through the Grace script gate, reviewed by Ralph, CURRENT in Drive, done messages sent.

- [ ] G1: Grace's original video(s) are in the Originals folder and downloaded at full resolution (Drive size = local size, not the Telegram copy)
  EVIDENCE: pending

- [ ] G2: The V2 script passes the Grace script gate (all PLAYBOOK §4 proofs newer than the script, no banned phrase, line audit, research)
  CHECK: python3 grace/gate.py ugc/baby-cherry-10pc-edit
  EXPECT: GATE OK
  CWD: ../..
  EVIDENCE: pending

- [ ] G3: V1 is 1080x1920, silent, 7-20 s, within 0.15 s of plan, no black frames
  CHECK: python3 check.py v1 7 20
  EXPECT: CUT_OK v1
  EVIDENCE: pending

- [ ] G4: V1 has every planned cut, no stray/flash frame, mean brightness >= 110
  CHECK: python3 cuts.py v1
  EXPECT: CUTS_OK
  EVIDENCE: pending

- [ ] G5: V2 is 1080x1920, silent (Grace adds her VO), length fits the script read at her pace (within 15-35 s), no black frames
  CHECK: python3 check.py v2 15 35
  EXPECT: CUT_OK v2
  EVIDENCE: pending

- [ ] G6: V2 has every planned cut, no stray/flash frame, mean brightness >= 110
  CHECK: python3 cuts.py v2
  EXPECT: CUTS_OK
  EVIDENCE: pending

- [ ] G7: Both cuts viewed on frame sheets: V1 shows all 10 pieces and the features (soft, stretchy, breathable...), V2 shots follow the script lines; V1 and V2 use different shots/order; same room per video; REMOVED.md checked; earshot skipped with reason (silent cuts)
  EVIDENCE: pending

- [ ] G8: Cuts + script on the review page; Ralph told (push + email); Grace answered on Telegram (no ✅/"done" while pending)
  EVIDENCE: pending

- [ ] G9: After Ralph's OK on those exact cuts: "CURRENT - Cherry Set V1.mp4", "CURRENT - Cherry Set V2.mp4" and the script Google Doc in the product folder, Drive size = local, nothing loose
  EVIDENCE: pending

- [ ] G10: "✅ Baby Girl Floral Cherry 10-Piece Set V1 (HD) is done and in Drive: <link>" (and V2) sent to Ralph on Telegram, and to Grace in the group
  EVIDENCE: pending

- [ ] G11: Brain job note + session log written, Active work line removed, BRAIN_OK; media packed MEDIA_OK
  EVIDENCE: pending
