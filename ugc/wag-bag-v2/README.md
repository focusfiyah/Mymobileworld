# Wag Bag v2 (Grace), 2026-10-06

Status: r3 (2026-10-06) in Drive as CURRENT: V3 jump + V4 clipped 'make' fixed (clips start after Grace's take joins; sample-exact audio, one-pass join), all checks pass (`GATES.md`, `qc/verify_fix.py`). Waiting on Ralph. Cost $0. V1/V2 hooks say "shit": KEEP as Grace filmed (Ralph 2026-10-06).

Drive: Grace Tiktok assets / WagBag Final Edits (https://drive.google.com/drive/folders/1ZgU9Z8oQkT_Wca_EkXtfd6AbDFHZZgG8):
`CURRENT - Wag Bag V1..V5 (2026-10-06).mp4` + captions doc; the 2026-09-30 set (V01-V10) moved to "Older versions (2026-09-30 set)".

## What Grace asked
5 videos. Part 1 hook + Part 2 body are NEW recordings ("WAG BAG 1 (NEW).mov", "WAG Bag 2 (NEW).mov"); Part 3 (pointing at the
box on the toilet, "NASA developed poop powder") and Part 4 ("12 kits in this box... family") reuse the 2026-09-30 raw files
("WAG BAG 2 (3-5).MOV" = Part 3, "WAGBAG3.MOV" = Part 4). Emojis on the first clip: food, water, poop + question mark.

## Take map (`videos.json`, seconds in the source file)
| Video | Hook (p1_new) | Body (p2_new) | Part 3 (old2_35) | Part 4 (old3, hflipped) | Close | Grade / frame |
|---|---|---|---|---|---|---|
| V1 | take 1 ("...shit?") | take 1 + "So I keep these now" | take 1 | take 1 | "It's linked below in that orange cart." | natural, 1.00 |
| V2 | take 2 ("...shit?") | take 2 + "So I keep these now" | take 2 | take 5 | + take-1 orange-cart line | warm bright, 1.03 |
| V3 | take 3 | take 3 (to "sanitation issue") | take 3 | take 3 | "I'll link it below in that orange cart for you." | bright cool, 1.00 |
| V4 | take 4 | take 4 | take 4 | take 7 | + take-3 orange-cart line | clean neutral, 1.05 |
| V5 | take 5 (short version) | take 5 ("...exactly why I keep these now", whip to toilet) | take 5 | take 9 | + take-1 orange-cart line | bright punchy, 1.02 |

Only two Part 4 takes end on "orange cart"; the others say "I'll link it somewhere below this video", so V2/V4/V5 jump-cut to
an orange-cart line (Grace's close, playbook §1). That 1.4-1.8s line is the only footage shared between videos.

## Edit notes
- Part 4 raw is mirrored (box text backwards): flipped, which also matches the room to the new takes.
- Emoji v2 (Ralph: quality, not simple): Microsoft Fluent 3D (MIT), 256px shown at 170-260px, pop-in 0.22s + bob. 💧 "water", 🔋 "battery",
  ⚡ "generator" (no generator emoji exists; free same-set stand-in, Ralph OK), 💩 "where", white ❔ 0.3s after. v1 was flat Twemoji with a food can. V1/V4 open on Grace's own camera swing; top emojis sit wide so they clear her head.
- Audio: each segment loudnorm -16, 20-30ms fades, final -14 LUFS (measured -14.2 to -14.6).

## QC (2026-10-06)
- Re-transcribed every final (faster-whisper small.en, free): every line whole; the "It's" clip in V2/V5 fixed (cut moved 8.28 -> 8.25s).
- Pace 3.9-4.2 words/sec, no pause over 0.5s. Durations 30.3 / 30.5 / 30.3 / 32.5 / 33.7s.
- Contact sheets `qc/`: product never cropped, same red top in every part, box text reads right, emoji clear of face.
- Coach: `research/tag-wagbag.json`, `tag-emergencytoilet.json`. Top Wag Bag shop videos: @dmoncrea 223k (344s, 5.25% saves),
  @mamarashaah 119.7k (50s, 2.99% saves). `video`/`compare` failed on 4 of 4 TikTok video pages this session (no video data),
  so the compare is metadata only. Grace's own @shewiththeglow Wag Bag posts: 108 to 6.9k views.
- Product fact: NASA claim checked, spinoff.nasa.gov/node/11511.

Rebuild: put the four source files in `src/` (names above), `python3 cut.py [n]`; host with `host.py`, upload via Composio.
