---
name: banana
description: "Banana Claude (AgriciDaniel, MIT): plans, generates, edits and reviews images with Google's Nano Banana models (Nano Banana 2.1, 3.1 Flash Lite Image, 3 Pro Image) straight through the Gemini API, with a frozen brief, an exact cost plan and approval before every paid call, exact-text layers (typeset), presets, a cost ledger and pixel review. Use only when Ralph calls for it: \"banana\", \"Banana Claude\", \"/banana\", or a Nano Banana image outside the client ad routes (posters, infographics, covers, diagrams, Day One AI or personal images). Grace and client product stills stay on ugc-product-ad (Kie); thumbnails start in thumbnail-looks; write the prompt with prompt-master."
---

# Banana Claude

Upstream image skill, kept whole: `GUIDE.md` is its own SKILL.md (brief, prompt, route, plan, approve, execute,
review), `references/` holds its model catalog, prompt craft, costs and recovery, `scripts/` its Gemini client.
Read `GUIDE.md` before the first call; it routes to the references it needs. `$CLAUDE_SKILL_DIR` in it means this
folder. `agents/visual-critic.md` and `agents/visual-architect.md` are its read-only review and planning briefs:
hand them to a subagent when the image matters.

## Ralph's setup

- **Every call costs money, so the cost gate applies:** show the planner's exact cost and the month so far
  (Mymobileworld `python3 grace/spend.py`) and get Ralph's yes for that call before running it; a retry is a new
  yes. Log what Google billed in `grace/spend.json` "other" (rule: Mymobileworld CLAUDE.md "Monthly budget").
- **Which jobs:** Nano Banana runs only when a route or Ralph calls for it (prompt-master). Grace and client product
  stills keep the ugc-product-ad route on Kie with its gate.py lock and product truth; this skill has neither.
  Use Banana for images outside that route. A product in frame still comes from its real photos (`edit.py` with
  the real photo as an object reference), never invented.
- **Prices (Banana's catalog, checked by its author 2026-10-20; re-check `references/models.json`):** 1K image
  Nano Banana 2.1 $0.034, 3.1 Flash Lite $0.034, 3 Pro Image $0.134 (Kie nano-banana-pro is $0.09). Batch is
  half price but slow. Start at 1K.
- **Key:** standalone scripts read `GEMINI_API_KEY`, which the cloud environment sets; never print or pass it.
- **Where files go:** images to `~/Documents/banana-claude/` unless `BANANA_OUTPUT_DIR` is set (set it to the job
  folder); approvals, presets and the cost ledger in `~/.banana/`. Job media then goes to Drive per the media rule,
  never git.
- **Prompts:** load prompt-master and write the prompt with it, then let Banana compile the brief; run the
  prompt double-check before the paid call (Mymobileworld CLAUDE.md "Double-check every prompt").
- **Free checks:** `python3 scripts/doctor.py` (setup, no Google call; its installation_layout, plugin_manifest and
  bundled_mcp_config lines fail by design in this repo copy, the catalog, key and output lines are the ones that count), `scripts/cost_tracker.py summary`,
  `scripts/presets.py list`, and every plan step run without executing.

Done when: the image passed Banana's own pixel review plus Ralph's QC (2x zoom on edges, real product unchanged,
REMOVED.md), its cost is logged, and the file is where the job keeps media.
