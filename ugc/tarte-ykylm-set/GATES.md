# Gates: tarte "you know you love me" 8-piece set edit (2026-11-10)

- [x] G1: Cut is 7-20 s (Grace msg 351), 1080x1920, no black frames, length matches the plan
  CHECK: python3 check.py tarte 7 20
  EXPECT: CUT_OK tarte
  EVIDENCE: automatic-evidence=v1; definition-sha256=0b5533262dc4c95a1c9ec327901cf02a79a61ba9d5fa1dd739f79c011d2be880; exit=0; EXPECT=matched; output-sha256=ef0948df6c329bf9c6c9d3204b233d590d411028de9d6c79ef0a3ff163e55750; output-bytes=20; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/tarte-ykylm-set; path=7f4fb4b02918/15 entries
- [x] G2: (manual) Every frame of the source viewed on a contact sheet; cut sheet at 5-6 fps viewed: strong first second, all 8 pieces shown (2 palettes, 2 wristlets, 2 mascaras, 2 lips), different angles, nothing stretched, no blur at cut points, edges at 2x clean, bright neutral grade, no on-screen text, checked against REMOVED.md
  EVIDENCE: original 595793bb...mov 126,445,447 B (= Drive), HEVC 1080x1920 SDR 59.94, 137.7 s, audio = handling noise only. 1 fps sheets of all 137.7 s + 6 fps sheets of 12 windows + 6 fps sheet of the cut viewed; box shot trimmed to 0.45 s before her zoom; full-size frames 0.1 s and 11.3 s + 2x crop sharp, no fringe; no text/overlay/grade; REMOVED.md has nothing to check yet.
- [x] G3: (manual) Review page up with the cut; Ralph push + email sent; Grace told on Telegram with pending wording (no ✅/done)
  EVIDENCE: review page https://claude.ai/artifact/QH94fzHHQHR9JNS82qwtPm (v1); push requested; email 1a1c37f02d1f5b97; Grace Telegram msg 357 (reply to 351, pending wording, no ✅/done).
- [x] G4: (manual) After Ralph's OK on that exact cut: Drive "CURRENT - tarte YKYLM V1 (HD).mp4" in the product folder, size = local, any older copy in Older versions; "✅ tarte YKYLM set V1 (HD) is done and in Drive: <link>" sent to Grace and Ralph
  EVIDENCE: CURRENT - tarte YKYLM V1 (HD).mp4 Drive 1KwmkEdOs0NJ8nV543mjUbZ6ICMowG3vz, 23,238,276 B = local; folder had no older copy; ✅ Telegram msgs 368 (Grace group) + 369 (Ralph).
- [x] G5: (manual) Brain note + session log pushed, Active work line removed, BRAIN_OK; job branch merged to main; media packed (MEDIA_OK)
  EVIDENCE: Brain job note + session log + Index + Jobs.md pushed, my Active work line removed; check.py --terms 'tarte YKYLM,collector's set' finds both terms and lists no tarte problem (the 3 remaining items belong to the two Modern Manners sessions still running); MEDIA_OK; tarte-ykylm-set-edit merged to main.
