# Gates: PURCELL 247 Colostrum Ampoule Mist edit (2026-11-10)

- [x] G1: Cut is 7-20 s (Grace msg 351), 1080x1920, silent, no black frames, length matches the segment plan
  CHECK: python3 check.py mist 7 20
  EXPECT: CUT_OK mist
  EVIDENCE: automatic-evidence=v1; definition-sha256=f650e8bf288ea4f801895f76125da134ee28bc2d904225f1e23f2eae73dedf30; exit=0; EXPECT=matched; output-sha256=49c0d1a74e01ea86fe174fe21e0151fc6fe121600c4fe5c23f62f05846a6479c; output-bytes=19; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/purcell-colostrum-mist; path=7f4fb4b02918/15 entries
- [x] G2: (manual) Every frame viewed at 10 fps: strong first second; different angles; shows the mist spraying, glow/hydration on skin, pore care, setting-spray use, the bottle; no hand sweep across the product, no blurry cut points, bright neutral grade, no on-screen text
  EVIDENCE: 10 fps sheets of all 14.8 s viewed 2026-11-10; two soft starts trimmed (40.6->41.1 s); no text, no hand sweep, room grade untouched
- [x] G3: (manual) Cut on the review page; Ralph push + email; his OK recorded BEFORE any Drive upload
  EVIDENCE: review https://claude.ai/artifact/HX22vSQ4Luzrus8TwbRzZu; push + email 1a1c37eab1c5c62e; Ralph replied "Ok" before upload
- [x] G4: (manual) After his OK: cut in Drive product folder as CURRENT (size matches local), older ones in Older versions; "✅ PURCELL 247 Colostrum Mist V1 (HD) is done and in Drive" sent to Grace and Ralph
  EVIDENCE: Drive 1paSkZ7W1_P8PzcneVHt0XtH1hwaeLFAK 11,680,922 B = local; first version so no Older versions; Telegram 370 (group) + 371 (Ralph)
- [x] G5: Cut is from her HD original (no Telegram draft needed) and 7-20 s, 1080x1920, no black frames
  CHECK: python3 check.py mist 7 20
  EXPECT: CUT_OK mist
  EVIDENCE: automatic-evidence=v1; definition-sha256=f650e8bf288ea4f801895f76125da134ee28bc2d904225f1e23f2eae73dedf30; exit=0; EXPECT=matched; output-sha256=49c0d1a74e01ea86fe174fe21e0151fc6fe121600c4fe5c23f62f05846a6479c; output-bytes=19; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/purcell-colostrum-mist; path=7f4fb4b02918/15 entries
- [x] G6: (manual) Brain note + session log pushed; Active work line removed; BRAIN_OK
  EVIDENCE: Brain note + session log pushed, Active work line removed, BRAIN_OK
