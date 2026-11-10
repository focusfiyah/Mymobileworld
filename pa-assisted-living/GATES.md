# Gates: PA assisted living business plan analysis + grant prep

OWNS: pa-assisted-living/**

Scope: A review page for Ralph that analyzes the client's PA assisted living plan, explains license choice, staffing math, money, gaps, realistic grant/funding options, the step-by-step roadmap and what the client must prepare, with sources, published as an Artifact and filed in the repo + Brain.

- [ ] G1: The review page has all nine sections (verdict, license, staffing, money, gaps, grant, roadmap, client checklist, questions)
  CHECK: node tools_check.mjs sections
  EXPECT: GATE_PASS sections
  CWD: pa-assisted-living
  EVIDENCE: pending

- [ ] G2: The page cites at least 12 distinct source links
  CHECK: node tools_check.mjs sources
  EXPECT: GATE_PASS sources
  CWD: pa-assisted-living
  EVIDENCE: pending

- [ ] G3: The staffing cost figures on the page match an independent recomputation from the wage inputs
  CHECK: node tools_check.mjs math
  EXPECT: GATE_PASS math
  CWD: pa-assisted-living
  EVIDENCE: pending

- [ ] G4: Page text has no em dashes or stock AI words (Humanizer pass)
  CHECK: node tools_check.mjs nobanned
  EXPECT: GATE_PASS nobanned
  CWD: pa-assisted-living
  EVIDENCE: pending

- [ ] G5: The job README records the published review page link
  CHECK: node tools_check.mjs readme
  EXPECT: GATE_PASS readme
  CWD: pa-assisted-living
  EVIDENCE: pending

- [ ] G6: Every fact from research that the page states is marked confirmed with a source or flagged "to confirm"; Ralph got push + email
  EVIDENCE: pending
