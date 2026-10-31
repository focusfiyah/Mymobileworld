# Source

Ralph 2026-10-31: "Watch this and get that last 2 skills mentioned" about Taki Wong's Short "Top 5 Claude Skills to
100x Your Claude Outputs" (youtube.com/shorts/SIVI3elT22Q, 2026-06-13). Skill five of five: "Context Engineering,
and this allows Claude to reduce the number of tokens that it uses". The Short names no repo; the match is
github.com/muratcankoylan/Agent-Skills-for-Context-Engineering (Muratcan Koylan, MIT, the Claude Code plugin
"context engineering" collection). The Short's token claim is oversold: the guides teach how, they save nothing
by being installed.

| Folder | Upstream | Commit | Licence |
| --- | --- | --- | --- |
| 18 folders `<name>/` | `skills/<name>/` with `SKILL.md` renamed `GUIDE.md`, references and scripts unchanged | 9ff0c99 (2026-10-11) | MIT (`licenses/context-engineering-LICENSE`) |

Why one skill, not 18: each installed skill puts its description into every session; 18 near-neighbour
descriptions would cost context in every session, the opposite of the point, and would fight over triggers.
Not taken: the repo's root collection SKILL.md (replaced by our router), `examples/`, `researcher/`,
`governance/`, release assets, the plugin marketplace file.

## Security review (SkillSpector --no-llm, 2026-10-31, one scan per guide)

- SAFE (0-15): advanced-evaluation, context-compression, context-degradation, context-fundamentals, evaluation,
  latent-briefing, memory-systems, project-development, self-managed-context, tool-design.
- CAUTION by score (27-46): bdi-mental-states 46, long-horizon-prompting 41, self-improvement-loops 39,
  multi-agent-patterns 35, hosted-agents 33, context-optimization 32, harness-engineering 27.
- DO_NOT_INSTALL by score: filesystem-context 69.
- Every HIGH read in place, all false positives: "memory manipulation" = the guides teach memory and state
  design; "self-modification" = self-improvement-loops describes that research topic; "omit warnings" = a line
  asking for a typed output contract; "parameter abuse" = `subprocess.run` in a documentation snippet and
  `git reset --hard origin/main` inside the hosted-agents sandbox example class; "exposes system prompts" = a
  function returning a rules list; "not completely inspected" = long files.
- Source read: no network, no environment reads, no writes outside the caller's own example paths; scripts are
  teaching code nobody runs automatically.
- Verdict: **CAUTION** (documentation set; do not run the example scripts against real repos or accounts).
