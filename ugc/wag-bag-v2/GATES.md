# Gates: Wag Bag r3 fix (Ralph 2026-10-06: V3 jump at ~21-22s, V4 "make" clipped at ~29s)

OWNS: ugc/wag-bag-v2/**

Scope: no clip in any of the 5 videos opens on frames of a neighbouring take, audio stays locked to picture, every spoken line intact, Drive updated.

- [x] G1: no segment starts within 0.35s before a take join in Grace's files, and no flash (two cuts 2 frames to 0.25s apart) in any final
  CHECK: python3 -I qc/verify_fix.py flash
  EXPECT: flash OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=4fd70847c6ffbb0ccaeda41bcc5fab22b794f592337b960a633db4e81e194a62; exit=0; EXPECT=matched; output-sha256=0de36b0fd4240b9ab6b02b35e217b58caf6b560c0da921828e57026b6d6144e7; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries

- [ ] G2: every segment's audio matches its source and sits within 15 ms of its picture, measured on the file's own audio timeline, all 5 videos
  CHECK: python3 -I qc/verify_fix.py sync
  EXPECT: sync OK
  CWD: .
  EVIDENCE: pending

- [ ] G3: free STT of each final contains every line of its takes (incl. V4 "just to make sure you have enough")
  CHECK: python3 -I qc/verify_fix.py words
  EXPECT: words OK
  CWD: .
  EVIDENCE: pending

- [x] G4: loudness -15 to -13 LUFS and true peak under -0.5 dBFS in all 5
  CHECK: python3 -I qc/verify_fix.py levels
  EXPECT: levels OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=aa95ba1f88753e14ec6e9bacb6f0eb81436b3749c2178835ba4db9ff3fed1ddf; exit=0; EXPECT=matched; output-sha256=e0debe9f1de872f3cb1b885f11c9bb46b9c956b5d6dce63467e94deb35037f3e; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries

- [ ] G5: I looked at V3 20.6-22.6s and V4 28.5-30s frame by frame (and every hook's emoji) after the fix
  EVIDENCE: pending

- [ ] G6: the 5 fixed videos replace the CURRENT files in Drive (sizes match), previous set renamed v2 in Older versions
  EVIDENCE: pending

- [ ] G7: job README, CLAUDE.md, playbook lesson committed and pushed
  EVIDENCE: pending
