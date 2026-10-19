# GATES: BodyJ castor roll-on v2g (Grace's own script over the r1 footage), 2026-10-18

- [x] G1: Grace's script word for word in the VO (Ralph 01:12Z: "Use this script and the same video")
  EVIDENCE: vo/stt.json transcript matches script.md (STT writes "Imma" as "I'm gonna"); 39.03 s tight.
- [x] G2: Script gate OK, readability <= 6
  CHECK: python3 ../../../grace/gate.py .
  EXPECT: GATE OK
  EVIDENCE: GATE OK, grade 5.5.
- [x] G3: Every line shows matching footage (Ralph 01:12Z: "Match the script with the video, if we need new shots let me know"); new shots only on his OK with cost
  EVIDENCE: cut_v2g.py maps every line; 4 new shots N1-N4 on Ralph's card OKs (stills $0.36, edits $0.18, clips $0.82 = $1.36) (card: 4 new shots $1.18)
- [x] G4: Claims the listing can't back flagged to Ralph, not edited ("hair growing longer")
  EVIDENCE: flagged in the thread reply 2026-10-18 ~01:25Z, kept verbatim
- [x] G5: Cut 1080x1920, 20-45 s, cuts between words, no freeze/black, loudness OK (qc/check_cut.py ALL OK)
  EVIDENCE: qc/check_cut.py ALL OK on out/bodyj_castor_v2g_r1_final.mp4 (39.30 s, cuts between words, -13.6 LUFS)
- [x] G6: QC: new clips 2x edge zoom, first second, real label pasted back, nails/skin match r1; AI finish; REMOVED.md; cut gate (compare) OK
  EVIDENCE: 2x zooms qc/v2g_zoom.jpg clean, nails short, real label on S1 S5 S7 S8 S9 N4 (S4 S6 N3 AI label), N3 cropped to drop the lips, AI finish, REMOVED.md, GATE OK --stage cut
- [x] G7: Drive: new file with an updated name in the same BodyJ folder; the r1 "CURRENT -" file left where it is (Ralph 01:12Z)
  EVIDENCE: Drive 'CURRENT - BodyJ castor roll-on v2 (Grace's script, 2026-10-18).mp4' (1mvIp_zGLc8FUFtBwrD9p8AeWTz6cgJfs) in folder 19jUSElPjnXIC0f3DFoiaxA1Kl9333_nk, size 101068256 matches; r1 left untouched
