# Gates: Grace UGC portfolio site

OWNS: grace/portfolio/**

Scope: a professional, private-by-default portfolio page for Grace (@shewiththeglow) that high-ticket brands can open from a link, showing her real TikTok work as playable videos with real stats, a clear way to contact her, built with the web-design-stack skill.

- [x] G1: every video the page references exists as a published file, plays as H.264/AAC mp4 under 15 MB, and has a poster image
  CHECK: python3 grace/portfolio/check.py files
  EXPECT: FILES_OK
  EVIDENCE: 2026-10-28 check.py files -> 33 media refs, 49.3 MB, FILES_OK

- [x] G2: every view/like number on the page matches the meta.json pulled from TikTok this session (no invented stats)
  CHECK: python3 grace/portfolio/check.py stats
  EXPECT: STATS_OK
  EVIDENCE: 2026-10-28 check.py stats -> 16 stats checked, STATS_OK; negative controls (changed number, AI video id) both FAIL as expected

- [x] G3: page copy has no banned words (reviewer, "the label says", dashes as punctuation, lorem, TODO) and no price numbers
  CHECK: python3 grace/portfolio/check.py copy
  EXPECT: COPY_OK
  EVIDENCE: 2026-10-28 check.py copy -> 517 words, grade 6.6, COPY_OK; control (reviewers, dash, $20) FAILS as expected

- [x] G4: motion budget holds (one scroll moment at most, reduced-motion path)
  CHECK: python3 .claude/skills/web-design-stack/scripts/motion_check.py grace/portfolio/site
  EXPECT: MOTION_OK
  EVIDENCE: 2026-10-28 motion_check.py -> scroll-driven 0/2, gsap 0, reduced-motion path True, MOTION_OK

- [x] G5: Impeccable detector run on the page; each finding fixed or named with its reason
  EVIDENCE: 2026-10-28 impeccable detect --json index.html -> [] (0 findings) after neutral shadows + 0.78rem minimum text

- [x] G6: Make Interfaces Feel Better review (full mode) ends in Approve
  EVIDENCE: 2026-10-28 MIFB full review: concentric radii 28=18+10, shadows not borders, tabular-nums, balance/pretty, image outline black 0.1, scale 0.96, no transition:all, 44px hit areas, 2px icons beside 700 text, currentColor icons -> Approve

- [x] G7: screenshots at 390 px and 1440 px looked at full size, light + dark, no console errors, no horizontal scroll
  EVIDENCE: 2026-10-28 Playwright 390 (2x) + 1440, normal + reduced motion: scrollWidth = viewport, fonts loaded, no page errors (one 404 = favicon on the local test server); screenshots viewed full size. Single committed pink look (no dark variant by choice, colors explicit)

- [x] G8: page copy run through Humanizer + readability (grade <= 8 for brand-facing copy)
  EVIDENCE: 2026-10-28 Humanizer pass (triad + heading-repeat lines rewritten); readability grade 6.6 via check.py copy

- [x] G9: only videos Ralph OK'd for the portfolio are shown (AI-made videos handled the way he chose)
  EVIDENCE: 2026-10-28 15 videos + intro, all self-filmed (Ralph: 'Her filmed videos only'); AI ids blocked in check.py

- [x] G10: published as a private Artifact, link sent to Ralph with push + email
  EVIDENCE: 2026-10-28 https://claude.ai/artifact/JeSC2FCYMuNH3RsREQDR2C v1; push + email sent (see session)

- [x] G11: files in Drive "Grace Tiktok assets" in one "UGC Portfolio" folder (CURRENT - prefix), link sent
  EVIDENCE: 2026-10-28 Drive Grace Tiktok assets/UGC Portfolio (Grace) 1Y3o9H--fhMzCiGk0yxg1JwWuy4Qxc0Mu, CURRENT - Portfolio v1 doc (read back OK)

- [x] G12: branch merged to main, Brain job note + session log written, brain check prints BRAIN_OK, Active work line removed
  EVIDENCE: 2026-10-28 merged to Mymobileworld main 3d211040; vault 5dd0721; brain check BRAIN_OK; Active work line not on main (never landed), none to remove
