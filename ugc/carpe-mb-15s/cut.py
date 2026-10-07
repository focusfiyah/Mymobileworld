"""Cut r2 (Ralph 2026-10-07: "re-edit to match the visuals from the compare" = @deals.with.dreamer): product held to the lens at
frame 0, then the problem, then the application on camera during the claim + how-to, then the close. Same 4 clips, same Grace B VO
(vo/voiceover_15.mp3), no text, no music. Each clip plays at 1.0x from its own start; cut points sit in the gaps between words."""
import subprocess, sys
EDIT = [  # r3 (Ralph 2026-10-07: no twisting the body, pea-size not a white patch, every shot <= 3s, stain shorter). (clip, start, length)
    ("A", 0.0, 2.3),    # 0.00-2.30  "If you also hate when sweat shows through your shirt," -> stick lifted to the lens, held still (real panel pasted)
    ("S1", 0.0, 2.0),   # 2.30-4.30  "look at this. Wet spots by noon?" -> sweat stain (2.0s)
    ("S4", 0.0, 2.6),   # 4.30-6.90  "Carpe Mountain Breeze is clinically tested for up to" -> two sticks on the marble
    ("B", 0.0, 1.5),    # 6.90-8.40  "a hundred hours of sweat and" -> one light swipe, clear sheen (after 1.5s the label warps)
    ("C", 0.0, 2.6),    # 8.40-11.00 "odor control. Pea-size, dry skin, at night." -> stick held still, small dab in the slots
    ("S4", 2.6, 2.0),   # 11.00-13.00 "Only downside? You'll want a spare." -> spare into the gym bag
    ("A", 2.5, 2.53),   # 13.00-15.53 "Party season's coming. It's in the orange cart." -> stick held to the lens
]
CLIP = {"S1": 5.04, "S2": 5.04, "S3": 4.04, "S4": 5.04, "A": 5.04, "B": 4.04, "C": 4.04}
SRC = {"A": "clips_fixed/A.mp4", "B": "clips_fixed/B.mp4", "C": "clips_fixed/C.mp4"}
ins, f = [], ""
for i, (k, a, d) in enumerate(EDIT):
    assert a + d <= CLIP[k] + 0.01, f"{k}: {a}+{d}s > clip (never stretch)"
    ins += ["-i", SRC.get(k, f"clips/{k}.mp4")]
    f += f"[{i}:v]trim={a}:{a + d},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}];"
f += "".join(f"[v{i}]" for i in range(len(EDIT))) + f"concat=n={len(EDIT)}:v=1:a=0[v]"
out = sys.argv[1] if len(sys.argv) > 1 else "out/carpe_mb_15s.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-i", "vo/voiceover_15.mp3", "-filter_complex", f, "-map", "[v]", "-map", f"{len(EDIT)}:a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest", out], check=True)
print("wrote", out)
