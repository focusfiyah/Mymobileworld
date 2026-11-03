---
name: ugc-product-ad
description: Produce short creator-style UGC product ads (TikTok Shop / Meta). Covers (1) a talking-to-camera spokesperson spot from a person's photo plus a product packshot; (2) multi-character dialogue skit ads (couple or family "POV" skits with a product handoff) from Gemini 3 Pro stills and Seedance 2.0 Mini on Kie; (3) longer multi-shot ads from ONE recurring persona (an AI influencer), one Grok Imagine clip per shot on Kie, optionally lip-synced to a cloned ElevenLabs voice; (4) patching a mumbled off-camera line by cloning the clip's own voice; and (5) demo/tips ads over a voiceover, hands-only or with the person on camera (Kie stills + Seedance Mini per shot, lip sync on face shots). Use for any "make a UGC ad", "creator video", "TikTok Shop ad", "spokesperson spot", "skit", "tech UGC", "AI influencer", "use my voice", "remove the pauses", "hands-only" request, and for Fungix / Grace / Carpe / Restlex / Ralph / Seller AI OS ad work. Encodes models, prompts, timing, cost control, QC and compliance.
---

# UGC Product Ad

Repeatable recipes for creator-style product ads. Follow them and a job takes a
handful of tool calls. Working it out from scratch takes fifty calls and produces
worse output, which is why this file exists.

**Pick the route, then read its reference file** (every route is also governed by Step 0 and "Working with Ralph" below):

| Ralph asks for | Route | Read |
|---|---|---|
| Any shot that shows the product (all routes) | Product lock: Flow takes first, then Wan 3.0 720P + free upscale, from the real-photo references; paste-back only as a last resort | `references/product-lock.md` |
| Single spokesperson, 10 s, talking to camera | "The recipe" (Gemini Omni) | `references/spokesperson-recipe-and-tools.md` |
| Recreate a trending spokesperson video (up to 15 s, product close-ups) | Gemini 3 Pro stills + one Seedance Mini clip | `references/recreate-spokesperson.md` |
| Multi-character skit with dialogue and a product handoff | Seedance Mini on Kie | `references/skit-ads.md` |
| Couple skit, one speaker OFF camera | Same file; read "Fix a line after the render" first (her lines can be rewritten for free) | `references/skit-ads.md` |
| One line mumbled or reworded after the render, speaker off camera | Patch a spoken line: ElevenLabs clone of the clip's voice + splice | `references/skit-ads.md` |
| Multi-shot ad, ONE recurring persona, 25-35 s, dialogue in every shot | Grok Imagine per shot, optional Kie lip sync to a cloned voice; about $3 for 30 s | `references/persona-per-shot.md` |
| Faceless hands-only demo or tips over a voiceover | Kie Nano Banana Pro stills + one Seedance Mini clip per shot, free ffmpeg cut | `references/hands-only-and-demo.md` |
| A real person (AI from their photo) demonstrating over a voiceover | Same stills + clips, lip sync on face shots; read its lessons (a 35 s ad ran $6.60 vs a $2.50 quote) | `references/hands-only-and-demo.md` |
| Lip sync choices | ElevenLabs + Kie sync by default; Fal.ai only as the fallback | `references/lipsync-options.md` |
| Complex product, real photo + paste-back | Last resort | `references/exact-product.md` |
| Editing a creator's REAL raw takes into combo ads | Not this skill: use `ugc-take-combos` | |

Which route was approved or proven on which job: `CHANGELOG.md`.


## Step 0, every job, unasked: the script gate (Ralph 2026-10-03)
Before any plan goes to Ralph or any paid call, run the whole `grace/PLAYBOOK.md` §4 checklist (audience research
first) and save its proof files with `python3 grace/gate.py <job> --init`; every paid runner refuses until the gate
passes, and it is never bypassed or weakened. Show the gate result in the plan message.
No paid call before Ralph's OK on the job's Production Book (`BOOK.md`, `templates/plan-message.md`), and spend never
passes its total plus the extras he OKs; runners save each paid task before submitting it, so no session pays twice
(`grace/gate.py` docstring, Ralph 2026-10-22). Close with "It's in the
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
  a close-up of each real logo, used clean; every clip with the product in frame first a free Flow take, else **Wan 3.0 on Kie at 720P + our free upscale**
  (`scripts/wan_clip.py`, 5 s $0.40; Ralph 2026-11-03, replaces Kie Omni, which stays for edit turns via `scripts/omni_clip.py`); Seedance 2.0 Mini only for clips without the product;
  Kling only for a shot that is difficult or needs it (Mymobileworld CLAUDE.md, Ralph 2026-11-02). A drifted take gets one Omni edit turn before any new take. **Pasting a real label is the last
  resort** (it reads as a sticker), only with Ralph's OK for that shot. Route, prompt template, costs:
  `references/product-lock.md`. Why: October's redos (Vans tab and gift-shot shoe, Cleanwaste boxes) cost more than
  the first takes.
