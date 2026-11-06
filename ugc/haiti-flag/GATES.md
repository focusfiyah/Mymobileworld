# Gates: Haiti flag edit (2026-11-06)

- [x] G1: Cut is 12-20 s, 1080x1920, silent, no black frames
  CHECK: python3 check.py haiti 12 20
  EXPECT: CUT_OK haiti
- [x] G2: (manual) Contact sheet of the cut viewed; blurred/red-only segment removed, pack, unfold, emblem, drape, wall hold all shown
  EVIDENCE: 2026-11-06 3-fps sheet viewed, 14.0 s, no freeze/black via ffmpeg detectors
- [x] G3: (manual) Cut + original in Drive "Haiti Flag (Grace)", sizes match (14402314, 15443036); review page published; Ralph told on Telegram + email
  EVIDENCE: Telegram ok=True; Drive sizes match local; folder NOT shared with Grace (blocked, Ralph gave no preference)
