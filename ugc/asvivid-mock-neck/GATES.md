# Gates: Asvivid reversible mock neck, music-only edit (Grace's own footage), 2026-11-02
Ralph: "Music-only fast edit", "1 video". $0.
1. Length 14-20 s. CHECK: ffprobe -v error -show_entries format=duration -of csv=p=0 out/edit_v1.mp4 | awk '{exit !($1>=14 && $1<=20)}' && echo OK  EXPECT: OK
2. Frame 0 = sweatshirt moving in her hands, close (her style rule 1). Look: out/qc/first.jpg
3. Cuts land on the music beat; middle shots ~1.5 s, end run 0.3-0.6 s, ends on the product. CHECK: python3 -I cut.py --check  EXPECT: CUTS_OK
4. No on-screen text, no overlays, no captions (hard rule 6). CHECK: grep -c drawtext cut.py  EXPECT: 0
5. Music continuous, no jump at cuts. CHECK: python3 -I cut.py --check  EXPECT: AUDIO_OK
6. Every shot's start/mid/end frame looked at (no blur smear, no shot opening mid-motion jerk). Look: out/qc/shots.jpg
7. 1080x1920, 30 fps, H.264 + AAC. CHECK: ffprobe -v error -show_entries stream=codec_name,width,height -of csv=p=0 out/edit_v1.mp4  EXPECT: h264,1080,1920
8. Review page published with the video playing in place; Drive product folder with CURRENT file; push + email sent.
