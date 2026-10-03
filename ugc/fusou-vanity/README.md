# FUSOU 2-in-1 Vanity Desk: 6 hands-only videos (Grace)

**Client: Grace** (Ralph, 2026-10-02). Product: https://shop.tiktok.com/us/pdp/1732251413004981161 ($639.99,
4.9★/83, 648 sold, white or black). Brief: Grace's hands only, voiceover = ElevenLabs Grace B (not Grace's own recording), 6 video styles × 6 scripts,
short, no text burned in (give on-screen text options), share in Drive. Rules: `grace/PLAYBOOK.md`.

Status: **DONE 2026-10-03: all 6 APPROVED by Ralph and in Drive (Grace Tiktok assets / FUSOU folder 1LDxaLUgsy_QR0Nq_9B7vokF_JqaYy1hx, sizes match): V1 1E-Tffp3nBT-ofMLtamdnXcm0G_zpIszA, V2 1CDcz7iwcGer8ru5uBObmjdycZZcaroLc, V3 1MHezZ8ea6r6NtUaQK0HymGZ2ZBvbgZCR, V4 1FNw1mZXHC9JpZW-0vxv8BhRCH_sDl9zh, V5 19EtRaHqmmEKosk9TLxmCb5zZYeBtxKRC, V6 1zuSTR7qUdmGk1Ilzz_3Yd_qOlJYh0VrV. Scripts doc 1kKPDR1Cv8RFQPYBhTnEQ0dLt2V8EK_-lZ5up3IPuwCs overwritten with the FINAL scripts (timed Grace B lines, on-screen per line, hooks, captions; `build_doc.py` -> `out/fusou_scripts_final.html`). Cost: Kie $4.28 vs $4.54 quote; ElevenLabs Grace B 331 + 1,680 + 610 chars. Rebuild any cut: `python3 cut.py N`. UPDATE 2026-10-03 (script gate round): full PLAYBOOK §4 checklist run (`checklist.json`, `research/`), gate OK (plan + cut). Humanizer fixes re-voiced (177 ElevenLabs chars, Ralph OK): V1 "It's almost six feet wide, so measure your wall first." (`vo_line.py`), V3 "That's five things in one order." (`vo_cta.py`). V1 re-cut to Grace structure, each shot on its words (tap / bathroom counter / light colours / lipstick at the lit mirror / wide / CTA): 0.5 -> 2.0 cuts per 10 s. Hook option "my teenage self would be SCREAMING" added (V1, V3). V1, V3 and the scripts doc replaced in Drive in place (sizes match). V1 DARK ROOM (Ralph): the light line is one shot with the room going dark (`darkroom.py`, LED mask `refs/v1s3_led_mask.png` = lit frame minus the real unlit photo), LEDs cold white -> warm white (dip on "dims") -> warm yellow (the listing's 3 modes) with a tap click each; free. Hook also starts in the dark room: the LED ring lights up at the tap (`refs/m1a_led_mask.png`, `--on 1.22 1.47`). V1 + doc replaced in Drive (size matches). Ralph: "I like it". Same dark opening on the V3 + V5 mirror shots (Ralph OK); V3, V5 + doc replaced in Drive (sizes match). ALL 6 FINAL.**

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
