# Gates: BodyJ castor roll-on, 4 x 15 s remixes of the selling video (Grace), 2026-10-20

OWNS: ugc/bodyj-castor-rollon/remix15/**

Scope: four 15 s remixes of Grace's selling castor video (3 sales) on Grace's 4 scripts, compared first, built free from the existing clips, QC'd, in Drive, Ralph notified.

- [x] G1: The posted winner is pulled for reference (video, timed captions) and is the 31-33 s castor video
  CHECK: python3 check.py ref
  EXPECT: REF_OK
  CWD: ugc/bodyj-castor-rollon/remix15
  EVIDENCE: automatic-evidence=v1; definition-sha256=31b6fc68de31895ada6e03b7746e00e16ff948a2d16d8e6c79796f4d8153d463; exit=0; EXPECT=matched; output-sha256=288d1b6d7a49f2be5f5fc2c4a47b9ec8bcafd54c79cb90d4de71a3752079ca13; output-bytes=7; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/bodyj-castor-rollon/remix15; path=7f4fb4b02918/15 entries

- [x] G2: Every one of the 12 castor clips is in INVENTORY.md with what moves, setting, label state and its place in the winner
  CHECK: python3 check.py inventory
  EXPECT: INVENTORY_OK 12
  CWD: ugc/bodyj-castor-rollon/remix15
  EVIDENCE: automatic-evidence=v1; definition-sha256=e472afbb68877c5f67528d7eaf6fccad67f1f3626af5b28a324baf7d1ab510a3; exit=0; EXPECT=matched; output-sha256=0459e934d290b45db3a1f2f9370129749e6711caea6f91399422c9ca14f1cc23; output-bytes=16; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/bodyj-castor-rollon/remix15; path=7f4fb4b02918/15 entries

- [x] G3: Grace's 4 scripts (from Ralph) saved word for word in scripts.json and compared in ONE table (words, length at 3.3 w/s, hook vs winner, structure, grade, unbacked claims, banned phrases, winning-formula parts kept) + a recommendation, sent to Ralph before any video work
  EVIDENCE: COMPARE.md table + recommendation sent to Ralph in chat and email 2026-10-20; scripts_received.json verbatim

- [x] G4: Each script Grace records fits its limit (15 s; script 4 up to 20 s, Ralph 2026-10-20) at 3.3 words/s, grade 6 or lower, no banned phrase; any script used word for word that fails has a per-video override in ../checklist.json with Ralph's quote
  CHECK: python3 check.py scripts
  EXPECT: SCRIPTS_OK
  CWD: ugc/bodyj-castor-rollon/remix15
  EVIDENCE: automatic-evidence=v1; definition-sha256=b2beb6b7bbbf005ded66a6bfea1b47dd0fdd65c1e22293e1ac681c4956234f25; exit=0; EXPECT=matched; output-sha256=3161c7f998608e04a24b4edc7024f576595484a0b0ba803950403a7f2858a804; output-bytes=11; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/bodyj-castor-rollon/remix15; path=7f4fb4b02918/15 entries

- [x] G5: Script gate passes for the job (proofs newer than the scripts)
  CHECK: python3 ../../../grace/gate.py .
  EXPECT: GATE OK
  CWD: ugc/bodyj-castor-rollon/remix15
  EVIDENCE: automatic-evidence=v1; definition-sha256=7908fc24a2c335f530262a05f49fe8b9a7001f554a71613959d13370a768f86d; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/bodyj-castor-rollon/remix15; path=7f4fb4b02918/15 entries

- [x] G6: Voice source settled with Ralph (default: Grace records each script and sends the audio) and Ralph's remix override of "every video different" recorded in ../checklist.json with his words
  EVIDENCE: Ralph 2026-10-20: "Use Grace new voice as the VO ... If Grace does not like the VO she will rerecord the VOs." = ElevenLabs "Grace" Rh3oAQMqRVf78UIVpBoQ (Ralph: 'called only Grace'); remix override with his words in checklist.json remix_override

- [x] G7: Four cuts, 1080x1920, 13.5 s up to each video's limit (15 s; video 3 = 20 s) +1 s, built from existing clips at 1.0x, edit lists all different (order/crop/grade vary)
  CHECK: python3 check.py cuts
  EXPECT: CUTS_OK
  CWD: ugc/bodyj-castor-rollon/remix15
  EVIDENCE: automatic-evidence=v1; definition-sha256=fc1761351122d150be72031f70a23cd2a51570cb80e6110467bab0727eb76214; exit=0; EXPECT=matched; output-sha256=2d4f718d2719eaa1a3c77703b75c5837a814a3f128ef9fb997f420c4c8562304; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/bodyj-castor-rollon/remix15; path=7f4fb4b02918/15 entries

- [x] G8: QC on every cut: qc/verify_fix.py (flash, sync, words, levels), 2x edge zooms + first second, REMOVED.md list checked, AI finish applied last, cut-stage gate (compare vs the winner)
  EVIDENCE: qc.py: QC OK v1-v4 on the finals (flash, sync on exact frames, words, -16 LUFS, TP < -1); 2x zooms qc/zoom2x.jpg clean; first seconds in qc/all_sheets.jpg; qc/removed_check.md; ai_finish.sh last (cut.py --final); gate --stage cut OK with compare proofs

- [x] G9: One Artifact review page with all 4 cuts playable; Drive BodyJ folder has CURRENT - names, older in Older versions; email + push sent to Ralph with the link
  EVIDENCE: Review page https://claude.ai/code/artifact/6841627a-baca-40c2-bdfd-55d8dc8f53eb (4 players embedded); Drive folder https://drive.google.com/drive/folders/1zDf5VAgV5Hoy5V3v61xl8snCiUN3GG9- in the BodyJ folder, CURRENT - V1..V4 sizes match local bytes + CURRENT scripts doc; email to Ralph 2026-10-21; push: PushNotification not in this session (tested)

- [x] G10: Nothing paid without Ralph's OK and exact cost; running total reported ($0 so far)
  EVIDENCE: Only paid step: ElevenLabs 1,143 characters (Ralph's 'Yes, start' card, ~$0.19 Starter); Kie file host free; video $0

## Round 5 (2026-10-23): Ralph's notes "v1 it shows a head missing" + "her hands do not stay true to Grace's skin tone"

- [ ] G11: Free check done before any spend: every round-4 shot compared to Grace's real hand sheet (3 frames per shot) and every headless shot found; findings + redo list written
  CHECK: python3 -c "import pathlib as p;f=p.Path('qc/r5/FINDINGS.md').read_text();ok=all(s in f for s in ['V1g','V1h','Redo list'])and all(p.Path(f'qc/r5/r4_v{n}_shots.jpg').exists() for n in '1234');print('FIND_OK' if ok else 'FIND_MISSING')"
  EXPECT: FIND_OK
  CWD: ugc/bodyj-castor-rollon/remix15
  EVIDENCE: run by hand 2026-10-23 (CHECK lines need Ralph's approval to run through the checker): FIND_OK
- [ ] G12: Ralph answered in ONE message: bracelet or no-bracelet sheet, the shots to redo, the exact total cost; his OK recorded before any paid call
  EVIDENCE: asked 2026-10-23 (BOOK.md TOTAL $9.96, review page v10, email 1a1670dc958d1311); waiting on his answer
- [ ] G13: Every new still and clip prompt written with prompt-master, Grace's chosen hand sheet passed as a reference on every hand still and clip; no Kling
  EVIDENCE: pending
- [ ] G14: One test clip passes QC (tone vs sheet at 2x, nails/rings, whole wrists, product unchanged, no headless body) before the batch
  EVIDENCE: pending
- [ ] G15: Four new cuts pass qc.py, check.py cuts, gate --stage cut, REMOVED.md, AI finish; no headless shot; every hand matches the sheet
  EVIDENCE: pending
- [ ] G16: Same review page republished, Drive CURRENT replaced (round 4 to Older versions as v3), Ralph emailed + pushed
  EVIDENCE: pending
