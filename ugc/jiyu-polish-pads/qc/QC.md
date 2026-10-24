# QC, out/jiyu_v1.mp4 (2026-10-24)
- qc/check.py: CHECK_OK (9 cuts on planned boundaries, -16.2 LUFS, only the end-hold silence, no black frames).
- Every clip at 1.0x (cut.py asserts each window fits its clip; S7 = clean window + reverse, no stretch).
- Product: real JIYU letters on every jar frame (S1 original peach/green; S2-S5, S8, S10 new jar); S3 Seedance letters checked at 2x on 3 frames.
- Hands: one hand per shot... MISSED: S3 had six digits (an extra crown-ring finger at top left); Ralph caught it at 6 s. Digit count added to the hand check.
- Face: half face only. S6/S9 lash tips painted out per frame (tools/lash_video.py, no shimmer); S7 uses 0.5-3.85 s only (eye corner at 0-0.25 s, face turn after 3.9 s).
- Flash: S3 starts at 0.125 s (Seedance's 3 bright first frames skipped); Flow clips max brightness jump <= 0.6.
- First second: S1 original jar in hand, clean edges.
- REMOVED.md: lavender jar none; full face/eyes/mouth none; on-screen text none; two same-side hands none.
- Voice: Grace cloned, word for word (STT), echo 150 ms. AI finish applied (grain 6, sharpen 0.6, saturation 0.92).
