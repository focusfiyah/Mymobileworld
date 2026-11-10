# Gates: 5-in-1 Smart Ear Wax Camera Detector edit (2026-11-10)

- [x] G1: Grace's original is in Drive Originals and saved locally at full quality (not the Telegram 464x848 copy)
  CHECK: python3 -c "import subprocess,glob,json;f=glob.glob('orig/hd.*')[0];s=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',f],capture_output=True,text=True).stdout)['streams'][0];print('ORIG_HD' if min(s['width'],s['height'])>=1080 else 'LOWRES')"
  EXPECT: ORIG_HD
  EVIDENCE: automatic-evidence=v1; definition-sha256=714dd9802ea060933b3a3785c4170dc288209a50908402ec1edefd0dbc8501d1; exit=0; EXPECT=matched; output-sha256=8b22e65cdd576ea11b85fd312de7c7f0548495cfb2f69d65d602f8d8b921c941; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/ear-wax-camera-detector; path=7f4fb4b02918/15 entries
- [x] G2: Cut is 7-20 s (Grace msg 351), 1080x1920, no black frames, no frozen run, length matches the plan
  CHECK: python3 check.py ear 7 20 silent
  EXPECT: CUT_OK ear
  EVIDENCE: automatic-evidence=v1; definition-sha256=fc852fa932f9799b3a6ed0d88c773ffcc42c1db08b7c782d1e3a15b3a529e8d4; exit=0; EXPECT=matched; output-sha256=3432508d16abd3f412d1f13a2e75eebe21410002a25bbb6cd3562703fe054fe7; output-bytes=18; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/ear-wax-camera-detector; path=7f4fb4b02918/15 entries
- [x] G3: (manual) Every frame viewed on a 4-6 fps sheet + 2x edges: strong first second, different angles, camera view on screen, light, tips, ear/nose/skin/teeth uses shown as filmed, nothing stretched, bright neutral grade, no text (REMOVED.md)
  EVIDENCE: 2026-11-10 6 fps sheet of all 16.9 s viewed; 2x crops at 0.1, 2.6, 11.0 s clean; no text; ear/nose/teeth not filmed (skin only)
- [x] G4: (manual) Review page up with the cut; Ralph push + email sent; Ralph's OK on that exact cut recorded
  EVIDENCE: 2026-11-10 review 5vgbArDCfVWakf9XMYvruT, push + email 1a1c37eb4c2d98f2; Ralph tapped "Yes, ship V1 (Recommended)"
- [x] G5: (manual) After the OK: "CURRENT - Ear Camera V1 (HD).mp4" in the product folder (Drive size = local), older ones in Older versions; "✅ ... V1 (HD) is done and in Drive" sent to Grace and Ralph; Brain note updated
  EVIDENCE: 2026-11-10 Drive 1O3Ef3KsarQhvQtYNRtyYo6T_hzYxlQcz 17,733,690 bytes = local; no older versions; Telegram ✅ msgs 382 + 383; Brain note updated

Evidence G3 (2026-11-10): 6 fps sheet of the whole 16.9 s cut viewed; 2x crops of 0.1 s, 2.6 s, 11.0 s; no text; source frames picked from 2 fps + 6 fps sheets of all 56.2 s. Ear/nose/teeth not filmed (skin only).
Evidence G4 (partial): review https://claude.ai/artifact/5vgbArDCfVWakf9XMYvruT ; push sent; email 1a1c37eb4c2d98f2; waiting on Ralph's OK.
Evidence G4: Ralph tapped "Yes, ship V1 (Recommended)" 2026-11-10.
Evidence G5: Drive 1O3Ef3KsarQhvQtYNRtyYo6T_hzYxlQcz, 17,733,690 bytes = local; no older versions in folder; Telegram ✅ group msg 382, Ralph msg 383.
