# QC report template (save as ugc/<job>/qc_<version>.md; Ralph must never find the problem first)

Cut: ____  Date: ____  Checked on the FINAL file, frame by frame where hands or product cross the face.

| Check | Pass | Evidence |
|---|---|---|
| Real product identical in every shot (top, cap, label, color) | | frames |
| Product never cropped off or smeared | | |
| No shimmer/flicker (measured on final) | | number |
| Hands: from frame edge, whole wrists, no background through hands, `qc_hands.py` all frames | | |
| No forehead wrinkles / face artifacts | | |
| Same outfit and nails in every shot | | |
| Every clip speed >= 1.0x (no stretch) | | min speed |
| Lips move whenever a face shows during VO | | |
| Real moving clips: no freezes, no Ken Burns on photos, no pictures Ralph didn't ask for | | |
| Audio: pauses trimmed, cuts on word timings, words/s in range | | |
| Caption/hook text from frame 0, readable | | |
| Banned phrases / price / client name absent (gate) | | |
| `REMOVED.md` checked: list every element in the cut against it and last round's notes | | elements |
| `tiktok.py compare` vs winner (gate `--stage cut`) | | file |
| Cost: running total vs quote | | $ vs $ |

Verdict: SEND / FIX FIRST (list). Free fixes before any reroll.
