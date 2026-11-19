# Gates: Noa Floating Double Diamond Studs edit (Grace, 2026-11-18)

OWNS: ugc/noa-floating-diamond-studs-edit/**

Scope: Grace's own footage edited at full quality from her Drive original, QC'd, OK'd by Ralph, CURRENT in Drive, done message sent.

- [ ] G1: Grace's original video(s) are in the Originals folder and downloaded at full resolution (not the Telegram copy), local size = Drive size
- [ ] G2: The edit Grace asked for is known (msg 559 brief, or her notes for this product)
- [ ] G3: V1 is 1080x1920, silent, 7-20 s long, within 0.15 s of the planned length, with no black frames
  CHECK: python3 check.py v1 7 20
  EXPECT: CUT_OK v1
- [ ] G3b: V1 has every planned cut, no stray or flash frame, mean brightness at least 110
  CHECK: python3 cuts.py v1
  EXPECT: CUTS_OK
- [ ] G3c: If Grace talks on camera (rule "No gaps in Grace's own talking edits", 2026-11-19): pauses >0.3 s trimmed to ~0.12-0.15 s, first word within ~0.1 s, no dead air at the end, voice at normal speed, her clip order kept, longest silence <= 0.25 s shown on the review page; N/A with reason if she does not talk
- [ ] G4: Every shot viewed on a frame sheet + frames around each cut; same hands/room per shot; every feature shown (pear-cut double stones, floating setting, gold tone, lightweight/on the ear); REMOVED.md and last notes checked; earshot run or skipped with reason
- [ ] G5: Cut on the review page; Ralph told (push + email); Grace answered on Telegram without ✅/"done"
- [ ] G6: After Ralph's OK on that exact cut: "CURRENT - Noa Studs V1.mp4" in the product folder, Drive size = local, nothing loose
- [ ] G7: "✅ Noa Floating Diamond Studs V1 (HD) is done and in Drive: <link>" sent to Ralph and in the group (reply to 586)
- [ ] G8: Brain job note + session log written, Active work line removed, brain check prints BRAIN_OK; media.py check MEDIA_OK
