# GATES: FORCHICS Pheromone Body Oil V1 (edit of Grace's original)

- [x] G1: cut is 7-20 s long (Grace's brief)
  CHECK: python3 -c "import subprocess;d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','out/FORCHICS_V1.mp4']));print('DUR_OK' if 7<=d<=20 else 'DUR_BAD',d)"
  EXPECT: DUR_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=b080838a39e63bb819db766090d2da1b819f0e2790f8466472c529999af83736; exit=0; EXPECT=matched; output-sha256=be630e471e687e53171f76a498078fc16729a8887e7974f63ff9491c56c286fd; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/forchics-pheromone-oil; path=7f4fb4b02918/15 entries
- [x] G2: full quality 1080x1920 H.264 from the HD original
  CHECK: ffprobe -v error -select_streams v -show_entries stream=codec_name,width,height -of csv=p=0 out/FORCHICS_V1.mp4
  EXPECT: h264,1080,1920
  EVIDENCE: automatic-evidence=v1; definition-sha256=fee88470d5c4a5738ecd8b3eb2773483b29037a2406bfbc10321b6ab9754df23; exit=0; EXPECT=matched; output-sha256=c4babe7b9c0c9d0bf7e6e6bc818cd318fa50f53059fad8a1f06413f28abaa708; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/forchics-pheromone-oil; path=7f4fb4b02918/15 entries
- [x] G3: audio is silent (Grace adds her own music)
  CHECK: bash -c "ffmpeg -v info -i out/FORCHICS_V1.mp4 -af volumedetect -f null - 2>&1 | grep max_volume"
  EXPECT: max_volume: -91
  EVIDENCE: automatic-evidence=v1; definition-sha256=65b67bcee906295c16c673fe52660c4988b044d12051a7939cb6e9ce32acadbb; exit=0; EXPECT=matched; output-sha256=5456198ade1628bc177b2cee537455f3a2c5858219a814b93c51dcd9c251ae95; output-bytes=62; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/forchics-pheromone-oil; path=7f4fb4b02918/15 entries
- [x] G4: no frozen frames (no freeze >= 0.5 s)
  CHECK: python3 qc_misc.py out/FORCHICS_V1.mp4
  EXPECT: FREEZES_NONE
  EVIDENCE: automatic-evidence=v1; definition-sha256=8a91a8c4cda50556ec9a7d91c09016be1768567736a940d4aa7eb5544139bd4b; exit=0; EXPECT=matched; output-sha256=4af9b36a74981fe5cd8961e12d039e0a97c3e55ae341bb07e210196a34faba37; output-bytes=23; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/forchics-pheromone-oil; path=7f4fb4b02918/15 entries
- [x] G5: no on-screen text drawn by the cut script
  CHECK: python3 qc_misc.py out/FORCHICS_V1.mp4
  EXPECT: NOTEXT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=3a299efbb72fb02847c682dead92a49b5c7f8b942b6cfbae638f0334564a139a; exit=0; EXPECT=matched; output-sha256=4af9b36a74981fe5cd8961e12d039e0a97c3e55ae341bb07e210196a34faba37; output-bytes=23; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/forchics-pheromone-oil; path=7f4fb4b02918/15 entries
- [x] G6: blue UI bubble gone from the cut (no strong blue pixels at the right edge of 10 frames)
  CHECK: python3 qc_bubble.py out/FORCHICS_V1.mp4
  EXPECT: BUBBLE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=2b329e093faea84bf8976435415523c7d32b0d23e46f1c038cbce88ec7309bd1; exit=0; EXPECT=matched; output-sha256=0cd24234c2760da6954d6ff6db310816b55deddbd6cb64e1c1378676cdd04bfb; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/forchics-pheromone-oil; path=7f4fb4b02918/15 entries
- [x] G7: every product feature in her footage is shown (box, unboxing, label, pump, application, rub-in, glow, hero) [manual: frame sheet proof/cut_sheet.png]
- [x] G8: REMOVED.md items checked against the cut [manual]
- [ ] G9: review page published, push + email sent [manual]
- [ ] G10: Drive upload only after Ralph's OK on this exact cut; Telegram done line after [manual, pending Ralph]

EVIDENCE G7 2026-11-17: proof/cut_sheet.png shows glow+bottle 0-1.5, box 1.5-3.5, unboxing 3.5-6.5, label 6.5-8.5, pump 8.5-10, application 10-12, rub-in 12-14, glow 14-15.5, hero 15.5-17.5.
EVIDENCE G8 2026-11-17: bubble gone (G6 BUBBLE_OK), muted (G3), no text (G5).
NOTE G9 2026-11-17: review page https://claude.ai/code/artifact/1fcd78bd-dde6-49ec-a687-b3721443845f published, email sent (Gmail id 1a1e7535c4233e68); PushNotification not found via ToolSearch this session, so no phone push.
