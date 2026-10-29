# Changelog

- 2026-10-29: Added from Scenario's "Kinetic Film" zip (Ralph: "acquire this skill to improve our motion graphics", X post by @emmanuel_2m). Renamed `kinetic-film`; SKILL.md reworked to the skill standard with a free-first route (Scenario MCP paid steps only on Ralph's OK); worked example moved to `references/worked-example.md`; added `scripts/synth_kit.py` (free numpy sound kit) and the `MAXS` review-render switch in `scripts/post.py` (full blur took ~2.9 s per frame on the 4-core cloud box). Rest of the upstream unchanged.
- 2026-10-29: Free only (Ralph: "No paid anything on this just use the free resources we already have"): Scenario MCP removed from the route; its references kept as the upstream's record.
- 2026-10-29: examples/starter/spec.js fixed: as shipped it failed finish.py (0.62 s hold at beat 6, 44% still frames); first word at frame 0, a beat cut at 6.5 with a zoom exit, Strike items 2.5 beats apart (test: hold gone, still frames 42%).