- **Every still, edit and clip prompt is written with the `prompt-master` skill, loaded with the Skill tool first in every session** (Ralph 2026-10-24: JIYU round-1 stills written from memory of its rules, 6 of 10 redone) (its "Ralph's stack"), every
  reference named by its tag and the print matched letter for letter (Ralph 2026-10-21: it locks the models to what we
  want). Paste the final prompt into the plan so Ralph sees it before spend.
- **Budget (Ralph 2026-10-21: "blowing through my budget"):** every plan and every redo question shows
  `python3 grace/spend.py` (month so far vs his cap: none in October 2026, $100/month from November) next to the job's quote. At the cap, `grace/gate.py` refuses every
  paid runner until Ralph's OK is recorded in `grace/spend.json` over_cap_ok. Spend nothing on a redo Ralph did not ask
  for; offer to let a small flaw go (Vans gift shot) before quoting a fix.
- **Real product photos always win (Ralph 2026-10-26, B12B6):** a detail from research, another creator's video or a listing
  render goes into a product prompt only after it is checked against the real photos. Write `JOB/product_truth.json` (photos,
  facts, forbid) from them before the first prompt; `grace/prompt_check.py` refuses any prompt that describes a forbidden
  detail. Why: a research note said "screw spout", Grace's photos showed a tear-off tab, all 9 stills drew a spout ($0.81).
- **Show the plan before the first paid call, even after an upfront "go ahead" (Ralph 2026-10-26):** his OK counts only on
  a book he has seen (`BOOK.md` needs a `Sent to Ralph:` line before `--approve-book`); act on his upfront choices
  (Kie vs Flow/Gemini) without asking them again. Why: the B12B6 stills ran before he saw anything, so he could not catch
  the wrong top.
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
- **Clip check on every paid clip (2026-10-26):** the runners (`wan_clip.py`, `omni_clip.py`, a job's `kie.py` copied from
  `ugc/oqq-wide-leg-pants/`) compare each downloaded clip's opening second with its still (`grace/clip_check.py`,
  calibrated on 242 real pairs) and log Kie's billed credits, which `grace/spend.py` counts instead of list prices.
- **QC extras beyond CLAUDE.md hard rule 3:** nothing resting on thin air (a Vicks still put the box past the vanity
  edge; free fix = crop the frame to end at the object's base). Use `templates/qc-report.md`.
- **Drift strip on every pasted, patched or tracked product shot, before any cut goes out:**
  `python3 grace/qc/strip.py CLIP --box X,Y,W,H --from S --to S` (box ~2.5x the product, the window the cut uses;
  `track_paste.py` writes it as `qc/strip_<shot>.jpg`), then again on the FINAL cut at every frame of each pasted
  window (15 fps), never sample frames (Ralph 2026-10-28: v9 passed sample crops, he still found a half-covered ring,
  a reshaped bag edge and AI handles between the fingers). Look at every tile at 2x: the product stays on what holds it,
  the background beside it moves with the camera (no smear, blur, blocks or seam), nothing left of the AI's own
  product, no slide. Why: Ralph caught drift twice on Mini Bag Charm (2026-10-27: a charm floating off its ring, a
  curtain smearing beside a patch), then "Make sure you have in your QC process to check for that"; a motion number
  could not tell the bad v5 from the fixed v6, so it is a look, made fast.
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
- Lip sync: default ElevenLabs voice + Kie sync; Fal.ai `minimax/h3-max/lip-sync/image-to-video` only as the fallback when Ralph doesn't like the result; Kie talking-avatar models (one still + the voice, no clip first, untested) for talking-head lines: `references/lipsync-options.md`
- Product lock (every product shot: Flow, Wan and Omni clips, edit turns, budget line): `references/product-lock.md`
- Exact-product route (real photo + paste-back, complex products; last resort since 2026-10-21): `references/exact-product.md`
- Templates (fill, don't improvise): `templates/plan-message.md` (the one plan message), `templates/readme-status.md` (job README + Status line), `templates/qc-report.md` (QC before any send).
- Scripts live in `scripts/` (gate.py, kie runners, cut/finish/qc tools); templates in the job folders named in CLAUDE.md.

## Final finish (Ralph 2026-10-07)
Last step on every AI video: `scripts/ai_finish.sh IN OUT` (20% grain, 20% sharpness, saturation down a little; keeps TikTok from tagging it as AI, per @ericdoesecom, unverified). Details: `grace/PLAYBOOK.md` §6.
