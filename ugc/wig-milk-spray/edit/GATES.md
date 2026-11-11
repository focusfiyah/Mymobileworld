# Gates: Wig Milk Spray edit V1 (2026-11-11)
Request: Grace, Telegram group -5234107715, msg 430 (folders for 4 products, she uploads originals for us to edit); original WigMilkSpray2.mov in Originals. Her own footage, no AI, $0.

- [x] G1: Cut is 20-30 s (r2, Grace's script; r1 was 7-20), 1080x1920, silent, length matches the plan, no black frames
  CHECK: python3 check.py wig 20 30
  EXPECT: CUT_OK wig
  EVIDENCE: automatic-evidence=v1; definition-sha256=cea79ea49a3275a622dc15f29d219150b359f9fd7460f5099f260a8a88a882bc; exit=0; EXPECT=matched; output-sha256=be71941cffbf82470c755198fdbd9522d8c482a1e2ecf57a26c726f598bf9959; output-bytes=18; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wig-milk-spray/edit; path=7f4fb4b02918/15 entries
- [x] G2: (manual) Every frame of the cut viewed (6 fps sheet) + 2x crops: messy hair in the first second, nothing stretched, sharp, bright neutral grade, no on-screen text
  EVIDENCE: original viewed at 0.5 fps (5 sheets) + 2 fps windows; cut at 6 fps (98 tiles) + 2x crops at each shot start and frame 0: messy hair pull at 0.17-0.5 s, sharp, no stretch, no text. Swapped the 2:14 spray (half face off frame) for the centred 1:42 spray. Transcript (base.en): no talk track, only "okay"/"yes", so silent like Calmi.
- [x] G3: Captions file has all four sections, 5 hooks + 5 captions, hashtags, no dashes, no price numbers
  CHECK: python3 captions_check.py captions_seo.txt
  EXPECT: CAPTIONS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=81f6dffbc4dbdb55652d52654b52694de108ffa7a45d4ce4e76cabb0db07aece; exit=0; EXPECT=matched; output-sha256=f6bf10bcf8e86642eff126e64885dbb2334e4dd15827c218aef6a436ead2383d; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/wig-milk-spray/edit; path=7f4fb4b02918/15 entries
- [x] G4: (manual) Captions sent to Grace on Telegram (pending wording, no ✅) and saved as a "Captions & SEO" Google Doc in the product folder; Humanizer + readability run
  EVIDENCE: Telegram msg 448 to Grace (reply to 430, pending wording); Doc 1aqdkuZaI7OqWLJmUebfwe1lOixQ-0DR2gakRlOYdd6c; Humanizer pass, proof/readability.txt (FK 5.6).
- [x] G5: (manual) Review page up (video full width); Ralph push + email + Telegram; nothing in Drive before Ralph's OK
  EVIDENCE: review https://claude.ai/code/artifact/4d155291-40ba-4010-b2ab-2a88a21dd8fc; email 1a1cc1873dd9841d; Telegram Ralph 449; PushNotification not found by ToolSearch (tested). Drive holds only the captions Doc from this job.
- [x] G6: (manual) After Ralph's OK: CURRENT - Wig Milk Spray V1.mp4 in folder (size = local); "✅ Wig Milk Spray V1 is done and in Drive" sent
  EVIDENCE: Ralph "Ok" 2026-11-11 on r2; CURRENT - Wig Milk Spray V1.mp4 1qHzrCFsVvgfASkpbUNdXRO_HNK4GsjZo 62,779,917 bytes = local; no older video to move; ✅ sent to Ralph + Grace.
- [x] G7: (manual) Brain note updated, BRAIN_OK, media packed, job merged to main
  EVIDENCE: Brain note updated, BRAIN_OK, media in Drive (sets 1-2 recorded), merged to main.

Evidence G1: CUT_OK wig 16.30s (6 shots, 1080x1920 source, no scaling beyond 1:1).
Evidence G3: CAPTIONS_OK.
Evidence r2 (2026-11-11 19:40): Grace msg 438 made the transcript the script. CUT_OK wig 26.90s; every line within 0.3 s of its spoken length at 3.5 w/s except the cart line (+0.9 s end hold); 6 fps sheet viewed (162 tiles): tangled hair only before the spray, no smooth-hair shot before the spray (dropped the 4:01 bottle shot for that). Grace msg 450, Ralph 451, email 1a1cc1d008c40e09, review v2.
