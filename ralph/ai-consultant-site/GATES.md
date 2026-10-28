# Gates: Ralph AI consultant landing page (C, studio reel)

OWNS: ralph/ai-consultant-site/**

Scope: a free one-page site at https://focusfiyah.github.io (repo focusfiyah/focusfiyah.github.io) that markets Ralph as an AI consultant: reel of real muted clips up top, what he builds, anonymous client work, Day One AI channel, AI receptionist, custom tools, and a working free-consult form to life22watch@gmail.com.

- [ ] G1: page renders at 390 and 1440 wide with no console errors and no sideways scroll
  CHECK: python3 ralph/ai-consultant-site/verify.py render
  EXPECT: RENDER_OK
  EVIDENCE: pending

- [ ] G2: first phone viewport (390x844) shows the name, the one-line pitch and the consult button
  CHECK: python3 ralph/ai-consultant-site/verify.py hero
  EXPECT: HERO_OK
  EVIDENCE: pending

- [ ] G3: no client names, handles, phone numbers or real people's details in the site files (checker tested on a positive control)
  CHECK: python3 ralph/ai-consultant-site/verify.py privacy
  EXPECT: PRIVACY_OK
  EVIDENCE: pending

- [ ] G4: every clip is silent (no audio stream), at most 1.6 MB, and the whole site is at most 15 MB
  CHECK: python3 ralph/ai-consultant-site/verify.py media
  EXPECT: MEDIA_OK
  EVIDENCE: pending

- [ ] G5: copy rules: no dashes as punctuation, no banned words, no prices, readability grade 8 or lower
  CHECK: python3 ralph/ai-consultant-site/verify.py copy
  EXPECT: COPY_OK
  EVIDENCE: pending

- [ ] G6: motion budget passes (web-design-stack motion_check)
  CHECK: python3 ralph/ai-consultant-site/verify.py motion
  EXPECT: MOTION_OK
  EVIDENCE: pending

- [ ] G7: Impeccable detector has no findings left on index.html (or each one named with its reason in README)
  CHECK: python3 ralph/ai-consultant-site/verify.py detect
  EXPECT: DETECT_OK
  EVIDENCE: pending

- [ ] G8: the form has name, email and message fields, posts to FormSubmit for Ralph's address, and shows sending / sent / error states
  CHECK: python3 ralph/ai-consultant-site/verify.py form
  EXPECT: FORM_OK
  EVIDENCE: pending

- [ ] G9: the copy went through Humanizer (proof file saved)
  EVIDENCE: pending

- [ ] G10: Ralph saw the full page on the review Artifact and said OK
  EVIDENCE: pending

- [ ] G11: https://focusfiyah.github.io is live and serves this page
  CHECK: python3 ralph/ai-consultant-site/verify.py live
  EXPECT: LIVE_OK
  EVIDENCE: pending

- [ ] G12: a test message sent through the live form reached life22watch@gmail.com
  EVIDENCE: pending

- [ ] G13: Brain note + session log written and tools/brain/check.py prints BRAIN_OK
  EVIDENCE: pending
