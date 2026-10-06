# Gates: Wag Bag r4 photo overlays (Ralph 2026-10-06: "use images instead" of emoji; water, battery, generator = real photo stickers, poop stays 3D)

OWNS: ugc/wag-bag-v2/**

Scope: the hook overlays on all 5 videos use the photo stickers, every quality check from r3 still passes, Drive replaced, committed and pushed.

- [x] G1: the three photo stickers exist at 512px with transparency and every overlay in videos.json is shown at <=1.2x of its 512px source
  CHECK: python3 -I qc/verify_overlay.py stickers
  EXPECT: stickers OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=01b8b4bce84340a9d34867ad5ccac874c10b4a7fa27b1d5fce4c83aa4e3cd4cf; exit=0; EXPECT=matched; output-sha256=b86973128cbf83b292f9217b63572513859d844a662f1b4afd6012174acf6643; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries

- [x] G2: no overlay covers Grace's face: every pop box stays inside the zones cleared in r3 (top emojis x<=300 or x>=780, y 440-960; poop and question mark in their r3 spots)
  CHECK: python3 -I qc/verify_overlay.py zones
  EXPECT: zones OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=7900f0003479493876be06d9a132683aa3cef1b0b79b29381a196013dd88bca6; exit=0; EXPECT=matched; output-sha256=75ddd2d51b1996bfe196cd2213540026b1904e31355b9cf9bc81a2db39d6be2c; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries

- [x] G3: no flash or stray cut in any final
  CHECK: python3 -I qc/verify_fix.py flash
  EXPECT: flash OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=4fd70847c6ffbb0ccaeda41bcc5fab22b794f592337b960a633db4e81e194a62; exit=0; EXPECT=matched; output-sha256=0de36b0fd4240b9ab6b02b35e217b58caf6b560c0da921828e57026b6d6144e7; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries

- [x] G4: audio locked to picture in all 5
  CHECK: python3 -I qc/verify_fix.py sync
  EXPECT: sync OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=6e64503a72a52e0888a4262d39f5d3b2ca85085a907c939f1afe185207624c00; exit=0; EXPECT=matched; output-sha256=75835a4df88c8adb06521393ee00d4253f2f2ad82da6cf7d46dc7bf7d660636c; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries

- [x] G5: free STT of every final contains every line
  CHECK: python3 -I qc/verify_fix.py words
  EXPECT: words OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=9a06aec59779ec26699d7f92e319814f0626f94ff4d7d087bd769951595cc432; exit=0; EXPECT=matched; output-sha256=aa00f45223f3371e932a137b5f5002ace6eeddd930ca0ccd07d419cbce0016d3; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries

- [x] G6: loudness -15 to -13 LUFS, true peak under -0.5 dBFS
  CHECK: python3 -I qc/verify_fix.py levels
  EXPECT: levels OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=aa95ba1f88753e14ec6e9bacb6f0eb81436b3749c2178835ba4db9ff3fed1ddf; exit=0; EXPECT=matched; output-sha256=e0debe9f1de872f3cb1b885f11c9bb46b9c956b5d6dce63467e94deb35037f3e; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries

- [x] G7: I looked at every hook at full size (2x zoom on sticker edges and Grace's head/hands) and the first second of each video
  EVIDENCE: qc/r4_hooks.png (all 5 hooks, 4 frames each: water, battery, generator, poop + question mark, none on a face), qc/r4_zoom_v1.png (2x on sticker edges: sharp, no logo, no halo), qc/r4_final_v2_crop.png; generator reflection trimmed after the first look

- [x] G8: the 5 new videos replace the CURRENT files in Drive (sizes match), the r3 set is renamed and moved to Older versions
  EVIDENCE: Composio 2026-10-06 23:37Z: CURRENT V1-V5 ids 1zn5KPdS.., 13DT-CUYN.., 1h4KGblT.., 1fKQ7HQk.., 1GL9zUGH..; Drive sizes 51989750/49277642/51061760/53621484/57757402 = local out/ = qc/hosted_r4.json; r3 files renamed 'v3 3D emoji' and moved to Older versions (1liz954H..)

- [x] G9: job README, CLAUDE.md, playbook lesson committed and pushed
  CHECK: test -z "$(git status --porcelain)" && git fetch -q origin ccr-dae93a3a-f9m9sa && git diff --quiet HEAD origin/ccr-dae93a3a-f9m9sa && echo pushed-clean
  EXPECT: pushed-clean
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=3f7c822c444b9262a40a9b5afb814a8e7f729d14722684faa94186a958d3a9ef; exit=0; EXPECT=matched; output-sha256=83fbb1afbfd2f27ded0367f10e41f60cbf06ee268604acd75d5093cf7047e84a; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wag-bag-v2; path=7f4fb4b02918/15 entries
