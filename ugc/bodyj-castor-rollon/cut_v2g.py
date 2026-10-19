"""Cut v2g (2026-10-18): Grace's own script (v2g/vo/voiceover_tight.mp3, 39.0 s) over the approved r1 clips + 4 new shots (N1-N4).
Every clip at 1.0x from its own start or an unused tail (never stretched); cuts between words (v2g/vo/words_trimmed.json). No text, no music.
  python3 cut_v2g.py [OUT]"""
import subprocess, sys
EDIT = [  # (clip, start, length)
    ("S3", 0.0, 4.41),   #  0.00-4.41  "The ONLY thing I don't like about castor oil is how thick and messy it is."
    ("N1", 0.0, 4.64),   #  4.41-9.05  "You're trying to apply a little, and suddenly it's dripping down your hands and getting everywhere."
    ("N2", 0.0, 4.30),   #  9.05-13.35 "And let's be for real, the smell isn't exactly something you want lingering all day!"
    ("S1", 0.0, 3.82),   # 13.35-17.17 "But if you know, you know, castor oil is liquid gold!"
    ("S8", 0.0, 2.42),   # 17.17-19.59 "But this roll-on? Freaking genius!"
    ("S4", 0.0, 4.10),   # 19.59-23.69 "No pouring, no oily fingers, just roll it exactly where you want it."
    ("S8", 2.42, 1.72),  # 23.69-25.41 "It's USDA organic,"
    ("S5", 0.0, 3.36),   # 25.41-28.77 "cold-pressed and hexane-free, with a rose quartz roller." (the pink ball rolling)
    ("S9", 0.0, 2.58),   # 28.77-31.35 "Imma do y'all a favor and link it in the orange cart!"
    ("N3", 0.0, 1.64),   # 31.35-32.99 "If you want conditioned brows,"
    ("N4", 0.0, 1.20),   # 32.99-34.19 "softer cuticles,"
    ("S6", 0.0, 1.08),   # 34.19-35.27 "moisturized skin,"
    ("S7", 0.0, 2.64),   # 35.27-37.91 "and hair growing longer, smoother and shinier,"
    ("S9", 2.58, 1.12),  # 37.91-39.03 "you know what to do!" (hand lifts the roller off the nightstand)
]
LABEL = {"S1", "S5", "S7", "S8", "S9", "N4"}   # real label pasted (label_track.py); S4 S6 N3 too small/turned to track
PRE = {"N3": "crop=562:1000:80:40,"}            # brows: crop out the lips (no talking mouth on screen during the VO)
ins, f = [], ""
for i, (k, a, d) in enumerate(EDIT):
    assert a + d <= 5.04 + 0.01, f"{k}: {a}+{d}s > clip (never stretch)"
    ins += ["-i", f"clips_label/{k}.mp4" if k in LABEL else f"clips/{k}.mp4"]
    f += f"[{i}:v]trim={a}:{a + d},setpts=PTS-STARTPTS,{PRE.get(k, '')}scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}];"
f += "".join(f"[v{i}]" for i in range(len(EDIT))) + f"concat=n={len(EDIT)}:v=1:a=0[v]"
out = sys.argv[1] if len(sys.argv) > 1 else "out/bodyj_castor_v2g_r1.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-i", "v2g/vo/voiceover_tight.mp3", "-filter_complex", f, "-map", "[v]", "-map", f"{len(EDIT)}:a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest", out], check=True)
print("wrote", out)
