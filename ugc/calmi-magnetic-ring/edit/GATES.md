# Gates: Calmi Magnetic Ring edit V1 (2026-11-11)
Request: Grace, Telegram group -5234107715, msgs 409 (video, "edit this video ... 7-20 seconds") + 410 (Drive folder; text overlay hooks, video caption options, SEO phrases, hashtags). Her own footage, no AI, $0.

- [x] G1: Draft cut is 7-20 s, 1080x1920, length matches the plan, no black frames
  CHECK: python3 check.py calmi 7 20
  EXPECT: CUT_OK calmi
- [x] G2: (manual) Every frame of the cut viewed on a contact sheet + 2x crops: strong first second, nothing stretched (>=1.0x), no blur at cuts, bright neutral grade, no on-screen text
- [x] G3: Captions file has all four sections (text overlay hooks, video captions, SEO phrases, hashtags), no dashes, no price numbers
  CHECK: python3 captions_check.py captions_seo.txt
  EXPECT: CAPTIONS_OK
- [x] G4: (manual) Captions sent to Grace on Telegram (pending wording, no ✅) and saved as a "Captions & SEO" Google Doc in the product folder; Humanizer + readability run (proof files)
- [x] G5: (manual) Telegram copy saved in "Telegram Assets (Azariah)" with a README index line, Drive size = local
- [x] G6: (manual) Review page up (video full width); Ralph push + email; nothing in Drive before Ralph's OK
- [ ] G7: (manual) HD cut from Grace's original after it lands; Ralph's OK; CURRENT - Calmi Ring V1.mp4 in folder (size = local); "✅ Calmi Magnetic Ring V1 (HD) is done and in Drive" sent
- [ ] G8: (manual) Brain note updated, BRAIN_OK, media packed, job merged to main

Evidence G1: CUT_OK calmi 15.00s (6 shots; 464x848 scaled to 1080 wide + cropped to 1920, not stretched).
Evidence G2: whole 72 s at 1 fps, windows at 4 fps, cut at 6 fps (90 tiles) + 2x crop at each shot start: lid-off hook at 0.7 s, her jump cut at 33.2 s and blurry 15-17 s avoided, weak edge-of-frame shot (68 s) dropped; grade eq brightness 0.025 contrast 1.03; no text. Soft = Telegram compression (draft).
Evidence G3: CAPTIONS_OK; negative control with a dash -> FAIL dash.
Evidence G4: Telegram msg 415 to Grace (reply to 410, pending wording); Doc 1Jfn7Cl9dUPnelVknQFQh2fAX2tp2Vtzf84JDke3oZWk in the product folder; proof/humanizer.md, proof/readability.txt (grade 3.0).
Evidence G5: Drive 1cxXnO7WwAOruN7CWf4bMUs7lAgwRI-zg 15,026,608 bytes = local; index line appended (6,543 bytes).
Evidence G6: review https://claude.ai/code/artifact/2e73cc5c-79f3-4b39-a3aa-cbd85f0c23f0; email 1a1c8a75fc775ca9; Telegram Ralph msg 416; PushNotification tool not found by ToolSearch this session (tested), so email + Telegram carried it. Nothing in Drive except the captions Doc and the Telegram asset.
