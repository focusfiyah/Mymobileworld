# Gates: Power Bank Flashlight V2 (Grace), Ralph's script word for word, 2026-10-22

OWNS: ugc/powerbank-flashlight-v2/**

Scope: one ~25 s hands-only AI video of the grey TINEKO flashlight on Ralph's script, shot order from his storyboard, real size, no text, in Drive with the script doc.

- [x] G1: script.txt is Ralph's script word for word ("flickering" = his fix)
  CHECK: python3 qc/gates.py script
  EXPECT: SCRIPT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=b9e982eac6f3c10b63b06c8bd2fa97699a916906c04eaa6d893f47e1ea615bfd; exit=0; EXPECT=matched; output-sha256=ca1feac20ca6f49301d378c911ed2e868c331982fbc7b6f0b1073327521875b7; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/powerbank-flashlight-v2; path=7f4fb4b02918/15 entries

- [x] G2: real size + modes from Grace's box recorded and the clip view saved for S1/S8
  CHECK: python3 qc/gates.py size
  EXPECT: SIZE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=390c39f0d43f3517aeecac2cc1c98cd623886fca1055dd1198ee7099c8aa32b3; exit=0; EXPECT=matched; output-sha256=8b8bca900b63d8fc0538301590db1b3ba619cf2031570c91183fbf3deb4332c0; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/powerbank-flashlight-v2; path=7f4fb4b02918/15 entries

- [x] G3: storyboard page has all 9 shots, clip view on S1/S8, real size, no McDonald's on screen, flicker from the front lens
  CHECK: python3 qc/gates.py storyboard
  EXPECT: STORYBOARD_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=dff4b99fbb520d301b8fe37b1c765b4527c61ceff60bf6ff5e46494b99989a70; exit=0; EXPECT=matched; output-sha256=064234a99d97206ac171b489f1fdd1db981a13b6d3e26980a1177b35df4b2c1e; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/powerbank-flashlight-v2; path=7f4fb4b02918/15 entries

- [x] G4: Ralph approved the storyboard (his words recorded here)
  EVIDENCE: manual: Ralph 2026-10-22 after storyboard v3 + gates: "Let's go with Gemini. Send me what you need" (stills via his Gemini app, $0)

- [x] G5: script gate passes (all PLAYBOOK §4 proofs + verbatim override recorded) before any paid call
  CHECK: python3 qc/gates.py gate
  EXPECT: SCRIPTGATE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=40d51ba4aa4ebcd23e16e050d9fffdb3b88ef015649b0b2f0705039983a033cf; exit=0; EXPECT=matched; output-sha256=4f7f8f0c523a60031853f1b96bc0441faf0f699c16dda20a65fa030577bcbe19; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/powerbank-flashlight-v2; path=7f4fb4b02918/15 entries

- [x] G6: 9 stills exist, each QC'd at 2x (size vs hand/phone/strap, clip shows where the top is in frame, grip, rings, no text, no brand)
  CHECK: python3 qc/gates.py stills
  EXPECT: STILLS_OK
  EVIDENCE: manual + CHECK STILLS_OK 2026-10-23: S1-S4 Ralph's Gemini stills, S5 (redo), S6 (side strip inpainted), S8, S9 Kie; QC 2x notes on the review page; S7 replaced by a Seedance clip on Ralph's word

- [x] G7: 9 clips exist (Omni on Kie for product shots), each QC'd: product shape/size unchanged, flicker from the front lens on S5, beam lands where the lens points on S4, edges 2x, no second product
  CHECK: python3 qc/gates.py clips
  EXPECT: CLIPS_OK
  EVIDENCE: manual + CHECK CLIPS_OK 2026-10-23: Omni S3 S4 S6; Seedance S1 S2 S5 S7 S8 S9 (Omni 500s, Ralph: 'Retry Omni first, then Seedance if it fails'); 4-frame strips + 2x crops; S5 flicker from the front lens via tools/flicker.py, panel off; S4 beam from the lens down the trail. Open for Ralph: cap print garbled at 2x on S1/S4, faint green ghost S6

- [x] G8: Grace cloned voice, word for word by STT, echo gate <= 150 ms
  EVIDENCE: manual 2026-10-23: vo/voiceover_paced.mp3, Grace cloned Rh3oAQMqRVf78UIVpBoQ, scribe_v2 transcript matches the script word for word (vo.py asserts), echo.py rt60_est_ms=150

- [x] G9: cut 9:16, no text, REMOVED.md checked, AI finish, gate --stage cut OK, review page + push + email
  EVIDENCE: manual 2026-10-23: out/flashlight_v2_r1.mp4 1080x1920 22.6 s, no text, REMOVED.md checked (research/compare_report.md), AI finish in cut.py, gate --stage cut GATE OK, review page v9, email sent; phone push tool not available this session

- [x] G10: approved cut + script doc in Drive "Grace Tiktok assets/Power Bank Flashlight (Grace)" as CURRENT, size matches; job branch merged to main
  EVIDENCE: manual 2026-10-23: Ralph "Approved"; Drive folder 1r_tveoqKXNKBRcBei6G-wSHfIGOFoIW9: CURRENT - Flashlight V2.mp4 (10THQFZmreJ9IHCLKv2vStjSaBsITZIyJ, 58,861,345 bytes = local) + CURRENT - Flashlight V2 script (1Okl2wel8AG0l3Zm238o3FGH1NEPaCEBGwcB4Q-YhjTw); V1 files stay (a different video); job branch merged to main
