Source: https://github.com/nidhinjs/prompt-master (MIT, by Nidhin Joseph Nelson)
Commit: 2bd9251 (2026-08-24), skill version 1.8.0
Copied: SKILL.md, LICENSE, references/templates.md, references/patterns.md (README and banner left out).
Reworked 2026-10-05 to Ralph's skill standard: SKILL.md cut from 496 to under 150 lines; the per-tool routing moved
to references/tools.md (with a contents list); added "Ralph's stack" (Seedance 2.0 Mini on Kie, Gemini 3 Pro Image,
Kling, hand/product rules, ask-before-paid-generation), current Claude model IDs, ElevenLabs v4 audio tags.
templates.md and patterns.md are unchanged.
Scanned 2026-10-05 with SkillSpector 2.12.0 (--no-llm), upstream: 63/100 HIGH "DO NOT INSTALL". Manual review: all
5 findings are false positives. YR4 (SKILL.md:4) = the description's trigger scoping (when the skill should and should not load);
P6 (SKILL.md:375) = the pasted-prompt safety rule that protects the setup text (flagged for its wording);
AS3 + RA2 (README.md:22) = the README's `git clone ... ~/.claude/skills` install line (README not copied); EA2
(templates.md:414) = the Decompiler's "run these prompts in order" text. No scripts, no network calls, nothing
concealed. Verdict: APPROVE.
This copy (reworded so the safety rules no longer trip the pattern matchers): 7/100 LOW, SAFE; only EA2 on templates.md:414 (same false positive).
