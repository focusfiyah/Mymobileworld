# Gates: JIYU NAD+ Anti-Aging Facial Daily Moisturizer edit (2026-11-10)

- [x] G1: Grace's original video is in Drive Originals (1XKh2S2O68y_UCqKIfWdcNyZRdmVd1Rva), downloaded, local size = Drive size
  EVIDENCE: 0eea04eac053423c9f1959714a7e72bc.mov (Drive id 1Rg7JoL6CkyRgDg_zXkUda9uh_VeD9QBE) 79,641,722 bytes local = Drive; HEVC 1080x1920 60 fps SDR, 90.5 s.
- [x] G2: Cut is 7-20 s (Grace msg 351: 7-20 s), 1080x1920, length matches the plan, no black frames
  CHECK: python3 check.py jiyu 7 20
  EXPECT: CUT_OK jiyu
  EVIDENCE: automatic-evidence=v1; definition-sha256=1ca528dd0fa495df23351a9602947cfc2d6121a7254749febeddf76842340a90; exit=0; EXPECT=matched; output-sha256=3087a5bd37e4c2b72bb0d4a27fe3cf9f745f200f157f39963686e3e1985936b7; output-bytes=19; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/jiyu-nad-moisturizer; path=7f4fb4b02918/15 entries
- [x] G3: (manual) Every frame viewed on a 5-6 fps contact sheet; strong first second; different angles; every product feature shown (jar, texture, application, finish); no blur at cuts, nothing stretched (all clips >= 1.0x); bright neutral grade; no on-screen text; 2x edges of hands/face clean; REMOVED.md checked
  EVIDENCE: 6 fps sheet of the whole 18.1 s viewed + full-size cut-point frames (0.03, 1.53, 6.40, 7.55, 11.65, 16.15 s): sharp, clean hand edges, bright neutral; 13 segs at 1.0x; no text. Audio: no voiceover (faster-whisper gave only inconsistent hallucinations); cut silent like Merach.
- [x] G4: (manual) Cut on the review page; Ralph push + email sent; Grace told on Telegram with pending wording (no ✅, no "done")
  EVIDENCE: review page https://claude.ai/artifact/C2kLU1fAaN1dyTM4nV4NCx; push requested; email 1a1c37f696abb752; Grace Telegram msg 358 (pending wording).
- [x] G5: (manual) After Ralph's OK on that exact cut: "CURRENT - JIYU NAD V1 (HD).mp4" in the product folder (size = local), older ones in Older versions; "✅ JIYU NAD+ Moisturizer V1 (HD) is done and in Drive: <link>" sent to Ralph and Grace
  EVIDENCE: Ralph 'Review ok' 2026-11-10; Drive file 1-w-pPMrXUU0rQBYnQNKi5Sav1k7LeWm9 'CURRENT - JIYU NAD V1 (HD).mp4' 23,044,656 bytes = local; folder had no older cut (only Originals); Telegram ✅ msgs 364 (Ralph) + 365 (Grace group)
- [x] G6: (manual) Brain note Brain/Jobs/JIYU NAD Moisturizer edit.md pushed; README Status current; media packed (MEDIA_OK); hourly Drive check deleted
  EVIDENCE: media set 1 (2 parts, 145 MB) recorded, 0 mismatched, MEDIA_OK; hourly check trig_01XMPLF2EyRGyqzDLBctWqY5 deleted; README + Brain note updated, Active work line removed (BRAIN_OK below)
