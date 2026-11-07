# Compare notes (cut v1, 2026-11-07)
A = @hannahv2246 (327.8K, 30.4 s, VO 4.53 words/s, 21 cuts = 6.9/10 s). B = our cut v1 (29.6 s, VO 3.5 words/s).
- First pass: 9 shots = 2.7 cuts/10 s, slow. Fix (free): punch-in cuts inside every shot over 2.6 s, on the word start nearest its middle, second part 1.12x -> 16 segments = 5.1 cuts/10 s (tiktok.py's detector does not count punch-ins or fades: it read 8 cuts both times).
- Hook: A opens on a question with the tree already on the fridge; ours opens on the toddler's hand putting the star on (product working at frame 0), question hook H062.
- Pace of speech: ours 3.5 words/s, Grace's approved pace (voice README); not pushed to 4.5.
- Wan built-in cross-fades found by eye (S4 1.2 s, S5 2.8 s, S7 2.8 s) and cut before them; boundary frames checked clean.
