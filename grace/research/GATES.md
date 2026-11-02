# Gates: Grace's research workflow as a standing rule (Ralph 2026-11-02)

- [ ] G1: PLAYBOOK §4 holds Grace's research workflow step with the 7 sections and the 4-role verdict
  CHECK: python3 -c "t=open('grace/PLAYBOOK.md').read(); import sys; need=['Step 0b, Grace research workflow','Product differentiation','Target buyer','Pain points and desires','Buyer motivation','Existing content research','Objections and purchase justification','Content opportunities','is the objection killer','is the purchase justification']; miss=[n for n in need if n not in t]; print('PLAYBOOK_OK' if not miss else miss)"
  EXPECT: PLAYBOOK_OK
  CWD: ..
- [ ] G2: gate.py refuses a new job without RESEARCH.md, accepts the filled template, rejects unknown hook ids, leaves old jobs alone
  CHECK: python3 grace/tests/test_research.py
  EXPECT: RESEARCH_TESTS_OK
  CWD: ..
- [ ] G3: the existing gate tests still pass
  CHECK: python3 grace/tests/test_gate_lock.py && python3 grace/tests/test_product_truth.py && echo OLD_TESTS_OK
  EXPECT: OLD_TESTS_OK
  CWD: ..
- [ ] G4: all five handoff memory files in Mymobileworld name the rule, MEMORY_SHORT stays <= 2000 chars
  CHECK: python3 -c "import os;fs=['REMEMBER_ME.txt','REMEMBER_ME_paste.txt','GLOBAL_MEMORY.md','CLAUDE_PREFERENCES.txt','MEMORY_SHORT.txt'];m=[f for f in fs if 'research workflow' not in open('handoff/'+f).read().lower()];n=len(open('handoff/MEMORY_SHORT.txt').read());print('MEM_OK' if not m and n<=2000 else (m,n))"
  EXPECT: MEM_OK
  CWD: ..
- [ ] G5: the change is on origin/main
  CHECK: git fetch -q origin main && git grep -q "Step 0b, Grace research workflow" origin/main -- grace/PLAYBOOK.md && echo ON_MAIN
  EXPECT: ON_MAIN
  CWD: ..
- [ ] G6: live Google Doc "Ralph standing rules (live)" refreshed with the rule (manual: live_rules.py output)
- [ ] G7: brain check passes
  CHECK: python3 tools/brain/check.py --terms "Grace research workflow,objection killer,purchase justification"
  EXPECT: BRAIN_OK
  CWD: ..
