# Gates: LGXNDS Creatine edit from Grace's original (2026-11-18)

- [ ] G1: Grace's original is in the Originals folder and downloaded at full quality (not the 464x848 Telegram copy)
  CHECK: ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 orig/* | awk '$1>=1280{ok=1} END{if(ok)print "ORIG_HD"}'
  EXPECT: ORIG_HD
- [ ] G2: Cut is 7-20 s, 1080x1920, silent, no black frames, length matches the plan
  CHECK: python3 check.py v1 7 20
  EXPECT: CUT_OK v1
- [ ] G3: Every planned cut lands, no stray or flash frame, stays bright
  CHECK: python3 cuts.py v1
  EXPECT: CUTS_OK
- [ ] G4: (manual) 6 fps sheet + frames around every cut viewed; every feature her footage shows appears (front label, 5G badge, scoop, powder/mix); same person and room throughout; no text; checked against REMOVED.md
- [ ] G5: (manual) earshot sound check skipped with reason (silent cut, Grace adds music) or run on a music version
- [ ] G6: (manual) Cut on the review page; Ralph told by push + email
- [ ] G7: (manual) After Ralph's OK on that exact cut: CURRENT in Drive (size matches local), older files in Older versions, ONE "✅ ... done and in Drive" line to Ralph and in the group (reply to msg 586)
- [ ] G8: (manual) Brain job note + session log, Active work line removed, brain check prints BRAIN_OK; media packed (MEDIA_OK)
- [ ] G9: (manual) If she talks on camera: longest silence in the cut <= 0.25 s (silencedetect), first word within 0.1 s, no dead air at the end, number shown on the review page; else marked not applicable with the reason
