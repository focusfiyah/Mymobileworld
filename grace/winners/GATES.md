# Gates: Grace AI-video sales tracker (winners) + better versions, 2026-10-20

OWNS: grace/winners/**, grace/PLAYBOOK.md, CLAUDE.md, .claude/skills/grace-sales-tracker/**

Scope: one tracker of Grace's AI videos that made sales (6 seeded from Ralph's links), a one-command intake for new links, a patterns read, 2 better versions per winner, all in Drive + repo, Ralph notified.

- [ ] G1: winners.json holds exactly the 6 seeded videos, each with every required field filled (product, link, sales, views, faceless, hook, hook_id/type, pain_point, problem_solved, why_converted, script, format)
  CHECK: python3 grace/winners/check.py fields
  EXPECT: PASS fields 6
  EVIDENCE: pending

- [ ] G2: intake works on a real link: `winners.py pull <link>` fetches product, caption, transcript, views, posted date from TikTok this session
  CHECK: python3 grace/winners/check.py intake
  EXPECT: PASS intake
  EVIDENCE: pending

- [ ] G3: the CSV/XLSX export matches winners.json row for row
  CHECK: python3 grace/winners/check.py export
  EXPECT: PASS export
  EVIDENCE: pending

- [ ] G4: PATTERNS.md covers every winner by product name and lists at least 5 shared patterns
  CHECK: python3 grace/winners/check.py patterns
  EXPECT: PASS patterns
  EVIDENCE: pending

- [ ] G5: VERSIONS.md has 2 new versions per winner (12), each hook word for word from the hook library, closes "It's in the orange cart.", no banned phrase, no price number, reading grade <= 6
  CHECK: python3 grace/winners/check.py versions
  EXPECT: PASS versions 12
  EVIDENCE: pending

- [ ] G6: humanizer pass + today's viral board saved as proof files
  CHECK: python3 grace/winners/check.py proofs
  EXPECT: PASS proofs
  EVIDENCE: pending

- [x] G7: Google Sheet tracker + versions doc in Drive "Grace Tiktok assets" in one folder, CURRENT- names, nothing loose; links in README
  EVIDENCE: 2026-10-20 Drive folder 1X_fNJZ_b3g2faWNtkfV_5y3rbMWyF2pX holds exactly 2 files (search parentId): Sheet 17qkOyW7s1jRoJsXLCnQxWzaNKL_8kUPy_y_C4CqPu7A (read back: 6 rows, emoji intact) + Doc 1bcdR7CBsvb6AZRVnWhKkVC8XOTycLykudlqIaVEpqZo; both CURRENT-; links in README.md

- [x] G8: skill grace-sales-tracker in focusfiyah/claude-skills, deployed to Mymobileworld, zip built for claude.ai
  EVIDENCE: 2026-10-20 skills/grace-sales-tracker in claude-skills, audit.py 0 errors 0 warnings, deploy.py -> Mymobileworld/.claude/skills/grace-sales-tracker + dist/grace-sales-tracker-skill.zip

- [ ] G9: committed and pushed (Mymobileworld + claude-skills) on claude/ai-video-sales-tracker-r3dl1y; Ralph emailed + pushed with the links
  EVIDENCE: pending
