# Gates: ThunderFit Silicone Rings 7-Pack (plan stage)

OWNS: ugc/thunderfit-silicone-7pack/**

Scope (widened 2026-11-03 after Ralph approved the plan and said 'Just use Kie'): plan, then stills, clips, cut, Drive delivery. Original scope: a 10-12 s music-only video plan (no VO) and a standard ~30 s VO script for Grace to record, built on the full script gate, planned shot by shot with one total cost, shown on a review page, Ralph pinged, no paid generation.

- [ ] G1: Script gate (Rule 0) passes for both scripts: audience, RESEARCH.md, coach, viral, facts, hooks, humanizer, readability, line sources.
  CHECK: python3 grace/gate.py ugc/thunderfit-silicone-7pack
  EXPECT: GATE OK
  EVIDENCE: 2026-11-03 run by hand: GATE OK

- [ ] G2: Product truth + free reference sheet from the real photo exist before any prompt, and every prompt in BOOK.md passes the prompt lint.
  CHECK: python3 ugc/thunderfit-silicone-7pack/tools/checks.py truth
  EXPECT: TRUTH_OK
  EVIDENCE: run by hand: TRUTH_OK (PROMPT_LINT_OK inside)

- [ ] G3: Both deliverables are in the book: a 10-12 s music-only shot plan (sum of shot windows 10.0-12.0 s, no VO line) and a ~30 s VO script (26-36 s at 3.3 words/s), each readability grade <= 6, each closing in the orange cart (VO) or on one product (video).
  CHECK: python3 ugc/thunderfit-silicone-7pack/tools/checks.py book
  EXPECT: BOOK_OK
  EVIDENCE: run by hand: BOOK_OK video 11.4s, VO 110 words ~33s

- [ ] G4: BOOK.md has one TOTAL line, the month-to-date spend line, and a "Sent to Ralph:" review-page link.
  CHECK: python3 ugc/thunderfit-silicone-7pack/tools/checks.py sent
  EXPECT: SENT_OK
  EVIDENCE: run by hand: SENT_OK

- [ ] G5: No paid generation ran before Ralph's approval (plan-stage gate).
  CHECK: python3 ugc/thunderfit-silicone-7pack/tools/checks.py nospend
  EXPECT: NOSPEND_OK
  EVIDENCE: NOSPEND_OK at plan stage (before approval); paid work began only after the tapped OK. Now superseded: spend $2.82 = book $0.90 + extra $1.92 (gate.py lock)

- [ ] G6: Ralph was told: phone push + email sent (one line each), and the plan question asked with AskUserQuestion (tappable options).
  EVIDENCE: email sent (Gmail id 1a1a1f3cd76b1ea8); phone push NOT sent: PushNotification not found by ToolSearch this session; tap question asked

- [ ] G7: Brain job note + session log written and pushed; README Status line current; job branch merged to main.
  EVIDENCE: job note + session log pushed, README Status set, merged to main c943b1d; brain check still lists my Active work line (kept while waiting for the OK) and sibling sessions broken links

- [ ] G8: Cut V1 passes the cut-stage gate (coach compare, no text) and is in Drive as CURRENT with a matching size.
  CHECK: python3 grace/gate.py ugc/thunderfit-silicone-7pack --stage cut
  EXPECT: GATE OK
  EVIDENCE: GATE OK --stage cut; Drive file 1IcGIl9r9zmQNVB7VUzU9QWmvjpGgfnjr size 57682199 = local
- [ ] G9: Job media stored in Drive.
  CHECK: python3 tools/media/media.py check
  EXPECT: MEDIA_OK
  EVIDENCE: MEDIA_OK
