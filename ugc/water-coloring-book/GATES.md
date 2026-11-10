# Gates: 3/6 Reusable Water Coloring Book edit (Grace, 2026-11-10)

- [x] G1: (manual) Session renamed, Originals folder checked, hourly Originals check scheduled into this session
  EVIDENCE: 2026-11-10 title set; Originals empty (Drive query parentId, positive control on the parent folder returned Originals); trig_012r1wwbGnwDDnKsEqGyyRar cron 23 * * * *
- [x] G2: (manual) Brain job note + Active work line pushed
  EVIDENCE: obsidian-vault 030e30e on main
- [x] G3: Cut from her footage is 7-20 s (Grace msg 351), 1080x1920, no black or frozen stretch, matches plan
  CHECK: python3 check.py hd 7 20
  EXPECT: CUT_OK hd
  EVIDENCE: automatic-evidence=v1; definition-sha256=583737184fb5bf51a896d6f2910a9a76fce0686363f8757af47d7a78795ee967; exit=0; EXPECT=matched; output-sha256=002f92ce6091650d8239482bd08244bf8e925377934ac3b6b2ac8a9389dfcdee; output-bytes=17; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/water-coloring-book; path=7f4fb4b02918/15 entries
- [x] G4: (manual) Every frame QC'd (5 fps sheet + 2x edges), no stretch (all clips >=1.0x), no text, bright neutral grade, every product feature shown
  EVIDENCE: 2026-11-10 qc/hd_5fps.jpg viewed (r1 hook had her hand over the page and a wrong timestamp; fixed in r2), qc/hook_2x.jpg sharp; scale-to-cover, no setpts speed change; mean luma 142; features: cover, blank page, pens, water fill, stickers, colour appearing, finished page, book stack; drying back to white not filmed
- [x] G5: (manual) Cut on the review page; Ralph told by push + email; his OK recorded
  EVIDENCE: 2026-11-10 https://claude.ai/artifact/7smDqik869aCyNWcaudJNC ; push requested; email 1a1c380bb9a75c6a; Ralph tapped "OK, upload it (Recommended)"
- [x] G6: (manual) After his OK: CURRENT in Drive (size = local), any draft in Older versions, "✅ ... V1 (HD) is done and in Drive" to Grace + Ralph
  EVIDENCE: 2026-11-10 Drive 1wCY2DhFEX3tlPNzEZyudSIwKBYF2Gppk 22354421 B = local; no draft existed; Telegram 362 (group, reply to 351) + 363 (Ralph)
- [x] G7: (manual) Brain note updated, Active work line removed, brain check BRAIN_OK
  EVIDENCE: 2026-11-10 job note DONE, session log in Index, Jobs.md row, Active work line removed, pushed; check.py --terms "Water Coloring Book" reports only sibling sessions' in-progress notes (JIYU NAD, 52 Modern Manners teens/kids), no problem on this job's notes
