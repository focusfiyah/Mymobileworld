# Grace playbook

One place for everything we've learned about making Grace's ads. Add to it after every Grace job (newest
lesson goes in the section it belongs to, with the date). Paste this file into a new chat to start a Grace job.

Grace is Ralph's client: UGC / TikTok Shop ads. Jobs so far: Fungix nail serum (real takes, 2026-09-18),
Restlex "2am" couple skit (AI, Grace as the wife), Carpe Vanilla Peach (hands-only AI, 2026-10-01). Fashion
products follow the same rules.

## 1. House rules (never break)
- **No personal-use lines** ("I use it", "it worked for me", "smells like…") unless true for Grace. Review
  findings are "reviewers say", never her experience.
- **Grace's point of view, every script** (Ralph 2026-10-03, after the Anemiaprin v2 scripts read like a nurse
  lecturing): write it as Grace talking to her friends ("girls", "this is the one I'd show you", "here's what I want
  you to know"), reading the label in her hand and giving her opinion. Never an expert or educator voice ("as a nurse",
  "you're taking it wrong" lectures). When the viral model is an expert's video, copy its format (numbered tips, label
  read, comment reply), not its voice. Facts stay, said the way she'd pass them on. Life details that may not be true
  for her ("me at 3pm every day") get an [only if true] tag plus a neutral version ("who else is done by three?").
- **No false scarcity.** No "selling out" / "ends tonight". Use "don't put it off" or a real seasonal reason.
- **Exact claim wording** from the label or listing. Never "cures / kills / fixes", never a timeframe unless the
  label gives one ("clinically tested… up to 100 hours when used as directed" is fine because the label says it).
- **Never say a price** (Ralph + Grace 2026-10-02): no prices, discounts, "$X value", "% off" or "on sale" in the
  spoken script, on-screen text or caption. TikTok gives violation cards for it. Deal talk without numbers is fine
  ("two for the price of one", "TikTok-only set").
- **Honest lines sell, never un-sell** (Grace 2026-10-02, replaces "one honest caveat"): no warnings, downsides or
  "heads up" lines ("measure your shower first", "a tall kid may outgrow it", "you still need a sink"). The honest
  beat is a sell-side confession: "I hate how easy it is to take this collagen, now I have no excuse", "I'm so upset I
  paid full price, now you get two for one", "the only downside? they won't want to get out". Scarcity only if true.
- ~~Detached CTA~~ replaced 2026-10-01: the CTA drives more units (see §4, "CTA sells more units").
- **Words to avoid:** "you NEED this", "obsessed", "game changer", "miracle", "so cute", reading off the size range.
- Disclosure in the caption: `#ad` or the brand's partner tag.
- **No "plenty to share" / "one is enough" lines in the CTA (Ralph 2026-10-03, GTT KN95).** Anything that tells the buyer one unit covers it kills multi-unit sales. Close with a line that makes them want more ("Grab a couple boxes, so there's always one close"), then "It's in the orange cart."
- **No "order it now" / "order now" (Ralph 2026-10-03).** Close with Grace's usual "It's in the orange cart." after the real reason (holidays, "don't put it off").

## 2. Sales psychology
| Principle | How we use it |
|---|---|
| Pain first | The hook names something the viewer already hates (toes tucked under the table, waistband digging in). Review complaints make great hooks. |
| Sell the moment | Put them in the exact scene: shoes off at a friend's house, the salon polish wall, the 5-minute get-ready. |
| Move away from pain | Escaping embarrassment sells faster than promising pretty. The product is the way out. |
| Clarity, not convincing | Calmly show why what they do now (hiding it, painting over it) doesn't fill the gap. Let them conclude. |
| Remove uncertainty | Every body answers: what's in it, how to use it, how often. Most hesitation is missing information. |
| Detachment builds trust | Honest review voice, one con, no pressure. |
| Price pushback = value question | Show 3–5 looks/uses so it reads as several outfits. Never say the price (§1). |
| Specificity | Exact numbers beat adjectives ("a pea-sized amount", "twenty-five percent"). |
| Take the shame out | Gift angle ("your dad will never buy this himself"): the pain is felt for someone else, and it gets shares. |

## 3. Hooks
- **Hook library (Ralph, 2026-10-05): `grace/hooks/HOOKS.md`** (source `hooks.json`, ids like `B1-15`). Pick spoken hook options from it first on every Grace job, fill blanks with concrete product moments, cite the id in line sources, never reuse one id across a product's videos. More batches coming: add them to `hooks.json`, run `build.py`.
- Types: problem call-out, result first, comment reply, curiosity gap, contrarian, visual pattern
  break, POV, social proof (true only), direct address.
- **Grace's own hook style (Grace 2026-10-02, Shnuggle; use it in every product):** (1) category-gap discovery:
  "There are a ton of baby bathtubs out there, but I've never seen a true toddler-size one until now."; (2) finally +
  the viewer's exact situation: "If you have a stand-up shower and have been looking to make bath time pleasant, this
  is the perfect one."; (3) features named one by one, each with what it does ("there's a bump inside, so they sit
  up"). Give every product at least one of each across its angles.
- **Text hook = curiosity only** (Grace, 2026-10-01): 5-7 words, never names the product, makes them ask "what?"
  ("Nobody puts this on a beard"). The spoken hook does a different job (names the pain).
- **Curiosity loops all the way through** (2026-10-01, from @dus_davis): answer one question and open the next in
  the same breath; an odd claim said without explanation keeps them watching. Mid-video overlays can open loops too.
- **Stack two layers:** spoken problem + on-screen text + product moving. The first second must make sense with the sound off.
- Film 3–4 takes of each hook; give each video **different on-screen bubble text** (TikTok treats them as distinct).
- Proven angles: timing ("boots season, nobody's looking at your feet"), cover-up ("painting over it isn't a plan"),
  read-the-label, "you're probably doing it wrong" tutorial, gift for a relative, "watch this before you use it".

## 4. Script structures
- **Grace's structure, every ad (Ralph 2026-10-02):**
  1. **Curiosity-loop hook**
  2. **Pain-point body**
  3. **Selling point and/or solution body**
  4. **FOMO and/or urgency CTA**

  The pain needs its own beat at the top of the body even when the hook already names it (2026-10-02 beauty pack:
  8 of 12 first-draft bodies went hook → product and had to be fixed in review).
  FOMO and urgency must be real (a season, a date, an event, a real deal, what they miss out on by waiting), never
  fake scarcity. Combine with "CTA sells more units" below (count, gift).
- What fills the bodies, by product type:
  - **Product / tips (Fungix, Carpe):** clarity → claim (exact wording) → how to use (what / how / how often) → sell-side confession (§1).
  - **Fashion:** fit facts (height, size, how it runs, where it hits) → proof (back turn, phone in pocket, sit-down,
    sheer check) → honest take (times worn, what she loves, best for whom; no cons, §1) → 3–5 looks.
- **Coach research = top shop SELLERS, not keyword pages** (Ralph 2026-10-02, after Grace rejected the v1 angles): run
  `tiktok.py viral --days 30 --category <cat> --add-tags <niche tags>`, keep shop videos selling products in the same
  niche, run `video` on the top 5–8 and look at every hook.png. Name the seller video each angle is modeled on
  (link + views/saves). What the winners did (beauty + parenting, 2026-10-02): product already in use at frame 0,
  identity call-out hooks ("for my lazy people", "if bath time is a struggle at your house"), speed claims ("smoky eye
  in 30 seconds"), zero caveats, brag-style confessions, TikTok-only bundle / gift / season CTA.
- **Tutorial beats hard sell.** Carpe research: the hard-sell video got 830k views but 0.02% saves; the "watch this
  before you use it" tips video got 1.4M views and 0.71% saves. Tips also answer the viral complaints.
- Ask what Grace has already filmed before scripting; the script must match the footage (2026-10-01 Viking:
  she'd filmed hands-only on the beard while the script talked about head curls).
- Get Grace's real facts before writing (fit, fabric, sheer, pockets, times worn, love/con, styling). Never invent them.

- **ENFORCED by `grace/gate.py` (Ralph 2026-10-03):** every paid runner refuses until the job's `checklist.json` proves each item below with a
  file newer than the script. Do it unasked, every job, every script change.
- **Every script uses ALL of these (Ralph 2026-10-01, Vicks VapoShower: "everything" means all of it):** (1) real data
  from the `tiktok-shop-coach` skill (discover/tag/shop on the product's keyword, `video` on the top 3 shop videos: their
  hook, format, length, CTA), (2) the coach playbook's hook types and buyer levers, (3) §2 sales psychology here,
  (4) product research (box, brand site), (5) the §4 structure, (6) the `humanizer` skill on the final script so Grace
  sounds like a person talking, (7) coach `readability` (grade ≤6), (8) §3 hook layers (on-screen hook text options, offered in the plan; burned in only on Ralph's yes), (9) after the cut: coach `compare` against the top winner, before Ralph sees it. Show Ralph
  which line comes from which source in the plan. The coach needs `bash setup.sh` from Dayone-ai first (Playwright).
- **CTA sells more units, not detached (Ralph 2026-10-01):** the close should make the buyer want more: say the count
  ("twelve tablets, twelve showers"), a second occasion or a gift ("one for you, one to gift"), real seasonal timing.
  Shower-steamer winners closed this way (JojoWell 879k "each pack comes with six"; bundle video 173k "you get 18
  tablets"). Still no false scarcity.
- **Script checklist (standard).** Every script, before the plan goes to Ralph (Ralph 2026-10-01, after the Plant Therapy hook shipped with no on-screen text):
  (1) tiktok-shop-coach: research + 3 hook options (spoken line AND on-screen hook text) modeled on proven videos;
  (2) humanizer pass on the script and caption; (3) after the cut, `tiktok.py compare <viral video> <our cut>` and fix
  what it shows (pace, cuts) before sending.
- **No text overlay unless Ralph asks (Ralph 2026-10-05, LGXNDS creatine: "Remove text overlay. I did not ask you to do so"):** write the on-screen hook text options as before, but only offer them in the plan as a yes/no item; burn text into a cut only when Ralph says yes for that ad. Default cut = no text overlay.

## 5. Pacing and edit
- Fast UGC speech: **3.0–3.6 words/sec**. Target ~30 words hook, ~60 body, ~20 CTA ≈ 35s after pauses are cut.
  Fashion default 30–45s. Category median is a good length check (Carpe: 35s).
- Cut every pause, never clip a word; end on a visual beat, not the last syllable.
- Retention: a steep drop in the first 1–2s = the hook failed; a slow slide mid-video = a beat runs too long.
- Say numbers as words in the script ("twenty-five percent") so captions and timing match.
- Real takes: film hook / body / CTA as separate files, 3–4 takes each, original HD files; keep body takes whole.
  Mix N hooks × M bodies × K CTAs into combo ads (`ugc-take-combos` skill).
- **On-screen text style (standard, Ralph 2026-09-18 Murano earrings; reapplied 2026-10-01):** TikTok "Classic": white
  semibold, NO background bubble, soft drop shadow, lowercase, two balanced lines past five words, no "orange cart"
  text line. Use `ugc-product-ad/scripts/classic_caption.py` (Open Sans SemiBold stands in for Segoe UI Semibold).
- Overlays: search-result "screenshot" card timed to the claim word, condition photos (never before/after),
  animated CTA. No burned-in captions unless Ralph asks.

## 6. Production notes
- **Time + cost discipline (Ralph 2026-10-01, after Carpe v2 took ~4h15m and $6.60 vs a $2.50 quote):**
  1. Lock the WHOLE plan before the first paid call, in one message: script, every shot, outfit, setting, face or
     no face, voiceover vs lip sync, total cost. One approval, then no mid-job redesigns without a new quote.
  2. One test clip before any batch.
  3. QC before sending anything, so Ralph never finds it first: no clip slower than 1.0x, no face on screen while
     the voice talks without lip sync, no product cut off or smeared (lip sync near the product), no forehead
     wrinkles, outfit/product consistent in every shot, frame-by-frame check where hands/product cross the face.
  4. Report running total vs quote at every step.
- Voices: ElevenLabs **Grace B** `bGrsdLmwBbYUgHRuMFOI` (eleven_v4) for voiceovers; Grace's Seedance clone
  `3dmagVYZFvrGkBbWWmGC` for AI skit dialogue.
- Before the first paid image: confirm the real product (top, cap, label, size) and the hand/person details
  (nail length). Ask before every paid generation, with the exact cost. Free fixes first.
- **Outfit changes go in the TEXT too** (Carpe v2, 2026-10-01, cost $1.52): the stills were edited to a grey tee but the
  video prompt's identity text still said "blue tank top", and Seedance redrew the tank in all 8 clips. When the
  look changes, update every prompt block, then grep the prompts for the old wording before rendering.
- **A product description in the prompt puts the product in the shot** (Carpe v2, 2026-10-01, $0.41): "no deodorant in this
  shot" lost to the identity block's detailed stick description; Seedance added it anyway. For no-product shots,
  leave the product text out of the prompt entirely. Also keep faces relaxed in stills ("raised eyebrows" = forehead
  wrinkles the clip copies).
- **Same for hands** (Vicks, 2026-10-01): the S5 no-hand clip still had the hand identity text in its prompt, and two
  pale hands walked in at 2.2s. Leave the hand block out of no-hand shots (`NO_HAND` in `ugc/vicks-vaposhower/kie.py`).
- **A no-box shot needs the box text out too** (Vicks S6, $0.09): the box block put the box on the shower glass. And
  say the exact surface plus pass the matching still as a ref (S4's tablet landed on a counter until S5 was the ref).
- **Voiceover ads: keep her mouth out of frame while the voice talks** (Ralph 2026-10-01, "why are her lips not
  moving"): Ralph then preferred lip sync over chin-down crops (crops cut the product off): `lipsync.py` in
  `ugc/carpe-mountain-breeze/`, $0.04/s, submit one at a time (parallel calls get "server busy", $0).
  Lip sync smears anything that passes in front of the mouth (the stick): check every frame where the product
  crosses the face and swap those frames back to the original clip
  (or keep only the lip-synced mouth in a soft oval over the original; the lip-synced clip runs ~2 frames late).
- **Test ONE clip before any batch** (Ralph 2026-10-01, after $1.93 was lost on two prompt mistakes in one day): render
  the cheapest affected clip, check it, then ask for the rest. Report the running total vs the quote at every step.
- Routes and costs: `ugc-product-ad` skill. Hands-only template: `ugc/carpe-vanilla-peach/` ($3.52 for 36s).

- **Removed items stay removed (Ralph 2026-10-04, FUSOU V1: the 3-boxes card and the hand sweep came back after he had removed them):** every job keeps a `REMOVED.md` (copy `ugc/fusou-vanity/v1ab/REMOVED.md`): every element Ralph or Grace removes or rejects goes in at once. Before ANY cut goes to Ralph, list every element in it (overlays, cards, hand shots, lighting treatment, framing, sounds, props) and check it against that list and against the previous round's notes. When rebuilding from an older cut script, re-read its notes first; never carry an old shot or overlay over by default.
- **Visuals match the words, not excessively (Grace 2026-10-04):** the pain line about pills shows pills and pill bottles; "twelve pouches" shows twelve pouches; the product shown is always the real one (a pouch stays a pouch: cut any clip where Seedance morphs it into a juice box/carton). Don't illustrate every word.
- **Check the real product from the brand/retailer photos before the first still (Ashwagandha 2026-10-04, $1.75 redo round):** the TikTok thumbnail made the pouch's flat teal tear-off top look like a screw cap; I wrote 'teal screw cap' into the product block and every clip showed the wrong pouch until Grace caught it. Pull the retailer's product + box photos (vitacost/iherb `cdn/shop/files/*.jpg`), crop them as refs, and describe the top/closure exactly. A 12-count generation came out as 16: count items in multi-product stills, crop to the right count.
- **Never say "the label says" (Grace 2026-10-04):** state the label's claim directly in Grace's voice ("it helps reduce stress").
- **No on-screen text, no product cards, every video different (Ralph 2026-10-04, campaign deadline):** no hook text or captions on the video unless Ralph asks (this overrides the §3 text-hook and §5 Classic caption defaults); no product overlay cards/pop-ups (a pasted listing crop looked blurry, black-bordered and fake); variants must never be the same footage with a new VO (TikTok flags it). Free fix that worked: `remix.py` per job: different clip sections and order (incl. the usable parts of rejected test clips), framing (zoom 1.0-1.25) and a grade per video, ALWAYS BRIGHT AND NEUTRAL (daylight / clean neutral / bright cool / bright punchy; no golden or yellow tint, Ralph 2026-10-04). Ralph 2026-10-04: no dark or vignette looks, they read as no lighting. Better still, plan a different setting per variant in the first plan and quote it.
- **The hand does NOT need to be in every shot (Ralph 2026-10-04, standing rule):** plan hand-free shots (the product alone, the setting, props) wherever they fit the line; they still need real motion (camera move or a product-only clip, rule 6) and their prompts leave the hand block out (`NO_HAND`). Don't force a hand into a shot just to have one.
- **Lights features (Grace 2026-10-04, replaces the "darken the room" idea for the FUSOU job):** do NOT darken the room; show the light colours in daylight.

## 7. Results log (add one line per job)
- 2026-09-18 Fungix: Grace's real takes (hook/body/CTA) cut into combo ads. Then 5 new script angles written:
  `fungix/grace-script-angles.md`.
- 2026-10-01 Carpe Vanilla Peach: 36.6s hands-only tips ad, $3.52 vs $2.53 planned; waiting on notes.
  Open: the "peach candle" scent line needs Grace to have smelled it.
- 2026-10-01 Carpe Mountain Breeze v2: AI Grace on camera from her photo, Ralph's structure (curiosity hook → pain →
  solution → urgency CTA, real seasonal urgency), grey tee throughout, face off the demo shots. 35s, $6.60 incl. $0.68 lip sync ($1.93 lost
  to prompt bugs). Free fixes that worked: PIL background blur, recolor, chin-down crops, pause trim, whip-pan.

- 2026-10-01 Plant Therapy Top 6 oils: 18.6s hands-only starter guide, $2.09 (on the revised quote), approved first cut; v2 adds the on-screen hook "Don't buy 20 essential oils" (the compare check found it missing). Label pop-ups
  cropped from the brand's own photo hid AI label garble for free. Small bottles drift to a coloured-label design in
  close-ups and multi-bottle shots: pin "cream label, vertical wordmark, NOT a coloured label" in every still prompt.
  Seedance redraws the scene late in a clip (caps appear, bottle count changes): plan windows from the clip's first ~1.5s.
- 2026-10-01 Vicks VapoShower Plus: 24.7s hands-only how-to (pain/moment hook, specificity, honest non-medicated
  caveat, count + gift CTA), $3.11 vs $2.04 quote: the 6-clip batch ran twice ($1.07 lost) because the old session kept working after its handoff
  and a new session started from the handoff. Before any paid call in a resumed job: re-fetch the branch, check its
  log/kie_log.json for the step, and make sure the old session is stopped. Seedance turned
  the handheld box to its side panel mid-clip despite "front facing the camera" in the prompt: free fix = clip's
  first 1.9s + push-in hold. Cut v3 approved 2026-10-02. QC stills for objects resting on nothing (the S2 still put the box in mid-air past
  the vanity edge; Ralph caught it): free fix = crop the frame to end at the object's base.
- 2026-10-01 Viking Revolution Curl Cream for Men: script v5 (~25s, $0) for Grace's hands-only footage of it on her
  husband's beard (curiosity loops, pain, real urgency); Grace records it next, `ugc/viking-curl-cream/README.md`. Ralph's structure: hook, problem, product, experience, benefit, CTA.
- 2026-10-02 FUSOU 2-in-1 Vanity Desk: 6 hands-only styles (light reveal, ASMR drawers, count-with-me, hidden door,
  GRWM outlet, clutter reset), ~20s each, $0. Furniture lesson: the honest caveat is size or build time; real urgency =
  "ships in 3 boxes" + holidays. Drive Docs: create_file garbles 4-byte emoji; overwrite the doc with Composio
  GOOGLEDRIVE_UPLOAD_UPDATE_FILE (workbench `upload_local_file` → s3key) to fix it in place.
- 2026-10-02 FUSOU 71" Vanity Desk (furniture, AI hands-only): **an AI that re-draws a complex product drifts** (drawer/cubby counts, mirror shape). What held it exact: use the
  brand's REAL listing photo as the base and EDIT it (extend to 9:16, light the LEDs, add the hand), never regenerate it from a description. The model leaves padding blurry
  sometimes: rebuild the bands free (wall from a clean copy, floor stretched + soft foreground blur; measure per-row Laplacian to find the band). A hand reaching in from the
  camera looks HUGE next to a far-away product: keep hands out of wide shots and use them only in mid-close shots at the product's distance. Check the voice plan with Ralph
  (Grace B vs Grace's own) before writing "Grace records it". Top FUSOU videos (1.2M-7.2M): handheld walk-through, 4.4 words/s, 2.7 cuts/10s, product shown filled with items,
  feature order whole vanity > lit mirror > cabinet behind the mirror > glass top + knobs > power station/dryer holder > stool drawers > light colours > link.
  **Paste-back (2026-10-03, zero product drift, free):** after the AI edit, align it to the real photo (ORB + affine), diff, keep only the changed blobs (hand, LED glow), fill mask holes (skin matching a dark gap left a grey hole), feather, paste the real photo back everywhere else (`ugc/fusou-vanity/pasteback.py`). Works on clips too if Seedance is told "locked-off camera on a tripod" (scale drift stayed <1%); per frame use max(current mask, 0.6 x previous) so a fast hand never turns see-through. Hands like @sdbby88: only the hand enters from the frame edge, no forearm (Ralph 2026-10-03); a free crop fixed M1a. **Video paste-back shimmer (2026-10-03):** a per-frame diff mask + per-frame alignment made every edge shimmer (3x the raw clip). Fix: smooth the alignment over 9 frames, colour-match once, AI pixels only for the hand (skin test with Y<170 so lit white is not skin, limited to a zone below the product edge) + a fixed LED-ring mask. Measure flicker (mean frame diff in a hand-free band) on the FINAL file before sending: a handheld sway added in post on a soft upscaled photo made fine lines crawl (Ralph saw it); keep it off (phone on a stand). Lights switching on: Seedance snaps the LEDs on in one frame and auto-darkens after: lock exposure per frame, hold ONE lit-ring plate and fade it in over 0.25 s, keep the room spill subtle and near-neutral (a warm spill read as a colour shift). Items in front of a light/near the hand must stay real: never take AI pixels for them; add LED light to the real photo (real + max(0, AI luminance - real) where the AI shows near-white light) and exclude pixels that are skin-coloured in the real photo from the hand mask. When the hand MOVES an object (plug, drawer, door, lipstick), give that object a fixed AI box; Seedance still drifts there (it swapped a whole lipstick tray in frame 1, and opened a door with no hand on it): check frame 1 vs the still. Free push-ins on soft real photos: one smooth zoom (1.05x, INTER_AREA) crawls less than Seedance's own push-in. Anchor timed overlays to the exact phrase (the first "three" was "three light colors"); keep pop-up cards left of TikTok's right-hand buttons. Excluding "skin-coloured in the real photo" from the hand mask also punches holes where the hand passes over gold/beige items or wood (items showed ON the hand, the wrist vanished): fill the hand's convex outline (extended to the frame edge) with AI skin pixels; apply it to EVERY hand clip and run `qc_hands.py` (each frame vs raw) before sending, not a few sample frames. Check the still for physics: a hand reaching past a hanging object (dryer) must pass in FRONT of it; if the still put it behind, crop it out.

- 2026-10-03 FUSOU 71" Vanity: 6 AI hands-only videos (17-24 s) APPROVED after 4 note rounds, in Drive with the final scripts doc. Kie $4.28 vs $4.54 quote. Method that held the product exact: edit the real listing photo + paste-back (`ugc/fusou-vanity/pasteback.py`), per-frame hand QC (`qc_hands.py`), free push-ins on real photos, cuts on word timings (`cut.py`). Ralph's notes were all hand-mask bugs (items on the hand, missing wrist) and the CTA (no "order it now"). Lights features: darken the room in post so the product's lights carry the shot (`ugc/fusou-vanity/darkroom.py`: LED mask = lit frame minus the real unlit photo; switch the LEDs through the listing's exact colour modes on the words, dip on "dims", a tap click per change; Ralph asked for it and liked it, 2026-10-03: use it for every product with lights). Drive Docs: write emoji as HTML character codes; the Drive reader tool shows 4-byte emoji as mojibake even when the doc is right (check with a text export).

- 2026-10-04 FUSOU V1, two versions from Grace's scripts (A, B): Grace's notes took 5 rounds: bad-light face opening in the first 3 s (vanity on screen by 3 s), room never dark, no light-tap shot, no hand sweep, no 3-boxes card, face farther + relaxed + mouth closed (Ralph: no lip sync needed, VO plays over). Face from Ralph's 3 Grace photos (`ugc/fusou-vanity/refs/grace/`; never the blue-shirt photo): $0.508 Kie for the opening (2 stills + 2 clips; the first tight, tense-brow pair was wasted: frame the face at medium distance, ask for relaxed brows in the first prompt). Free fixes that worked: grade for bad light, crop, zoom-out bridge between close-up and wide, push-in on the real photo. Ralph's rule after v4: removed items stay removed (`REMOVED.md`). Drive: FUSOU folder, FINAL files.
- 2026-10-03 Anemiaprin (Approved Science iron): 3 talking-head scripts ($0), reworked from coach data (top iron videos = numbered
  "how to take iron" tips, coffee blocks iron, label read; 5-6% saves), then rewritten in Grace's voice (new §1 rule).
  Google Doc in Drive "Anemiaprin scripts (2026-10-03)".
- 2026-10-02 Super Blanky wearable blanket: 3 talking-head scripts (dorm, Breast Cancer Awareness Month comfort gift, stays-on demo), $0. Doc https://claude.ai/code/artifact/400ca34e-3585-4133-a50a-bafbba29edf1 + PDF. Cancer angle = comfort-gift framing only, never "chemo must-have" (the brand's own wording). Cloud env 'My World'-less sessions may block tiktok.com (proxy 403): coach video/tag/shop can't run; WebFetch of shop.tiktok.com search/pdp pages still works.

- 2026-10-02 Beauty script pack (Bobbi Brown Prep & Brighten Duo, Bobbi Brown 3-Minute Eye Look Trio, ELASCO Melt Off,
  + Shnuggle Toddler Bath): 3 talking-head angles each, 2 hooks per angle, $0. Claude doc only (no PDF, Ralph):
  https://claude.ai/code/artifact/69b642ee-715d-4183-8c7e-3e7bdf76c19e. No personal-use lines needed (Ralph: don't ask
  Grace what she's tried); brand claims said as "the brand says". Remover winners all hook on stinging/foggy eyes.

- 2026-10-02 Beauty script pack v2: Grace rejected v1 (prices said, caveats that un-sell, weak angles). Rebuilt all 12
  angles from the top shop sellers in each niche (coach viral board, 1,728 videos), no prices, sell-side confessions.
  Shnuggle angles 1-2 then replaced with Grace's own ideas (true toddler-size tub with the safety features; stand-up
  shower). When Grace sends angle ideas, they go first and the coach patterns fill in hooks and structure.
- 2026-10-03 Grace B voiceover stutters (FUSOU V5 "Ho- holiday", V6 "If, if someone"; eleven_v4, stability 0.4): the timestamps from TTS are text-based and do NOT show it. After EVERY voiceover and every splice, run an ElevenLabs STT (scribe_v2) on the final audio and scan for repeated words and hyphen fragments; fix free by cutting the fragment out of the wav at the STT times. Ralph heard both, I hadn't: check before sending.

- 2026-10-03 GTT Black KN95 50-pack (mask, ELEHOME GTT shop): AI hands-only ad, 31s, 10 shots matched word-for-word to the VO, Grace B full re-record after a CTA change. Kie $4.375 vs $2.75 first quote (4 stills redone for the wrong mask/box, rug shake redo, S7, car + shelf redo: each redo asked first). APPROVED, in Drive (Grace Tiktok assets/GTT Black KN95 50-pack ad (2026-10-03)). Lessons: (1) The model draws a generic flat-fold KN95, not the real fish-shape mask, when the ref is the box-and-mask packshot; give it a tight crop of the REAL mask only plus a shape description with 'NOT a flat-fold/duckbill', and a strict box colour ('silver-grey, not blue/white/black/beige': the white-mask box is blue). (2) A hand that touches an item must GRIP it (pinch by the edge, fingers curled): flat-hand-on-item reads as unnatural (rug stuck to the palm, masks under a palm, box under a flat hand). Prompt 'pinches ... between thumb and finger by its top edge, NOT lying flat' in both still and clip. (3) A clip can move the object the wrong way (box slid AWAY): use the half that moves right, or reverse the part that moves the wrong way (free). (4) Seedance min clip is 4s; windows of 1-1.5s still need a 4s clip: use the first 1.5s or an offset where the action happens. (5) Compliance for masks: dust/outdoor angle only (the listing's own pitch); KN95 is not NIOSH-approved and TikTok restricts medical claims, so no illness/N95/FDA/layer-count lines. (6) Plain words for this audience ('filter out ninety-five percent or more', not 'filtration efficiency') and Grace does not say 'the box says'. (7) Face shot tried and dropped: AI Grace from her photos changed her hair colour and drew the wrong mask; Grace reference sheet (`grace/ref/grace_reference_sheet.png`, 3 views) kept for a separate job. (8) Coach: the mask niche has no viral winners (best 2.6k views); ~35% of 'viral board' mask videos are copy-paste seller clips, so make the ad better made, not louder. Job: `ugc/gtt-kn95/`.

- 2026-10-04 LGXNDS Creatine Monohydrate (unflavored, scoop inside): hands-only AI ad, 31s, 9 clips each matched to its VO line (Ralph: "match the scenes with the script"), Grace B VO, no text overlay (v3, 2026-10-05: Ralph had the hook text removed). Kie $2.573 vs $2.57 quote (S1 still + S3 clip redone, each asked). v3 (v2 without the text overlay) is the final in Drive (Grace Tiktok assets/LGXNDS Creatine ad (2026-10-04)), v1 and v2 removed. Lessons: (1) Nano Banana Pro redraws a tub label (small print garbled, once the whole layout); paste the REAL label back with `ugc/lgxnds-creatine/label.py` (SIFT homography on the printed block only, skin and dark occluders kept in front) on stills AND every clip frame. (2) Per-frame homography fits jitter up to 25 px and shimmer: for a locked camera use ONE fit per clip (`--ref`). (3) Seedance turns a tub when the hand twists its lid (frames 10-33) and cannot show powder dissolving (it clumps, goes milky, or sinks into a pile): keep tub shots hands-off the label and use only the pour. (4) 2026-10-05 v2 after Ralph asked why Beet Root looked better: paste from the sharpest real packshot you can find (TikTok pdp images load at up to ~1350 px via `resize-webp:2000:2000`, not the phone screenshot), carry the tub's paper shading onto the print (median-filtered brightness ratio), never add synthetic grain; and for the label line use the real packshot with a slow push-in (Ralph OK'd it per shot). (5) Coach: creatine shop winners sell texture ("not chalky", Bloom 256K) and the 5 g number. Job: `ugc/lgxnds-creatine/`.

## 8. Tracking and sample volume (2026-10-01)
- Grace gets 25+ samples a week. She doesn't film them all: **Grace's Creator Desk**
  (https://claude.ai/artifact/78TpktwxYTM4cf4z5xnyS2, `grace/desk/`) scores each sample and shows her top few for the week.
  She batches the shoot by setting, uses a script pack (4 hooks × 1 body × 1 CTA) per product, and logs each posted video.
- What we judge a video on: save rate first (Carpe benchmark: tips 0.71%, hard sell 0.02%), then share rate and $ per 1k views.

## 9. To add later
- Looping: curiosity loops are in §3 (Viking, 2026-10-01). Endings that flow back into the start for rewatches: not
  covered yet; add here when we need it.
- 2026-10-03 Horbaach Beet Root+ gummies: 24.5s hands-only (VO Grace B, no overlay text at all, hand-free shots allowed per Ralph), $1.68 Kie vs $1.69 quote.
  Ralph: the hand does not need to be in every shot; no juice on screen (confuses what the product is); don't claim "beet juice tastes like dirt" (not true for everyone). Hand-free shots = free slow push-ins on stills (real label photo for the label shot) instead of clips: no stray hands, no label drift. Lessons: Nano Banana added a phone date stamp ("OCT 26 8:14 AM") and a stray pale hand at the frame edge in no-hand shots, and invented a label line ("Support Serotonin...") on a jar alone: crop the stamp/hand free, add the exact small label text to the jar block, say "nothing at any edge of the frame". Seedance label text drifts once a jar is lifted/rotated: cut the clip before that. Coach tool needs `pip install playwright` + `apt-get install libnss3-tools` in a fresh cloud session. Kie balance can drop from other jobs between sessions: check it first.

- 2026-10-04 Supplement pack (Youtheory ashwagandha + turmeric, Neuro sour mints, Penetrex): 20 hands-only ads <=16s, Kie $4.9 (~$0.25/video). Lessons: (1) **Never prompt a hand to 'turn the product until the label faces the lens'**: Seedance spins it edge-on/to the back (3 of 4 test clips, $0.74 lost). Use 'holds it facing the camera the entire time, tilts only a few degrees, never rotates' (fixed all three). (2) **Cheap variants**: 4 extra videos per product cost $0 Kie by reusing the V1 footage with a new hook text + new VO + new script (only ElevenLabs chars); the cut moves overflow into the push-in shot when a line runs longer than its clip (`cut.py N`). (3) ElevenLabs returns 429 on >~3 parallel TTS calls: run them one at a time. (4) Brand names: 'Youtheory' came out as 'Eufaery/Euphony' in STT; spell it 'You-theory' for the voice and STT-check every VO. (5) Real listing crops shown as a rounded card over a blurred still of the same kitchen look clean; self-blur fill gave black/orange bars. (6) Prices in Grace's screenshots are never said (rule §1). (7) A label-less still (bottle facing away) is not usable: reuse a good still as the clip's first frame instead of paying for another still.

## Lessons 2026-10-03 (FUSOU V2, Grace's own script)
- A client's own script may fail the gate (readability grade 9.4, unsupported claims). Use it verbatim only when Ralph says so, record it in `checklist.json` `overrides` (rule, videos, by, date, his quote, real grade): the gate prints it every run and only that video is exempt. Flag unverifiable claims in product_facts, never edit them out silently.
- "Looks like pictures" = Ken Burns on photos and freezes. Motion-first fix: every shot a real moving clip (walk-in/dolly-out from the real-photo bedroom plate, top-down hand slide of a drawer, hand drags a bag out of a cabinet), 4-5 s clips at 1.0x, ~$0.2 each. A reused start frame makes a good dolly-out (grab a frame from the walk-in clip).
- Grace B at 42 s for 136 words = 3.2 words/s; her 706-char script cost ~705 ElevenLabs chars, STT-check found no stutters this time.
- 2026-10-04 TIRTIR Mask Fit Red Cushion: 3 talking-head scripts (light full coverage, label read, sensitive skin), $0, Drive doc, no PDF (Ralph). `tiktok.py video` returned no data in the cloud session (missing setup, fixed in v2), so hooks came from viral/shop/tag data and captions; the gate scans scripts.md, so keep banned phrases out of the rules text too. Job: `ugc/tirtir-red-cushion/`.
- 2026-10-04 TIRTIR v2: `tiktok.py video` works in a cloud session once `bash setup.sh` (Dayone-ai) and `pip install playwright` have run (the v1 "no video data" was a missing setup, not a TikTok block). Rebuilt hooks from 7 real winners: reveal hook (@jawarshere "it's not a concealer, it's a foundation"), label read with the box held to the face (@machyismuch), shade-range loop (@missdarcei). Add a beats-vs-winner table to hooks.md.
- 2026-10-04 Base Laboratories Ingrown Hair Pads + Oil (beauty, AI hands-only, silent: Grace records her own VO): 3 script options each on ONE shared six-beat grid, so one video fits any option; hook text varies per option. 28.2s each, `ugc/base-labs/{pads,oil}/`. Kie $4.85-ish vs $3.46 quote (see README). Lessons: (1) a prompt word like "label" on a bottle whose text is printed on the glass made Nano Banana draw a yellow label: describe the real print ("printed directly on the clear glass, NO separate label"); describe the real cap shape ("squat two-tier teal cylinder, NOT a rubber bulb"). (2) Seedance in a "hands-free" scene adds a light-skinned hand after ~1-2s: negative prompt harder, or use only the clean first seconds. (3) Tilting a held jar turns its lid white and stacks a second cap on a bottle: hold steady, no tilt. (4) Moving two product units together makes them change scale: lock them still and move only the finger. (5) Nano Banana can return a phone-camera UI screenshot (record button, timer): free fix = crop the frame to the clean glass area. (6) Check the shop search for the exact brand first: web search returned First Aid Beauty/Bushbalm facts, not Base's.

- **Hand size and forearm (Ralph 2026-10-04, FUSOU V3 pointing still: "too big, takes the whole screen, did you not remember no forearm"):** the rule "hands from the frame edge, no forearm" applies to EVERY hand prompt, including a pointing hand: write "only the hand and wrist enter from the frame edge, no forearm, hand small (about 15% of frame height), the product stays the hero". Never prompt "whole forearm visible". Free fix for an oversized AI hand: cut the hand with the paste-back mask, scale it down about 45-55% and move it so the wrist sits on the frame edge (`stills/P1_small.png`). Check the first still against the winners' hand size before any clip. Examples: `ugc/fusou-vanity/v3ab/research/pointing_examples.jpg`.
- **Pointing-hand AI clips drift (FUSOU V3, 2026-10-04, $0.164 lost):** Seedance Mini grew the hand + forearm, lit the LED mirror and curled the finger; a skin-colour mask cut the fingertip. For a simple point, animate the CLEAN small-hand still for free instead (`ugc/fusou-vanity/v3ab/hand_still_anim.py`: hand slides in from the frame edge, holds, slides out, slight handheld sway). Only pay for a clip when the hand must do something real (open a drawer, plug in).
- **Zoomed edge check before spending or showing (Ralph 2026-10-04, FUSOU V3 Kling clip: "you should have picked up on the halo before I mentioned it"):** any still that goes to a paid clip, and every clip before Ralph sees it, gets a 2x zoom check on the edges of EVERY person or body part in it (hands, face, hair line, neck, shoulders, full body, held products) and on the first 1 s of frames: halo, sticker outline, smear, colour fringe, shimmer, anything that does not look natural (Ralph 2026-10-04: applies to face and full body too, not only hands). I had even noted "faint halo" and sent it without checking how long it lasted. Paste-back masks are ERODED (13 px), never dilated. Fix the cause in the still (free) before paying for a clip.
