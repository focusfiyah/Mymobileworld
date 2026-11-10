# Gates: 5-in-1 Smart Ear Wax Camera Detector edit (2026-11-10)

- [ ] G1: Grace's original is in Drive Originals and saved locally at full quality (not the Telegram 464x848 copy)
  CHECK: python3 -c "import subprocess,glob,json;f=glob.glob('orig/hd.*')[0];s=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',f],capture_output=True,text=True).stdout)['streams'][0];print('ORIG_HD' if min(s['width'],s['height'])>=1080 else 'LOWRES')"
  EXPECT: ORIG_HD
- [ ] G2: Cut is 12-20 s, 1080x1920, no black frames, no frozen run, length matches the plan
  CHECK: python3 check.py ear 12 20 audio
  EXPECT: CUT_OK ear
- [ ] G3: (manual) Every frame viewed on a 4-6 fps sheet + 2x edges: strong first second, different angles, camera view on screen, light, tips, ear/nose/skin/teeth uses shown as filmed, nothing stretched, bright neutral grade, no text (REMOVED.md)
- [ ] G4: (manual) Review page up with the cut; Ralph push + email sent; Ralph's OK on that exact cut recorded
- [ ] G5: (manual) After the OK: "CURRENT - Ear Camera V1 (HD).mp4" in the product folder (Drive size = local), older ones in Older versions; "✅ ... V1 (HD) is done and in Drive" sent to Grace and Ralph; Brain note updated
