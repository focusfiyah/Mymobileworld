# GATES: HofR versions of 4 approved Grace cuts (Ralph 2026-11-15: "make a HofR versions of cleanwaste and others if they do not exist")
Order: Cleanwaste first (posts Nov 16), then BodyJ v2g, PRITECH V1, Vans V13. $0 only. QC script: hor_qc.py (basic/hook/different/grade).

- [x] G1: Cleanwaste HofR passes hor_qc (QC_OK)
  CHECK: cd ../../../ugc/cleanwaste-toilet-kit && python3 ../../houseoframeau/posts/_tools/hor_qc.py out/cleanwaste_hor.mp4 "$GRACE_DIR/cleanwaste.mp4" out/hor_hookbox.json
  EXPECT: QC_OK
- [x] G2: BodyJ HofR passes hor_qc (QC_OK)
  CHECK: cd ../../../ugc/bodyj-castor-rollon && python3 ../../houseoframeau/posts/_tools/hor_qc.py out/bodyj_v2g_hor.mp4 "$GRACE_DIR/bodyj.mp4" out/hor_hookbox.json
  EXPECT: QC_OK
- [x] G3: PRITECH HofR passes hor_qc (QC_OK)
  CHECK: cd ../../../ugc/pritech-cleansing-brush && python3 ../../houseoframeau/posts/_tools/hor_qc.py out/pritech_hor.mp4 "$GRACE_DIR/pritech.mp4" out/hor_hookbox.json
  EXPECT: QC_OK
- [x] G4: Vans HofR passes hor_qc (QC_OK)
  CHECK: cd ../../../ugc/vans-vo5 && python3 ../../houseoframeau/posts/_tools/hor_qc.py out/vans_hor.mp4 "$GRACE_DIR/vans.mp4" out/hor_hookbox.json
  EXPECT: QC_OK
- [x] G5: (manual) each cut's frame sheet + dense strip looked at: product never cut off, no shimmer, hook not over a label, people/room same as Grace's approved shots, REMOVED.md ticked
- [x] G6: (manual) earshot `es critique` ran on each final cut, each note applied or skipped with a reason
- [ ] G7: (manual) review page published, videos stacked full width; push + email sent; Cleanwaste sent first, alone
- [x] G8: (manual) after Ralph's OK per cut only: Drive "HofR - <Product> BF.mp4" in the product folder, Drive size = local size, hub session messaged

## Status 2026-11-15
- G1-G4 met: hor_qc.py printed QC_OK for all four (re-run before reporting).
- G5 met: frame sheets + 2.5 fps strips looked at; fixes made (Cleanwaste S3/S4/S6 crops + S4/S6 in-points, PRITECH S7 crop, Vans A crop). REMOVED.md rows ticked: no captions/cards, no eyes/mouth (PRITECH), no wrist band (Vans), bright cool grade.
- G6 met: earshot critique on all four; every note is the voice-only shape (syllable hit density, little sub/low, mono): skipped, Grace's approved VOs, launch-film music refs do not apply. Earshot's own loudness reads -11.9..-12.7 "web" LUFS; ffmpeg ebur128 integrated -14.9..-15.7.
- G7 partly met: review page https://claude.ai/code/artifact/7974df3b-8e90-475c-9f98-3b1803fba6b0 (Cleanwaste sent first, alone), 2 emails sent. Phone push NOT sent: PushNotification is not in this session's tool list (ToolSearch twice).
- G8 met: Ralph tapped Approve on all four (2026-11-15); Drive sizes = local (75071770, 100861674, 65314586, 63066481); hub session_01Y1Pt3pfP7HcKsjq5xn9T1H messaged (delivered).
- Vans: V13 clips were never stored in Drive; cut from Grace's V13 mp4 (in-points inside each shot unchanged; swaps + crops + grade carry the difference; AI finish not re-applied, the source has it).
