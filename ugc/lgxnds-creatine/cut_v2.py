"""v2 cut (2026-10-19 redo): 7 shots on the trimmed Grace B voiceover (vo/v2_voiceover_tight.mp3), no text overlay.

  python3 cut_v2.py [--v5]   -> out/lgxnds_creatine_v4(_raw).mp4, or v5 (no pasted label), via ai_finish.sh

Every piece is real clip footage at 1.0x (no holds, no Ken Burns). Frame ranges were picked by QC (clips_v2/lab/*.jpg):
S1 pour onto the counter, first 2.4 s; S2 pour (0-40) + bottle clearing (62-120, cropped 1.16x so the powder ring on the
counter stays out of frame); S3/S4/S5/S7 full or near-full; S6 from frame 48 (label.py --flow --from 48 output) where the tub
goes into the bag. Tub clips carry the real label (label.py: S3 --flow --wordmark, S4/S5 --track, S6 --flow --rigid --from 48,
S7 --ref 0, all --deshade). Pieces run slightly off the line breaks so no clip is stretched.
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIN = ROOT / ".claude/skills/ugc-product-ad/scripts/ai_finish.sh"
raw, fin = "out/lgxnds_creatine_v4_raw.mp4", "out/lgxnds_creatine_v4.mp4"
# (source, first frame, frame count, extra filter)
P = [("clips_v2/S1.mp4", 0, 57, ""),
     ("clips_v2/S2.mp4", 0, 41, ""),
     ("clips_v2/S2.mp4", 62, 59, "crop=619:1100:50:0,"),
     ("clips_v2/lab/S3.mp4", 0, 97, ""),
     ("clips_v2/lab/S4.mp4", 0, 111, ""),
     ("clips_v2/lab/S5.mp4", 0, 78, ""),
     ("clips_v2/lab/S6.mp4", 0, 49, ""),
     ("clips_v2/lab/S7.mp4", 0, 120, "")]
if "--v5" in sys.argv:   # 2026-10-19 (Ralph: pasted label looks fake): no paste anywhere; tub clips from the clean Google stills,
    # Seedance reference mode (real label as a ref) for hand shots, Kling for hand-free; S7 second lid removed (lid_fix.py)
    P = P[:3] + [("clips_v2/S3_refs.mp4", 0, 97, ""), ("clips_v2/S4_raw.mp4", 0, 111, ""), ("clips_v2/S5_raw.mp4", 0, 78, ""),
                 ("clips_v2/S6_refs.mp4", 0, 49, ""), ("clips_v2/lab/S7_v5.mp4", 0, 120, "")]
    raw, fin = "out/lgxnds_creatine_v5_raw.mp4", "out/lgxnds_creatine_v5.mp4"
inp, ch = [], []
for i, (src, a, n, f) in enumerate(P):
    inp += ["-i", src]
    ch.append(f"[{i}:v]trim=start_frame={a}:end_frame={a + n},setpts=PTS-STARTPTS,{f}scale=720:1280:flags=lanczos,setsar=1,fps=24[v{i}]")
k = len(P)
fc = ";".join(ch) + ";" + "".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0[v]"
Path("out").mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp, "-i", "vo/v2_voiceover_tight.mp3", "-filter_complex", fc,
                "-map", "[v]", "-map", f"{k}:a", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", raw], check=True)
subprocess.run(["bash", str(FIN), raw, fin], check=True)
print("frames", sum(p[2] for p in P), "=", round(sum(p[2] for p in P) / 24, 3), "s")
