# Gates: Grace's research workflow as a standing rule (Ralph 2026-11-02)

- [x] G1: PLAYBOOK §4 holds Grace's research workflow step with the 7 sections and the 4-role verdict
  CHECK: python3 -c "t=open('grace/PLAYBOOK.md').read(); import sys; need=['Step 0b, Grace research workflow','Product differentiation','Target buyer','Pain points and desires','Buyer motivation','Existing content research','Objections and purchase justification','Content opportunities','is the objection killer','is the purchase justification']; miss=[n for n in need if n not in t]; print('PLAYBOOK_OK' if not miss else miss)"
  EXPECT: PLAYBOOK_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=4c5d7eb0f28e87171e9720bbbb0c8e08492d0740063145451b580ca14b7d9221; exit=0; EXPECT=matched; output-sha256=692b31e432358c4b6a3d0997b7244bf5cfa0681a6387bfc4064e8ac78db11773; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries
- [x] G2: gate.py refuses a new job without RESEARCH.md, accepts the filled template, rejects unknown hook ids, leaves old jobs alone
  CHECK: python3 grace/tests/test_research.py
  EXPECT: RESEARCH_TESTS_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=72044d979786ecfe44701403d5d21f39b1ed2bec87bb4bbbe77786459f82fbf1; exit=0; EXPECT=matched; output-sha256=7c81fa05ae6576fe2cabbcbc0d52f6b2b98acbb7cd7f86054c49100c658fdd97; output-bytes=592; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries
- [x] G3: the existing gate tests still pass
  CHECK: python3 grace/tests/test_gate_lock.py && python3 grace/tests/test_product_truth.py && echo OLD_TESTS_OK
  EXPECT: OLD_TESTS_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=c9a7f908e5cca6405ec62032010f643b8cb5469ec239e3226521aed9d2f75c39; exit=0; EXPECT=matched; output-sha256=500c6c46d864926c442bb54d42261afd5410ef599c4d01c27050fdf02824e0ad; output-bytes=2634; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries
- [x] G4: all five handoff memory files in Mymobileworld name the rule, MEMORY_SHORT stays <= 2000 chars
  CHECK: python3 -c "import os;fs=['REMEMBER_ME.txt','REMEMBER_ME_paste.txt','GLOBAL_MEMORY.md','CLAUDE_PREFERENCES.txt','MEMORY_SHORT.txt'];m=[f for f in fs if 'research workflow' not in open('handoff/'+f).read().lower()];n=len(open('handoff/MEMORY_SHORT.txt').read());print('MEM_OK' if not m and n<=2000 else (m,n))"
  EXPECT: MEM_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=12d422b8f208e2e2ac5955f272c631ff3edd59582427a6fe2fb33e72854bcf82; exit=0; EXPECT=matched; output-sha256=e84b6552b91e91875e22b03eb943e36ba4108b2675823cc436bbec93c0b1f911; output-bytes=7; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries
- [x] G5: the change is on origin/main
  CHECK: git fetch -q origin main && git grep -q "Step 0b, Grace research workflow" origin/main -- grace/PLAYBOOK.md && echo ON_MAIN
  EXPECT: ON_MAIN
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=d1bd616921ddc5676b6aea56f7b1c93935edea1f15c639d436231d95296df01e; exit=0; EXPECT=matched; output-sha256=2a2087143cc4438b163af6526189ba0225d318a56f27850b5d4cfde2ccc15faf; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries
- [x] G6: live Google Doc "Ralph standing rules (live)" refreshed with the rule (manual: live_rules.py output)
  EVIDENCE: 2026-11-02 Drive search title='Ralph standing rules (live)' and fullText contains 'objection killer' -> 1U6mRn-pwzKGDDNIg7Vcn-EJU2iiHug_g4vzKoWf10lQ; old 1TssbcCr... and 1zfTNiem... trashed
- [x] G7: brain check passes
  CHECK: python3 tools/brain/check.py --terms "Grace research workflow,objection killer,purchase justification"
  EXPECT: BRAIN_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=70edea0cacd5b9a4e1a433544d482feb400d66a227f86fde6f8a7c334c9f9b87; exit=0; EXPECT=matched; output-sha256=7b4e4a86825efe8147b4cc4bb18a51167ff5f930e3f2a2d8299487667cc81637; output-bytes=52; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries
