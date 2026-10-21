# Gates: tracker round 2 (Ralph's answers + House of Rameau access), 2026-10-20

OWNS: grace/winners/**, houseoframeau/**, CLAUDE.md, grace/PLAYBOOK.md, .claude/skills/grace-sales-tracker/**

Scope: apply Ralph's 5 answers to the tracker and the 12 versions, and set up House of Rameau (Composio TikTok access) as a shared account we pull from and post to.

- [ ] R1: every winner row has a promoted field; the 4 TikTok-marked ad videos say promoted by the brand
  CHECK: python3 grace/winners/check.py promoted
  EXPECT: PASS promoted
  EVIDENCE: pending

- [ ] R2: the 12 versions use Grace's looser wording: each names its library hook id as the base, none opens with the library line word for word, every close mentions the orange cart, no banned phrase, grade <= 6, no "Check with Ralph" notes left
  CHECK: python3 grace/winners/check.py versions
  EXPECT: PASS versions 12
  EVIDENCE: pending

- [ ] R3: houseoframeau/videos.json lists all 26 public videos from the Composio pull, with shop products found for the shop videos
  CHECK: python3 houseoframeau/check.py
  EXPECT: PASS houseoframeau
  EVIDENCE: pending

- [ ] R4: humanizer proof newer than VERSIONS.md
  CHECK: python3 grace/winners/check.py proofs
  EXPECT: PASS proofs
  EVIDENCE: pending

- [x] R5: Drive: new sheet + doc as CURRENT, the first ones renamed v1 (2026-10-20) inside "Older versions", nothing loose
  EVIDENCE: 2026-10-20 folder listing: CURRENT sheet 17qk... (updated in place A1:X7, read back), CURRENT doc v2 1V5w..., Older versions/ holds v1 doc 1bcd...; nothing else loose. Deviation: sheet updated in place (living tracker) instead of a v1 copy.

- [x] R6: committed + pushed; Ralph emailed + pushed
  EVIDENCE: 2026-10-20 pushed 39fbd23 (Mymobileworld) + 669e06a (claude-skills) to claude/ai-video-sales-tracker-r3dl1y; Gmail id 1a1573d4262b9769; PushNotification 'Mobile push requested'
