# Gates: OQQ High-Waisted Loose Pants edit (Grace, 2026-11-18)

OWNS: ugc/oqq-loose-pants-edit/**

Scope: Grace's own footage edited at full quality from her Drive original, QC'd, OK'd by Ralph, CURRENT in Drive, done message sent.

- [ ] G1: Grace's original video(s) are in the Originals folder and downloaded at full resolution (not the Telegram copy)
- [x] G2: The edit Grace asked for is known (her group notes read, or asked on Telegram and answered)
  EVIDENCE: 2026-11-18 msg 586 (batch, she adds originals for an edit) + her standing brief msg 559: 7-20 s, silent (she adds music), show every product feature; relayed by the Telegram check session
- [ ] G3: V1 is 1080x1920, silent, 7-20 s long, within 0.15 s of the planned length, with no black frames
  CHECK: python3 check.py v1 7 20
  EXPECT: CUT_OK v1
- [ ] G3b: V1 has every planned cut, no stray or flash frame, mean brightness at least 110
  CHECK: python3 cuts.py v1
  EXPECT: CUTS_OK
- [ ] G3c: If Grace talks on camera: every pause between her lines closed (silence > 0.3 s cut to ~0.12-0.15 s, first word within ~0.1 s, no dead air at the end, normal speed, her clip order kept), longest silence <= 0.25 s measured and shown on the review page; if she does not talk, recorded as not applicable (rule "No gaps in Grace's own talking edits", 2026-11-19)
- [ ] G4: Every shot viewed on a frame sheet + frames around each cut; same hands/room per shot, REMOVED.md and last notes checked; earshot sound check run or skipped with reason
- [ ] G5: Cut on the review page; Ralph told (push + email); Grace answered on Telegram without ✅/"done"
- [ ] G6: After Ralph's OK on that exact cut: "CURRENT - OQQ pants Grace edit V1.mp4" in the product folder, Drive size = local, nothing loose
- [ ] G7: "✅ OQQ High-Waisted Loose Pants V1 (HD) is done and in Drive: <link>" sent to Ralph on Telegram
- [ ] G8: Brain job note + session log written, Active work line removed, brain check prints BRAIN_OK
