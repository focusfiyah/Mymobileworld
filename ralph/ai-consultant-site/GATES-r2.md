# Gates: round 2, redesign options (Ralph 2026-10-28: outside feedback says the design could be better; "make it pop", "more dynamic")

OWNS: ralph/ai-consultant-site/r2/**

Scope: three different design directions as working sample pages (same content, same rules: bright, anonymous clients,
no prices, never name Claude/Android/"mobile app", clips muted), shown on the review Artifact with phone and desktop
screenshots and a short screen recording each; Ralph picks one, then it replaces the live page.
Ralph's "more dynamic" overrides the skill's one-scroll-moment budget; every option still has a reduced-motion path.
MP = ralph/ai-consultant-site/r2

- [x] G1: each option (a, b, c) renders at 390 and 1440 wide, no console errors, no sideways scroll
  CHECK: cd /home/user/Mymobileworld && for x in a b c; do SITE=$PWD/ralph/ai-consultant-site/r2 PAGE=$x.html timeout 300 python3 ralph/ai-consultant-site/verify.py render | tail -1; done | sort | uniq -c
  EXPECT: 3 RENDER_OK
  EVIDENCE: met 2026-10-28: 3 RENDER_OK (a, b, c at 390 + 1440, no console errors, no sideways scroll)
- [x] G2: copy rules pass on each option (no dashes, banned words, prices; grade 8 or lower)
  CHECK: cd /home/user/Mymobileworld && for x in a b c; do SITE=$PWD/ralph/ai-consultant-site/r2 PAGE=$x.html python3 ralph/ai-consultant-site/verify.py copy | tail -1 | cut -d, -f1; done | sort | uniq -c
  EXPECT: 3 COPY_OK
  EVIDENCE: met 2026-10-28: 3 COPY_OK (grade 4.4 / 4.3 / 4.5)
- [x] G3: no client names, numbers, "Claude", "Android" or "mobile app" in any option
  CHECK: cd /home/user/Mymobileworld/ralph/ai-consultant-site/r2 && grep -ciE 'claude|android|mobile app|grace|rameau|diaspo|576' a.html b.html c.html | awk -F: '{s+=$2} END{print "HITS",s}'
  EXPECT: HITS 0
  EVIDENCE: met 2026-10-28: HITS 0 (a colour code #52576a had matched 576; changed to #51566a)
- [x] G4: each option has a prefers-reduced-motion path and its text shows with JavaScript off
  CHECK: cd /home/user/Mymobileworld/ralph/ai-consultant-site/r2 && grep -c 'prefers-reduced-motion' a.html b.html c.html | awk -F: '$2>0{n++} END{print "RM",n}'
  EXPECT: RM 3
  EVIDENCE: met 2026-10-28: RM 3; text is plain HTML, scroll effects only add motion
- [x] G5: screenshots at 390 + 1440 and a screen recording of each option, looked at full size (no overlap, cut-off text, blank tiles)
  EVIDENCE: met 2026-10-28: full-page shots at both widths + C chapter shots looked at; fixed A word-swap overlap, A/C sideways overflow, B grid + chat text colour, A hook contrast; 3 recordings (27 s each) checked as frame strips
- [x] G6: review Artifact updated with the three options (live sample links + images + recordings); phone push + email sent
  EVIDENCE: met 2026-10-28: https://claude.ai/artifact/F6TEtGRLuofgeNG5hhFnP5 (new URL; the old review page RA6Ytv... was not reused because this session no longer had its publish), push requested, Gmail 1a1843ada0180426
- [ ] G7: Ralph picked an option
  EVIDENCE:
- [ ] G8: Brain note + session log updated, my Active work line removed, BRAIN_OK
  CHECK: cd /home/user/Mymobileworld && python3 tools/brain/check.py --terms "redesign options,AI consultant" | tail -1 | cut -c1-8
  EXPECT: BRAIN_OK
