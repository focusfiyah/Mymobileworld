# Power bank flashlight (Grace), phase 2: stills -> clips -> VO -> cut (Ralph approved 2026-10-21)

Ralph 2026-10-21: "OK, dusk is fine, same hand rings. Use this product reference sheet." Quote: Kie $2.00, Kling ~128 cr, ~600 EL chars.
Phase 1 ledger (research, script, sheet, plan): all 6 met, see git history.

- [x] G1: Ralph's product sheet is the product reference in every product still/clip
  CHECK: python3 -c "import json;j=json.load(open('shots.json'));print('REF_OK' if j['refs']['product']==['refs/front_crop_ralph.png','refs/product_sheet.png'] and 'gunmetal' in j['product_block'] else 'NO')"
  EXPECT: REF_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=319d7ff85ad1dbc679ad6074af4930a19d4b310c18474b5fb033a7794b797f24; exit=0; EXPECT=matched; output-sha256=288d1b6d7a49f2be5f5fc2c4a47b9ec8bcafd54c79cb90d4de71a3752079ca13; output-bytes=7; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/powerbank-flashlight; path=7f4fb4b02918/15 entries
- [x] G2: 9 stills exist, S4 test still approved by me at full size before the rest (manual QC: grip, product parts, rings, edges 2x)
  EVIDENCE: manual: S4 r3 QC at 2x then 8 stills; contact sheet review/stills_sheet.jpg; S6 + S9 free fixes (2026-10-21)
- [x] G3: 9 clips exist (all Seedance, no Kling per Ralph 2026-10-21), every clip QC'd (product unchanged, hand edges 2x, no text)
  CHECK: python3 -c "import pathlib;n=[p for p in ['S1','S2','S3','S4','S5','S6','S7','S8','S9'] if not pathlib.Path(f'clips/{p}.mp4').exists()];print('CLIPS_OK' if not n else 'MISSING '+' '.join(n))"
  EXPECT: CLIPS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=0d00e7f3eba450853479018e1df87f584d57346393ab60910bc1abed62026ce6; exit=0; EXPECT=matched; output-sha256=e4543291756688621fb6b61d03da089b559a00890565e641b0d68b66a9359fd1; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/powerbank-flashlight; path=7f4fb4b02918/15 entries
- [x] G4: Grace voiceover, loudnorm -16 LUFS, STT shows no stutter or dropped word
  EVIDENCE: manual: Grace C deleted from ElevenLabs (404); used 'Grace cloned' Rh3oAQMqRVf78UIVpBoQ (2026-10-20 pick). vo/stt.json transcript matches the script word for word (vo.py asserts it); cut -16.9 LUFS
- [x] G5: cut is 9:16, no text drawn, AI finish applied, compare vs @zin5bamu done, gate --stage cut OK
  CHECK: cd ../.. && python3 grace/gate.py ugc/powerbank-flashlight --stage cut
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=9b322c4de27cb04b1fc4dda5c54e18414398a903a3fb66c0c6120c6167b6bb6b; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/powerbank-flashlight; path=7f4fb4b02918/15 entries
- [x] G6: running total reported vs the quote at each paid step; cut on the review page + push + email (manual)
  EVIDENCE: manual: totals in every reply + review page v7 with cut_r1.mp4; email + push sent 2026-10-21
