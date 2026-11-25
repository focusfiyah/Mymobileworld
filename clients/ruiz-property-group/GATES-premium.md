# GATES: Ruiz premium rebuild (stage 4, $0, NO deploy)
Scope: Ralph 2026-11-25: apply the whole web design stack (Impeccable craft floor, Make Interfaces Feel Better, Transitions.dev, one GSAP moment) so the site reads as a premium build. Review page only.
Run from this folder. Browser checks need NODE_PATH=$(npm root -g).

- G1 Craft floor bans absent: no eyebrow/kicker labels, no colored border-left, no emoji icons
  CHECK: grep -c -E 'class="eyebrow"|border-left:[2-9]' site/*.html site/styles.css
  EXPECT: ^(site/[a-z.-]+:0\s*)+$
- G2 Detector clean apart from reviewed padding warnings
  CHECK: python3 detect_summary.py
  EXPECT: DETECT_OK
- G3 Pages load, links resolve, Luigi's headings present, phone on every page
  CHECK: python3 tools_check.py && grep -c "233-0110" site/index.html site/we-buy-houses.html site/property-management.html
  EXPECT: PAGES_OK
- G4 Motion budget and reduced-motion path
  CHECK: python3 "$(ls -d /root/.claude/skills/synced/*/web-design-stack | head -1)/scripts/motion_check.py" site
  EXPECT: MOTION_OK
- G5 Each page at 390 and 1440: no sideways scroll, no console errors, alt text, labels, h1 once; menu, accordion and form states work; reduced motion
  CHECK: node pages_check.js
  EXPECT: PAGES_BROWSER_OK
- G6 Polish review (Make Interfaces Feel Better, full mode) ends in Approve (manual, written in POLISH-REVIEW.md)
- G7 Humanizer pass on every line of copy I wrote (manual, HUMANIZER.md)
- G8 Review artifact published, nothing deployed (manual)
