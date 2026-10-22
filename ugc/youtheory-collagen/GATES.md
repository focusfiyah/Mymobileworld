# Youtheory Collagen Liquid (Grace), 2026-10-22, phase 1: research + script gate + plan (no paid calls)

- [x] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability override, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/youtheory-collagen
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=8bedfb0359f646b69b32d59f16d0517f77c3b5acb95968d57316978fc7331631; exit=0; EXPECT=matched; output-sha256=1c97b16c8da6889040a1ae659812e2a6a89e307e25edb10d90fdefa97fe17478; output-bytes=91; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G2: the script says no vitamin C and keeps the 5,000 mg line
  CHECK: python3 -c "t=open('scripts.md').read().split('## V1')[1].lower();print('VITC_OK' if 'vitamin c' not in t and 'five thousand milligrams' in t and 'need water' in t else 'BAD')"
  EXPECT: VITC_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=51051b8d3cf0000603abb127658364999d4d6c0983729ff1f1655b4128e0e552; exit=0; EXPECT=matched; output-sha256=f7d42894a3e2238f166a60b43aeb62c0c66e92c273bbac4016fae2aad7308397; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G3: Ralph's real photos saved and the product sheet built from them (sheet >= 1500 px)
  CHECK: python3 -c "import os;from PIL import Image;ok=all(os.path.exists('refs/real/'+f) for f in ['ralph_pouch_flat.jpg','ralph_pouches_in_box.jpg']);im=Image.open('refs/product_sheet.png');print('SHEET_OK' if ok and min(im.size)>=1500 else 'NO',im.size)"
  EXPECT: SHEET_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=7a5b8a410afd33be7daa45c65fc6bcc130d86b692e785873f09e9c1946711cf2; exit=0; EXPECT=matched; output-sha256=ad7ebcebd50ed0ffa9e0fc26c22430555ed18d7c8eef089c776f6ff7b14f783d; output-bytes=22; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G4: shots.json marks every shot HAND or HAND-FREE, a third to half hand-free, every product shot on Omni, no Kling
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['videos'][0]['shots'];f=sum(1 for x in s if not x['hand'])/len(s);ok=1/3-0.01<=f<=0.51 and all((x['model']=='omni')==x['product'] for x in s) and not any(x['model']=='kling' for x in s);print('MIX_OK' if ok else 'BAD',f)"
  EXPECT: MIX_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=92cc184a909c7660cecaf2876fcfffbd70685efee884e6c351afbda791c380c4; exit=0; EXPECT=matched; output-sha256=6de9dce5ffd78b1e339570ba6e3e617384eb532f3955007b754f794c99e3edec; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G5: REMOVED.md carries the standing removals and vitamin C
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns','vitamin c']) else 'NO')"
  EXPECT: REMOVED_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=6b974d714093ba6e6d8297d58e802e5b4f27e4e2a9973a522bcb2f2d872d6c1b; exit=0; EXPECT=matched; output-sha256=fdd0ffce6701454c76a66b240abb2c3bf4ad8cf481d672c18ea787906a38db7a; output-bytes=11; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G6: review page published with script, reference sheet, shot list and one total; push + email sent (manual)
  EVIDENCE: plan on artifact https://claude.ai/artifact/VD9ib3CWos6aH4hbrafzjX v1 with one total ($3.38, up to $3.79); push sent; email Gmail id 1a16193e390e46f8 (2026-10-22)
