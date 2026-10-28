# Gates: Ralph AI consultant landing page (C, studio reel)

OWNS: ralph/ai-consultant-site/**

Scope: a free one-page site at https://focusfiyah.github.io (repo focusfiyah/focusfiyah.github.io) that markets Ralph as an AI consultant: reel of real muted clips up top, what he builds, anonymous client work, Day One AI channel, AI receptionist, custom tools, and a working free-consult form to life22watch@gmail.com.

- [x] G1: page renders at 390 and 1440 wide with no console errors and no sideways scroll
  CHECK: python3 ralph/ai-consultant-site/verify.py render
  EXPECT: RENDER_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=51f56f0f2bcd5803fa47e2f461268644ad3f6950dcf140a4820bdae2b5b2cce9; exit=0; EXPECT=matched; output-sha256=221e28e9557974242923d962aa7b9c2e774f0f196a33d1419726d643ba580341; output-bytes=30; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G2: first phone viewport (390x844) shows the name, the one-line pitch and the consult button
  CHECK: python3 ralph/ai-consultant-site/verify.py hero
  EXPECT: HERO_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=7ba7ffb27c67f0c6ddf0dccec503f02beb5e3437efd5379ea474ef1d0ad113ee; exit=0; EXPECT=matched; output-sha256=e36164c4a7829edef68fdaa7c003c1473564fd493ed7c9c7c65edc09a8b452ec; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G3: no client names, handles, phone numbers or real people's details in the site files (checker tested on a positive control)
  CHECK: python3 ralph/ai-consultant-site/verify.py privacy
  EXPECT: PRIVACY_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=70d0bfb90a8a09848ca2c78c65693efa5559ea1cece5df2fe9730425382e7890; exit=0; EXPECT=matched; output-sha256=a0d2462202290233a69e996137c7fb885e3f45a605ddbded9ca527b8a36d9de6; output-bytes=11; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G4: every clip is silent (no audio stream), at most 1.6 MB, and the whole site is at most 15 MB
  CHECK: python3 ralph/ai-consultant-site/verify.py media
  EXPECT: MEDIA_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=51e054d4b0cb5730c054632348607cfaaf1c2fd43b41570f4add5b2c3b297c17; exit=0; EXPECT=matched; output-sha256=fe01a9d32642957c6687197ba25f57c9017c1f7b8ee4d8f5f9490440ab5d4cb1; output-bytes=38; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G5: copy rules: no dashes as punctuation, no banned words, no prices, readability grade 8 or lower
  CHECK: python3 ralph/ai-consultant-site/verify.py copy
  EXPECT: COPY_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=05da5a4accb66997c8fc6bfe7179eefcbd8a34dd966b6580368a556c68769f26; exit=0; EXPECT=matched; output-sha256=8224eba70705b0a8d8edc9910ae3bac070d81a7f0078758b87b42d461738a22c; output-bytes=43; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G6: motion budget passes (web-design-stack motion_check)
  CHECK: python3 ralph/ai-consultant-site/verify.py motion
  EXPECT: MOTION_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=e5cd078c4984155a5c6980a544b53049651c2aff60003159af38699ca55cf317; exit=0; EXPECT=matched; output-sha256=a46b8d20838168c807ef660c0087e2de64b43001872fae9f89e71508e5e0ee38; output-bytes=73; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G7: Impeccable detector has no findings left on index.html (or each one named with its reason in README)
  CHECK: python3 ralph/ai-consultant-site/verify.py detect
  EXPECT: DETECT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=3a50f4df49e2594d741088fd4dc52ab2d634b4ebec351fcc3abea54b5fe1df54; exit=0; EXPECT=matched; output-sha256=830056cb6a57bc6b4ab03cdba7cb68cb4133fefa703a2a67baa2cf5473910d8a; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G8: the form has name, email and message fields, posts to FormSubmit for Ralph's address, and shows sending / sent / error states
  CHECK: python3 ralph/ai-consultant-site/verify.py form
  EXPECT: FORM_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=14aecd60e96326d1f128ac7c7a6d95cbb82d703d61e4d04f3a556962dac1095e; exit=0; EXPECT=matched; output-sha256=94b956fe2c775bbe37a1b408aa0c39b4f5016c93ac91d065bcd5d1df0a38a036; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G9: the copy went through Humanizer (proof file saved)
  EVIDENCE: met 2026-10-28: proof/humanizer.md (4 tells fixed)

- [x] G10: Ralph saw the full page on the review Artifact and said OK
  EVIDENCE: met 2026-10-28: Ralph on v3 preview: "Okay, this is very good. Let's move forward."

- [x] G11: https://focusfiyah.github.io is live and serves this page
  CHECK: python3 ralph/ai-consultant-site/verify.py live
  EXPECT: LIVE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=7508811417963ab5a494d8d8194df217e4a95c8f41cc6678aecf1e9b83c5db90; exit=0; EXPECT=matched; output-sha256=7c18db06db10e0f490444667c49105c7bfd37bb848795c4d6066d008ec551a0a; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

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
  EVIDENCE: automatic-evidence=v1; definition-sha256=193e70a78cd774892b0ada2ab3d30d70d02ab0e65254452f8329a478889a29f8; exit=0; EXPECT=matched; output-sha256=375656c67f2d76199433d681a4cdbbe8db263cf0de5005cca11d5945ac9b3d42; output-bytes=295; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G16: Ralph can see it before it goes live
  EVIDENCE: 2026-10-28: review page https://claude.ai/artifact/RA6YtvCKGPqkztYQuNWtmg version 4 = the new page with a "Preview, not live yet" bar and a jump link; 390 px and 1440 px screenshots looked at (no sideways scroll, no console errors).

- [x] G17: Ralph OKs it, it is merged to main and https://focusfiyah.github.io serves it
  CHECK: python3 ralph/ai-consultant-site/verify.py live
  EXPECT: LIVE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=7508811417963ab5a494d8d8194df217e4a95c8f41cc6678aecf1e9b83c5db90; exit=0; EXPECT=matched; output-sha256=7c18db06db10e0f490444667c49105c7bfd37bb848795c4d6066d008ec551a0a; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries
