# Product facts: Migrastil Extra Strength Neuropathy Cream (2026-11-06)

Sources, all read this session:
- [L] TikTok Shop listing (Migrastil shop), https://shop.tiktok.com/us/pdp/migrastil-neuropathy-cream-with-aloe-shea-essential-oils-for-relief/1729438563366113689 (page text saved: research/page_pdp_migrastil.txt, loaded with Playwright Chromium 2026-11-06).
- [B] Brand site product JSON, https://migrastil.com/products/migrastil-neuropathy-cream.json (saved: research/listing_migrastil_site.json, research/page_migrastil_site.txt).
- [J] Jar label, from Grace's photos + listing back image (refs/real/, refs/jar_back.png; media in Drive).
- [S] coach `shop` output, research/shop/shop-migrastil.json and shop-neuropathy-cream.json.
- Amazon (B09XC6788X): curl got a 3.7 KB stub page; a browser read was refused by this session's permission check, so no Amazon facts are used. camofox: setup printed CAMOFOX_SETUP_OK, but every POST /tabs failed with "Protocol error (Browser.setDownloadOptions) ... legacyInterceptor" (tested twice), so not used.

## Name, size, look
| Fact | Source |
|---|---|
| "Migrastil Neuropathy Cream - Soothing Cream for Feet, Legs, Hands, Etc. Aloe Shea Butter Gentle Clove Moisturizing Body Care Daily. HSA/FSA Eligible" (TikTok title) | L |
| "Migrastil Extra Strength Neuropathy Cream" (brand site title) | B |
| Net weight 4 oz (113 g); "NET WT 4 oz. (113 g)" on label | L, J |
| Dark cobalt-blue round jar, black screw lid; front: "MIGRASTIL", "Extra Strength", "Neuropathy Cream" (lime green), "Gentle, Non-Burning Relief", USA shield "Made in the USA" | J (README) |
| Container type: Jar; Product form: Cream; Body part: Legs, Ft, Hand; Application time: Nighttime | L (Details) |
| Made in USA / "Crafted in USA" / "Made in the USA - Vegan & Cruelty-Free" | L, B, J |
| Seller: Basic Vigor Nutraceuticals, LLC, 312 Passage Gate Way, Wilmington, North Carolina 28412 | L |

## Ingredients (label, back of jar) [J]
Water, Carbopol, Propylene Glycol, Glyceryl Stearate, Tetrasodium EDTA, Aloe Vera, Organic Shea Butter, Stearic Acid, Cetyl Alcohol, Vitamin E, Organic Jojoba Seed Oil, Organic Olive Oil, Almond Oil, Coconut Oil, Phenoxyethanol, Essential Oils of Roman Chamomile, Rosemary, Ginger, Eucalyptus, Lavender, Marjoram, Clove Bud, Ravensara.
- No menthol, camphor, capsaicin or lidocaine in the list (checked line by line). The top competitors list menthol in the title: Hrvsta "with Menthol" (7,953 sold), Earth Essentials "High Menthol Cooling ... with Camphor" (1,820), Raitera "... Menthol" (1,741) [S].
- Almond and coconut oil are in it: tree-nut note for anyone allergic (not for the script, for Grace's comments).

## Listing claims, word for word
| Claim | Source | Use in script? |
|---|---|---|
| "Non-Burning Relief" / "Gentle, Non-Burning Formula" / "Gentle, Non-Burning Relief" | L, J | Yes, it is the label. Say it as the feel: "it doesn't burn". |
| "Our moisturizing cream sinks right in without leaving any residue." | L | Yes ("sinks right in"). |
| "With a subtle, naturally occurring scent from botanicals and essential oils." / "You won't smell like a medicine cabinet." | L | Yes. Note: buyers say it smells "like noxema" (comments). |
| "This cream is designed for regular use. Best results are seen over time with daily use, not just after one use." | L | Yes, as honest framing ("it's an every night thing"). |
| "It's perfect for feet, legs, hands, etc." | L | Yes. |
| "Apply at bedtime for overnight support." | L | Yes (the bedtime ritual). |
| "Helpful if your legs are restless." | L | FLAG: health-type claim; do not say. |
| "Extra Strength Neuropathy Cream for gentle, non-burning relief." | L | Product name only; no promise about nerves. |
| HSA/FSA Eligible | L (title) | OK to say as listed; not checked against an HSA/FSA list. |
| 109.3K sold, 4.3 shown / 4.2 global from 7,075 reviews (5-star 4,958; 1-star 771) | L, S | "Over a hundred thousand sold" is backed (lifetime, TikTok Shop). |
| "Effective, Natural Support for Neuropathy" | B | FLAG: health claim, do not say. |
| "Powerful botanicals reach deep to calm irritated nerves and support circulation" | B | FLAG: nerve/circulation claim the listing can't back; do not say. |
| "Use Daily for Maximum Benefit - Best results seen in 2-4 weeks" | B | FLAG: brand-site only; say "every night" without a timeline. |
| "Non-Greasy & Fast-Absorbing" | B | Yes ("not greasy"). |
| "A Little Goes a Long Way - Long-lasting formula for all-day comfort" | B | "a little goes a long way" OK; "all-day comfort" FLAG. |
| "100% Money-Back Guarantee - Try it risk-free!" | B | Brand-site orders only; TikTok Shop has its own return policy, so do not say it. |
| Price: $32.49 TikTok [L]; $24.99 1-pack, $54.00 3-pack on site [B] | L, B | No price in script (house rule). |

## Health-claim flags (keep out of every script, caption and overlay)
- "Neuropathy" is on the label; the product is sold as Beauty & Personal Care / body care [L]. No line may say it treats, heals, repairs, cures or "gets to the root" of neuropathy or nerve damage (creator @amazingaffiliate said "gets to the root"; a viewer answered "It gets to the root of the pain? Try reading some of the unhappier reviews...").
- No time-to-relief promise (creator @jeff_el_colombiano: "in a matter of thirty minutes or less" is not on the listing).
- No "no more burning, no more tingling" (creator @aunteeknows caption) and no "only thing that worked".
- Say what it is and how it feels: gentle, non-burning, no menthol in the list, sinks in, light botanical scent, used at bedtime on feet, legs, hands. Results talk only as "people say" with mixed honesty ("it doesn't take everything away, but...").
- Diabetic feet: suggest nothing medical; no "calling all diabetics" claim line.
