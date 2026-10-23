# Source

- Upstream: https://github.com/morluto/rea, folder `.agents/skills/reverse-engineer-anything`, tag `rea-agents-6.7.0`
  (commit 27dc42d, 2026-10-18), matching npm `rea-agents` 6.7.0. MIT (LICENSE). Main was ahead (skill v45); the release
  copy (v42) was taken so the instructions match the pinned package.
- Changes (Ralph's skill standard): SKILL.md cut from 355 to under 120 lines; "Route the target first" moved unchanged to
  `references/target-routing.md`, "Work summary-first" + "Plan broader investigations" to `references/investigation.md`;
  contents lists added to references over 100 lines; the unpinned upstream npx calls pinned to `@6.7.0`; GitHub doc links pinned to
  the release tag; description rewritten with trigger words and neighbour skills; a note that the MCP server is not
  registered in Ralph's sessions.
- SkillSpector --no-llm (2026-10-23, main copy): 54/100 HIGH, max issue MEDIUM. RP1 unpinned `npx -y rea-agents` (real,
  fixed by pinning); RA2 "plist" (Apple file format, not persistence); MP2/P9 Markdown table padding; EA2 "no approval"
  (a read-only DMG mount needs no flag). Manual review: instructions only, no scripts, no hidden text; setup and config
  changes already require a dry-run plan and user approval. Verdict CAUTION: the skill is clean; the risk sits in the
  `rea-agents` npm package it launches, which was not reviewed or run.
- To update: re-copy upstream `references/` from the new release tag, redo the two moved files, bump the pin.
