# GATES: Ruiz multi-page review build (stage 3, $0, NO deploy)
Scope: Ralph 2026-11-25: put Luigi's edited copy on the site as separate pages, review page only, do not deploy.
Run from this folder. Browser checks need NODE_PATH=$(npm root -g).

- G1 Three pages exist
  CHECK: ls site/index.html site/we-buy-houses.html site/property-management.html | wc -l
  EXPECT: ^3$
- G2 No template blanks or invented contact details on any page
  CHECK: grep -ciE "\[Your|lorem|TODO|555|\(516\)|@yahoo|Ralph|Azariah" site/*.html
  EXPECT: ^site/index.html:0\nsite/property-management.html:0\nsite/we-buy-houses.html:0$
- G3 Every internal link and image resolves, headings from Luigi's copy are present
  CHECK: python3 tools_check.py
  EXPECT: PAGES_OK
- G4 Motion budget
  CHECK: python3 "$(ls -d /root/.claude/skills/synced/*/web-design-stack | head -1)/scripts/motion_check.py" site
  EXPECT: MOTION_OK
- G5 Each page: no horizontal scroll at 390 and 1440, no console errors, every image has alt, every control has a label
  CHECK: node pages_check.js
  EXPECT: PAGES_BROWSER_OK
- G6 Review artifact published, nothing deployed to Netlify (manual)
- G7 Copy read for AI tells (manual)
