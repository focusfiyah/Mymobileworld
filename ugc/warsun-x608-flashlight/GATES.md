# Gates: WARSUN X608 Flashlight edit (Grace, 2026-11-16)

Scope: Grace's own footage edited at full quality from her originals, OK'd by Ralph, CURRENT in Drive, done message sent.

- [x] G1: Grace's original video(s) are in the Originals folder (1gUy3XgKqmlCpmCApQg6K1KqXMyi5t1Ki) and downloaded at full resolution (not the 464x848 Telegram copy)
  EVIDENCE: 2026-11-17 b0980aeda1584a71b039f8ca163eaf59.mov (Drive 1sXwwXUrzEbe8qrW1hSDmKd-AyYIiAqr9), 89,141,521 B local = Drive, HEVC 1080x1920 60 fps, 102.8 s
- [x] G2: The edit Grace wants is known (her group notes, or her answer on Telegram) and written in README
  EVIDENCE: group msg 559 (2026-11-17, relayed by the Telegram-check session): 7-20 s, she adds music, show every feature; in README
- [x] G3a: V1 is 7-20 s, 1080x1920, silent, length = plan, no black frames
  CHECK: python3 check.py v1 7 20
  EXPECT: CUT_OK v1
  EVIDENCE: automatic-evidence=v1; definition-sha256=c6ac709f67cdf49873ef2150843e7fd4734b3e8c5d42a12e0a77533188ee1ebd; exit=0; EXPECT=matched; output-sha256=895bf881256ecbf2232cc2688cc0f0d41dc356a950c5f7ef78914e85109f1e92; output-bytes=17; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/warsun-x608-flashlight; path=7f4fb4b02918/15 entries
- [x] G3b: V1 has every planned cut and no stray/flash frame, bright
  CHECK: python3 cuts.py v1
  EXPECT: CUTS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=f0b78c2df040047ac6ab556b6e07f1cff9707fb0d5fb1618e6df3501df41f648; exit=0; EXPECT=matched; output-sha256=ff23601cd8b5656738ca56ba62c8a001a0a962857c9810b49f59d04390be8768; output-bytes=45; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/warsun-x608-flashlight; path=7f4fb4b02918/15 entries
- [x] G3: (manual) Cut QC: every frame at 6 fps viewed, REMOVED.md checked, sound check
  EVIDENCE: 2026-11-17 qc/v1b.jpg viewed: fixed lunge blur (COB), dark frame (spotlight), source jump (92.3 s), dead frame (UV), two strip shots back to back; REMOVED.md empty (first cut); earshot skipped with reason: cut is silent, Grace adds her own music
- [x] G4: (manual) Cut on a review page, Ralph told (push + email), Ralph OK'd that exact cut
  EVIDENCE: Ralph 2026-11-17 "Ok" in chat. Review https://claude.ai/artifact/LqJb9m4ejoAZy3Zn2JVyxn, push sent, email 1a1e753aca02aa57 (2026-11-17)
- [x] G5: (manual) "CURRENT - WARSUN X608 V1.mp4" in the folder, Drive size = local size; "✅ WARSUN X608 Flashlight V1 (HD) is done and in Drive: <link>" sent to Ralph
  EVIDENCE: 2026-11-17 Drive 1zZuWQCSQGRNWB714X3SyjOPDJdR2uPa2, 17297070 B = local out/warsun_v1.mp4; Telegram to Ralph msg 566
- [x] G6: (manual) Brain note + session log, brain check prints BRAIN_OK
  EVIDENCE: 2026-11-17 job note, Jobs.md row, session log in Index, active line removed; check.py --terms "WARSUN X608" passes for this job; its only remaining fail is another session's note (Baby Soft-Sole Walking Shoes, still in review)
