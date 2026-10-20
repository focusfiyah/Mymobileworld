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

- [ ] G3: Grace's 4 scripts (from Ralph) saved word for word in scripts.json and compared in ONE table (words, length at 3.3 w/s, hook vs winner, structure, grade, unbacked claims, banned phrases, winning-formula parts kept) + a recommendation, sent to Ralph before any video work
  EVIDENCE: pending

- [ ] G4: Each script is 38-52 words, grade 6 or lower, no banned phrase; any script used word for word that fails has a per-video override in ../checklist.json with Ralph's quote
  CHECK: python3 check.py scripts
  EXPECT: SCRIPTS_OK
  CWD: ugc/bodyj-castor-rollon/remix15
  EVIDENCE: pending

- [ ] G5: Script gate passes for the job (proofs newer than the scripts)
  CHECK: python3 ../../../grace/gate.py ..
  EXPECT: GATE OK
  CWD: ugc/bodyj-castor-rollon/remix15
  EVIDENCE: pending

- [ ] G6: Voice source settled with Ralph (default: Grace records each script and sends the audio) and Ralph's remix override of "every video different" recorded in ../checklist.json with his words
  EVIDENCE: pending

- [ ] G7: Four cuts, 1080x1920, 13.5-16.5 s each, built from existing clips at 1.0x, edit lists all different (order/crop/grade vary)
  CHECK: python3 check.py cuts
  EXPECT: CUTS_OK
  CWD: ugc/bodyj-castor-rollon/remix15
  EVIDENCE: pending

- [ ] G8: QC on every cut: qc/verify_fix.py (flash, sync, words, levels), 2x edge zooms + first second, REMOVED.md list checked, AI finish applied last, cut-stage gate (compare vs the winner)
  EVIDENCE: pending

- [ ] G9: One Artifact review page with all 4 cuts playable; Drive BodyJ folder has CURRENT - names, older in Older versions; email + push sent to Ralph with the link
  EVIDENCE: pending

- [ ] G10: Nothing paid without Ralph's OK and exact cost; running total reported ($0 so far)
  EVIDENCE: pending
