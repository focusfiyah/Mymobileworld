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

- [ ] G7: live Google Doc "Ralph standing rules (live)" refreshed with the b-roll line
  EVIDENCE: pending

- [ ] G8: free-assets skill points to broll-mcp (claude-skills repo, deployed via skill-smith), zip ready for Ralph
  EVIDENCE: pending
