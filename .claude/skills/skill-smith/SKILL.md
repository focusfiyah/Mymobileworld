---
name: skill-smith
description: Writes new skills, fixes existing ones, and audits Ralph's whole skill library for what is out of date, what contradicts itself or another skill, and what is no longer needed. Use whenever a skill is created, updated, renamed, merged, split, deleted, re-zipped or uploaded; whenever a SKILL.md or a skill's reference file or script is edited; when a standing rule changes that a skill repeats; and when Ralph asks to review, clean up, audit or check his skills. The source of truth is the private repo focusfiyah/claude-skills. For a safety scan of a third-party skill use skill-inspector, to find new skills to install use find-skills, and to benchmark a skill with evals use skill-creator.
---

# Skill smith

A skill is a set of instructions a future session follows with Ralph not in the room. When it is stale, it sends
that session down a route he already abandoned; when it repeats another skill, the two drift apart and one of them
becomes wrong; every extra line competes for the context window with the job itself. Your job is to keep each
skill short, correct and the only home for what it says.

Read `references/rules.md` before writing or changing any skill. It holds the writing rules, each with the reason
it exists. Do not copy those rules into other skills or files; link to them.

## Where skills live

- **Source:** `skills/<name>/` in focusfiyah/claude-skills. Every change starts there and is committed there; git
  history is the version history. If the repo is not in the session, attach it (`add_repo`) before editing.
- **Deployments:** the copies in focusfiyah/Mymobileworld and focusfiyah/Dayone-ai (`.claude/skills/`) and the
  claude.ai account upload. `deploy.json` at the repo root says which skill goes where.
  `python3 <skill-dir>/scripts/deploy.py <name>` copies the source to the repo deployments and builds `dist/<name>-skill.zip`
  for Ralph to upload. A deployment is never edited by hand; if one was, bring the change back to the source first.
- Anthropic's built-in skills (docx, pdf, pptx, xlsx, skill-creator, docs, morning, browser and computer-use
  skills) are not Ralph's and are not stored or edited here.

## Write a new skill

Start from what keeps going wrong or what Ralph keeps re-explaining: a skill earns its place by saving a real,
repeated cost. Check `skills/` first; extending an existing skill beats adding a near-duplicate. Gather the facts
from where they already live (job READMEs, playbooks, CLAUDE.md files, the tool's own docs) and decide, fact by
fact, whether the skill owns it or links to its owner. Copy `templates/SKILL.template.md` and fill it in.

Done when: the description says what the skill does and when to use it, in the words Ralph actually uses; the body
gives the goal, the context and what done looks like; every hard rule has a why; `python3 <skill-dir>/scripts/audit.py
skills/<name>` reports no errors; a run of the skill on one real task from Ralph's history needed no correction
that the skill should have prevented; skill-inspector has scanned anything taken from outside; it is committed,
deployed and the zip is with Ralph.

## Fix an existing skill

Find the source of the problem before editing text: a wrong fact, a rule that lost its reason, a missing trigger
word in the description, or a contradiction with a newer rule somewhere else. Fix it in its one home. When the fix
changes a fact that other skills link to, those links still work; when other skills copied the fact instead of
linking, replace the copies with links. Add one line to the skill's `CHANGELOG.md` (date, what changed, why).

Done when: the problem is gone at its source, nothing else now contradicts it (`grep` the library for the old
wording), the audit script is clean for that skill, and the change is committed and deployed. Tell Ralph when the
claude.ai copy needs a re-upload; the account copy does not update itself.

## Audit the library

Read every skill against what is true today, not against itself. "True today" lives in the two repos' CLAUDE.md
files, `grace/PLAYBOOK.md`, the handoff memory files and the job READMEs; open them, including ones the request
did not name. Run `python3 <skill-dir>/scripts/audit.py skills --deploy` first for the mechanical findings (length, broken or
external links, dead-weight phrases, duplicated paragraphs, drift between source and deployments), then read each
skill for what a script cannot judge. `references/audit.md` defines the three findings and how to tell them apart.

Done when: every skill folder appears in the report under out of date, contradicts, not needed, or clean; each
finding names the file and line, the evidence and the proposed fix; small, certain fixes (a contradiction with a
dated rule from Ralph) are made and listed; anything that removes a skill or changes what it does waits for Ralph.
Save the report as `audits/YYYY-MM-DD.md` in the repo.

## When to ask Ralph

Ask before deleting or merging a skill, before changing what a skill does (as opposed to how it says it), before
any paid step a skill would trigger in testing, and before installing anything from outside. Ralph's own words
outrank everything here: a dated instruction from him in a CLAUDE.md or playbook wins over a skill's text, and the
fix is to update the skill.

## Files

`<skill-dir>` is the folder holding this SKILL.md; run the scripts from the claude-skills repo root.


- `references/rules.md`: the writing rules and their reasons. Read before any write or fix.
- `references/audit.md`: definitions, signals and the report template for an audit.
- `templates/SKILL.template.md`: the skeleton for a new skill.
- `scripts/audit.py`: mechanical checks over one skill or the whole library (`--help`).
- `scripts/deploy.py`: copies a skill to its deployments and builds its upload zip.
