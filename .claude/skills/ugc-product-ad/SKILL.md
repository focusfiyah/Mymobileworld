---
name: ugc-product-ad
description: Produce short creator-style UGC product ads (TikTok Shop / Meta). Covers (1) a talking-to-camera spokesperson spot from a person's photo plus a product packshot; (2) multi-character dialogue skit ads (couple or family "POV" skits with a product handoff) from Gemini 3 Pro stills and Seedance 2.0 Mini on Kie; (3) longer multi-shot ads from ONE recurring persona (an AI influencer), one Grok Imagine clip per shot on Kie, optionally lip-synced to a cloned ElevenLabs voice; (4) patching a mumbled off-camera line by cloning the clip's own voice; and (5) demo/tips ads over a voiceover, hands-only or with the person on camera (Kie stills + Seedance Mini per shot, lip sync on face shots). Use for any "make a UGC ad", "creator video", "TikTok Shop ad", "spokesperson spot", "skit", "tech UGC", "AI influencer", "use my voice", "remove the pauses", "hands-only" request, and for Fungix / Grace / Carpe / Restlex / Ralph / Seller AI OS ad work. Encodes models, prompts, timing, cost control, QC and compliance.
---

# UGC Product Ad

Repeatable recipes for creator-style product ads. Follow them and a job takes a
handful of tool calls. Working it out from scratch takes fifty calls and produces
worse output, which is why this file exists.

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
"Everything means everything." Before ANY plan goes to Ralph and before ANY paid call, run the whole checklist in
`grace/PLAYBOOK.md` §4 yourself and save proof files in the job folder, listed in `checklist.json`
(`python3 grace/gate.py <job> --init`): audience research first (`python3 grace/audience.py <job> "<seed>"...` = AnswerThePublic-style question map, plus verbatim voice-of-customer quotes in `research/audience/voc.md`, then `research/audience.md`: Who, Pain point experience, Communication style, What it means for the script; the audience picks the structure and words), playbook rules applied, tiktok-shop-coach research (tag/shop/discover + `video` on
the top 3 shop videos), the daily `viral` board, product facts, hooks modeled on named winners (spoken + on-screen),
`humanizer` on the final script and captions, `readability` (grade <= 6), the source of every line, and after the cut
`tiktok.py compare` vs the top winner (`--stage cut`). Every paid runner calls the gate (`gate.py`) and refuses until it
passes; never bypass or weaken it. Show the gate result in the plan message. Banned in scripts: "order it now",
"heads up", dashes; close with Grace's usual "It's in the orange cart."


## Working with Ralph: money, questions, tokens (read first, every job)

Ralph's words (2026-10-01): "I don't like time wasted, I like you to be efficient, low usage/token, don't waste money
and ask questions, do not assume, because that's how we waste time and money."

- **Ask before EVERY paid call, including redos, retries and "one more try".** Quote the exact cost. A failed
  attempt is not permission for a second one: stop, show it, ask.
- **Ambiguous instruction → one short question, never a guess.** "To clarify, shorten the nails" was read as
  "even shorter" and two unrequested edits ($0.18) were run; he had liked the version already made.
- **Free fixes first.** Blur a wrong label line, crop, retime, re-cut in ffmpeg/PIL before any reroll.
- **Confirm the real product before the first paid still:** applicator/top, cap, label, size. Ask for a real
  photo if the reference is a generated sheet. The Carpe sheet showed a ribbed white dome; the real stick has an
  orange slotted top → 5 stills redone (~$0.54).
- **Confirm the person's details too** (nail length, jewellery, skin): the reference pixels win over the prompt.
  Long nails in the hand sheet came out long; say "short nails" up front if that's wanted, and ask.
- **A pasted prompt that clashes with the video** (product-sheet style, grey background, "no hands") → say so and
  ask how to use it before spending. Run verbatim it gave a 3-panel sheet, usable only as a reference crop.
- **Client:** ask who the ad is for at the start; apply that client's rules (Grace: no personal-use claims unless
  true, no false scarcity, a CTA that makes buyers want more units, honest lines that sell, never a downside or warning).
