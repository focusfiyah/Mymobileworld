"""Cut: 4 clips on the Grace B voiceover (vo/voiceover_15.mp3 = tight VO at 1.07x). No text, no music.
Windows come from shots.json "t" (tight VO) divided by the VO speed-up. Footage is never slowed or sped up."""
import json, subprocess, sys
J = json.load(open("shots.json")); SPEED = 1.07; TAIL = 0.25
vo = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "vo/voiceover_15.mp3"], capture_output=True, text=True).stdout)
S = {s["id"]: s for s in J["shots"]}
w = {k: [S[k]["t"][0] / SPEED, S[k]["t"][1] / SPEED] for k in S}; w["S4"][1] = vo + TAIL
S2_MAX = 3.0   # S2 after ~3.0s: the cream turns into a solid white dome (not the real slotted top) -> S3 starts early instead
w["S3"][0] = w["S2"][0] + S2_MAX; w["S2"][1] = w["S3"][0]
ins, f, n = [], "", 4
for i, k in enumerate(["S1", "S2", "S3", "S4"]):
    s = S[k]; d = round(w[k][1] - w[k][0], 3); assert d <= s["dur"] + 0.04, f"{k} window {d}s > clip {s['dur']}s (never stretch)"
    ins += ["-i", f"clips/{k}.mp4"]; print(k, round(w[k][0], 2), round(w[k][1], 2), d)
    f += f"[{i}:v]trim=0:{d},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}];"
f += "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
out = sys.argv[1] if len(sys.argv) > 1 else "out/carpe_mb_15s.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-i", "vo/voiceover_15.mp3", "-filter_complex", f, "-map", "[v]", "-map", f"{n}:a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest", out], check=True)
print("wrote", out)
