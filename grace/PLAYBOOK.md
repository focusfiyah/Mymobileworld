# Grace playbook

One place for everything we've learned about making Grace's ads. Add to it after every Grace job (newest
lesson goes in the section it belongs to, with the date). Paste this file into a new chat to start a Grace job.

Grace is Ralph's client: UGC / TikTok Shop ads. Jobs so far: Fungix nail serum (real takes, 2026-09-18),
Restlex "2am" couple skit (AI, Grace as the wife), Carpe Vanilla Peach (hands-only AI, 2026-10-01). Fashion
products follow the same rules.

## 1. House rules (never break)
- **No personal-use lines** ("I use it", "it worked for me", "smells like…") unless true for Grace. Review
  findings are "reviewers say", never her experience.
- **No false scarcity.** No "selling out" / "ends tonight". Use "don't put it off" or a real seasonal reason.
- **Exact claim wording** from the label or listing. Never "cures / kills / fixes", never a timeframe unless the
  label gives one ("clinically tested… up to 100 hours when used as directed" is fine because the label says it).
- **One honest caveat** in every video, said calmly like a friend.
- **Detached CTA:** give permission to scroll on ("If it doesn't bother you, skip this. If it does, it's in the orange cart.").
- **Words to avoid:** "you NEED this", "obsessed", "game changer", "miracle", "so cute", reading off the size range.
- Disclosure in the caption: `#ad` or the brand's partner tag.

## 2. Sales psychology
| Principle | How we use it |
|---|---|
| Pain first | The hook names something the viewer already hates (toes tucked under the table, waistband digging in). Review complaints make great hooks. |
| Sell the moment | Put them in the exact scene: shoes off at a friend's house, the salon polish wall, the 5-minute get-ready. |
| Move away from pain | Escaping embarrassment sells faster than promising pretty. The product is the way out. |
| Clarity, not convincing | Calmly show why what they do now (hiding it, painting over it) doesn't fill the gap. Let them conclude. |
| Remove uncertainty | Every body answers: what's in it, how to use it, how often. Most hesitation is missing information. |
| Detachment builds trust | Honest review voice, one con, no pressure. |
| Price pushback = value question | Show 3–5 looks/uses before the price so it reads as several outfits. |
| Specificity | Exact numbers beat adjectives ("a pea-sized amount", "twenty-five percent"). |
| Take the shame out | Gift angle ("your dad will never buy this himself"): the pain is felt for someone else, and it gets shares. |

## 3. Hooks
- Types: problem call-out, result first, comment reply, curiosity gap, contrarian, price shock, visual pattern
  break, POV, social proof (true only), direct address.
- **Stack two layers:** spoken problem + on-screen text + product moving. The first second must make sense with the sound off.
- Film 3–4 takes of each hook; give each video **different on-screen bubble text** (TikTok treats them as distinct).
- Proven angles: timing ("boots season, nobody's looking at your feet"), cover-up ("painting over it isn't a plan"),
  read-the-label, "you're probably doing it wrong" tutorial, gift for a relative, "watch this before you use it".

## 4. Script structures
- **Product / tips (Fungix, Carpe):** hook (pain) → clarity → claim (exact wording) → how to use (what / how / how often)
  → honest caveat → detached CTA.
- **Fashion:** hook (pain) → fit facts (height, size, how it runs, where it hits) → proof (back turn, phone in pocket,
  sit-down, sheer check) → honest take (times worn, one love, one con, best for whom) → 3–5 looks → price → CTA.
- **Tutorial beats hard sell.** Carpe research: the hard-sell video got 830k views but 0.02% saves; the "watch this
  before you use it" tips video got 1.4M views and 0.71% saves. Tips also answer the viral complaints.
- Get Grace's real facts before writing (fit, fabric, sheer, pockets, times worn, love/con, styling). Never invent them.

- **Script checklist (standard).** Every script, before the plan goes to Ralph (Ralph 2026-10-01, after the Plant Therapy hook shipped with no on-screen text):
  (1) tiktok-shop-coach: research + 3 hook options (spoken line AND on-screen hook text) modeled on proven videos;
  (2) humanizer pass on the script and caption; (3) after the cut, `tiktok.py compare <viral video> <our cut>` and fix
  what it shows (hook text in frame 0, pace, cuts) before sending.

## 5. Pacing and edit
- Fast UGC speech: **3.0–3.6 words/sec**. Target ~30 words hook, ~60 body, ~20 CTA ≈ 35s after pauses are cut.
  Fashion default 30–45s. Category median is a good length check (Carpe: 35s).
- Cut every pause, never clip a word; end on a visual beat, not the last syllable.
- Retention: a steep drop in the first 1–2s = the hook failed; a slow slide mid-video = a beat runs too long.
- Say numbers as words in the script ("twenty-five percent") so captions and timing match.
- Real takes: film hook / body / CTA as separate files, 3–4 takes each, original HD files; keep body takes whole.
  Mix N hooks × M bodies × K CTAs into combo ads (`ugc-take-combos` skill).
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
- **Voiceover ads: keep her mouth out of frame while the voice talks** (Ralph 2026-10-01, "why are her lips not
  moving"): Ralph then preferred lip sync over chin-down crops (crops cut the product off): `lipsync.py` in
  `ugc/carpe-mountain-breeze/`, $0.04/s, submit one at a time (parallel calls get "server busy", $0).
  Lip sync smears anything that passes in front of the mouth (the stick): check every frame where the product
  crosses the face and swap those frames back to the original clip
  (or keep only the lip-synced mouth in a soft oval over the original; the lip-synced clip runs ~2 frames late).
- **Test ONE clip before any batch** (Ralph 2026-10-01, after $1.93 was lost on two prompt mistakes in one day): render
  the cheapest affected clip, check it, then ask for the rest. Report the running total vs the quote at every step.
- Routes and costs: `ugc-product-ad` skill. Hands-only template: `ugc/carpe-vanilla-peach/` ($3.52 for 36s).

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

## 8. To add later
- Looping (endings that flow back into the start for rewatches): not covered yet; add here when we need it.
