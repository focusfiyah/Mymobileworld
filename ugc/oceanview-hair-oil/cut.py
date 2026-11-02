"""Ocean View hair oil cut (music only), 2026-11-02. Trims each clip to its window, 1080x1920, concat, Mixkit music,
then ai_finish. Review render: veryfast, all cores. No text drawn (hard rule 6; no text_overlay_ok)."""
import subprocess, sys, json
from pathlib import Path
# shot, file, start in clip, length (s)
EDL = [("S1", "clips/S1_crop.mp4", 0.6, 2.0), ("S2", "clips/S2.mp4", 0.4, 1.4), ("S3", "clips/S3.mp4", 0.4, 1.6),
       ("S4", "clips/S4_t1_crop.mp4", 0.5, 1.6), ("S5", "clips/S5.mp4", 0.4, 1.4), ("S6", "clips/S6.mp4", 0.4, 1.6),
       ("S7", "clips/S7.mp4", 0.3, 2.0)]
MUSIC, MSTART = "music/mixkit_872.mp3", 4.0
OUT = sys.argv[1] if len(sys.argv) > 1 else "cuts/v1_raw.mp4"
Path("cuts/parts").mkdir(parents=True, exist_ok=True)
VF = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,setsar=1,format=yuv420p"
parts = []
for sid, f, ss, d in EDL:
    p = f"cuts/parts/{sid}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(d), "-i", f, "-vf", VF, "-an", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "17", "-threads", "4", p], check=True)
    parts.append(p)
Path("cuts/parts/list.txt").write_text("".join(f"file '{Path(p).name}'\n" for p in parts))
total = sum(d for *_, d in EDL)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "cuts/parts/list.txt", "-ss", str(MSTART), "-t", str(total),
                "-i", MUSIC, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-threads", "4",
                "-af", f"afade=t=in:d=0.15,afade=t=out:st={total-0.6}:d=0.6,loudnorm=I=-14:TP=-1.5", "-c:a", "aac", "-b:a", "192k",
                "-shortest", OUT], check=True)
print("CUT_OK", OUT, round(total, 2))
