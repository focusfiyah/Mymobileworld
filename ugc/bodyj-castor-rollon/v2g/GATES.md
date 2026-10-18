# GATES: BodyJ castor roll-on v2g (Grace's own script over the r1 footage), 2026-10-18

- [x] G1: Grace's script word for word in the VO (Ralph 01:12Z: "Use this script and the same video")
  EVIDENCE: vo/stt.json transcript matches script.md (STT writes "Imma" as "I'm gonna"); 39.03 s tight.
- [x] G2: Script gate OK, readability <= 6
  CHECK: python3 ../../../grace/gate.py .
  EXPECT: GATE OK
  EVIDENCE: GATE OK, grade 5.5.
- [ ] G3: Every line shows matching footage (Ralph 01:12Z: "Match the script with the video, if we need new shots let me know"); new shots only on his OK with cost
  EVIDENCE: pending (card: 4 new shots $1.18)
- [x] G4: Claims the listing can't back flagged to Ralph, not edited ("hair growing longer")
  EVIDENCE: flagged in the thread reply 2026-10-18 ~01:25Z, kept verbatim
- [ ] G5: Cut 1080x1920, 20-45 s, cuts between words, no freeze/black, loudness OK (qc/check_cut.py ALL OK)
  EVIDENCE: pending
- [ ] G6: QC: new clips 2x edge zoom, first second, real label pasted back, nails/skin match r1; AI finish; REMOVED.md; cut gate (compare) OK
  EVIDENCE: pending
- [ ] G7: Drive: new file with an updated name in the same BodyJ folder; the r1 "CURRENT -" file left where it is (Ralph 01:12Z)
  EVIDENCE: pending
