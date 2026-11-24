# GATES: Ruiz Property Group preview landing page (stage 2, $0)
Scope: Ralph 2026-11-24: $750 job, build a preview so Luigi sees the vision; own brand, generic imagery, free tools only.
Run from this folder. Browser checks need NODE_PATH=$(npm root -g).

- G1 Site files and 7 images exist
  CHECK: ls site/index.html site/styles.css site/app.js site/img/*.jpg | wc -l
  EXPECT: ^10$
- G2 Every image is listed with a licence
  CHECK: grep -c "^| img/" SOURCES.md
  EXPECT: ^7$
- G3 No placeholder text, no invented contact details
  CHECK: grep -ciE "lorem|TODO|555|\(516\)|@yahoo|Ralph|Azariah" site/index.html
  EXPECT: ^0$
- G4 Motion budget
  CHECK: python3 "$(ls -d /root/.claude/skills/synced/*/web-design-stack | head -1)/scripts/motion_check.py" site
  EXPECT: MOTION_OK
- G5 No horizontal scroll, no console errors, alt text, labels, form validation, reduced motion (Chromium)
  CHECK: node /tmp/ruizsite/t.js
  EXPECT: errors \[\]
- G6 Live URL serves html, css and js correctly
  CHECK: curl -sSI https://ruiz-property-group-preview.netlify.app/styles.css | grep -i content-type
  EXPECT: text/css
- G7 Impeccable detect: only the 4 reviewed cramped-padding warnings (full-bleed sections whose inner wrapper holds the gutter) (manual)
- G8 Copy read for AI tells, Humanizer pass (manual)
