# Coach compare vs the top winner (2026-10-21, after the final cut)
A = @itskristaadams Jool tub https://www.tiktok.com/@itskristaadams/video/7683397629056699679 (563,800 views, 1.49% saves). B = out/shnuggle_next_bath.mp4.
Raw output: research/compare/compare/compare.md + compare.png (hook frames). No --stt (would use ElevenLabs credits; our transcript is vo/stt.json).

| | A (winner) | B (ours) |
|---|---|---|
| length | 34.9 s | 31.8 s |
| pace | 4.58 words/s | 3.40 words/s (108 words; Grace's paced voice, 3.5 w/s setting) |
| cuts | 18 (5.2 per 10 s) | 13 real (10 shot cuts + 3 punch-ins = 4.1 per 10 s); the tool's own scene detector counts 9 because our cuts are low-contrast (white/blue every shot) |
| first word | 0.0 s | 0.0 s |
| frame 0 | baby bath in use, hand | infant tub next to the toddler tub (the hook's "outgrew the baby bathtub") |

What I fixed from it: cuts were 2.8 per 10 s; added a 1.15x punch-in halfway through the three longest shots (S3, S5, S8) in cut.py (free, no clip stretched). S4 kept without one (its own push-in plus a punch-in cropped the tub).
Not changed: pace. Grace's voice is set to her own 3.5 words/s (her pick 2026-10-20) and the playbook range is 3.0-3.6; the winner talks faster than Grace does.
