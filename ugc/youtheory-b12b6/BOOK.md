# Production Book: Youtheory B12B6 Liquid (Grace), 2026-10-26

Sent to Ralph: https://claude.ai/artifact/LvrMBi3CNvBuXW4MCHv16j (2026-10-26, review page v1)

## 1. Job
- Client: Grace  Product: Youtheory B12B6 Liquid, raspberry, 12 x 1 fl oz pouches  Route: hands-only AI + product lock (`.claude/skills/ugc-product-ad/references/product-lock.md`), template `ugc/youtheory-collagen/`
- Job folder: `ugc/youtheory-b12b6/`  Target length: ~23-25 s (68 words at Grace's ~3 words/s)  Shots: 9 (5 HAND / 4 HAND-FREE)

## 2. Gate result (`python3 grace/gate.py ugc/youtheory-b12b6`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | research/playbook.md | OK |
| Audience research | research/audience.md + audience/ (1,746 search phrases, 22 TikTok comments, Reddit) | OK: they say "tired", ask "does b12 give you energy", skeptics present (keep "may") |
| Coach research (shop/tag + video x5) | research/coach.md, shop/, tag/, videos/ | OK: listing 7,757 sold, 4.6 stars; only ready-to-drink pouch in the top 25; Youtheory B12 videos all under 1.4k views |
| Daily viral board | research/viral/viral-2026-10-26.json | OK (no B12 product on today's board) |
| Product facts (source) | research/product_facts.md | OK, 1 claim flagged (Q2) |
| Hooks modeled on named winners | research/hooks.md | Ralph's hook, word for word; on-screen options offered only |
| Humanizer | research/humanizer.md, captions.md | OK, no words changed; line 6 reads like a label (Q2) |
| Readability (grade) | research/readability_v1.txt | 5.7, no override needed |
| Banned-phrase check | gate.py | OK |

## 3. Script (Ralph's, word for word: Q1)
> A pouch a day keeps laziness away. Because sometimes, you don't need more motivation. Your body may need B vitamins! This delicious raspberry-flavored B6 and B12 pouch makes it easy. There are twelve in a box, so I'd stock up on a few! B6 and B12 support normal energy metabolism, and B12 promotes brain health. Tap the orange cart and grab yours while they're in stock!

Only change: "12" written as "twelve" so the voice and timing match. Source of each line: research/line_sources.md.
Line 6b swapped to the box wording "promotes brain health" (Ralph: "3. Say box"). Flags, kept as written: the close is "Tap the orange cart..." instead of Grace's "It's in the orange cart."; "while they're in stock" is soft urgency.

## 4. Shot list (straw in the pouch in EVERY shot, per your note)
| # | VO words | On screen | HAND? | Clip | Room |
|---|---|---|---|---|---|
| S1 | "A pouch a day keeps laziness away." | Pouch with straw on a bedside table, rumpled bed at the edge; hand comes in, grips it and lifts it toward the lens | HAND | Omni 4 s | A bedroom nightstand + snake plant |
| S2 | "Because sometimes, you don't need more motivation." | Pouch alone on the nightstand by a plain alarm clock and books, slow dolly in | HAND-FREE | Omni 4 s | A |
| S3 | "Your body may need B vitamins!" | Hand holds the pouch at chest height, two little shakes (the pouch says shake well), B12B6 big | HAND | Omni 4 s | B bright kitchen, plants |
| S4 | "This delicious raspberry-flavored" | Pouch on the counter by a bowl of fresh raspberries, slow arc | HAND-FREE | Omni 4 s | B |
| S5 | "B6 and B12 pouch makes it easy." | Hand lifts the pouch up out of frame top as if to sip from the straw (no face) | HAND | Omni 4 s | B |
| S6 | "There are twelve in a box, so I'd stock up on a few!" | Grace's real open display box full of pouches; hand sets the straw pouch down beside it (RISKIEST: box print + pouch + hand) | HAND | Omni 4 s | B |
| S7 | "B6 and B12 support normal energy metabolism," | Pouch on an entryway bench by a yoga mat, tote and sneakers, slow dolly in | HAND-FREE | Omni 4 s | C entryway |
| S8 | "and B12 promotes brain health." | Pouch on a plant-filled desk by the laptop and an open notebook, slow push-in | HAND-FREE | Omni 4 s | D plant office |
| S9 | "Tap the orange cart and grab yours while they're in stock!" | ONE pouch with straw held toward the lens, slow push-in | HAND | Omni 4 s | D |

Face: none. Voiceover only (Grace cloned, echo gate <=150 ms), no lip sync.
Setting: 4 real Pexels rooms (rooms/SOURCES.md, colour, not all-white). Bright neutral grade, no text, AI finish last.
Hand (Q3): Grace's hand sheet WITH bracelet, as on Youtheory Collagen: French tips, silver crown ring, gold solitaire, blue silicone band, flat gold link bracelet + pearl chain.
Real product (refs/product_sheet.png, from Grace's photos + the listing): white glossy foil pouch ~6.5 x 15 cm, flat magenta tear-off tab, magenta dot circle, magenta "B12B6", grey "liquid", "promotes brain health*", "helps support energy production*", magenta "raspberry flavor" bar. Grace's pouch has NO "essential daily vitamins" (the listing render does; removed from the sheet). Box = her real display box, torn open along the perforation (front "B6 liquid", three + lines, raspberry splash).
Straw (Q4): the flat magenta tear-off tab torn off, ONE plain white paper straw standing upright in the torn opening (as Ashwagandha v2). Ralph 2026-10-26: "It is a tear off top not screw".

## 5. Order of work (machine time ~35-40 min + your review stops)
All 9 stills at once -> still storyboard on the review page (stop 1) -> S6 test clip as a Flow kit to you, nothing on Kie unless Flow fails (stop 2) -> Flow kits for the other 8 while the Grace voice renders -> cut + QC (2x edges, first second, straw in every frame, REMOVED.md, verify_fix) + compare vs the top winner -> AI finish -> review page (stop 3) -> Drive.
Free fixes first: crop/retime before any reroll.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Round 1 stills, Gemini 3 Pro Image on Kie (spent; wrong screw top from my prompt, rejected) | 9 x $0.09 | 0.81 |
| Stills redo on Kie (or $0 in Ralph's Gemini app) | 9 x $0.09 | 0.81 |
| Product clips, Omni 1.1 Flash: Flow first on your phone (12 credits each, 108 credits) | 9 x $0 | 0.00 |
| ...same 9 on Kie only if Flow fails or you can't (asked first) | 9 x $0.315 | 2.835 |
Expected spend with Flow: $1.62 ($0.81 if the redo is made in your Gemini app). The total includes the Kie fallback so nothing surprises you. ElevenLabs: ~400 chars (Grace cloned).
Month so far (`python3 grace/spend.py`): $168.02 (no cap in October).

TOTAL: $4.455

**Approve?**

## 7. Questions (all of them, now)
1. Use your script word for word (only "12" written as "twelve")?
2. "B12 supports normal nervous system function" isn't on the box/pouch/listing. Keep it, or swap free to "and B12 promotes brain health" (their wording)?
3. Hand: Grace's sheet WITH bracelet (French tips, rings + bracelets, as on Collagen)?
4. Straw: plain white paper straw in the torn-open top, OK? (Or pink to match the pouch?)
5. Stills on Kie ($0.90) or your Gemini app ($0)?
6. On-screen text: default none. Want any?

## 7b. Ralph's answers (2026-10-26: "1. None 2. Yes 3. Say box 4. Yes 5. Yes 6. Kie 7. Yes")
1. Product details correct. 2. Script word for word. 3. Line 6b = "and B12 promotes brain health" (box wording). 4. Hand sheet with bracelet. 5. White paper straw in the torn-open top. 6. Stills redo on Kie ($0.81); clips on Kie too (his earlier "You can also create the stills and shots"). 7. No on-screen text.

## 8. Prompts (final, written with prompt-master; every reference named)
Every still prompt: prompts/still_S1..S9.txt; every Omni clip prompt: prompts/S1..S9.txt; refs per shot: prompts/refs.json. All pass grace/prompt_check.py lint.
Still refs: 1 product sheet, 2 logo + dot circle close-up, 3 "B12B6 liquid" + claims + flavor bar close-up, (S6: 4 real box photo, 5 box print close-up), room photo, Grace's hand sheet on hand shots. Clip refs: 1 the approved still, 2-3 the close-ups, 4 the sheet, 5 hand sheet (hand shots), box close-up (S6). Size first, print letter for letter and colour for colour, straw in every frame, one grip, never flips, hand-free shots say no hand appears at any time, no text, no music or voice.
