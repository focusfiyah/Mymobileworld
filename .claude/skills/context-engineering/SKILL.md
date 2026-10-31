---
name: context-engineering
description: "Context engineering guides (Agent Skills for Context Engineering, MIT): how to keep an agent's context small and sharp, compress long sessions into handoffs, spot context rot (lost in the middle, poisoning, distraction), offload work to files, isolate work in subagents, design memory, tool descriptions, evaluation and long-running agent prompts. Use when Ralph says context engineering, tokens, usage limits, context window, compact, handoff, session getting long, CLAUDE.md or skills too big, subagent brief, multi-agent, memory system, or when designing or debugging any agent, routine or prompt that runs for a long time. For writing Ralph's own skills use skill-smith; for paid image or video prompts use prompt-master."
---

# Context engineering

Eighteen upstream guides on what goes into a model's context and how to keep it worth its tokens. Each guide sits
unchanged in its own folder as `<name>/GUIDE.md` with its `references/` and example `scripts/`; this file only
routes. Read the one guide the task needs, then its references only if the guide points there.

What it is for, honestly: the guides are design knowledge. They do not lower Claude's usage by being installed (an
installed skill costs its description on every session); the saving comes from applying them: shorter rule files,
work pushed into subagents and files, tighter handoffs, fewer re-reads. The Short that suggested it
(source: `SOURCE.md`) oversells this.

## Pick the guide

| The task | Read |
|---|---|
| A session is getting long, needs a compaction or handoff summary | `context-compression/GUIDE.md` |
| Cut tokens: budgets, masking long tool output, cache-friendly prompts, splitting work | `context-optimization/GUIDE.md` |
| Output got worse as the session grew (forgot rules, mixed up jobs) | `context-degradation/GUIDE.md` |
| What context is and why placement matters (start here if new to it) | `context-fundamentals/GUIDE.md` |
| Scratch files, offloading tool output, handoff files between agents | `filesystem-context/GUIDE.md` |
| Memory across sessions (our Obsidian brain, job READMEs) | `memory-systems/GUIDE.md` |
| The model edits its own live context | `self-managed-context/GUIDE.md` |
| Subagents, supervisor vs swarm, when to split at all | `multi-agent-patterns/GUIDE.md` |
| Sharing context between orchestrator and workers (KV level) | `latent-briefing/GUIDE.md` |
| Launch prompt for a long autonomous run or parallel fan-out | `long-horizon-prompting/GUIDE.md` |
| Tool or MCP descriptions, schemas, response formats | `tool-design/GUIDE.md` |
| Checks, regression suites, quality gates for agent output | `evaluation/GUIDE.md` |
| LLM-as-judge, pairwise comparison, rubric calibration | `advanced-evaluation/GUIDE.md` |
| Research loops, locked vs editable surfaces, rollback | `harness-engineering/GUIDE.md` |
| Loops that improve the harness or prompt itself | `self-improvement-loops/GUIDE.md` |
| Background agents in sandboxes, warm pools, snapshots | `hosted-agents/GUIDE.md` |
| Is an LLM the right tool; shape of a batch pipeline | `project-development/GUIDE.md` |
| Belief/desire/intention models of agents (research niche) | `bdi-mental-states/GUIDE.md` |

The guides name each other in backticks (`context-compression` and so on); that name is the folder here.

## Where it fits Ralph's setup

- Long sessions: Ralph compacts when the context-watch hook asks (rule in Mymobileworld CLAUDE.md "Context watch").
  Use `context-compression` for what the summary must keep: files touched, decisions with his quotes, costs, next step.
- Rule files and skills: when a CLAUDE.md, playbook or skill grows, `context-optimization` and `context-degradation`
  explain what to move out; skill-smith owns how Ralph's skills are written.
- Subagent briefs and routines: `multi-agent-patterns` and `long-horizon-prompting` before a fan-out or a scheduled
  routine prompt; unlazy still owns the gates.
- Example scripts are teaching code (sandbox manager, compaction, memory store); read them, do not run them against
  Ralph's repos or accounts.

Done when: the guide's advice was applied to the real file, prompt or session it was read for, and the change is
measured where it can be (lines or tokens before and after, the check that proves nothing was lost).
