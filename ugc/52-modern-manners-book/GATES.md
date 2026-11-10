# Gates: 52 Modern Manners for Kids (book) edit (2026-11-10)

- [x] G1: Grace's original (not the Telegram copy) is downloaded and its size equals the Drive size
  EVIDENCE: 2026-11-10 5d9fb9c90b7e42cbb8cf75c8b68a108c.mov local 53,643,057 bytes = Drive size; HEVC 1080x1920 30 fps SDR, 61.5 s
- [x] G2: Cut is 7-20 s (Grace msg 351), 1080x1920, no black frames, length matches the plan
  CHECK: python3 check.py manners 7 20
  EXPECT: CUT_OK manners
  EVIDENCE: automatic-evidence=v1; definition-sha256=dfb343ce817e941f3dfab01788dd35c0e673df29fa6ec65f333a760277ce5b8e; exit=0; EXPECT=matched; output-sha256=e863fb2e5e3bc5cb6e0b11af375c104ccb7a2ec6af275553865516e39c482978; output-bytes=22; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/52-modern-manners-book; path=7f4fb4b02918/15 entries
- [x] G3: (manual) Every frame of the whole source and of the cut viewed on contact sheets; cut shows cover, inside pages/spreads, several angles, strong first second; nothing stretched (every clip >= 1.0x); 2x edges clean; bright neutral grade; no on-screen text
  EVIDENCE: source 2 fps sheets 0-61.5 s + cut points at 10 fps + cut at 6 fps viewed; 2 blur cut points fixed and rechecked; first second 2x clean; back cover dropped (upside down); no grade/text, silent (hum, no voice)
- [x] G4: (manual) Review page up with the cut stacked full width; Ralph push + email sent; Grace told (pending wording, no ✅/done)
  EVIDENCE: review page https://claude.ai/artifact/AQA2g1zFtRjcaDyKqCjUm6 v1; push requested; email 1a1c37e3cd43ec37; Grace Telegram msg 354 (pending wording)
- [x] G5: (manual) After Ralph's OK on that exact cut: Drive "CURRENT - Manners Book V1 (HD).mp4" size = local, any older file in Older versions, "✅ 52 Modern Manners for Kids V1 (HD) is done and in Drive: <link>" to Ralph and Grace
  EVIDENCE: Ralph OK 2026-11-10 ("Ok"); Drive file 1eJ0zfM1seuKNXlMEcjOmWBKPtspKttNG 20,454,614 bytes = local; first version, so nothing to move to Older versions; Telegram ✅ msgs 374 (Ralph) + 375 (group)
- [x] G6: (manual) Brain note Brain/Jobs + session log pushed; Active work line removed; media packed (MEDIA_OK)
  EVIDENCE: media set 1 in Drive 1efN10aZmAlqnBRHmRdDdHauHVYt6niB9 (sha256 matched), MEDIA_OK; Brain note + session log + Active work removal pushed, brain check below
