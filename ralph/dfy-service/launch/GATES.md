# Gates: Front Desk launch kit (Ralph 2026-10-26)

OWNS: ralph/dfy-service/launch/**

Scope: Ralph picked the #1 + #3 bundle as one fixed plan, sold to Jean's network, Freeport/Baldwin, Reddit and online, with no sales calls (people call him or book). Build every free piece of the launch and one plan with the total cost for his OK.

- [x] G1: OFFER.md defines the one fixed plan (what's in it for calls and reviews, price, setup, minutes cap, founding offer, terms) and 3 name options with a check of each name
  CHECK: python3 ralph/dfy-service/launch/verify.py offer
  EXPECT: OFFER_OK
  EVIDENCE: OFFER_OK (by hand 2026-10-26)

- [x] G2: landing page built (call + booking buttons, price, sourced stats with links, FAQ), standalone index.html for hosting, grade 8 or below, no side scroll at 390px
  CHECK: python3 ralph/dfy-service/launch/verify.py page
  EXPECT: PAGE_OK
  EVIDENCE: PAGE_OK, grade 4.1, scrollWidth 390 (by hand 2026-10-26)

- [x] G3: AGENT.md spec for our own line: inbound only, says it's the assistant and the call may be recorded, AI only when asked, transfers to Ralph in his hours, else books or takes a message; matches OFFER.md price
  CHECK: python3 ralph/dfy-service/launch/verify.py agent
  EXPECT: AGENT_OK
  EVIDENCE: AGENT_OK

- [x] G4: CHANNELS.md covers Jean's network (message drafts), Freeport/Baldwin (named places with links), Reddit (rules checked, reply drafts, no promo posts where banned), online (Google Business Profile, directories); no cold calls anywhere
  CHECK: python3 ralph/dfy-service/launch/verify.py channels
  EXPECT: CHANNELS_OK
  EVIDENCE: CHANNELS_OK

- [x] G5: PLAN.md lists every paid item with its price and one TOTAL line, and the decisions Ralph must make
  CHECK: python3 ralph/dfy-service/launch/verify.py plan
  EXPECT: PLAN_OK
  EVIDENCE: PLAN_OK, TOTAL $1.60

- [x] G6: Humanizer pass on all copy; page previewed at phone width in light and dark
  EVIDENCE: Humanizer rules applied to all copy; tell scan found one natural "not just" in a Reddit reply, kept; overclaim "owners I've helped" removed; page screenshotted at 390px light + dark, step-number padding fixed

- [x] G7: plan + page sent to Ralph (doc section, page link), email + push; brain note updated, BRAIN_OK; merged to main
  EVIDENCE: Doc "Launch plan" section (rev 9) + website preview https://claude.ai/artifact/X3Hc8iZ4evAvodEGaPqMs3; Gmail 1a176e593f596e15; push requested; brain BRAIN_OK, vault pushed; Mymobileworld merged to main

## Round 2 (Ralph 2026-10-26: Always Answered, transfers to 786-496-3177 10-6 Mon-Sat, after hours to booking, price OK, extras off; redesign with thumbnail-looks; Pipecat?)

- [x] G8: Ralph's answers saved in AGENT.md, PLAN.md, OFFER.md (after hours = booking page, no callbacks)
  CHECK: python3 ralph/dfy-service/launch/verify.py agent
  EXPECT: AGENT_OK
  EVIDENCE: AGENT_OK; AGENT.md status line + UNAVAILABLE rule rewritten; PLAN/OFFER decision lines added (2026-10-26)

- [x] G9: three landing looks from one brand block (site/looks.py), each a different familiar format, measured with the thumbnail-looks sameness score, all at or under 0.30 vs each other and the v1 page, no side scroll at 390 and 1280
  CHECK: python3 -I ralph/dfy-service/launch/site/looks.py measure
  EXPECT: LOOKS_OK
  EVIDENCE: LOOKS_OK, worst shared 0.23 (lockscreen vs v1 phone) after two measured fixes (0.40 then 0.32); review page https://claude.ai/artifact/9KDzAvC72Z7RgrttjXjPXT

- [x] G10: Pipecat answer with sources and a recommendation (research/pipecat.md); marked not tested
  EVIDENCE: research/pipecat.md written 2026-10-26, 4 source links, "Not tested this session"

