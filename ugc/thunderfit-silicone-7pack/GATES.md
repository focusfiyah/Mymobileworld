# Gates: ThunderFit Silicone Rings 7-Pack (plan stage)

OWNS: ugc/thunderfit-silicone-7pack/**

Scope: Ralph's 2026-11-03 ask, up to his plan approval: a 10-12 s music-only video plan (no VO) and a standard ~30 s VO script for Grace to record, built on the full script gate, planned shot by shot with one total cost, shown on a review page, Ralph pinged, no paid generation.

- [ ] G1: Script gate (Rule 0) passes for both scripts: audience, RESEARCH.md, coach, viral, facts, hooks, humanizer, readability, line sources.
  CHECK: python3 grace/gate.py ugc/thunderfit-silicone-7pack
  EXPECT: GATE OK
  EVIDENCE: pending

- [ ] G2: Product truth + free reference sheet from the real photo exist before any prompt, and every prompt in BOOK.md passes the prompt lint.
  CHECK: python3 ugc/thunderfit-silicone-7pack/tools/checks.py truth
  EXPECT: TRUTH_OK
  EVIDENCE: pending

- [ ] G3: Both deliverables are in the book: a 10-12 s music-only shot plan (sum of shot windows 10.0-12.0 s, no VO line) and a ~30 s VO script (26-36 s at 3.3 words/s), each readability grade <= 6, each closing in the orange cart (VO) or on one product (video).
  CHECK: python3 ugc/thunderfit-silicone-7pack/tools/checks.py book
  EXPECT: BOOK_OK
  EVIDENCE: pending

- [ ] G4: BOOK.md has one TOTAL line, the month-to-date spend line, and a "Sent to Ralph:" review-page link.
  CHECK: python3 ugc/thunderfit-silicone-7pack/tools/checks.py sent
  EXPECT: SENT_OK
  EVIDENCE: pending

- [ ] G5: No paid generation ran in this job (no paid task ledger, no Kie log).
  CHECK: python3 ugc/thunderfit-silicone-7pack/tools/checks.py nospend
  EXPECT: NOSPEND_OK
  EVIDENCE: pending

- [ ] G6: Ralph was told: phone push + email sent (one line each), and the plan question asked with AskUserQuestion (tappable options).
  EVIDENCE: pending

- [ ] G7: Brain job note + session log written and pushed; README Status line current; job branch merged to main.
  EVIDENCE: pending
