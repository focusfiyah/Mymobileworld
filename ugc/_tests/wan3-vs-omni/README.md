# Wan 3.0 vs Omni test (ZYTRELL S3)

Status: 2026-11-03 DONE. Wan 3.0 beat Omni on this held-product shot (same grip all 5 s; Omni swapped the hand at ~2 s). Kie $0.40 of $0.40 approved. Review page: https://claude.ai/artifact/BqEPDXFux8jH7489HiA525

- Ralph's OK: tapped "One test vs Omni (Recommended)" ($0.40), 2026-11-03.
- Shot: ugc/zytrell-acne-cream S3 (hand lifts the tube), same three refs as the Omni take: stills/S3.png, refs/logo_closeup.png, refs/product_sheet.png.
- Run: `python3 run.py` (wan/3-0-video, reference mode, 720P, 9:16, 5 s, audio off). Task 5f2222e59a71e5c99f387c8030adee69, billed 80 credits = $0.40, CLIP_CHECK_OK 0.89.
- Compare: `python3 compare.py` -> compare.png, label_2x.png, strip/.

## QC (looked at every frame at 6 fps + 2x crops)
- Grip: same hand, rings and thumb position the whole clip. No regrip, no flip, no turn.
- Label at 2x: "zytrell", TM, SKIN SOLUTIONS, leaf icon, ACNE TREATMENT CREAM right. The tiny lines (fast acting / vegan & botanical / Net Wt) are soft and garbled, same as Omni's.
- Hand edges at 2x (first frame, 4.8 s): clean, no halo, smear or background through the hand.
- Motion: holds still ~1.6 s, then lifts toward the lens and holds; slow push-in.
- Weak points: 720p (our cuts are 1080p); 1080P costs $0.16/s ($0.80 for 5 s) vs Omni $0.315 for 4 s.

## Free upscale (2026-11-03, Ralph: "Can we do wan at 720 then upscale on our own to keep the lower cost")
- Yes. Wan 720P = $0.08/s, the same per second as Omni ($0.315 / 4 s). `upscale.sh IN OUT` (lanczos + light unsharp) takes ~4 s per clip.
- At 2x the label is close to Omni's native 1080p; it matched a free AI upscaler (FSRCNN x2, 2 min per clip); hand edges clean, no halos.
- So Wan's 1080P ($0.16/s) is not needed. Review page section "Wan at 720p, upscaled by us to 1080p".
