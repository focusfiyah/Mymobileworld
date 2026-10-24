# Gates: camofox-browser first, Playwright MCP as backup (Ralph 2026-10-24)

OWNS: tools/camofox/**, .claude/hooks/camofox_setup.sh, .mcp.json, .claude/settings.json, CLAUDE.md, handoff/**

Scope: camofox-browser installs itself in every cloud session, is the first browser tool in both repos with the Playwright MCP kept as backup, telemetry off, Python Playwright kept for the scripts that import it, rules and memory saved, merged to main.

- [ ] G1: the setup hook installs camofox + Camoufox from a clean state and the server answers
  CHECK: python3 tools/camofox/verify.py health
  EXPECT: CAMOFOX_HEALTH_OK

- [ ] G2: a real HTTPS page loads through the session proxy and snapshots
  CHECK: python3 tools/camofox/verify.py browse
  EXPECT: CAMOFOX_BROWSE_OK

- [ ] G3: the MCP command in .mcp.json lists the camofox tools and opens a tab
  CHECK: python3 tools/camofox/verify.py mcp
  EXPECT: CAMOFOX_MCP_OK

- [ ] G4: both repos register camofox-browser AND the playwright MCP (Ralph: "Both"), telemetry off, both hooks run, hook copies identical
  CHECK: python3 tools/camofox/verify.py config
  EXPECT: CAMOFOX_CONFIG_OK

- [ ] G5: CLAUDE.md + the four handoff memory files carry the camofox-first, Playwright-backup rule in both repos, MEMORY_SHORT <= 2,000 chars
  CHECK: python3 tools/camofox/verify.py docs
  EXPECT: CAMOFOX_DOCS_OK

- [ ] G6: origin/main of both repos carries the hook and the new .mcp.json
  CHECK: python3 tools/camofox/verify.py merged
  EXPECT: CAMOFOX_MERGED_OK

- [x] G7: live Google Doc "Ralph standing rules (live)" refreshed (handoff/live_rules.py ran without error)
  EVIDENCE: 2026-10-24 new doc 1O9r0jaUCsstyiWaeWfBrzZQbusUPUqALV50d10H1qj0 read back with the Browser (2026-10-24) line; old 154uyZqp... trashed; LIVE_DOC.txt updated

- [x] G8: honest comparison vs Playwright reported (same pages, both browsers, this session)
  EVIDENCE: 2026-10-24 example.com + nowsecure.nl OK on both; google.com/search blocked on both (camofox 'unusual traffic', Playwright 429 /sorry); tiktok.com/@houseoframeau 0 video links + 'Something went wrong' on both; bot.sannysoft.com webdriver passed on camofox

Run 2026-10-24 (commands run by hand; unlazy CHECK approvals need Ralph's say): G1-G6 printed their success tokens, see final report.
