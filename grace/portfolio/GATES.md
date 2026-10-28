# Gates: Grace UGC portfolio site

OWNS: grace/portfolio/**

Scope: a professional, private-by-default portfolio page for Grace (@shewiththeglow) that high-ticket brands can open from a link, showing her real TikTok work as playable videos with real stats, a clear way to contact her, built with the web-design-stack skill.

- [ ] G1: every video the page references exists as a published file, plays as H.264/AAC mp4 under 15 MB, and has a poster image
  CHECK: python3 grace/portfolio/check.py files
  EXPECT: FILES_OK
  EVIDENCE: pending

- [ ] G2: every view/like number on the page matches the meta.json pulled from TikTok this session (no invented stats)
  CHECK: python3 grace/portfolio/check.py stats
  EXPECT: STATS_OK
  EVIDENCE: pending

- [ ] G3: page copy has no banned words (reviewer, "the label says", dashes as punctuation, lorem, TODO) and no price numbers
  CHECK: python3 grace/portfolio/check.py copy
  EXPECT: COPY_OK
  EVIDENCE: pending

- [ ] G4: motion budget holds (one scroll moment at most, reduced-motion path)
  CHECK: python3 .claude/skills/web-design-stack/scripts/motion_check.py grace/portfolio/site
  EXPECT: MOTION_OK
  EVIDENCE: pending

- [ ] G5: Impeccable detector run on the page; each finding fixed or named with its reason
  EVIDENCE: pending

- [ ] G6: Make Interfaces Feel Better review (full mode) ends in Approve
  EVIDENCE: pending

- [ ] G7: screenshots at 390 px and 1440 px looked at full size, light + dark, no console errors, no horizontal scroll
  EVIDENCE: pending

- [ ] G8: page copy run through Humanizer + readability (grade <= 8 for brand-facing copy)
  EVIDENCE: pending

- [ ] G9: only videos Ralph OK'd for the portfolio are shown (AI-made videos handled the way he chose)
  EVIDENCE: pending

- [ ] G10: published as a private Artifact, link sent to Ralph with push + email
  EVIDENCE: pending

- [ ] G11: files in Drive "Grace Tiktok assets" in one "UGC Portfolio" folder (CURRENT - prefix), link sent
  EVIDENCE: pending

- [ ] G12: branch merged to main, Brain job note + session log written, brain check prints BRAIN_OK, Active work line removed
  EVIDENCE: pending
