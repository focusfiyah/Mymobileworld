# Grace's AI-video sales tracker (winners)

Status: 2026-10-20 seeded with 6 videos that made 1 sale each (5 @shewiththeglow + 1 @houseoframeau), patterns read, 12 new
versions written (2 per winner, $0, gate checks pass). Next: Ralph picks which versions to make (cost asked first) and
answers the open questions below. Cost so far: $0 (local transcript instead of ElevenLabs STT).

Drive (Grace Tiktok assets/AI Video Sales Tracker (Grace)): https://drive.google.com/drive/folders/1X_fNJZ_b3g2faWNtkfV_5y3rbMWyF2pX
- CURRENT - Grace AI Video Sales Tracker (2026-10-20): Google Sheet 17qkOyW7s1jRoJsXLCnQxWzaNKL_8kUPy_y_C4CqPu7A
- CURRENT - What sold + 12 new versions (Grace, 2026-10-20): Google Doc 1bcdR7CBsvb6AZRVnWhKkVC8XOTycLykudlqIaVEpqZo

## Adding a video (Grace sends link + sales)
Skill `grace-sales-tracker` (source focusfiyah/claude-skills). Short version:
`WINNERS_OUT=<scratch> python3 grace/winners/winners.py pull <link> --sales N`, look at the frames, `winners.py set <id> ...`
for the judgment fields, `winners.py export`, replace the sheet in Drive (older copy to "Older versions").

## Files
- `winners.json` source of truth; `winners.csv` / `winners.xlsx` exports (xlsx = what goes to Drive).
- `PATTERNS.md` what the winners share; `VERSIONS.md` the 12 new versions; `check.py` gate checks; `GATES.md` ledger.
- `research/` today's viral board, readability, humanizer proof.

## Open questions for Ralph / Grace
1. Did Grace pay to promote any of these? TikTok marks 4 of 6 as ads (changes how views per sale reads).
2. All 6 winners had on-screen text Grace typed in TikTok. Keep that as Grace's step, or burn text in on our side?
3. 4 of 5 were re-worded by Grace when she posted (her version sold). Should new versions use library hooks word for
   word (current rule) or her looser wording?
4. Facts to confirm for 3 scripts: glasses-B "my mom", sofyre-B "my kids or my dog", bodyj-B "every night".
