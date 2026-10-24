# Gates: Open-Higgsfield-AI option A (Ralph 2026-10-24)

- [x] G1: the field table covers the 7 models our jobs have used and the 6 talking-avatar models
  CHECK: python3 -c "import json;m=json.load(open('/home/user/Mymobileworld/grace/kie_fields.json'))['models'];need=['nano-banana-pro','bytedance/seedance-2-mini','google/gemini-omni-flash-1-1','kling-3.0-omni/image-to-video','hailuo/2-3-image-to-video-standard','veo-3-1','volcengine/video-to-video-lip-sync','kling/ai-avatar-standard','kling/ai-avatar-pro','omnihuman-1-5','omnihuman-2-0','infinitalk/from-audio','wan/2-2-a14b-speech-to-video-turbo'];miss=[x for x in need if x not in m];print('TABLE_OK' if not miss else miss)"
  EXPECT: TABLE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=0fd5dfa7dcda33298ae1ade4a9d1511c3cb1108a0a2b9899d3c8b596575b6461; exit=0; EXPECT=matched; output-sha256=d40c72aa9b62942e910570d14514f729c9adc00df43d106e1d8c43a88a9c7f3a; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/_toolkit/open-higgsfield-ai; path=7f4fb4b02918/15 entries

- [x] G2: every request in our job logs passes the field check (positive control)
  CHECK: python3 /home/user/Mymobileworld/grace/kie_fields.py audit
  EXPECT: , 0 with unknown fields
  EVIDENCE: automatic-evidence=v1; definition-sha256=7c32fce1bbde13aa53701fb971ccb51bd686b4373ea718d1ddc9dd8154b2281f; exit=0; EXPECT=matched; output-sha256=8729a7460fe23a410b43a4f5a5059d3736034e82ca2e4f8b40b5442544563aa5; output-bytes=43; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/_toolkit/open-higgsfield-ai; path=7f4fb4b02918/15 entries

- [x] G3: gate tests pass, including a misnamed field refused before anything is claimed (negative control)
  CHECK: python3 /home/user/Mymobileworld/grace/tests/test_gate_lock.py
  EXPECT: ALL CHECKS PASSED
  EVIDENCE: automatic-evidence=v1; definition-sha256=e6eb90ad338e655ece9aea4aea7788332730f65509f999e5b96eb1793a34aa7e; exit=0; EXPECT=matched; output-sha256=48ac4861760008f34d891d02120acfd72818d116647f1bebd47433b6750c52e1; output-bytes=1797; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/_toolkit/open-higgsfield-ai; path=7f4fb4b02918/15 entries

- [x] G4: spend.py prices all 6 avatar models
  CHECK: python3 -c "import sys;sys.path.insert(0,'/home/user/Mymobileworld/grace');import spend;n=[m for m in ['kling/ai-avatar-standard','kling/ai-avatar-pro','omnihuman-1-5','omnihuman-2-0','infinitalk/from-audio','wan/2-2-a14b-speech-to-video-turbo'] if m in spend.PRICES];print('PRICES_OK' if len(n)==6 else n)"
  EXPECT: PRICES_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=9236effcc1dea1398db19cc4967e7d6acadeb597ee103dc6c1d477c2cfe6aeaa; exit=0; EXPECT=matched; output-sha256=9200acc2c83355a1f537f0258c48d6b60a3b291a7a07fb36cf644eb070832479; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/_toolkit/open-higgsfield-ai; path=7f4fb4b02918/15 entries

- [x] G5: the skill source lists all 6 avatar models and the deployed copy matches it
  CHECK: python3 -c "import filecmp;s='/home/user/claude-skills/skills/ugc-product-ad/references/lipsync-options.md';t=open(s).read();ok=all(m in t for m in ['ai-avatar-standard','ai-avatar-pro','omnihuman-2-0','omnihuman-1-5','infinitalk/from-audio','speech-to-video-turbo']);print('SKILL_OK' if ok and filecmp.cmp(s,'/home/user/Mymobileworld/.claude/skills/ugc-product-ad/references/lipsync-options.md',shallow=False) else 'BAD')"
  EXPECT: SKILL_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=0dba01868501ca7ed0205619b6aa0ab3e796359693c0cd600da4d8db98f16a37; exit=0; EXPECT=matched; output-sha256=3938d97c65e323cb99033235fa3623a24dfb255a4043cbf4edbbef2a7c04a6c8; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/_toolkit/open-higgsfield-ai; path=7f4fb4b02918/15 entries

- [x] G6: skill audit has no errors
  CHECK: cd /home/user/claude-skills && python3 skills/skill-smith/scripts/audit.py skills/ugc-product-ad
  EXPECT: 0 errors
  EVIDENCE: automatic-evidence=v1; definition-sha256=ae8ede641600f2ce779b443db55ae6d23c048644dd4abba8544522a664321837; exit=0; EXPECT=matched; output-sha256=22ef03b7e4a28b2139499ae83a7d28dd8a311bd3e732dcbca6d930a9431f6371; output-bytes=124; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/_toolkit/open-higgsfield-ai; path=7f4fb4b02918/15 entries
