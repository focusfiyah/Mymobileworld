---
name: ugc-product-ad
description: Produce short creator-style UGC product ads (TikTok Shop / Meta). Covers (1) a talking-to-camera spokesperson spot from a person's photo plus a product packshot; (2) multi-character dialogue skit ads (couple or family "POV" skits with a product handoff) from Gemini 3 Pro stills and Seedance 2.0 Mini on Kie; (3) longer multi-shot ads from ONE recurring persona (an AI influencer), one Grok Imagine clip per shot on Kie, optionally lip-synced to a cloned ElevenLabs voice; (4) patching a mumbled off-camera line by cloning the clip's own voice; and (5) demo/tips ads over a voiceover, hands-only or with the person on camera (Kie stills + Seedance Mini per shot, lip sync on face shots). Use for any "make a UGC ad", "creator video", "TikTok Shop ad", "spokesperson spot", "skit", "tech UGC", "AI influencer", "use my voice", "remove the pauses", "hands-only" request, and for Fungix / Grace / Carpe / Restlex / Ralph / Seller AI OS ad work. Encodes models, prompts, timing, cost control, QC and compliance.
---

# UGC Product Ad

Repeatable recipes for creator-style product ads. Follow them and a job takes a
handful of tool calls. Working it out from scratch takes fifty calls and produces
worse output, which is why this file exists.

- **Any shot that shows the product (every route below):** "Product lock" (references/product-lock.md) (Google
  Gemini Omni clips from the real-photo references; paste-back only as a last resort). Ralph, 2026-10-21.
- **Single spokesperson, 10s, talking to camera:** "The recipe" (references/spokesperson-recipe-and-tools.md) (Gemini Omni).
- **Recreate a trending spokesperson video (up to 15s, product close-ups):** "Recreate a trending
  spokesperson video" (Gemini 3 Pro stills + one Seedance Mini clip). Approved by Ralph on 2026-09-14.
- **Multi-character skit with dialogue and a product handoff:** "Multi-character
  skit ads" (Seedance Mini on Kie). Approved by Ralph on 2026-09-14.
- **One line mumbled or reworded after the render, speaker off camera:** "Patch a spoken line
  (audio only)" (ElevenLabs clone of the clip's voice + splice). Approved by Ralph on 2026-09-15.
- **Multi-shot ad from ONE persona, 25-35s, on-camera dialogue in every shot:** "Per-shot ads with
  a recurring persona" (Grok Imagine per shot, optional Kie lip sync to a cloned voice).
  Approved by Ralph on 2026-09-16. Cheapest route here by far: a 30s ad costs about **$3**.
- **Couple skit with one speaker OFF camera (a "caught you" POV, a partner reacting):** "Multi-character
  skit ads" (references/skit-ads.md), but read **"Fix a line after the render"** first — an off-camera speaker means every one
  of her lines can be rewritten later for free. Proven on the Fungix "CAUGHT YOU" skit, 2026-09-19.
- **Editing a creator's REAL raw takes (hook / body / CTA files) into many combo ads:** not this
  skill, use the **`ugc-take-combos`** skill (no generation; audio-snapped cuts, reference-style
  overlays, previews before render). Approved on the Fungix / Grace job, 2026-09-18.
- **Faceless hands-only product demo / tips video over a voiceover (no face, no lip sync):**
  "Hands-only product ad" (references/hands-only-and-demo.md) (Kie Nano Banana Pro stills + one Seedance Mini clip per shot, free ffmpeg cut).
  Proven on Grace's Carpe Vanilla Peach ad, 2026-10-01 (36s, 9 shots, $3.52 actual vs $2.53 planned).
- **A real person (AI from their photo) demonstrating the product over a voiceover, face on some shots:**
  "On-camera demo over a voiceover" (references/hands-only-and-demo.md) (Kie stills + Seedance Mini per shot, lip sync on face shots, free
  edit-list cut). Carpe Mountain Breeze for Grace, 2026-10-01: 35s, $6.60 vs a $2.50 quote; read its lessons.


## Step 0, every job, unasked: the script gate (Ralph 2026-10-03)
Before any plan goes to Ralph or any paid call, run the whole `grace/PLAYBOOK.md` §4 checklist (audience research
first) and save its proof files with `python3 grace/gate.py <job> --init`; every paid runner refuses until the gate
passes, and it is never bypassed or weakened. Show the gate result in the plan message. Close with "It's in the
orange cart."; never "order it now", "heads up" or dashes. (source: grace/PLAYBOOK.md §4, the one home for the list)


## Working with Ralph (read first, every job)

The general rules have one home, Mymobileworld `CLAUDE.md` ("How Ralph wants to work" and "Hard rules for every
ad"): exact cost before every paid call including redos, one short question instead of a guess, free fixes first,
the whole plan and total cost in ONE message, one test clip before any batch, the running total vs the quote at
every paid step, an email AND a phone push (PushNotification is deferred: ToolSearch `select:PushNotification` first; skipped while he has the app open, so the email is the backup) at every review point, the Drive folder layout, no on-screen text unless he says yes for
that ad, premium overlays, unlazy, and a current `Status:` line in the job README. Follow them from there. The
lessons below are specific to making ads:

- **Product reference sheet first (Ralph 2026-10-19):** before any product still, build a free sheet (real front label big +
  side/top/bottom shape views) and pass it on every product still. Also the maker's real dimensions with an everyday size
  anchor + a real in-room photo for scale, and every product detail confirmed by Ralph in the plan before spend; a quote
  includes one likely redo (Shnuggle 2026-10-19: AI tub too big, an invented dot pattern). Details: `grace/PLAYBOOK.md` §6.
- **Product lock on every product (Ralph 2026-10-21):** product stills from Gemini 3 Pro Image + the reference sheet +
  a close-up of each real logo, used clean; every clip with the product in frame on **Google Gemini Omni 1.1 Flash on Kie**
  (`scripts/omni_clip.py`, 4 s $0.315; never through the Gemini API key, Ralph 2026-10-22); Seedance 2.0 Mini only for clips without the product; no
  Kling unless Ralph asks. A drifted take gets one Omni edit turn before any new take. **Pasting a real label is the last
  resort** (it reads as a sticker), only with Ralph's OK for that shot. Route, prompt template, costs:
  `references/product-lock.md`. Why: October's redos (Vans tab and gift-shot shoe, Cleanwaste boxes) cost more than
  the first takes.
- **Every still, edit and clip prompt is written with the `prompt-master` skill** (its "Ralph's stack"), every
  reference named by its tag and the print matched letter for letter (Ralph 2026-10-21: it locks the models to what we
  want). Paste the final prompt into the plan so Ralph sees it before spend.
- **Budget (Ralph 2026-10-21: "blowing through my budget"):** every plan and every redo question shows
  `python3 grace/spend.py` (month so far vs his cap: none in October 2026, $100/month from November) next to the job's quote. At the cap, `grace/gate.py` refuses every
  paid runner until Ralph's OK is recorded in `grace/spend.json` over_cap_ok. Spend nothing on a redo Ralph did not ask
  for; offer to let a small flaw go (Vans gift shot) before quoting a fix.
- **Confirm the real product before the first paid still:** applicator/top, cap, label, size; ask for a real photo
  if the reference is a generated sheet. Why: the Carpe sheet showed a ribbed white dome, the real stick has an
  orange slotted top, 5 stills redone (~$0.54).
- **Confirm the person's details** (nail length, jewellery, skin); the reference pixels win over the prompt. Why:
  long nails in the hand sheet came out long; "to clarify, shorten the nails" was misread and cost $0.18.
- **A pasted prompt that clashes with the video** (product-sheet style, grey background, "no hands"): say so and ask
  before spending. Why: run verbatim it gave a 3-panel sheet, usable only as a reference crop.
- **Ask who the ad is for** and apply that client's playbook (Grace: `grace/PLAYBOOK.md`).
- **Resuming from a handoff: re-check before paying.** Re-fetch the job branch, read its `kie_log.json` / clips
  folder for that step, and make sure the old session has stopped. Why: Vicks VapoShower (2026-10-01) rendered the
  same 6 clips in two sessions, $1.07 lost.
- **QC extras beyond CLAUDE.md hard rule 3:** nothing resting on thin air (a Vicks still put the box past the vanity
  edge; free fix = crop the frame to end at the object's base). Use `templates/qc-report.md`.
- **End shot shows ONE product; the voiceover still says to grab more than one.** Why: Ralph, 2026-10-14 (Throw Hands).
- **Grip check on every still before its clip is paid for:** zoom on each hand that touches an item; it must pinch
  or hold it (thumb on one side, fingers curled on the other). Fingertips resting on a card, a palm flat on a box,
  or an item lying loose next to the hand = redo the still first, never "fix it in the video prompt". Why: Throw
  Hands (2026-10-14) put no-grip stills S5/S7 into clips; Seedance and then Veo both dragged the card under her
  nails and melted the loose one, $0.30+ wasted and a cut Ralph rejected. The video model copies the still's grip.
- **When Ralph says yes to on-screen text:** TikTok "Classic" style (white semibold, no bubble, soft shadow,
  lowercase, two balanced lines past five words, no "orange cart" line) via `scripts/classic_caption.py`.
- **When an overlay is asked for:** Microsoft Fluent 3D emoji (MIT,
  `cdn.jsdelivr.net/gh/microsoft/fluentui-emoji@main/assets/<Name>/3D/<name>_3d.png`, 256px) or sharp photos, never
  past ~1.2x source; with no free match, first offer a same-set stand-in, then a generated one with its cost.
  Overlays follow the spoken words. Example: `ugc/wag-bag-v2/`.


## Reference map (read the file for the route you are using; each has a table of contents)
Every route below is still governed by Step 0 (script gate) and "Working with Ralph" above.
- Single spokesperson 10s ("The recipe", prompt template, say-ability, verify, compliance, cost table, tool list):
  `references/spokesperson-recipe-and-tools.md`
- Trending spokesperson recreate (up to 15s): `references/recreate-spokesperson.md`
- Multi-character skits, patching a spoken line, fix a line after render, skit traps and costs: `references/skit-ads.md`
- One recurring persona, per-shot Grok clips, trim dead air, animated CTA, lip sync, Kie stills and prices:
  `references/persona-per-shot.md`
- Hands-only ad, on-camera demo over a voiceover, GTT KN95 lessons: `references/hands-only-and-demo.md`
- Lip sync: default ElevenLabs voice + Kie sync; Fal.ai `minimax/h3-max/lip-sync/image-to-video` only as the fallback when Ralph doesn't like the result: `references/lipsync-options.md`
- Product lock (every product shot: Omni clips, edit turns, budget line): `references/product-lock.md`
- Exact-product route (real photo + paste-back, complex products; last resort since 2026-10-21): `references/exact-product.md`
- Templates (fill, don't improvise): `templates/plan-message.md` (the one plan message), `templates/readme-status.md` (job README + Status line), `templates/qc-report.md` (QC before any send).
- Scripts live in `scripts/` (gate.py, kie runners, cut/finish/qc tools); templates in the job folders named in CLAUDE.md.

## Final finish (Ralph 2026-10-07)
Last step on every AI video: `scripts/ai_finish.sh IN OUT` (20% grain, 20% sharpness, saturation down a little; keeps TikTok from tagging it as AI, per @ericdoesecom, unverified). Details: `grace/PLAYBOOK.md` §6.
