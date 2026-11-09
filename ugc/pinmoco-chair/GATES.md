# Gates: Pinmoco cross-leg chair edit (2026-11-08)

- [x] G1: Draft cut is 12-20 s, 1080x1920, silent, no black frames, length matches the segment plan
  CHECK: python3 check.py chair 12 20
  EXPECT: CUT_OK chair
- [x] G2: (manual) Every frame viewed at 10 fps: hook = nursing cross-legged at frame 0; shows cross-leg seat, desk use with baby, cloud footstool (baby on it, moving it), swivel, heart backrest, teddy texture, overview; no hand sweep across the product, no blurry cut points
- [x] G3: (manual) Draft in Drive product folder (CURRENT - draft), Telegram copy in Originals; review page up; Ralph push + email; Grace answered on Telegram (no ✅, no "done")
- [x] G4: (manual) HD original from Grace re-cut with the same edit, QC'd, CURRENT; draft in Older versions; "✅ Pinmoco Cross-Leg Chair V1 (HD) is done and in Drive" sent
- [x] G5: HD cut is 12-20 s, 1080x1920, silent, no black frames
  CHECK: python3 check_hd.py chair 12 20
  EXPECT: CUT_OK chair
