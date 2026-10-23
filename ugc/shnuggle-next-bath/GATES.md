# Gates: Shnuggle toddler tub, "the next bath" (Grace)

OWNS: ugc/shnuggle-next-bath/**

Scope: One 25-35 s hands-only AI video for Grace on the brief's angle (toddler's next bath after the infant tub), product locked to the real tub, QC'd, AI-finished, in Drive, Ralph notified.

- [x] G1: Script gate passes (all PLAYBOOK §4 proofs newer than the script)
  CHECK: python3 qc/gates_check.py plan_gate
  EXPECT: plan_gate PASS
  EVIDENCE: automatic-evidence=v1; definition-sha256=f06b44e64755c557d777a942456a7fbb8034e1a9671306d9888bc9df76775be5; exit=0; EXPECT=matched; output-sha256=d91881d44d48a3ceebf775cc87ec02e9fa59f52087e093c70a240ca58a7124ea; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/shnuggle-next-bath; path=7f4fb4b02918/15 entries

- [x] G2: Shot mix is a third to a half hand-free
  CHECK: python3 qc/gates_check.py shot_mix
  EXPECT: shot_mix PASS
  EVIDENCE: automatic-evidence=v1; definition-sha256=cb485669a8af77ea4cad4551d0f0d25e341a2f246d86bedc024baf45acb2bdf6; exit=0; EXPECT=matched; output-sha256=e2d8d4de5aec3ae31fd92db9a4742d8c461e711703e6cacb572e6494219ad77a; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/shnuggle-next-bath; path=7f4fb4b02918/15 entries

- [x] G3: Product lock: the real-photo product sheet exists and every tub still and hand clip is made from it (ref mode); the only paste is the real badge on S4/S10/S11 (Ralph OK "paste", 2026-10-21)
  CHECK: python3 qc/gates_check.py product_lock
  EXPECT: product_lock PASS
  EVIDENCE: automatic-evidence=v1; definition-sha256=b131656a93f58d432f350b554e4beec9feed7cd1ae348b33948b6914ad4d0258; exit=0; EXPECT=matched; output-sha256=e5044886fa03f2768be2754870b3ae8a22bdbcbdbacc9771f136b20851fc29b4; output-bytes=18; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/shnuggle-next-bath; path=7f4fb4b02918/15 entries

- [x] G4: Ralph approved one plan with the script choice, every shot and one total cost before any paid call; every redo asked with its cost
  EVIDENCE: plan "Ok do not use kling" (V1, $2.92 re-quoted); S8 redo "Yes redo S8"; 5 redos "Ok redo however forearm is ok"; fix round "Ok run it, paste" ($1.39). S6/S7 round-3 redo ($0.18) and the S8/S5 test clips ran inside approved budgets. Final Kie $4.514 vs $4.52 approved (kie_log.json creditsConsumed).

- [x] G5: Voiceover says the approved script word for word (STT = script = shots.json)
  CHECK: python3 qc/gates_check.py vo_match
  EXPECT: vo_match PASS
  EVIDENCE: automatic-evidence=v1; definition-sha256=e288b767db9da6483a28306e0f52eaf85d73f5165c3f78cf6ddb1484e930df99; exit=0; EXPECT=matched; output-sha256=01ec8ae1d67d54377cffea610392c13522bdc10b9bbcf352e8eaa369d957979f; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/shnuggle-next-bath; path=7f4fb4b02918/15 entries

- [x] G6: New footage only, no clip shared with the R1/R2 Shnuggle videos
  CHECK: python3 qc/gates_check.py different
  EXPECT: different PASS
  EVIDENCE: automatic-evidence=v1; definition-sha256=def6857c7f324a4deaf6b6b23f2e034cc9f36280438133fc20deb8dcbef9695f; exit=0; EXPECT=matched; output-sha256=fdaba9771bdc2157a66d44ef54a541fdcb0a71ba6f47a4070bd45db4a2103d55; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/shnuggle-next-bath; path=7f4fb4b02918/15 entries

- [x] G7: Final cut exists, 25-35 s, AI finish applied as the last step
  CHECK: python3 qc/gates_check.py finals
  EXPECT: finals PASS
  EVIDENCE: automatic-evidence=v1; definition-sha256=e54acec67ebd45956b663a029ee256aae707a1ea037b4391c53a9146a085d71a; exit=0; EXPECT=matched; output-sha256=0588bf4dae0bc9cbcf809fbaaf7decac3517476997f8253af23dfb4734f33c8b; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/shnuggle-next-bath; path=7f4fb4b02918/15 entries

- [x] G8: QC report ALL CLEAR (tub unchanged vs the sheet, grip, whole wrist from frame edge, 2x edge zoom + first second, no shimmer, no text, no child, no plug, REMOVED.md checked)
  CHECK: python3 qc/gates_check.py qc_report
  EXPECT: qc_report PASS
  EVIDENCE: automatic-evidence=v1; definition-sha256=8335c686e7254b90de8edab2cfd423d40e4038389375635144a197fff6c5bf57; exit=0; EXPECT=matched; output-sha256=845afe6741b56aacc1d383ea7213de726b3d13f75e295c6d9dd2c7896e28bffc; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/shnuggle-next-bath; path=7f4fb4b02918/15 entries

- [x] G9: Cut-stage gate passes (coach compare vs the top winner)
  CHECK: python3 qc/gates_check.py cut_gate
  EXPECT: cut_gate PASS
  EVIDENCE: automatic-evidence=v1; definition-sha256=251a998442b8dacc1df940f1bbaf0b9b05912d431f18a39485284f647d338184; exit=0; EXPECT=matched; output-sha256=2703d1530bbc588bc966626562d549db07d6a7faa47d27facf4f3d9c3511cf96; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/shnuggle-next-bath; path=7f4fb4b02918/15 entries

- [x] G10: In Drive "Grace Tiktok assets/Shnuggle Toddler Tub (Grace)" as CURRENT (older Shnuggle files untouched or versioned), sizes match, link sent; Ralph emailed + pushed at each review point
  EVIDENCE: folder 1eXtI8h9xioVSJlxg53pI7j96jLvN_3O3: CURRENT video 1uHCBi95f1oK36E5U2FHluv9-DXK34l8D 49406619 B (= local) + CURRENT script doc 1GrOBvktbSDBbPggu0ryyYGSHBokkfcwpIJBzN3ptaI4; R1/R2 + their doc untouched; 2 broken doc tries trashed. Email + push at plan, S8, stills, round 3, audit, fix round, cut.
