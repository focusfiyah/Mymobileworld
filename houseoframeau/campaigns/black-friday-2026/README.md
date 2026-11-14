# TikTok Shop "Big Dreams Start With Black Friday" video challenge, House of Rameau (2026-11-12)

Status: Day 1 sent 2026-11-12; days 2-3 staged (Niagara, Earth Breeze). Next: holiday remake test (NovaTabz, Ralph voice) for his OK.

Rules of the challenge (Ralph's screenshot 2026-11-12): post qualified videos (>= 15 s) on more days, Nov 11 - Dec 1 2026;
each day counts once. Milestones: 4 days $15, 10 days $40, 18 days $100. Nov 11 was missed, so 20 days are left and
18 days allows 2 misses.
Ralph 2026-11-12: drafts the old way (TikTok inbox, he adds the shop link and posts), one per day (tapped "One per day"),
Camera Detector HofR included (tapped "Yes, include it"), the rest from "previous videos we have done" (Grace's cuts that
already have a voiceover, as they are). Route: Composio GOOGLEDRIVE_DOWNLOAD_FILE (googledrive_lin-ernst) -> s3key ->
TIKTOK_UPLOAD_VIDEO on tiktok_buck-flunk, publish false, is_aigc true. Check >= 15 s with ffprobe first. $0.

## Queue (one product per video, no repeats: Ralph 2026-11-12)
Ralph 2026-11-12 (after day 1): remake the gift-type ones with a holiday theme for free: holiday b-roll (free Pexels/Pixabay
clips) + holiday hook text, his voice on the VO ("You can also change the Vo to my voice", Ralph Azariah clone
5YVjMzHn641xyj0jM38O, ElevenLabs subscription characters, ~300 a video), "there should not be any repeat products".
The daily task only sends rows whose Drive id is filled in; a remake row gets its id only after Ralph OKs that cut.

| Day | Date | Video (Drive file id) | Length | Sent |
|---|---|---|---|---|
| 1 | 11-12 | HofR - Christmas Cheer V2 (1zbPmq2zmAIaWPVYoYqd1dLzdd2CSRhLp) | 18.8 s | 2026-11-12 v_inbox_file~v2.7707409749188904991 |
| 2 | 11-13 | CURRENT - Niagara topper V1 HofR (1H143eRkxHKiDaMcXgawApHYNZLvnK5O1) | 16.5 s | |
| 3 | 11-14 | HofR - Earth Breeze V2 (1c4G0egMPtkDDYdjXyow5MTikFp58V-hZ, in Earth Breeze product folder) | 17.2 s | |
| 4-20 | 11-15..12-01 | Rows added when Ralph OKs each cut (sessions below report Drive ids here) | >= 15 s | |

Measured 2026-11-12: Boo-Boo Gel HofR V2 is 13.6 s (does not qualify as is); NovaTabz HofR 15.2 s; Camera Detector HofR
full cut is not stored (only a 3.9 MB review copy), so it needs a rebuild. Jelliquid HofR 12 s, music only: not used.
If no approved row is waiting on a day, the task tells Ralph on Telegram instead of sending a repeat.

## Sessions making days 4-20 (Ralph 2026-11-12: "separate the task into different sessions")
Voice for all of them: Ralph's free Chatterbox clone (the "Sorry I Lied" voice), never ElevenLabs (Ralph 2026-11-12:
"Do not use 11 Labs for voiceovers. Use the other voice that we use."). Grace's silent edits get his voiceover; gift-type
products get holiday b-roll + holiday hook text; $0.
- session_01Y1Pt3sNUxJgWP8wwrrA85e: NovaTabz holiday test, re-voiced (bf-novatabz)
- session_01Y1Pt3tFjRJnrDnWs8aN8At: Boo-Boo Gel HofR to 15 s+ with more b-roll
- session_01Y1Pt3qAXodVhTYn1pPRJUL: silent A: GALENTAL Mirror, Crowned Skin Body Butter, Ear Wax Camera, Water Coloring Book, Meat Sticks
- session_01Y1Pt3pFXuhqRgggqDLNecT: silent B: Pinmoco Chair, Calmi Ring, COSRX Lip Care, Waterproof Eyeliner, Wig Milk Spray
- session_01Y1Pt3t3hdge7mW6xtDdj2C: silent C: PURCELL Mist, JIYU NAD, LUVUM Gel Mask, Momo & Nashi Tracing, 52 Manners (Kids)
Each sends this hub "<product>, Drive file id, length, approved by Ralph <date>"; the hub adds the row.
