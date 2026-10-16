"""Cut a response video on its tight VO: python3 cut.py R1|R2. Each shot plays its clip at 1.0x from `cut_in` (default 0) for its VO
window `t` (shots.json); hard cuts; no text, no music. Writes out/shnuggle_<V>_raw.mp4, then the AI finish -> out/shnuggle_<V>.mp4."""
import json, subprocess, sys
V = sys.argv[1]; J = json.load(open("shots.json")); shots = J["videos"][V]
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
ins, f = [], ""
for i, s in enumerate(shots):
    a, d, c = s.get("cut_in", 0.0), s["t"][1] - s["t"][0], f"clips/{s['id']}.mp4"
    assert a + d <= dur(c) + 0.01, f"{s['id']}: {a}+{d:.2f}s > clip {dur(c):.2f}s (never stretch)"
    ins += ["-i", c]
    f += f"[{i}:v]trim={a}:{a + d},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}];"
f += "".join(f"[v{i}]" for i in range(len(shots))) + f"concat=n={len(shots)}:v=1:a=0[v]"
raw, out = f"out/shnuggle_{V}_raw.mp4", f"out/shnuggle_{V}.mp4"
subprocess.run(["mkdir", "-p", "out"])
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-i", f"vo/{V}_tight.wav", "-filter_complex", f, "-map", "[v]", "-map", f"{len(shots)}:a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest", raw], check=True)
subprocess.run(["bash", "../../.claude/skills/ugc-product-ad/scripts/ai_finish.sh", raw, out], check=True)
print("wrote", out, round(dur(out), 2))
