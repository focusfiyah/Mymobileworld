# Gates: JTV Pink Heart Necklace, 10 x 16 s edits (2026-11-12)
Request: Grace, Telegram group -5234107715, msg 466 ("I need up 10 videos that are 16 seconds long. Make sure no two videos start or end the same and don't duplicate clips in the same video"); originals A (export_1794449898752.mov) + B (788f8e00773c481687702813256f4441.mov) in Originals. Her own footage, no AI, $0.

- [x] G1: Every planned video is 16 s (+-0.15), 1080x1920, silent, no black frames, rendered from the full-quality originals
  CHECK: python3 check.py all
  EXPECT: ALL_CUTS_OK
- [x] G2: Grace's rules hold: no take used twice inside a video, no two videos share an opening or closing take, no two videos share the same shot order, every source window inside its file
  CHECK: python3 plan.py check
  EXPECT: RULES_OK
- [x] G3: (manual) Every frame of every cut viewed (6 fps sheets) + 2x crops of the first second: hook strong at frame 0, no blurry or blink frames kept, bright neutral grade, no text, nothing upscaled past 1.1x
- [x] G4: Captions file has the four sections, 5 hooks + 5 captions, hashtags, no dashes, no price, never says diamond or solid gold
  CHECK: python3 captions_check.py captions_seo.txt
  EXPECT: CAPTIONS_OK
- [x] G5: (manual) Humanizer + readability proofs; captions sent to Grace on Telegram (no ✅); "Captions & SEO" Google Doc in the product folder
- [x] G6: (manual) One review page, videos stacked full width; Ralph email (+ push if the tool exists); nothing uploaded to Drive before Ralph's OK
- [ ] G7: (manual) After Ralph's OK: CURRENT - JTV Heart Necklace V1..V10 in the product folder (sizes = local); one "✅ ... V1-V10 are done and in Drive" message
- [ ] G8: (manual) Brain note + session log, media packed, BRAIN_OK, merged to main

Evidence G1: ALL_CUTS_OK, V1-V10 16.00 s 480 frames each, 21.4-27.4 MB.
Evidence G2: RULES_OK 10 videos (openers b4 b1 b5 a5 b9 a4 b11 a2 b2 b6; closers b14 b13 a7 a1 b8 b12 b7 a3 b3 a6).
Evidence G3: 6 fps sheets of all 10 viewed; fixes after round 1: b10 closer dropped (phone hid the necklace and leaked a frame of the next take), a6 retimed to 34.4-36.6, a5 trimmed to 33.9 (chin swing), b9 starts 48.4 (blink), b3 retimed 15.4-17.4. 2x crops of all 10 openers: heart sharp and pink. Grades eq brightness 0.015-0.035, contrast 1.02-1.05, saturation 0.98-1.05; zoom 1.0-1.08.
Evidence G4: CAPTIONS_OK; negative control (empty file) FAILs.
Evidence G5: proof/humanizer.md, proof/readability.txt grade 3.0; Telegram Grace 472 (reply to 468, no ✅); Doc 1vlP1k-KUraPUvO8l231fqSwlT1M5JjWJKYF1gE6XbsY in the product folder (content read back).
Evidence G6: review https://claude.ai/code/artifact/488c44a5-f56a-4920-8e9a-61c566b683a0 (single column); email 1a1cdb2d762df526; Telegram Ralph 473; PushNotification not found by ToolSearch this session (tested). No video in the product folder.
