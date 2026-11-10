# Gates: ili New York Double Flap Eyeglass Case edit (2026-11-10)

- [ ] G1: Grace's original video is downloaded and its size equals the Drive file size
  CHECK: python3 -c "import os,json;m=json.load(open('orig/meta.json'));print('ORIG_OK' if os.path.getsize(m['path'])==int(m['drive_size']) else 'MISMATCH')"
  EXPECT: ORIG_OK
- [ ] G2: (manual) Frames of the whole original viewed (contact sheet); shot list picks the case open/closed, both flaps, sunglasses + eyeglasses in, closure, leather close-up, in-hand/in-bag angles
- [ ] G3: Cut is 12-20 s, 1080x1920, no black frames, within 0.15 s of plan
  CHECK: python3 check.py ili 12 20
  EXPECT: CUT_OK ili
- [ ] G4: (manual) Every frame of the cut viewed (5-6 fps sheet) + 2x edges: no blur at cuts, nothing stretched (every clip >= 1.0x), bright neutral grade, no text, REMOVED.md checked
- [ ] G5: (manual) Cut on the review page (video full column width); Ralph push + email; Grace told on Telegram with pending wording (no ✅, no "done")
- [ ] G6: (manual) After Ralph's OK on that exact cut: Drive "CURRENT - ili Case V1 (HD).mp4" size = local; nothing loose; "✅ ili New York Eyeglass Case V1 (HD) is done and in Drive: <folder link>" sent to Ralph and Grace; hourly check task deleted
- [ ] G7: (manual) Brain note Brain/Jobs + Active work line removed; tools/brain/check.py prints BRAIN_OK
