# Source

One skill built on 2026-10-28 from four free upstreams (Ralph: "4 skills that should combine to one so it's used
together"; "We are only doing the free. No paid"). Each upstream sits unchanged in its own folder except where
noted, so it can be re-copied on update.

| Folder | Upstream | Commit | Licence |
| --- | --- | --- | --- |
| `impeccable/` | github.com/pbakaus/impeccable, `.claude/skills/impeccable/` (skill v4.8.0, engine 0.1.18) | d34c87e | Apache-2.0 (`licenses/impeccable-*`) |
| `polish/` | github.com/jakubkrehel/make-interfaces-feel-better, `skills/make-interfaces-feel-better/` | 35545ea | MIT |
| `transitions/` | github.com/Jakubantalik/transitions.dev, `skills/transitions-dev/` + `skills/transitions-polish/SKILL.md` | 6a7d682 | Transitions.dev licence: free set free for personal and commercial use, no redistribution of the library as a product (`licenses/transitions.dev-LICENSE.txt`) |
| `gsap/` | github.com/greensock/gsap-skills, `skills/gsap-*/SKILL.md` (GreenSock's official skills) | aed9cfd | MIT |

## Changes

- Every upstream `SKILL.md` renamed `GUIDE.md` (one SKILL.md per skill); GSAP's eight skills became
  `gsap/<name>.md` and their "Related skills" names became links to those files.
- Impeccable: `.claude/skills/impeccable/` paths rewritten to `.claude/skills/web-design-stack/impeccable/`;
  "SKILL.md's" mentions in its references now point at GUIDE.md. Its LICENSE and NOTICE kept in `licenses/`.
- Transitions.dev: `transitions-polish/SKILL.md` became `transitions/tokens.md` with its Refine-panel section and
  mentions cut (the Refine relay and the Motion Agent belong to the paid plans); `transitions-ui-generation`
  (fake "agent is generating" wireframe effect) and the Pro CLI login were not taken.
- Make Interfaces Feel Better: `agents/openai.yaml` (Codex metadata) not taken.
- Added: `SKILL.md` (pipeline, motion budget, free-only rules), `scripts/motion_check.py`, this file, `CHANGELOG.md`.

## Security review (SkillSpector --no-llm, 2026-10-28, scans in the session scratchpad)

- **Impeccable: 100/100 CRITICAL** from count, no single CRITICAL finding. HIGH: AE1 (long files not fully parsed),
  AR2 (doc phrases "without warning", "Ask only when"), AS1 (hooks.md documents where its optional design hook goes
  in `.claude/settings*.json`; installs only on `/impeccable hooks on`), MP3 (same hook docs). MEDIUM: SSRF2 and E1 =
  `live-browser.js` talking to its own `localhost` server (checked: every URL in it is localhost or w3.org), EA2
  (decision wording), RP1 (`npx impeccable`, not used here). Network use, read in the launcher and docs: the engine
  binary downloads once from github.com/pbakaus/impeccable/releases and is checked against
  `scripts/engine-checksums.txt` (sha256); a free roll API at impeccable.style deals visual-world options; an
  anonymous "which card won" ping is sent unless `IMPECCABLE_NO_TELEMETRY=1` or `DO_NOT_TRACK=1` (set in both repos'
  `.claude/settings.json`). Verdict CAUTION, installed.
- **Make Interfaces Feel Better: 0/100 LOW.** APPROVE.
- **Transitions.dev transitions-dev: 75/100 HIGH.** P6 "prompt extraction" = CSS comments about the tooltip's "show
  rule"; AE1 = long reference tables. False positives. transitions-polish 0/100 LOW. APPROVE.
- **GSAP skills: 30/100 MEDIUM.** PE3 "credential access" = the lines telling the agent NOT to create a GreenSock
  `.npmrc` auth token (GSAP is free). False positive. APPROVE.
- Engine run tested 2026-10-28: `impeccable/scripts/impeccable context` downloaded engine 0.1.18 and exited 0.

## Update

Re-clone each upstream, re-copy its folder over the matching one here, redo the Changes above (rename, path
rewrite, Refine cut), re-scan with skill-inspector, run `scripts/motion_check.py` on a test page, then deploy.
