# Source

- Upstream: https://github.com/gokapso/agent-skills, folder `skills/automate-whatsapp`, commit 415c1b4 (2026-10-09). Kapso's own skills, marked alpha
  (they change fast). The repo has no LICENSE file (checked 2026-10-23); Kapso publishes them for installing with
  `npx skills add gokapso/agent-skills`. Kept in Ralph's private repo only.
- Changes (Ralph's skill standard): description rewritten with trigger words and neighbour skills; a "Ralph's setup"
  section added; the generated FILEMAP block dropped (it goes stale); sections moved verbatim to references/ to bring SKILL.md under 200 lines (references/functions-and-sandbox-guide.md, references/project-events-guide.md, references/rules.md, references/scripts-and-assets.md). Scripts, assets and other references unchanged.
  The split is reproducible: `tools/split.py` + `tools/ralph.py` in claude-skills `audits/2026-10-23-kapso/`.
- Review 2026-10-23: SkillSpector --no-llm on upstream, then a manual read. Findings were API documentation, not
  behaviour: AE1 (file longer than the parser reads), TM1 (`DELETE` endpoints listed in docs), PE3/E1 (docs about
  tokens, API keys and example URLs), RA1 (the secret-output-file feature), SC1/SC4 (`yaml` ^2.6.0 dependency not
  pinned). Scripts call only the Kapso API (`KAPSO_API_BASE_URL`, default api.kapso.ai) and Meta's Graph API via
  Kapso; no child processes, no eval, no telemetry, no hidden Unicode; two HTML comments are plain TODOs. They reject
  redirects and plain HTTP and redact secrets in output. Verdict: CAUTION (clean skill; the risk is what an API key
  lets it do: send WhatsApp messages and change routing, so those wait for Ralph's OK).
- To update: pull the new upstream commit, rerun the two tools, rescan, diff against this copy.
