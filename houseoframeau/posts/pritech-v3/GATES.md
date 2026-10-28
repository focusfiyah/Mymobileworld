# Gates: PRITECH V3, House of Rameau own cut (2026-10-28)

OWNS: houseoframeau/posts/pritech-v3/**, houseoframeau/README.md, houseoframeau/videos.json

Scope: a free own cut of the approved PRITECH V3 for @houseoframeau in Grace's edit style, uploaded as a draft (AI label on) to the House of Rameau TikTok inbox; Ralph adds the product and posts.

- [x] P1: the cut is 1080x1920, its length matches V3's voiceover + hold (18.8-19.6 s), audio present
  CHECK: python3 qc.py basic
  EXPECT: PASS basic
  EVIDENCE: 2026-10-28 PASS basic 1080,1920 19.4 s aac -16.6 dB

- [x] P2: it is its own cut: at least 11 shots (V3 had 7) and every one of 8 sample times differs from Grace's V3 frame (mean abs diff >= 12)
  CHECK: python3 qc.py different
  EXPECT: PASS different
  EVIDENCE: 2026-10-28 PASS different 13 shots, min diff 32.7 (first run FAILED at 4.8/5.2: S1 + S3 framed like Grace's; fixed with a tighter S1 and a mirrored S3)

- [x] P3: grade stays bright and not yellow: mean luma >= Grace's V3 and blue-minus-red not lower than hers by more than 3
  CHECK: python3 qc.py grade
  EXPECT: PASS grade
  EVIDENCE: 2026-10-28 PASS grade luma 139.2 vs 134.1, b-r 21.9 vs 24.1 (first run failed at equal luma; brightness 0.025 -> 0.045)

- [x] P4: looked at every shot at full size (contact sheet + 2x crops of hands/face edges): no full face, no glowing bristles, no text, punch-ins not soft
  EVIDENCE: 2026-10-28 contact sheet of all 13 shots + 2x crops (silver-end punch-in, pump run shot, cheek shot at 17.25 s): cheek/ear only, no eyes or mouth, no glow, no text, punch-ins soft only at 2x

- [x] P5: draft upload returned a publish_id on account tiktok_buck-flunk with is_aigc true, and the status was read back
  EVIDENCE: 2026-10-28 TIKTOK_UPLOAD_VIDEO on tiktok_buck-flunk, publish false, is_aigc true -> publish_id v_inbox_file~v2.7701523686330992671, upload_completed true; status read back PROCESSING_UPLOAD, 50,633,782 bytes = the file
