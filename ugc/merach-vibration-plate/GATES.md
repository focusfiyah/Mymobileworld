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

## Round 2: VO scripts for Grace (request 2026-11-09, Telegram msg 309)
- [x] G5: script gate passes on the 3 VO scripts
  CHECK: python3 grace/gate.py ugc/merach-vibration-plate
  EXPECT: GATE OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=5eac1e956fbe8d0f9100a411d61074d020e34c60beb2d3ac671ee8c108fb868f; exit=0; EXPECT=matched; output-sha256=f1593586a3b76b7e1e5b3b735586bb8c0f0a8bceb1fb5cf70412976ed465c768; output-bytes=162; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries
- [x] G6: (manual) scripts sent to Grace (Telegram msg 311, pending wording), Drive "CURRENT - Merach Scripts V1" + "CURRENT - Merach Research verdict", Ralph push + email 1a1bfa76696ad52a
- [x] G7: V2 cut (Grace's own script) is 12-30 s, 1080x1920, silent, no black frames, matches the plan
  CHECK: python3 check.py merachv2 12 30
  EXPECT: CUT_OK merachv2
  EVIDENCE: automatic-evidence=v1; definition-sha256=7f4d972e78652faf7ee689915932353331cd56771fbbd9c508e85930a4831a98; exit=0; EXPECT=matched; output-sha256=74e6d914dac2a69b186231d2891a4e0951ab1043a4deb2d5400db04966adb0b2; output-bytes=23; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/merach-vibration-plate; path=7f4fb4b02918/15 entries
- [x] G8: (manual) V2 sheet viewed at 5-6 fps: blurry display swing and out-of-order feet-on shot removed, crop jump fixed, edges at 2x clean; review page v3; Ralph push + email 1a1c10294d1d2a76; Grace comparison sent (msg 318)
- [ ] G9: (manual) Ralph OKs V2 -> Drive CURRENT, old to Older versions, Grace told; strap clip from Grace swapped into line 6; re-timed to her VO
