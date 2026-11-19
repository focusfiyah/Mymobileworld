# Gates: Cleanwaste Wag Bag November edits (Grace's own footage, 2026-11-19)

OWNS: ugc/wag-bag-nov-edit/**

Scope: 3 edits of Grace's "November Wag Bag Assets" (Drive 1XFgvGUCgiOur-NgC80uUl82dap__y2pY): G1 grey shirt with WagBag2, G2 grey shirt without it (1,3,4), B1 black shirt. Full quality from her originals, QC'd, OK'd by Ralph, CURRENT in Drive, done messages sent. 7 more later (total 10).

- [x] G1: All 4 originals downloaded at full size (local bytes = Drive bytes), 1080x1920 HEVC
  EVIDENCE: 2026-11-19 wb1 206,925,709 / wb2 13,996,041 / wb3 116,006,552 / wb4 72,136,612 B = Drive sizes; all 1080x1920 30 fps HEVC with AAC audio
- [ ] G2: Grace's open questions (voice kept or silent, length) answered by her on Telegram
  EVIDENCE:
- [x] G3: All 3 cuts are 1080x1920, the agreed length, within 0.15 s of plan, no black frames, audio as agreed
  CHECK: python3 check.py all
  EXPECT: ALL_CUTS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=06eb386ded0cad4b5e32cda6e14c17c0b6f1a49b9f3f2f916ac537da87da8759; exit=0; EXPECT=matched; output-sha256=c08d4d8350f591b7898ee5f326e3e6066941081ec2cd7dbc81ca03231aa521de; output-bytes=142; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-nov-edit; path=7f4fb4b02918/15 entries
- [x] G4: The 3 cuts are different from each other (no take of the same line used in two cuts at the same source time, different order/framing)
  CHECK: python3 check.py distinct
  EXPECT: DISTINCT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=5b97486201ce443182f73c6d5d64f62c65000b825a3f58e8418aa7bdfaecabbc; exit=0; EXPECT=matched; output-sha256=ed29a59926234dab38a4c18d3c27c5d68a5e9a18998cbea0383fa601b79e3e86; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-nov-edit; path=7f4fb4b02918/15 entries
- [x] G5: Every cut viewed on a frame sheet + around each cut: right shirt in every shot, every line clean (no flubbed word, no cut mid-word), earshot sound check run (or skipped with reason), REMOVED.md checked
  EVIDENCE: 2026-11-19 qc/*_1fps.jpg + first-second strips + seam strips viewed; fixed stray frames (takes now start on her clip's first frame, source cuts at scene 0.28), clipped "anywhere"/"everyone", grey_v2 hook swapped to the clean 0:23 take; medium.en transcripts qc/tr_* show every line whole; earshot critique qc/critique_*.txt: loudness/sync ok, "no music" + "hit density" skipped (Grace adds music; hits = box rustle under voice); REMOVED.md empty (nothing removed yet). Known: grey CTA takes open on her top ~0.8 s (flagged to Ralph)
- [x] G6: Review page with the 3 cuts stacked; Ralph told (push + email) incl. flagged claims (Pentagon 90 days, "sold out before", the word "shitting"); Grace answered without ✅
  EVIDENCE: 2026-11-19 https://claude.ai/artifact/9SLqU3JZzN6C7cVACyARSQ ; push requested; email 1a1f1579512599c8; Grace group msg 601 (questions, no ✅), Ralph private msg 602
- [ ] G7: After Ralph's OK on each exact cut: CURRENT files in the Wag Bag product folder in "Grace Tiktok assets", Drive size = local, older versions moved per rule
  EVIDENCE:
- [ ] G8: One "✅ ... is done and in Drive: <link>" per version to Ralph and in the group (reply to 598)
  EVIDENCE:
- [ ] G9: Brain job note + session log, Active work line removed, BRAIN_OK; media packed MEDIA_OK
  EVIDENCE:
