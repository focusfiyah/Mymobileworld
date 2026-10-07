"""Cut r2 (Ralph 2026-10-07: "re-edit to match the visuals from the compare" = @deals.with.dreamer): product held to the lens at
frame 0, then the problem, then the application on camera during the claim + how-to, then the close. Same 4 clips, same Grace B VO
(vo/voiceover_15.mp3), no text, no music. Each clip plays at 1.0x from its own start; cut points sit in the gaps between words."""
import subprocess, sys
EDIT = [  # (clip, start in clip, length) ; output time in the comment
    ("S2", 0.0, 3.05),   # 0.00-3.05  hook "If you also hate when sweat shows through your shirt, look at this." -> product to the lens, cream rising (S2 is clean to ~3.0s)
    ("S1", 0.0, 3.83),   # 3.05-6.88  "Wet spots by noon? Carpe Mountain Breeze is clinically tested for up to" -> the sweat patch
    ("S3", 0.0, 3.55),   # 6.88-10.43 "a hundred hours of sweat and odor control. Pea-size, dry skin" (after ~3.6s the lifted stick shows a cream lump) -> the swipe on the underarm
    ("S4", 0.0, 5.0),    # 10.43-15.43 "at night. Only downside? You'll want a spare. Party season's coming. It's in the orange cart." -> spare into the gym bag
]
CLIP = {"S1": 5.04, "S2": 5.04, "S3": 4.04, "S4": 5.04}
ins, f = [], ""
for i, (k, a, d) in enumerate(EDIT):
    assert a + d <= CLIP[k] + 0.01, f"{k}: {a}+{d}s > clip (never stretch)"
    ins += ["-i", f"clips/{k}.mp4"]
    f += f"[{i}:v]trim={a}:{a + d},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}];"
f += "".join(f"[v{i}]" for i in range(len(EDIT))) + f"concat=n={len(EDIT)}:v=1:a=0[v]"
out = sys.argv[1] if len(sys.argv) > 1 else "out/carpe_mb_15s.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-i", "vo/voiceover_15.mp3", "-filter_complex", f, "-map", "[v]", "-map", f"{len(EDIT)}:a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest", out], check=True)
print("wrote", out)
