# Gates: Baby Soft-Sole Walking Shoes edit (Grace, 2026-11-16)

OWNS: ugc/baby-soft-sole-shoes-edit/**

Scope: Grace's own footage edited at full quality from her Drive original, QC'd, OK'd by Ralph, CURRENT in Drive, done message sent.

- [x] G1: Grace's original video(s) are in the Originals folder and downloaded at full resolution (not the Telegram copy)
  EVIDENCE: 2026-11-17 a39f5312...mov Drive 19PUmQ5_DOLYWnxNPXNSEVSC6CNso08Bz, 46,927,808 B downloaded = Drive size; HEVC 1080x1920 60 fps 52 s
- [x] G2: The edit Grace asked for is known (her group notes read, or asked on Telegram and answered)
  EVIDENCE: group msg 559 (relayed by the Telegram check session): "I will have music in the background ensure all aspects of product features show. Should 7-20 seconds videos"
- [x] G3: V1 is 1080x1920, silent, 7-20 s long, within 0.15 s of the planned length, with no black frames
  CHECK: python3 check.py v1 7 20
  EXPECT: CUT_OK v1
  EVIDENCE: automatic-evidence=v1; definition-sha256=c6ac709f67cdf49873ef2150843e7fd4734b3e8c5d42a12e0a77533188ee1ebd; exit=0; EXPECT=matched; output-sha256=32b44607e1053303073112a1e86dd6aefc40ecc5ccc0c4b5e2591fdb411725e5; output-bytes=17; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/baby-soft-sole-shoes-edit; path=7f4fb4b02918/15 entries
- [x] G3b: V1 has every planned cut, no stray or flash frame, mean brightness at least 110
  CHECK: python3 cuts.py v1
  EXPECT: CUTS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=f0b78c2df040047ac6ab556b6e07f1cff9707fb0d5fb1618e6df3501df41f648; exit=0; EXPECT=matched; output-sha256=8f9d9fb3d62580256efef15784bb5f9c6d8229aa9768e0990f4bb870d12c082b; output-bytes=44; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/baby-soft-sole-shoes-edit; path=7f4fb4b02918/15 entries
- [x] G4: Every shot viewed on a frame sheet + frames around each cut; same hands/room per shot, REMOVED.md and last notes checked; earshot sound check run or skipped with reason
  EVIDENCE: 2026-11-17 qc/v1_6fps.jpg + qc/v1_cuts.jpg viewed; fixed shot 2 start (focus settle, +0.2 s) and shot 6 end (mid-turn, -0.3 s); one room, one pair of hands, all features shown (fold, front, tread, stretch, side, back tab). Blue circle = mirror's own touch button (room, kept). earshot skipped: cut is silent by Grace's brief (she adds music). REMOVED.md written (nothing removed by Ralph/Grace yet)
- [x] G5: Cut on the review page; Ralph told (push + email); Grace answered on Telegram without ✅/"done"
  EVIDENCE: 2026-11-17 review https://claude.ai/artifact/F1eZaAUogTHkqk6U8Qg5aE (preview copy crf 23, 9.4 MB; HD file out/shoes_v1.mp4 18.0 MB for Drive); push requested; email id 1a1e753941320e60; Telegram group msg 562 (reply to 559)
- [x] G6: After Ralph's OK on that exact cut: "CURRENT - Baby Shoes V1.mp4" in the product folder, Drive size = local, nothing loose
  EVIDENCE: 2026-11-17 Ralph tapped "Approve, upload (Recommended)"; Drive 1g3w6EmvKglpDCPubeHRgWs9fREBxihXW size 18043712 = local out/shoes_v1.mp4; parent 1lp3nAIKOfFgr_21HKoUJ-daDnrtrCF9O; folder holds only Originals + this file
- [x] G7: "✅ Baby Soft-Sole Walking Shoes V1 (HD) is done and in Drive: <link>" sent to Ralph on Telegram
  EVIDENCE: 2026-11-17 Ralph private chat msg 567, Grace group msg 568
- [x] G8: Brain job note + session log written, Active work line removed, brain check prints BRAIN_OK
  EVIDENCE: 2026-11-17 BRAIN_OK (458 notes, terms found); media.py check MEDIA_OK (tar 1q8v3bKP0IMz5fdrkpXUD-dXVl-avD0pQ, sha256 match)
