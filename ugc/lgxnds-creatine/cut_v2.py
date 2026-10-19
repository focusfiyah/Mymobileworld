"""v2 cut (2026-10-19 redo): 7 shots on the trimmed Grace B voiceover (vo/v2_voiceover_tight.mp3), no text overlay.

  python3 cut_v2.py   -> out/lgxnds_creatine_v4_raw.mp4, then ai_finish.sh -> out/lgxnds_creatine_v4.mp4

Every piece is real clip footage at 1.0x (no holds, no Ken Burns). Frame ranges were picked by QC (clips_v2/lab/*.jpg):
S1 pour onto the counter, first 2.4 s; S2 pour (0-40) + bottle clearing (62-120, cropped 1.16x so the powder ring on the
counter stays out of frame); S3/S4/S5/S7 full or near-full; S6 from frame 48 (label.py --flow --from 48 output) where the tub
goes into the bag. Tub clips carry the real label (label.py: S3 --flow --wordmark, S4/S5 --track, S6 --flow --rigid --from 48,
S7 --ref 0, all --deshade). Pieces run slightly off the line breaks so no clip is stretched.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIN = ROOT / ".claude/skills/ugc-product-ad/scripts/ai_finish.sh"
# (source, first frame, frame count, extra filter)
P = [("clips_v2/S1.mp4", 0, 57, ""),
     ("clips_v2/S2.mp4", 0, 41, ""),
     ("clips_v2/S2.mp4", 62, 59, "crop=619:1100:50:0,"),
     ("clips_v2/lab/S3.mp4", 0, 97, ""),
     ("clips_v2/lab/S4.mp4", 0, 111, ""),
     ("clips_v2/lab/S5.mp4", 0, 78, ""),
     ("clips_v2/lab/S6.mp4", 0, 49, ""),
     ("clips_v2/lab/S7.mp4", 0, 120, "")]
inp, ch = [], []
for i, (src, a, n, f) in enumerate(P):
    inp += ["-i", src]
    ch.append(f"[{i}:v]trim=start_frame={a}:end_frame={a + n},setpts=PTS-STARTPTS,{f}scale=720:1280:flags=lanczos,setsar=1,fps=24[v{i}]")
k = len(P)
fc = ";".join(ch) + ";" + "".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0[v]"
Path("out").mkdir(exist_ok=True)
raw, fin = "out/lgxnds_creatine_v4_raw.mp4", "out/lgxnds_creatine_v4.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp, "-i", "vo/v2_voiceover_tight.mp3", "-filter_complex", fc,
                "-map", "[v]", "-map", f"{k}:a", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", raw], check=True)
subprocess.run(["bash", str(FIN), raw, fin], check=True)
print("frames", sum(p[2] for p in P), "=", round(sum(p[2] for p in P) / 24, 3), "s")
