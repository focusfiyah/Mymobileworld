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

## v2 (2026-10-28, Ralph: "the portfolio picture of Grace. Give me something better. Where she is smiling ... reduce the videos make it a top 10. If the brand wants to see more they can visit her Tiktok")
- [x] V2-G1: hero shows a smiling photo of Grace at rest (frame 0.55 s of her own intro, light free finish), intro plays with sound + captions on tap
  EVIDENCE: 2026-10-28 Playwright: #watch -> paused False, muted False, captions showing; 2x face crop before/after checked, no halo
- [x] V2-G2: exactly 10 videos, ranked by views, ending in a TikTok link tile
  EVIDENCE: 2026-10-28 10 articles, 10 rank badges, tile links to tiktok.com/@shewiththeglow; check.py files 22 refs FILES_OK, stats 24 STATS_OK, copy grade 6.9 COPY_OK, MOTION_OK, detect 0 findings, nesting 0 errors
- [x] V2-G3: republished to the same Artifact (v2), dropped media removed; Drive CURRENT v2 doc + photo (149,479 bytes, matches), v1 doc in Older versions
  EVIDENCE: 2026-10-28 version 1793193647-8e38; Drive 1qnlFTBNn-NXKJUEUtAHgpfPR6fjsc4_snRQ_WySBzOg + 19m-NsTnEw6xmoYsbJGGf3qjdTmMjpA9h
- [x] V2-G4: hero photo = Ralph's pick (his circled frame, "Use this one"): closed-lip smile at 33.00 s of her intro, same light free finish; republished (version 1793194831-4cae); Drive CURRENT - Portfolio photo v2.jpg 1zY707s_uwit-wVhzOa9Kw2sWHV9qKHMx (198,811 bytes, matches) + CURRENT - Portfolio v2 doc 1b882gfZXD1BVI3XsaDFFzAWMoJbwTr38Xy1R_iYoefI; earlier photo + draft doc in Older versions
  EVIDENCE: 2026-10-28 frames 32.3-33.1 s compared at 2x; 33.00 s matches his circled frame (lips closed, eyes open)

## v3 (2026-10-30, Grace: "super light green almost white background color", "Don't say 2.8M views", "Remove 11.4K followers · 66.1K likes · 1,229 videos posted")
- [x] V3-G1: page background is a super light green, almost white (#f1f8f2); pink stays as the accent
  EVIDENCE: 2026-10-30 Playwright screenshots 390 px + 1280 px checked; no horizontal scroll (scrollWidth = width)
- [x] V3-G2: no "2.8M" and no account numbers (followers, likes, videos posted) anywhere on the page
  CHECK: python3 grace/portfolio/check.py stats
  EXPECT: STATS_OK
  EVIDENCE: 2026-10-30 starburst, record line and tile count removed; card 1 Views 2.8M put back (Ralph 2026-10-30: "you didn't put the view count for her number 1 video"); check.py now fails on 2.8M or any account stat; 18 stats STATS_OK, copy grade 6.8 COPY_OK
- [x] V3-G3: republished to the same Artifact (version 1793325070-1085), media kept
  EVIDENCE: 2026-10-30 publish result Version 4
- [ ] V3-G4: Drive CURRENT doc updated (waiting for Grace's remaining notes, then one update)
