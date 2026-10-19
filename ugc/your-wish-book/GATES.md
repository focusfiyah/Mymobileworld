# Gates: Your Wish Is Your Command book, 3 Grace scripts

OWNS: ugc/your-wish-book/**, CLAUDE.md

Scope: three talking-head TikTok Shop scripts for Grace for the book, every Rule 0 proof saved, delivered as a Claude doc + Drive Google Doc in one product folder, Ralph notified.

- [ ] G1: grace/gate.py passes for the job (all PLAYBOOK §4 proofs present, newer than the script, no banned phrase)
  CHECK: python3 ../../grace/gate.py .
  EXPECT: GATE OK
  CWD: ugc/your-wish-book
  EVIDENCE: pending

- [ ] G2: exactly 3 scripts, each with HOOK, BODY, CTA and the "It's in the orange cart." close
  CHECK: node check.mjs structure
  EXPECT: STRUCTURE OK
  CWD: ugc/your-wish-book
  EVIDENCE: pending

- [ ] G3: every hook (main + 2 alts per script) is a library hook said word for word, no id reused
  CHECK: node check.mjs hooks
  EXPECT: HOOKS VERBATIM OK 9
  CWD: ugc/your-wish-book
  EVIDENCE: pending

- [ ] G4: no price number, "reviewer", "the label says", dash or other banned phrase anywhere in scripts.md
  CHECK: node check.mjs banned
  EXPECT: BANNED CLEAN
  CWD: ugc/your-wish-book
  EVIDENCE: pending

- [ ] G5: every book claim in the scripts is backed in product_facts.md (no outcome promises for manifesting)
  EVIDENCE: pending

- [ ] G6: Claude doc published with all 3 scripts; Drive "Grace Tiktok assets" has ONE folder for the book with a "CURRENT - " Google Doc, nothing loose
  EVIDENCE: pending

- [ ] G7: Ralph notified: thread reply with links, phone push and email (or failure stated)
  EVIDENCE: pending

- [ ] G8: README Status line + CLAUDE.md Jobs line written and pushed to claude/project-thread-mx5xol
  CHECK: git -C ../.. log origin/claude/project-thread-mx5xol -1 --format=%s
  EXPECT: Your Wish
  CWD: ugc/your-wish-book
  EVIDENCE: pending
