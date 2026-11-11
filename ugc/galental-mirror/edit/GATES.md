# Gates: GALENTAL Iceberg Vanity Mirror edit V1 (2026-11-11)
Request: Grace, Telegram group -5234107715, msg 430 (folders for 4 products, she uploads originals). Original Mirror1.mov (Drive 1i3778nzWGtD0DHopyZQJI-ELYptnfAKa, only file in Originals). Her own footage, no AI, $0.

- [x] G1: Cut is 7-20 s, 1080x1920, length matches the plan, no audio, no black frames
  CHECK: python3 check.py galental 7 20
  EXPECT: CUT_OK galental
- [x] G2: (manual) Every frame of the cut viewed (6 fps sheet) + 2x crops at each shot start: strong first second, not stretched, sharp, bright neutral grade, no on-screen text
- [x] G3: Captions file has all four sections, 5 hooks + 5 captions, hashtags, no dashes, no price numbers
  CHECK: python3 captions_check.py captions_seo.txt
  EXPECT: CAPTIONS_OK
- [x] G4: (manual) Captions sent to Grace in the group (pending wording, no ✅) and saved as a "Captions & SEO" Google Doc in the product folder; Humanizer + readability proof files
- [x] G5: (manual) Review page up (video full width); Ralph push + email; nothing in Drive before Ralph's OK
- [ ] G6: (manual) After Ralph's OK on this exact cut: CURRENT - GALENTAL Mirror V1.mp4 in the folder (size = local); "✅ GALENTAL Iceberg Vanity Mirror V1 is done and in Drive" sent
- [ ] G7: (manual) Brain note updated, BRAIN_OK, media packed, job merged to main

Evidence G1: CUT_OK galental 15.80s (planned 15.75), 474 frames.
Evidence G2: 6 fps sheet of the whole cut (95 tiles) + 2x crops at each shot start: sharp, real footage, not stretched (1080x1920 source, no scale change), tap hook flips cool->warm at 0.83 s, white flash ~9.2 s is the mirror's own brightest setting; no text.
Evidence G3: CAPTIONS_OK; readability grade 4.6 (proof/readability.txt).
Evidence G4: Telegram msg 439 to Grace (reply to 430, pending wording, no ✅); Doc 1PJQWoTJQLVY3MXkJrsNbdPLSoGqQ3wHZkOx57E2lO-4 in the product folder; proof/humanizer.md.
Evidence G5: review https://claude.ai/code/artifact/86f94278-821c-4988-b260-a0970ef95b96; email 1a1cc1395be787ad; Telegram Ralph 440; PushNotification not found by ToolSearch this session (tested). Drive holds only the captions Doc.
