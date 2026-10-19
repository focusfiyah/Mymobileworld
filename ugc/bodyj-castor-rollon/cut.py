"""Cut r1 (2026-10-17): 9 shots on the Grace B voiceover (vo/voiceover_tight.mp3, 31.8s), no text, no music. Every clip plays at 1.0x
from its own start (never stretched); cut points sit in the gaps between words (vo/words_trimmed.json). Product clips are the
label-pasted versions (clips_label/, label_track.py). S2 = Grace's own viral clip, head only, 0.3-4.7s only (REMOVED.md).
  python3 cut.py [OUT]"""
import subprocess, sys
EDIT = [  # (clip, start, length)
    ("S1", 0.0, 4.06),   #  0.00-4.06  "If you are wondering whether castor oil is only for babies, here you go."
    ("S2", 0.3, 4.40),   #  4.06-8.46  "I used castor oil to get my daughter's cradle cap out. But did you know" (Grace's clip)
    ("S3", 0.0, 4.22),   #  8.46-12.68 "people use it everywhere? The problem is it's thick and drips all over your fingers."
    ("S4", 0.0, 2.54),   # 12.68-15.22 "This one rolls on with a rose quartz roller."
    ("S5", 0.0, 0.80),   # 15.22-16.02 "Your scalp,"
    ("S6", 0.0, 0.96),   # 16.02-16.98 "your elbows,"
    ("S7", 0.0, 1.10),   # 16.98-18.08 "the ends of your hair."
    ("S8", 0.0, 3.52),   # 18.08-21.60 "USDA organic, cold pressed and hexane free."
    ("S4", 2.30, 2.70),  # 21.60-24.30 "Honestly, I'm upset I didn't find the roller first." (rest of the back-of-hand stroke; 0.24s re-seen, cut after "first.")
    ("S6", 0.96, 3.84),  # 24.30-28.14 "My old one isn't sold anymore, and dry winter skin is coming." (rest of the elbow clip)
    ("S9", 0.0, 3.63),   # 28.14-31.77 "Grab one for your purse and one for your nightstand. It's in the orange cart."
]
CLIP = {"S2": 4.7}
SRC = {"S2": "research/grace_video/7566790233325391135/video.mp4"}
LABEL = {"S1", "S5", "S7", "S8", "S9"}   # clips_label/ exists (S4, S6: label too small/turned to track; checked by eye)
GRACE = "crop=540:960:0:300,eq=brightness=0.07:gamma=1.12:saturation=0.95,colorbalance=rm=-0.04:bm=0.06,"
ins, f = [], ""
for i, (k, a, d) in enumerate(EDIT):
    assert a + d <= CLIP.get(k, 5.04) + 0.01, f"{k}: {a}+{d}s > clip (never stretch)"
    ins += ["-i", SRC.get(k, f"clips_label/{k}.mp4" if k in LABEL else f"clips/{k}.mp4")]
    f += f"[{i}:v]trim={a}:{a + d},setpts=PTS-STARTPTS,{GRACE if k == 'S2' else ''}scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}];"
f += "".join(f"[v{i}]" for i in range(len(EDIT))) + f"concat=n={len(EDIT)}:v=1:a=0[v]"
out = sys.argv[1] if len(sys.argv) > 1 else "out/bodyj_castor_rollon_r1.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-i", "vo/voiceover_tight.mp3", "-filter_complex", f, "-map", "[v]", "-map", f"{len(EDIT)}:a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest", out], check=True)
print("wrote", out)
