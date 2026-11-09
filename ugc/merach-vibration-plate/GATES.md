# Gates: Merach Slim Vibration Plate edit (2026-11-08)

- [x] G1: Draft cut is 12-20 s, 1080x1920, silent, no black frames, length matches the plan
  CHECK: python3 check.py merach 12 20
  EXPECT: CUT_OK merach
  EVIDENCE: automatic-evidence=v1; definition-sha256=b36bb874a2c1cb70bcc96ff69f0267b2add4f15b99adc02534e28d0cc86f0740; exit=0; EXPECT=matched; output-sha256=534dc47fde4bb0dd876720980dbddabdd4f7655c4ac5e32a5494e5cb85a51399; output-bytes=21; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/merach-vibration-plate; path=7f4fb4b02918/15 entries
- [x] G2: (manual) Every frame of the cut viewed on a 4 fps contact sheet: plate, LED display, remote, stepping on, vibration from above and from behind, side angle; no blur at cut points, nothing stretched
- [x] G3: (manual) Telegram copy in Drive Telegram Assets (Originals kept free for Grace's upload); draft in product folder as CURRENT; review page up; Ralph push + email; Grace told on Telegram (pending wording, no ✅/done)
- [x] G4: (manual) HD re-cut from Grace's original, QC'd, CURRENT; draft in Older versions; "✅ ... V1 (HD) is done and in Drive" sent

Evidence G2 (2026-11-08): 6 fps sheet of the whole 15.97 s viewed; blur at 2.25 s and the 53 s camera swing trimmed, remote-leaving frame fixed, near-duplicate overhead shot dropped.
Evidence G3: Drive draft 12,721,936 bytes = local; review page 2bcf37c1; Grace msg 276; email 1a1bd5864b184233; push tool absent (tested via ToolSearch).
Evidence G4 (2026-11-08/09): original VibrationalPlate.mov 62,106,756 bytes (= Drive), HEVC 1080x1920 SDR, same footage, +0.1 s offset measured on 7 points; re-cut CUT_OK 15.97 s, 6 fps sheet + 2x crops viewed; CURRENT - Merach V1 (HD).mp4 21,842,107 bytes (= local); draft renamed v1 draft (2026-11-08) in Older versions; Telegram ✅ msgs 293 (Ralph) + 294 (Grace); email 1a1bdb42fafac776; hourly task deleted.
