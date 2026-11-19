# Gates: 8cm Endless Bubble Popping Squishy Fidget Toy edit (Grace, 2026-11-18)

OWNS: ugc/bubble-squishy-fidget-edit/**

Scope: Grace's own footage edited at full quality from her Drive original, QC'd, OK'd by Ralph, CURRENT in Drive, done message sent.

- [ ] G1: Grace's original video(s) are in the Originals folder and downloaded at full resolution (not the Telegram copy)
- [ ] G2: The edit Grace asked for is known (her group notes read, or asked on Telegram and answered)
- [ ] G3: V1 is 1080x1920, silent, 7-20 s long, within 0.15 s of the planned length, with no black frames
  CHECK: python3 check.py v1 7 20
  EXPECT: CUT_OK v1
- [ ] G3b: V1 has every planned cut, no stray or flash frame, mean brightness at least 110
  CHECK: python3 cuts.py v1
  EXPECT: CUTS_OK
- [ ] G3c: No gaps (rule 2026-11-19): if Grace talks, longest silence <= 0.25 s and first word within 0.1 s, shown on the review page; if silent, no dead visual pause (every shot shows motion or a new feature)
- [ ] G4: Every shot viewed on a frame sheet + frames around each cut; same hands/room per shot, REMOVED.md and last notes checked; earshot sound check run or skipped with reason
- [ ] G5: Cut on the review page; Ralph told (push + email); Grace answered on Telegram without ✅/"done"
- [ ] G6: After Ralph's OK on that exact cut: "CURRENT - Squishy V1.mp4" in the product folder, Drive size = local, nothing loose
- [ ] G7: "✅ Bubble Squishy Fidget V1 (HD) is done and in Drive: <link>" sent to Ralph on Telegram
- [ ] G8: Brain job note + session log written, Active work line removed, brain check prints BRAIN_OK
