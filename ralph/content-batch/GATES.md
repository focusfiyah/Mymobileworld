# Gates: weekly content batch pipeline, week 1 (Ralph 2026-11-15: 2 twin/week, all 3 formats as one batch, mix kit + AI tips)

- [x] G1: Week 1 scripts pass the public-content checks (no 6-word run shared with Grace's material, no hook close to hers, grade 6 or lower, no price)
  CHECK: python3 checks.py scripts week1
  EXPECT: SCRIPTS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=8bdf0b7b85c633f2cdad43ff612d8ee35d22ed8b98170ccd31c047b99ff195b5; exit=0; EXPECT=matched; output-sha256=6609da8e91fd55b71ebe5777253a5f15cab4c349e7bf2585568b8fb54970bc92; output-bytes=31; shell=/bin/sh; cwd=/home/user/Mymobileworld/ralph/content-batch; path=7f4fb4b02918/15 entries
- [x] G2: Two twin Flow kits exist, 4 shots each, each with its own room image, angle, lowercase keywords and no finger counting
  CHECK: python3 checks.py kits week1
  EXPECT: KITS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=b491f8b0fe475a7d0d1be134a24c94ee0b8aa4822be43ee7d1e5c836394a1404; exit=0; EXPECT=matched; output-sha256=204a60710d3e986691fcef4a69eee2c99ba2d49bdc961c52aa6070dba956e36a; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ralph/content-batch; path=7f4fb4b02918/15 entries
- [x] G3: Two faceless videos are 1080x1920, 10-45 s, with audio, and every scripted word is heard
  CHECK: python3 checks.py faceless week1
  EXPECT: FACELESS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=72d05eaacc02353cc363f281b7f8e90d5ad2b853b269e2f1d88b0d62dbbeb0e2; exit=0; EXPECT=matched; output-sha256=0facb06c24e24f1bd7705a00bfd0879919d18b9ed4f0c01a8bbb274ead103228; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ralph/content-batch; path=7f4fb4b02918/15 entries
- [x] G4: Two carousels exist as 1080x1350 PNG sets with the scripted slide counts
  CHECK: python3 checks.py carousels week1
  EXPECT: CAROUSELS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=97adce0a1852388dc2b814cd95fb65f9b501aae8b6b0d581bcd9a26048b852a1; exit=0; EXPECT=matched; output-sha256=4339b67100f06f9d6c4c4c3aa3068a3e00e6ad27128b353271bf97345cbfb36d; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/ralph/content-batch; path=7f4fb4b02918/15 entries
- [x] G5: The week 1 review page shows the kits, both faceless videos (stacked) and both carousels, published
  EVIDENCE: published https://claude.ai/artifact/XzVZhtyLPHpXUafNt2VBdj v1 (2026-11-15): 8 kit cards, F1+F2 stacked, C1 6 + C2 7 slides.
- [x] G6: Brain note updated
  CHECK: python3 /home/user/Mymobileworld/tools/brain/check.py --terms "content batch,faceless,carousel"
  EXPECT: BRAIN_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=9d9bedc6ef75e87654044ab701d6f82f0dcd4cde3faf83c3c583b37cb78aeb76; exit=0; EXPECT=matched; output-sha256=85c6576a10b4511b3de2274f92e0a23bcdb0ced52cb120ab2a444055c3266211; output-bytes=51; shell=/bin/sh; cwd=/home/user/Mymobileworld/ralph/content-batch; path=7f4fb4b02918/15 entries
