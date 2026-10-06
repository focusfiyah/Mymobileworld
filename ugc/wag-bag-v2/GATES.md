# Gates: Wag Bag r3 fix (Ralph 2026-10-06: V3 jump at ~21-22s, V4 "make" clipped at ~29s)

OWNS: ugc/wag-bag-v2/**

Scope: no clip in any of the 5 videos opens on frames of a neighbouring take, audio stays locked to picture, every spoken line intact, Drive updated.

- [x] G1: no segment starts within 0.35s before a take join in Grace's files, and no flash (two cuts 2 frames to 0.25s apart) in any final
  CHECK: python3 -I qc/verify_fix.py flash
  EXPECT: flash OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=4fd70847c6ffbb0ccaeda41bcc5fab22b794f592337b960a633db4e81e194a62; exit=0; EXPECT=matched; output-sha256=0de36b0fd4240b9ab6b02b35e217b58caf6b560c0da921828e57026b6d6144e7; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries

- [x] G2: every segment's audio matches its source and sits within one frame (33 ms) of its picture, measured on the file's own audio timeline, all 5 videos
  CHECK: python3 -I qc/verify_fix.py sync
  EXPECT: sync OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=6e64503a72a52e0888a4262d39f5d3b2ca85085a907c939f1afe185207624c00; exit=0; EXPECT=matched; output-sha256=75835a4df88c8adb06521393ee00d4253f2f2ad82da6cf7d46dc7bf7d660636c; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries

- [x] G3: free STT of each final contains every line of its takes (incl. V4 "just to make sure you have enough")
  CHECK: python3 -I qc/verify_fix.py words
  EXPECT: words OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=9a06aec59779ec26699d7f92e319814f0626f94ff4d7d087bd769951595cc432; exit=0; EXPECT=matched; output-sha256=aa00f45223f3371e932a137b5f5002ace6eeddd930ca0ccd07d419cbce0016d3; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries

- [x] G4: loudness -15 to -13 LUFS and true peak under -0.5 dBFS in all 5
  CHECK: python3 -I qc/verify_fix.py levels
  EXPECT: levels OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=aa95ba1f88753e14ec6e9bacb6f0eb81436b3749c2178835ba4db9ff3fed1ddf; exit=0; EXPECT=matched; output-sha256=e0debe9f1de872f3cb1b885f11c9bb46b9c956b5d6dce63467e94deb35037f3e; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries

- [x] G5: I looked at V3 20.6-22.6s and V4 28.5-30s frame by frame (and every hook's emoji) after the fix
  EVIDENCE: qc/r3_v3_21s.png (one clean cut hand -> Grace at ~21.7s, no other-take frames), qc/r3_v4_29s.png (one continuous shot), qc/r3_hooks.png (all 5 hooks: water, battery, lightning, poop + question mark)

- [x] G6: the 5 fixed videos replace the CURRENT files in Drive (sizes match), previous set renamed v2 in Older versions
  EVIDENCE: Composio 2026-10-06 20:39Z: CURRENT V1-V5 ids 130Y6zxf.., 11m7D03o.., 1N6yUptR.., 181GYySG.., 1sSuNb8d..; Drive sizes 51861104/49165005/50883055/53528766/57685102 = qc/hosted_r3.json; old CURRENT renamed 'v2 3D emoji, jump+audio issues' and moved to Older versions

- [x] G7: job README, CLAUDE.md, playbook lesson committed and pushed
  CHECK: test -z "$(git status --porcelain)" && git fetch -q origin ccr-a0dae179-slh3lv && git diff --quiet HEAD origin/ccr-a0dae179-slh3lv && echo pushed-clean
  EXPECT: pushed-clean
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=73011179d59a02d369e8229f6dc2ca6f424a1163ed7c82a227c0ceb900296129; exit=0; EXPECT=matched; output-sha256=83fbb1afbfd2f27ded0367f10e41f60cbf06ee268604acd75d5093cf7047e84a; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries
