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
- **Text hook = curiosity only** (Grace, 2026-10-01): 5-7 words, never names the product, makes them ask "what?"
  ("Nobody puts this on a beard"). The spoken hook does a different job (names the pain).
- **Curiosity loops all the way through** (2026-10-01, from @dus_davis): answer one question and open the next in
  the same breath; an odd claim said without explanation keeps them watching. Mid-video overlays can open loops too.
- **Stack two layers:** spoken problem + on-screen text + product moving. The first second must make sense with the sound off.
- Film 3–4 takes of each hook; give each video **different on-screen bubble text** (TikTok treats them as distinct).
- Proven angles: timing ("boots season, nobody's looking at your feet"), cover-up ("painting over it isn't a plan"),
  read-the-label, "you're probably doing it wrong" tutorial, gift for a relative, "watch this before you use it".

## 4. Script structures
- **Grace's default (2026-10-01):** curiosity-loop hook → pain body → selling point / solution → urgency CTA.
  Urgency must be real (a season, a date, an event), never fake scarcity.
- **Product / tips (Fungix, Carpe):** hook (pain) → clarity → claim (exact wording) → how to use (what / how / how often)
  → honest caveat → detached CTA.
- **Fashion:** hook (pain) → fit facts (height, size, how it runs, where it hits) → proof (back turn, phone in pocket,
  sit-down, sheer check) → honest take (times worn, one love, one con, best for whom) → 3–5 looks → price → CTA.
- **Tutorial beats hard sell.** Carpe research: the hard-sell video got 830k views but 0.02% saves; the "watch this
  before you use it" tips video got 1.4M views and 0.71% saves. Tips also answer the viral complaints.
- Ask what Grace has already filmed before scripting; the script must match the footage (2026-10-01 Viking:
  she'd filmed hands-only on the beard while the script talked about head curls).
- Get Grace's real facts before writing (fit, fabric, sheer, pockets, times worn, love/con, styling). Never invent them.

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
- Voices: ElevenLabs **Grace B** `bGrsdLmwBbYUgHRuMFOI` (eleven_v4) for voiceovers; Grace's Seedance clone
  `3dmagVYZFvrGkBbWWmGC` for AI skit dialogue.
- Before the first paid image: confirm the real product (top, cap, label, size) and the hand/person details
  (nail length). Ask before every paid generation, with the exact cost. Free fixes first.
- Routes and costs: `ugc-product-ad` skill. Hands-only template: `ugc/carpe-vanilla-peach/` ($3.52 for 36s).

## 7. Results log (add one line per job)
- 2026-09-18 Fungix: Grace's real takes (hook/body/CTA) cut into combo ads. Then 5 new script angles written:
  `fungix/grace-script-angles.md`.
- 2026-10-01 Carpe Vanilla Peach: 36.6s hands-only tips ad, $3.52 vs $2.53 planned; waiting on notes.
  Open: the "peach candle" scent line needs Grace to have smelled it.
- 2026-10-01 Viking Revolution Curl Cream for Men: script v3 for Grace's hands-only footage of it on her
  husband's beard (hook "he'd never buy it himself"), `ugc/viking-curl-cream/README.md`. Ralph's structure: hook, problem, product, experience, benefit, CTA.

## 8. To add later
- Looping (endings that flow back into the start for rewatches): not covered yet; add here when we need it.
