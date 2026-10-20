# Grace's AI-video sales tracker (winners)

Status: 2026-10-20 r2: Ralph's answers applied (versions v2 in Grace's looser wording, Promoted column), House of Rameau inventory pulled. Seeded with 6 videos that made 1 sale each (5 @shewiththeglow + 1 @houseoframeau), patterns read, 12 new
versions written (2 per winner, $0, gate checks pass). Next: Ralph picks which versions to make (cost asked first) and
answers the open questions below. Cost so far: $0 (local transcript instead of ElevenLabs STT).

Drive (Grace Tiktok assets/AI Video Sales Tracker (Grace)): https://drive.google.com/drive/folders/1X_fNJZ_b3g2faWNtkfV_5y3rbMWyF2pX
- CURRENT - Grace AI Video Sales Tracker (2026-10-20): Google Sheet 17qkOyW7s1jRoJsXLCnQxWzaNKL_8kUPy_y_C4CqPu7A
- CURRENT - What sold + 12 new versions v2 (Grace's wording, 2026-10-20): Google Doc 1V5w_FAxlilqTWa8IBXXrl3WHUJsx1HFxzrVgyiXA0AE
- Older versions/ (1OR84Wn5rzn2nvUe6zIEm9Sll5ZsSZ0O2): v1 (2026-10-20) doc 1bcdR7CBsvb6AZRVnWhKkVC8XOTycLykudlqIaVEpqZo
- The sheet is a living tracker: updated in place (Drive keeps its history), not copied per update.

## Adding a video (Grace sends link + sales)
Skill `grace-sales-tracker` (source focusfiyah/claude-skills). Short version:
`WINNERS_OUT=<scratch> python3 grace/winners/winners.py pull <link> --sales N`, look at the frames, `winners.py set <id> ...`
for the judgment fields, `winners.py export`, replace the sheet in Drive (older copy to "Older versions").

## Files
- `winners.json` source of truth; `winners.csv` / `winners.xlsx` exports (xlsx = what goes to Drive).
- `PATTERNS.md` what the winners share; `VERSIONS.md` the 12 new versions; `check.py` gate checks; `GATES.md` ledger.
- `research/` today's viral board, readability, humanizer proof.

## Ralph's answers (2026-10-20)
1. Which versions to make: not decided yet.
2. Promotion: Grace paid nothing; the brands paid to promote the 4 with TikTok's ad label (Promoted column).
3. New versions use Grace's looser wording (VERSIONS.md v2; HOOKS.md exception).
4. On-screen text: no change for now (nothing burned in; the text lines stay optional for Grace).
5. "my mom", "my kids or my dog", "every night" are true for Grace.
House of Rameau: Composio TikTok access, shared account we pull from and will post to (`houseoframeau/README.md`).
