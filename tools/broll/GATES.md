# Gates: broll-mcp for b-roll when editing (Ralph 2026-10-24)

OWNS: tools/broll/**, .claude/hooks/broll_setup.sh, .mcp.json, .claude/settings.json, CLAUDE.md, handoff/**

Scope: broll-mcp (github.com/edigeh/broll-mcp, MIT, pinned d8fda0a) is safety-reviewed, registered as an MCP server in Mymobileworld + Dayone-ai, pre-warmed each session, proven on a real archive.org search + cut, and written into the rules so every editing session reaches for it when a cut needs b-roll.

- [ ] G1: security review recorded (SkillSpector or stated fallback + manual source review, verdict)
  CHECK: python3 tools/broll/verify.py review
  EXPECT: BROLL_REVIEW_OK

- [ ] G2: the pinned .mcp.json command starts, lists the 4 tools, and search_footage returns ranked archive.org items
  CHECK: python3 tools/broll/verify.py search
  EXPECT: BROLL_SEARCH_OK

- [ ] G3: extract_clip writes a verified MP4 (duration within 0.1 s of the ask) with a provenance JSON next to it
  CHECK: python3 tools/broll/verify.py cut
  EXPECT: BROLL_CUT_OK

- [ ] G4: both repos register broll (same pinned command, no model id), hook runs at SessionStart, hook copies identical
  CHECK: python3 tools/broll/verify.py config
  EXPECT: BROLL_CONFIG_OK

- [ ] G5: CLAUDE.md + the four handoff memory files mention broll-mcp in both repos, MEMORY_SHORT <= 2,000 chars
  CHECK: python3 tools/broll/verify.py docs
  EXPECT: BROLL_DOCS_OK

- [ ] G6: origin/main of both repos carries the broll .mcp.json entry
  CHECK: python3 tools/broll/verify.py merged
  EXPECT: BROLL_MERGED_OK

- [x] G7: live Google Doc "Ralph standing rules (live)" refreshed with the b-roll line
  EVIDENCE: 2026-10-24 new doc 1L6FmtzrETiSC5eIWtqiZh7m6XkGUCI-Gk3f9u8FMqrs read back with the "B-roll (2026-10-24" line; old 1O9r0jaU... trashed; LIVE_DOC.txt updated

- [x] G8: free-assets skill points to broll-mcp (claude-skills repo, deployed via skill-smith), zip ready for Ralph
  EVIDENCE: 2026-10-24 claude-skills main 7f6128f; audit.py 0 errors 0 warnings; deployed to both repos; dist/free-assets-skill.zip (6,086 bytes) sent to Ralph

Run 2026-10-24 (commands run by hand; unlazy CHECK approvals need Ralph's say): G1-G6 printed their success tokens (search 87 matches; cut 4.004 s, commercial_use allowed, 640x480 B&W).
