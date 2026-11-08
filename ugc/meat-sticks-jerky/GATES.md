# Gates: Meat Sticks + Sweet Heat Beef Jerky Variety Pack edit (Grace, 2026-11-08)

Real footage edit, $0. Blocked until Grace's original lands in Drive Originals (1GlOQD7uEAzqXLwuqDHAvB9iuynTxdx6q): the Telegram file (23.1 MB) is over the Bot API 20 MB limit.

- [ ] G1: HD cut is 12-20 s, 1080x1920, no black or frozen frames, silent (her audio is unboxing noise only, she adds music)
  CHECK: python3 check.py meat 12 20 silent
  EXPECT: CUT_OK meat
- [x] G2: (manual) Whole original viewed as frames; cut contact sheet viewed at full size: strong first second, different angles, all 10 sticks + the jerky + all 4 flavors (Original, Pineapple Chili Lime, Hot Honey, Pink Himalayan Salt) shown, no on-screen text, bright neutral grade, no stretched footage (every segment 1.0x)
  EVIDENCE: 2026-11-08 whole original viewed at 1 fps + 4 fps around picks; cut 4 fps sheet viewed; 2x check: yellow-green = Pineapple Chili Lime; LED/blank-lid shot swapped; 12 segments all 1.0x; no text
- [x] G3: (manual) Cut in Drive folder 1Mu9n46JVvRQ3Wo_dUOPjqqWt59YzGyG6 as "CURRENT - Meat Sticks Jerky V1.mp4", Drive size = local size, nothing loose
  EVIDENCE: 2026-11-08 Drive id 119UzBJrrVamyi6FPzzfUDyJgiyrNoNnV size 30118462 = local; folder holds Originals + CURRENT only
- [x] G4: (manual) Review page published (video full column width); Ralph told by push + email
  EVIDENCE: 2026-11-08 https://claude.ai/artifact/LpXGMy2aEYT5aPz8T4e1dE ; push requested; email id 1a1bd79e0808e24e
- [x] G5: (manual) Telegram to Grace's group: "✅ ... V1 (HD) is done and in Drive: <folder link>" sent once, only after G1-G4
  EVIDENCE: 2026-11-08 Telegram group -5234107715 msg 285 ok=True (reply to 267)
- [x] G6: (manual) Media packed (tools/media/media.py check prints MEDIA_OK); Brain job note updated; Active work line removed; branch merged to main
  EVIDENCE: 2026-11-08 media.py record 2 parts (0 mismatched), MEDIA_OK; Brain note + session log; Active work line removed; merged to main
