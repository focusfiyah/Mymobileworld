"""Cut a response video on its tight VO: python3 cut.py R1|R2. Each shot plays its clip at 1.0x from `cut_in` (default 0) for its VO
window `t` (shots.json); hard cuts; no text, no music. Writes out/shnuggle_<V>_raw.mp4, then the AI finish -> out/shnuggle_<V>.mp4."""
import json, subprocess, sys
V = sys.argv[1]; J = json.load(open("shots.json")); shots = J["videos"][V]
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
ins, f = [], ""
for i, s in enumerate(shots):
    a, d, c = s.get("cut_in", 0.0), s["t"][1] - s["t"][0], s.get("clip", f"clips/{s['id']}.mp4")
    assert a + d <= dur(c) + 0.01, f"{s['id']}: {a}+{d:.2f}s > clip {dur(c):.2f}s (never stretch)"
    ins += ["-i", c]
    n = round(s["t"][1] * 30) - round(s["t"][0] * 30); a0 = round(a * 30)   # whole frames on a shared 30 fps grid: no drift vs the VO
    f += f"[{i}:v]fps=30,trim=start_frame={a0}:end_frame={a0 + n},setpts=PTS-STARTPTS,{"crop=%d:%d:%d:%d," % (s["crop"][2], s["crop"][3], s["crop"][0], s["crop"][1]) if s.get("crop") else ""}scale=1080:1920:flags=lanczos,format=yuv420p[v{i}];"
f += "".join(f"[v{i}]" for i in range(len(shots))) + f"concat=n={len(shots)}:v=1:a=0[v]"
raw, out = f"out/shnuggle_{V}_raw.mp4", f"out/shnuggle_{V}.mp4"
subprocess.run(["mkdir", "-p", "out"])
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-i", f"vo/{V}_tight.wav", "-filter_complex", f, "-map", "[v]", "-map", f"{len(shots)}:a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest", raw], check=True)
# AI finish = ai_finish.sh's exact filter (grain 6, sharpen 0.6, saturation 0.92), plus a 12 Mbps cap: uncapped the grain made 300 MB files
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t", "-c:v", "libx264", "-crf", "18",
                "-maxrate", "12M", "-bufsize", "24M", "-preset", "veryfast", "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", out], check=True)
print("wrote", out, round(dur(out), 2))