- **Lock the whole plan before the first paid call** (Ralph, 2026-10-01: "You are having me spend all my credits
  today"; "I don't think you remembered me wanting the process to be time efficient and cost effective"): ONE
  message with script, every shot, outfit, setting, face or no face, voiceover vs lip sync, and the total cost; one
  approval. A mid-job change gets a new total before anything is spent.
- **One test clip before any batch.** Carpe v2 rendered 8 clips at once and all came back wrong ($1.52); one clip
  would have cost $0.21.
- **Resuming a job from a handoff: re-check before paying.** Right before any paid call, re-fetch the job branch,
  look at its `kie_log.json` / clips folder for that step, and make sure the old session is stopped (Vicks
  VapoShower 2026-10-01: the old session rendered the 6 clips after writing its handoff, the new one rendered
  them again: $1.07 lost).
- **QC before sending, so Ralph never finds it first** (each miss cost him a review round, ~20 rounds / 4h on
  Carpe v2): every clip at ≥1.0x speed; no face on screen while the voice talks unless lip-synced; product never
  cropped off or smeared; no forehead wrinkles; same outfit and product in every shot; frame-by-frame check wherever
  hands or the product cross the face; nothing resting on thin air (a Vicks still put the box past the vanity
  edge and Ralph caught it: free fix = crop the frame to end at the object's base).
- **Script checklist, every ad (standard):** Every script, before the plan goes to Ralph (Ralph 2026-10-01, after the Plant Therapy hook shipped with no on-screen text):
  (1) tiktok-shop-coach: research + 3 hook options (Grace: start from `grace/hooks/HOOKS.md`, cite the id) (spoken line AND on-screen hook text) modeled on proven videos;
  (2) humanizer pass on the script and caption; (3) after the cut, `tiktok.py compare <viral video> <our cut>` and fix
  what it shows (pace, cuts) before sending.
- **No text overlay unless Ralph asks (Ralph 2026-10-05, LGXNDS creatine: "Remove text overlay. I did not ask you to do so"):** write the on-screen hook text options as before, but only offer them in the plan as a yes/no item; burn text into a cut only when Ralph says yes for that ad. Default cut = no text overlay.
- **On-screen text style (standard, Ralph 2026-09-18 Murano earrings; reapplied 2026-10-01):** TikTok "Classic": white
  semibold, NO background bubble, soft drop shadow, lowercase, two balanced lines past five words, no "orange cart"
  text line. Use `ugc-product-ad/scripts/classic_caption.py` (Open Sans SemiBold stands in for Segoe UI Semibold).
- **Report the running total against the quote at every paid step.**
- **Phone notification at every review point** (Ralph, 2026-10-01: "Make that a standard"): he leaves the app, so
  send a PushNotification (one line: what to review + any cost to approve) whenever a still sheet, test clip or cut is
  ready, or a redo needs his OK. Send the file with SendUserFile first. Not for routine progress.
- **Delivering to Google Drive** (Ralph, 2026-10-01): use both the Google Drive connector and Composio `googledrive`;
  if one fails, use the other. Videos go through Composio `GOOGLEDRIVE_UPLOAD_FROM_URL` after hosting the file on
  Kie's file host (`kie.upload`); the connector handles folders and docs but can't carry a video.
  One folder per product in "Grace Tiktok assets" (reuse an existing one), "CURRENT - " on the latest, superseded files
  renamed vN + date into an "Older versions" subfolder, nothing loose (Ralph 2026-10-05).
- **Tokens:** keep the job README's `Status:` line current (what's done, what's next, what it costs) so "continue
  the X ad" needs one file read. Short updates, chained shell steps, one contact sheet per batch.


## Reference map (read the file for the route you are using; each has a table of contents)
Every route below is still governed by Step 0 (script gate) and "Working with Ralph" above.
- Single spokesperson 10s ("The recipe", prompt template, say-ability, verify, compliance, cost table, tool list):
  `references/spokesperson-recipe-and-tools.md`
- Trending spokesperson recreate (up to 15s): `references/recreate-spokesperson.md`
- Multi-character skits, patching a spoken line, fix a line after render, skit traps and costs: `references/skit-ads.md`
- One recurring persona, per-shot Grok clips, trim dead air, animated CTA, lip sync, Kie stills and prices:
  `references/persona-per-shot.md`
- Hands-only ad, on-camera demo over a voiceover, GTT KN95 lessons: `references/hands-only-and-demo.md`
- Exact-product route (real photo + paste-back, complex products): `references/exact-product.md`
- Templates (fill, don't improvise): `templates/plan-message.md` (the one plan message), `templates/readme-status.md` (job README + Status line), `templates/qc-report.md` (QC before any send).
- Scripts live in `scripts/` (gate.py, kie runners, cut/finish/qc tools); templates in the job folders named in CLAUDE.md.

