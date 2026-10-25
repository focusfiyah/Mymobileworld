# Open-Higgsfield-AI review (Ralph 2026-10-24: "Read and install ... should help with our image and video production")

Status: done 2026-10-24, $0. Ralph picked A: take the useful parts into our toolkit, don't run the app.
The updated ugc-product-ad skill zip was uploaded to claude.ai by Ralph 2026-10-24.

## What the repo is
github.com/Autom8AI/Open-Higgsfield-AI @ 3c47454: a 2026-10-18 fork (by "Matas", rebranded MATAI) of
Anil-matcha/Open-Higgsfield-AI (MIT per its README; no LICENSE file in the fork). A browser studio (image, video,
lip sync, "cinema" camera presets) whose backend the fork switched from muapi.ai to Kie, plus a Netlify backend for the
fork author's own business (login, Airtable via Composio, Resend email, fal). It builds (`npm ci` + `vite build`, 21 s).

## Why not the app (told to Ralph 2026-10-24)
- It spends Kie money outside grace/gate.py: no Production Book, budget lock or paid-task ledger.
- Dev mode proxies `/.netlify/functions` and `/download-media` to the fork author's site higgsfield-matu.netlify.app.
- "Cinema Studio" only appends words such as "8K digital cinema camera, f/1.4" to the prompt: the polished look we avoid in UGC.
- No Seedance 2.0 Mini, no Gemini Omni; Ralph works from his phone (no PC).

## What we took
1. Kie talking-avatar models (portrait + audio, no clip first), fields from docs.kie.ai and prices from kie.ai/pricing:
   ugc-product-ad `references/lipsync-options.md` (source focusfiyah/claude-skills). Untested on a job.
2. Input-field check: `grace/kie_fields.py` + `grace/kie_fields.json` (15 models, built from docs.kie.ai);
   `grace/gate.py start_task()` refuses a field the model's doc does not list. Audit of every logged request: 0 unknown fields.
3. Prices for the 6 avatar models in `grace/spend.py`.
