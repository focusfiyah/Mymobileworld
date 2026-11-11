# Gates: COSRX Peptide Lip Care edit V1 (2026-11-11)
Request: Grace, Telegram group -5234107715, msg 430 (folders for 4 products, she uploads originals to edit). Her own footage, no AI, $0.

- [x] G1: Cut is 7-20 s, 1080x1920, length matches the plan, no black frames, no audio
  CHECK: python3 check.py cosrx 7 20
  EXPECT: CUT_OK cosrx
- [x] G2: (manual) Every frame of the cut viewed (6 fps sheet) + big crops at each shot: product from frame 0, sharp, no blur at cuts, nothing stretched, bright neutral, no on-screen text
- [x] G3: Captions file has all four sections, 5 hooks + 5 captions, no dashes, no price numbers
  CHECK: python3 captions_check.py captions_seo.txt
  EXPECT: CAPTIONS_OK
- [x] G4: (manual) Captions sent to Grace on Telegram (pending wording, no ✅), "Captions & SEO" Doc in the product folder, Humanizer + readability proofs, no medical claims
- [x] G5: (manual) Review page up (video full width); Ralph email + Telegram (push tool not found this session); nothing in Drive but the Doc
- [ ] G6: (manual) Ralph's OK on this exact cut; CURRENT - COSRX Lip Care V1.mp4 in the product folder (Drive size = local); "✅ COSRX Peptide Lip Care V1 is done and in Drive: <link>" sent
- [ ] G7: (manual) Brain note + session log, BRAIN_OK, media packed (MEDIA_OK), job merged to main

Evidence G1: CUT_OK cosrx 15.37s (6 shots, original 1080x1920 HEVC 30 fps, no scaling).
Evidence G2: proof/cut_sheet.png (6 fps, 93 tiles), cut_sheet2.png after the fix, zoom_sheet.png; r1 label shot went blurry (her camera move at 2:09) and swatch opened on a still second, both replaced (label 123.6-126.4, swatch 142.0-144.5).
Evidence G3: CAPTIONS_OK; negative control with a dash -> FAIL dash.
Evidence G4: Telegram group msg 443 (reply to 431); Doc 1xZ6GtbpDhUaYIJkC1FvrPfLEsBXrj9Ky03UXqXhlGhQ; proof/humanizer.md, proof/readability.txt (grade 1.9).
Evidence G5: review https://claude.ai/code/artifact/c1260536-203d-495c-89c9-36ae458bd36e; email 1a1cc14cd42ccd46; Telegram Ralph msg 444.
