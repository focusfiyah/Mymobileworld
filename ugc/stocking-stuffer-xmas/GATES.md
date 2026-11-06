# Gates: Stocking Stuffer Finds, plan stage (2026-11-06)

- [x] G1: LOOK_SPEC.md covers palette, props, light, framing, VO, structure and what changes per video
  CHECK: node -e "const t=require('fs').readFileSync('LOOK_SPEC.md','utf8');const k=['Palette','Props kit','Light','Framing','VO','Script structure','What changes per video'];const m=k.filter(x=>!t.includes(x));console.log(m.length?'MISSING '+m:'SPEC_OK')"
  EXPECT: SPEC_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=03bb955b817ec8dbc89cdd8f02c37757f0666869ba78017df988bb5da80e28b6; exit=0; EXPECT=matched; output-sha256=b2f2f578ce2787456311e4f021313c4b8223dcffddedfe5b5c93ee8f115a7938; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/stocking-stuffer-xmas; path=7f4fb4b02918/15 entries
- [x] G2: no paid task was started for this job (no paid_tasks.json)
  CHECK: node -e "console.log(require('fs').existsSync('paid_tasks.json')?'PAID':'NO_SPEND')"
  EXPECT: NO_SPEND
  EVIDENCE: automatic-evidence=v1; definition-sha256=373451d892d44c721aa0c158b66c2a3c56d496093a8bb4b97682db38416d9f3d; exit=0; EXPECT=matched; output-sha256=be6f45f8afc8279e8c381dde0c648f7e0b486b0d8b55a1d20e4d0d5af4ccd418; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/stocking-stuffer-xmas; path=7f4fb4b02918/15 entries
- [x] G3: both screenshots in Drive "Telegram Assets (Azariah)" at the local size, with index lines
  EVIDENCE: Drive ids 1r_DAGDXGfHrdLjv3kzj5SB6m4ztZV9GO (147217 B = local), 1Pv3x8hmhsnJTlxBQEdjWhf083ZZVjx04 (189067 B = local); index file 1UyaqzHKU8k8T1De7X6fsEmYf63yioVe5 edited 2026-11-06
- [x] G4: Telegram reply to Grace in the group with the per-product info list (message id recorded)
  EVIDENCE: sendMessage ok, chat -5234107715, message_id 143
- [x] G5: Brain job note pushed to obsidian-vault main
  EVIDENCE: obsidian-vault main 0c1c38c
- [ ] G6: Ralph notified: phone push + email, review page link included
  NOTE: email sent (Gmail id 1a1b24908150df2a, review link in body); push FAILED: "PushNotification is disabled for this session"
