# Gates: Waterproof Ultra-Fine Eyeliner edit V1 (2026-11-11)
Request: Grace, Telegram group -5234107715, msg 430 (folders for 4 products, she uploads originals to edit); original WaterproofEyeliner.mov in Originals. Her own footage, no AI, $0.

- [x] G1: Cut is 7-20 s, 1080x1920, silent, length matches the plan, no black frames
  CHECK: python3 check.py eyeliner 7 20
  EXPECT: CUT_OK eyeliner
- [x] G2: (manual) Every frame viewed (6 fps sheet) + 2x crops at each shot: strong first second, nothing stretched, sharp, bright neutral grade, no text, no other brand's product (RCMA palette, mascara left out)
- [x] G3: Captions file has all four sections, 5 hooks + 5 captions, no dashes, no price numbers
  CHECK: python3 captions_check.py captions_seo.txt
  EXPECT: CAPTIONS_OK
- [x] G4: (manual) Humanizer + readability proofs; captions sent to Grace on Telegram (pending wording, no ✅); "Captions & SEO" Google Doc in the product folder
- [x] G5: (manual) Review page up (video full width); Ralph push + email; nothing in Drive before Ralph's OK
- [ ] G6: (manual) Ralph's OK; CURRENT - Eyeliner V1.mp4 in folder (size = local); "✅ Waterproof Ultra-Fine Eyeliner V1 is done and in Drive" sent
- [ ] G7: (manual) Brain note updated, BRAIN_OK, media packed, job merged to main

Evidence G1: CUT_OK eyeliner 14.90s (6 shots, source already 1080x1920, no stretch).
Evidence G2: whole 3:58 at 1 fps, candidate windows at 4 fps, cut at 6 fps (90 tiles) + 2x crops at each shot: hook moved 0.7 s later so the smile lands at 1.2 s; no RCMA palette or mascara in frame; box print sharp at 2x; grade eq brightness 0.02 contrast 1.03; no text.
Evidence G3: CAPTIONS_OK.
Evidence G4: proof/humanizer.md (3 edits), proof/readability.txt grade 3.1; Telegram Grace msg 441 (reply to 430, pending wording); Doc 1gQnqpohQxFQvGxyvOeZNSb8T9uIR2tr2gxlbp9_erBo in the product folder.
Evidence G5: review https://claude.ai/code/artifact/40c360b1-1104-49a7-a8fe-9cbde2491bb0; email 1a1cc14ac0ada537; Telegram Ralph 442; PushNotification not found by ToolSearch (tested). Nothing in the product folder except the captions Doc.
Progress G7: Brain note + Active work line pushed (6e1d3f4); media set1 in Drive 16ANovRjuPybKJO3ew4X3vj4x7YGMpVzf (sha256 recorded). Left: Ralph's OK, merge, Active line removal, BRAIN_OK.
