"""Cut the Shnuggle "next bath" video on its voiceover: python3 cut.py [--review]. Each shot plays its clip at 1.0x from `cut_in`
(default 0) for its VO window `t` (shots.json, set by vo.py); hard cuts; no text, no music. Writes out/shnuggle_next_bath_raw.mp4,
then the AI finish (ai_finish.sh's filter: grain 6, sharpen 0.6, saturation 0.92) -> out/shnuggle_next_bath.mp4.
--review: veryfast + 720p for a quick look (Ralph's speed rule); the final always runs without it."""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
J = json.loads((HERE / "shots.json").read_text()); shots = J["shots"]; REVIEW = "--review" in sys.argv
W, H = (720, 1280) if REVIEW else (1080, 1920)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout)
ins, f = [], ""
for i, s in enumerate(shots):
    c = HERE / s.get("clip", f"clips/{s['id']}.mp4"); a = s.get("cut_in", 0.0)
    n = round(s["t"][1] * 30) - round(s["t"][0] * 30); a0 = round(a * 30)   # whole frames on a shared 30 fps grid: no drift vs the VO
    assert (a0 + n) / 30 <= dur(c) + 0.01, f"{s['id']}: {a}+{n / 30:.2f}s > clip {dur(c):.2f}s (never stretch)"
    ins += ["-i", str(c)]
    crop = "crop=%d:%d:%d:%d," % tuple(s["crop"]) if s.get("crop") else ""
    f += f"[{i}:v]fps=30,trim=start_frame={a0}:end_frame={a0 + n},setpts=PTS-STARTPTS,{crop}scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[v{i}];"
f += "".join(f"[v{i}]" for i in range(len(shots))) + f"concat=n={len(shots)}:v=1:a=0[v]"
(HERE / "out").mkdir(exist_ok=True)
tag = "_review" if REVIEW else ""
raw, out = HERE / f"out/shnuggle_next_bath{tag}_raw.mp4", HERE / f"out/shnuggle_next_bath{tag}.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-i", str(HERE / "vo/voiceover.mp3"), "-filter_complex", f, "-map", "[v]", "-map", f"{len(shots)}:a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest", str(raw)], check=True)
# ai_finish (PLAYBOOK §6, last step): same filter as .claude/skills/ugc-product-ad/scripts/ai_finish.sh, capped bitrate (grain bloats files)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t", "-c:v", "libx264", "-crf", "18",
                "-maxrate", "12M", "-bufsize", "24M", "-preset", "veryfast" if REVIEW else "medium", "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "copy",
                "-movflags", "+faststart", str(out)], check=True)
print("wrote", out, round(dur(out), 2))
