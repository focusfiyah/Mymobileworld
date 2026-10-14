# Coach compare, cut r1 vs top winner (2026-10-14)
A = @wrldoflyrics_ 7689185394939710750 (3.1M views, SoFyre's category winner), B = out/sofyre_r1.mp4.
`tiktok.py compare` output: research/coach/compare/compare.md + compare.png (no TikTok captions on either; word counts below
from our faster-whisper transcript of A and ElevenLabs STT of B).

| | A (winner) | B (ours) |
|---|---|---|
| duration | 68.1s | 34.9s |
| words / sec | 4.99 | 3.48 |
| cuts / 10s | 1.0 | 2.9 |
| first 3s | "As temperatures start dropping, guess who's trying to look for somewhere warm to live?" | "This is going to matter once it gets cold outside, because" |
| product on screen | ~40s in | frame 0 |

Findings
- Same opener (cold weather -> mice want somewhere warm), same beats (droppings, where to put them, smell, pets, count).
- Ours is half as long and shows the product from frame 0; the winner is a talking head that reaches the product late.
- Our VO is slower (3.5 vs 5.0 words/s). Free fix if Ralph wants it punchier: speed the VO + picture 1.1x (never below 1.0x),
  ~31.7s. Not applied in r1 (Grace B already sounds natural at this pace).
- 3x more cuts than the winner: fits a hands + voiceover video with no face to hold attention.
