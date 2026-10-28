# Gates: Ralph AI consultant landing page (C, studio reel)

OWNS: ralph/ai-consultant-site/**

Scope: a free one-page site at https://focusfiyah.github.io (repo focusfiyah/focusfiyah.github.io) that markets Ralph as an AI consultant: reel of real muted clips up top, what he builds, anonymous client work, Day One AI channel, AI receptionist, custom tools, and a working free-consult form to life22watch@gmail.com.

- [x] G1: page renders at 390 and 1440 wide with no console errors and no sideways scroll
  CHECK: python3 ralph/ai-consultant-site/verify.py render
  EXPECT: RENDER_OK
  EVIDENCE: met 2026-10-28: RENDER_OK (390 + 1440, no console errors, no sideways scroll)

- [x] G2: first phone viewport (390x844) shows the name, the one-line pitch and the consult button
  CHECK: python3 ralph/ai-consultant-site/verify.py hero
  EXPECT: HERO_OK
  EVIDENCE: met 2026-10-28: HERO_OK

- [x] G3: no client names, handles, phone numbers or real people's details in the site files (checker tested on a positive control)
  CHECK: python3 ralph/ai-consultant-site/verify.py privacy
  EXPECT: PRIVACY_OK
  EVIDENCE: met 2026-10-28: PRIVACY_OK; control tripped on 'Grace sent it; call Diaspo at 718-576-2667'

- [x] G4: every clip is silent (no audio stream), at most 1.6 MB, and the whole site is at most 15 MB
  CHECK: python3 ralph/ai-consultant-site/verify.py media
  EXPECT: MEDIA_OK
  EVIDENCE: met 2026-10-28: MEDIA_OK, 27 media files, site 4.06 MB, no audio streams

- [x] G5: copy rules: no dashes as punctuation, no banned words, no prices, readability grade 8 or lower
  CHECK: python3 ralph/ai-consultant-site/verify.py copy
  EXPECT: COPY_OK
  EVIDENCE: met 2026-10-28: COPY_OK, 592 words, grade 6.7

- [x] G6: motion budget passes (web-design-stack motion_check)
  CHECK: python3 ralph/ai-consultant-site/verify.py motion
  EXPECT: MOTION_OK
  EVIDENCE: met 2026-10-28: MOTION_OK (1 scroll moment, reduced-motion path)

- [x] G7: Impeccable detector has no findings left on index.html (or each one named with its reason in README)
  CHECK: python3 ralph/ai-consultant-site/verify.py detect
  EXPECT: DETECT_OK
  EVIDENCE: met 2026-10-28: DETECT_OK (font swapped from Geist, contrast/leading/padding fixed)

- [x] G8: the form has name, email and message fields, posts to FormSubmit for Ralph's address, and shows sending / sent / error states
  CHECK: python3 ralph/ai-consultant-site/verify.py form
  EXPECT: FORM_OK
  EVIDENCE: met 2026-10-28: FORM_OK (empty, bad email, success and server-error states)

- [x] G9: the copy went through Humanizer (proof file saved)
  EVIDENCE: met 2026-10-28: proof/humanizer.md (4 tells fixed)

- [x] G10: Ralph saw the full page on the review Artifact and said OK
  EVIDENCE: met 2026-10-28: Ralph on v3 preview: "Okay, this is very good. Let's move forward."

- [x] G11: https://focusfiyah.github.io is live and serves this page
  CHECK: python3 ralph/ai-consultant-site/verify.py live
  EXPECT: LIVE_OK
  EVIDENCE: met 2026-10-28: LIVE_OK, https://focusfiyah.github.io serves this index.html

- [x] G12: a test message sent through the live form reached life22watch@gmail.com
  EVIDENCE: met 2026-10-28: after Ralph activated, FormSubmit replied success true and Gmail shows 'New consult request from your site' at 05:57 UTC (message 1a18115b29a7097d)

- [x] G13: Brain note + session log written and tools/brain/check.py prints BRAIN_OK
  EVIDENCE: met 2026-10-28: Brain/Jobs/AI Consultant Site.md + session log, BRAIN_OK

## Round 2: "Is this a fit?" section (Acuna idea 6, Ralph 2026-10-28: "Do 6. Since my consultant landing page is live")

- [x] G14: the page has an "Is this a fit?" section (4 good-fit lines, 4 skip lines) right above the form, built with web-design-stack, every claim already true for Ralph's work (no income promise, consented calls only, no fake reviews, he checks before live)
  EVIDENCE: 2026-10-28: section.fit in index.html on branch fit-section; Impeccable detect 0 findings (after raising the list headings 20 -> 26 px for type hierarchy); copy grade 2.2, no dashes, one "not X, Y" line rewritten (Humanizer); CSS braces 156/156.

- [x] G15: the full check suite still passes with the new section
  CHECK: python3 ralph/ai-consultant-site/verify.py all
  EXPECT: FORM_OK
  EVIDENCE: 2026-10-28: RENDER_OK, HERO_OK, PRIVACY_OK, MEDIA_OK, COPY_OK (grade 5.4), MOTION_OK, DETECT_OK, FORM_OK.

- [x] G16: Ralph can see it before it goes live
  EVIDENCE: 2026-10-28: review page https://claude.ai/artifact/RA6YtvCKGPqkztYQuNWtmg version 4 = the new page with a "Preview, not live yet" bar and a jump link; 390 px and 1440 px screenshots looked at (no sideways scroll, no console errors).

- [ ] G17: Ralph OKs it, it is merged to main and https://focusfiyah.github.io serves it
  EVIDENCE: pending
