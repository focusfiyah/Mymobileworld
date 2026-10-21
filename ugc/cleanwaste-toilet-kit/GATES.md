# Cleanwaste Portable Toilet Bags (Grace), 2026-10-21, phase 1: research + script gate + plan (no paid calls)

- [x] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/cleanwaste-toilet-kit
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=ec6a63b92366ae69c4c1317fff54b37486acb4b55b46ddcccb9add3ca51c2190; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G2: every script readability file is grade <= 6
  CHECK: python3 -c "import re,glob;fs=sorted(glob.glob('research/readability_v*.txt'));g=[float(re.search(r'Kincaid\):\s*([0-9.]+)',open(f).read()).group(1)) for f in fs];print('GRADES_OK' if fs and max(g)<=6 else 'BAD',g)"
  EXPECT: GRADES_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=c707d2caefc96b3b2487f4946592d549d7a18415b4abbbfe05ba2bca651089c1; exit=0; EXPECT=matched; output-sha256=c7c82a0598c5ceaf8a9036a74e35cd7a01cdcad0c980817069685cea4701439a; output-bytes=21; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G3: Grace's script claims each have a source verdict in product_facts.md
  CHECK: python3 -c "t=open('research/product_facts.md').read().lower();ks=['gels','odor','toilet paper','wipe','zip','toilet that won']; m=[k for k in ks if k not in t];print('FACTS_OK' if not m else 'MISSING',m)"
  EXPECT: FACTS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=015f599d52c22ff1d6277a633d16509cf5d811649acd61e46d4fed3a787c8d81; exit=0; EXPECT=matched; output-sha256=38f4673593f304c3dabbcff73b594ce880df6dfa1574d20bd17b3c939de53d0a; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G4: real product photos saved (box front at least 800 px wide)
  CHECK: python3 -c "import glob;from PIL import Image;fs=[f for f in glob.glob('refs/real/*') if f.lower().endswith(('.jpg','.jpeg','.png','.webp'))];w=max([Image.open(f).size[0] for f in fs] or [0]);print('PHOTOS_OK' if len(fs)>=3 and w>=800 else 'NO',len(fs),w)"
  EXPECT: PHOTOS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=7580f9f0bdf4fd592026c330b386f3dc64cb986215c2bf31e000032e47debe88; exit=0; EXPECT=matched; output-sha256=5151b51cf888204a79850d50be90970bafb9b986c0d85dd8a6a07c23accbbfad; output-bytes=18; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G5: product reference sheet built from real pixels
  CHECK: python3 -c "from PIL import Image;im=Image.open('refs/product_sheet.png');print('SHEET_OK' if min(im.size)>=900 else 'SMALL',im.size)"
  EXPECT: SHEET_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=532f28ec3ad6eb2d1f80b50a9c3b24cc54acabe0fd1a6bdcf569b8a974edcc90; exit=0; EXPECT=matched; output-sha256=86c81dbf840520112d38d2552d1c87e83cf856e476ba2d16f80abcf3fd118f71; output-bytes=22; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G6: shots.json marks every shot HAND or HAND-FREE, a third to half hand-free, every prompt passed through prompt-master rules
  CHECK: python3 -c "import json;d=json.load(open('shots.json'));r=[];[r.append((v['id'],sum(1 for s in v['shots'] if not s['hand'])/len(v['shots']))) for v in d['videos']];print('MIX_OK' if all(1/3-0.01<=x<=0.5+0.01 for _,x in r) else 'BAD',r)"
  EXPECT: MIX_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=ba839909f08094b1d694cbc90ef46fc81a8372c25bae8903306e8fed111b97ee; exit=0; EXPECT=matched; output-sha256=56acfad09edbe0e16cfd8b3ea95daff52916d11af54ca4f69a81d4618ddd2e97; output-bytes=49; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G7: REMOVED.md exists and carries Ralph's standing removals (no text, no cards, no Ken Burns)
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns']) else 'NO')"
  EXPECT: REMOVED_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=013a407bf9538486765030b1ef6dfb1517e8b37c02c4fd804b29ca767557b9ea; exit=0; EXPECT=matched; output-sha256=fdd0ffce6701454c76a66b240abb2c3bf4ad8cf481d672c18ea787906a38db7a; output-bytes=11; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [ ] G8: review page published with the script + reference sheet; plan sent to Ralph with one total cost; push + email sent (manual)
