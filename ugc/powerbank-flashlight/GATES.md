# Power bank flashlight (Grace), phase 1: research + script + reference sheet + plan (no paid calls)

Ralph 2026-10-21: "Grace need ai video pls ... Prompt Master Skill. Do everything. Generate reference sheet for product lock."

- [x] G1: product reference sheet exists (real listing pixels, front big + side/end views)
  CHECK: python3 -c "from PIL import Image;im=Image.open('refs/product_sheet.png');print('SHEET_OK' if im.size[0]>=1500 else 'SMALL')"
  EXPECT: SHEET_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=484a8bea1e1e6ceaef904ba27069f958775e31378accc3ec792c5a7cd9be704e; exit=0; EXPECT=matched; output-sha256=13755046e36583c42ddc1aa76634dc72c1d8396345c5ead366a1d475e68e4b7d; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/powerbank-flashlight; path=7f4fb4b02918/15 entries
- [x] G2: script gate passes (audience, coach, viral, facts, hooks, humanizer, readability, line sources)
  CHECK: cd ../.. && python3 grace/gate.py ugc/powerbank-flashlight
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=5aca15a9999ef0a77c77b074ad7b84b9e622488279411fa60a684b0a5afd4fca; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/powerbank-flashlight; path=7f4fb4b02918/15 entries
- [x] G3: script has none of Ralph's banned words (price, reviewer, label says, order now) and ends on the orange cart
  CHECK: python3 -c "import re;t=open('research/script.txt').read();l=t.lower();bad=re.search(r'[$]|dollar|reviewer|label says|order (it )?now|girls',l);print('CLEAN' if not bad and t.strip().endswith(\"It's in the orange cart.\") else 'BAD')"
  EXPECT: CLEAN
  EVIDENCE: automatic-evidence=v1; definition-sha256=577e370d5a8972b4a135ca68d28b67c8967c6bb7a78ec41450a40b580924e22e; exit=0; EXPECT=matched; output-sha256=0b98843240a0b1a2384483206c02be8968dd809eb73838820be24cb7d6d6aeb9; output-bytes=6; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/powerbank-flashlight; path=7f4fb4b02918/15 entries
- [x] G4: shot plan marks every shot HAND or HAND-FREE with a third to half hand-free
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['shots'];n=sum(1 for x in s if not x['hand']);r=n/len(s);print('MIX_OK' if 0.33<=r<=0.5 and all('hand' in x for x in s) else 'MIX_BAD %d/%d'%(n,len(s)))"
  EXPECT: MIX_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=05cab2e9c4b41995b9fb3398fc6dc5630bf1be2e2e4ea7e20f5ee2defe17690d; exit=0; EXPECT=matched; output-sha256=8d545cfca588653860c6f8f98dac1f94265f8f7b6c4a972130deacf05cf250b3; output-bytes=7; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/powerbank-flashlight; path=7f4fb4b02918/15 entries
- [x] G5: review page published with the reference sheet + plan (manual: link in the reply)
  EVIDENCE: manual: https://claude.ai/artifact/Xp1Z3kXSxUqNjS8ygSr9MA published 2026-10-21
- [ ] G6: Ralph notified by push + email with the plan and the total cost (manual)
