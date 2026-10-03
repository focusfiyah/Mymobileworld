# FUSOU 2-in-1 Vanity Desk: 6 hands-only videos (Grace)

**Client: Grace** (Ralph, 2026-10-02). Product: https://shop.tiktok.com/us/pdp/1732251413004981161 ($639.99,
4.9★/83, 648 sold, white or black). Brief: Grace's hands only, voiceover = ElevenLabs Grace B (not Grace's own recording), 6 video styles × 6 scripts,
short, no text burned in (give on-screen text options), share in Drive. Rules: `grace/PLAYBOOK.md`.

Status: **2026-10-03: ALL 6 CUTS v1 READY FOR RALPH'S REVIEW: `out/fusou_v1.mp4` ... `out/fusou_v6.mp4` (17.0-21.8 s, 5-9 shots, 2.7-4.2 cuts/10 s, -15.6 to -16.6 LUFS), sheet `out/cuts_sheet.jpg`. Built by `cut.py` (shots on Grace B word timings, clips 1.0x or reversed, never stretched; free push-ins `kb.py` on real photos; finish grain; tap click + pop tick CC0 `sfx/`; brown-noise room tone; real 3-boxes photo card pops on "three boxes", left side clear of TikTok buttons). VO: Grace B V2-V6 made (1,680 chars, `vo.py`), all 6 tightened free (`vo_prep.py`: pauses 0.25 s, 1.2x). Ralph chose FREE for M5a: 0.45 s of hand on the door, then the real open-cabinet photo. M3c unused (drift), V6 uses M3a reversed. Kie total $4.28 vs $4.54 quote (balance 794.8 cr). Ralph notes round 1 (V2): real shelf items showed ON her hand (M3a, M3b) and part of the wrist vanished (M4a) because the hand mask dropped pixels that are skin-coloured in the real photo (gold bottles, brushes, wood). Fix `--hull`: fill the hand outline (convex hull, extended to the frame edge) with AI skin; M3a/M3b/M4a redone, V2 V3 V6 re-cut (free). Round 2 (V3-V6): same see-through/missing-wrist bug in the outlet + door clips, and the M2 still put the wrist BEHIND the hanging dryer (impossible). Fix: `--hull` on all hand clips (edge reach 120 px, +-2 frames), `qc_hands.py` checks every frame vs raw, outlet shots cropped 560x996+0+284 so the wrist exits at the frame edge (no dryer crossing). V2-V6 re-cut (free). Round 3 (V2): wrist still cut at the lower right as she opened the stool drawer (outline missed the corner over wall/floor). Fix: M4a object area widened to the right edge (`--ai-box 110,520,720,1010`), checked 7 frames vs raw. V2 V3 re-cut. NEXT: Ralph checks V2 -> Drive (Grace Tiktok assets/FUSOU folder 1LDxaLUgsy_QR0Nq_9B7vokF_JqaYy1hx) + update the scripts doc (still says Grace's own voice).**

- `scripts.md`: the 6 scripts (time / voice / hands shot), 3 on-screen hook options + post caption per video,
  product facts with sources, research notes. Same content as the Drive doc.
- `refs/`: 20 listing photos (`listing_sheet.jpg` = contact sheet).

## Styles
1. Lights On (dark-to-light mirror reveal) 2. Drawer by Drawer (ASMR tour) 3. Count With Me (value stack)
4. The Mirror Is a Door (hidden cabinet) 5. Get Ready Hands (outlet + USB routine) 6. Clear the Counter (clutter → organized)
Each: curiosity hook → pain → selling points → one honest caveat (6 ft wide / build time / only 2 outlets) →
real urgency (ships in 3 boxes that can arrive on different days + holidays). ~19-21s at 3.3 words/s, grade 1.7-3.1.

## Research (tiktok-shop-coach, 2026-10-02)
- `shop "vanity desk"`: HONGWAY $107 21k sold; FUSOU 47" $338 8k; this 71" FUSOU listing family 2.1k sold.
- `tag vanitydesk`: @ivy.rogers3 2.3M (6s, mirror light turning on), @teddyandhudson 363k (18s, price-shock hook,
  one feature per cut with a hand: lights, outlet + dryer, glass-top drawers).
- Same vanity: @katyhogar (Spanish walk-through, confirms 12 drawers + 2 in the stool), @abigailrodriguez767: 1-2k views,
  no hooks. @missathena.rose: two 8-9 min build videos ("chaotic").
- Listing quirk: title says 14 drawers, bullets say 12 → 12 in the vanity + 2 in the stool.

## AI route quote (only if Ralph picks it)
Per video ~6 shots: 6 stills × $0.09 + 6 clips × 4s × $0.041 = $1.52; 6 videos ≈ $9.15 (+ ~$0.25 per redone shot).
Voice = ElevenLabs Grace B (bGrsdLmwBbYUgHRuMFOI, eleven_v4), Ralph 2026-10-02. Risk: a 71" vanity with 12 drawers, 2 mirrors and a cabinet door is
hard to keep consistent across AI shots; Grace's real footage will look truer.
