# GATES: Grace UGC upload (Shnuggle toddler tub TikTok -> Full HD)
1. Grace got an "on it" reply on Telegram (message id logged).
2. Output file is exactly 1080x1920, H.264, audio kept.
   CHECK: ffprobe -v error -select_streams v:0 -show_entries stream=width,height,codec_name -of csv=p=0 out/*.mp4
   EXPECT: h264,1080,1920
3. 2x zoom check of edges: no halo/smear (looked at frames).
4. File in Drive Grace Tiktok assets / Shnuggle folder, CURRENT- name, size matches local.
5. Grace got the direct Drive link with done ✅.
6. Brain note added.
