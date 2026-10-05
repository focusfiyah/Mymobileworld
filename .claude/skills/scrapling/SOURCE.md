# Source

- Upstream: https://github.com/D4Vinci/Scrapling, folder `agent-skill/Scrapling-Skill`, commit 54e9510 (2026-10-03), library v0.4.15. BSD-3-Clause (LICENSE.txt).
- Changes (Ralph's skill standard, 2026-10-05): SKILL.md cut from 415 to under 100 lines; its CLI and code sections moved
  unchanged to `references/cli.md` and `references/code-overview.md`; a contents line added to references over 100 lines;
  `scripts/setup.sh` added (venv + browsers + cloud proxy CA fix); name `scrapling-official` -> `scrapling`.
- SkillSpector --no-llm (2026-10-05): see the commit message / CLAUDE.md for the score and verdict.
- To update: re-copy upstream `references/` and `examples/`, then redo the two moved files.
