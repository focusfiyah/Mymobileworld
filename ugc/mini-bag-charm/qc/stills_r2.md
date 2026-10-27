# Still QC, round 2 (2026-10-27): S1 S7 S9 redone ($0.27, Ralph: "Redo all 3")
| Shot | Verdict | Notes |
|---|---|---|
| S1 | PASS | No key; empty with tissue; gold key ring chain at the left handle. Scarf plainer than the real print (small). |
| S7 | PASS | Open bucket, scarf on the charm. The key ring hangs loose rather than visibly on the handle (small). |
| S9 | PASS | Scarf back on the charm, empty, tree behind, one charm. Key ring hangs loose (small). |
- 2026-10-27 Ralph: "Use Kie, 2. Let go" (product clips on Kie Omni instead of Flow; S3 watch-bracelet kept)
- 2026-10-27 Ralph: "Seedance from the stills now" (Omni on Kie: 5 tries, all 500, $0)
- 2026-10-27 S1 Seedance r1: clean 0-0.7 s only (hand lets go, a gold logo-ring charm appears ~1.5 s). Ralph: "Redo S1 on Seedance, $0.164 (Recommended)"
- 2026-10-27 Ralph: "V2 when putting in stocking stuffer its outside of it on V1 it went inside. Edit so that v1 shot is used on V2" -> cut.py FILE S8 = v1 clip ($0)

## Round 4 (2026-10-27) lessons
- Seedance 2.0 Mini first-frame keeps a tiny product's size but redraws it within 1-2 s (flap, wide scarf, padlock mark). A strong push-in makes it worse (S9 take 1).
- Free fix that holds: track the camera on the handbag NEAR the product (ORB + RANSAC partial affine, smoothed), cover the AI product with an inpaint from the frame itself, warp the real composite layer on top (tools/track_paste.py). Works on slow camera moves (S7, S8); fails when a hand moves the product (S4 take 1).
- Short lines: use the clean opening of a take (S5a 1.66 s).
