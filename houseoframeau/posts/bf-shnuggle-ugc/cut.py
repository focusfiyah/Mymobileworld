"""HofR BF version of Grace's real 'Shnuggle Toddler Tub UGC 1080' (Drive 1th71ktg0U7KD6QlWKji-YfSh-pUhX_d9, 37 s, her own POV hook text
burned in, her audio). Ralph 2026-11-25 tapped "UGC 1080 (37 s)". Own framing (1.04 zoom anchored at top so her hook text stays in the
safe zone) + own grade; no captions, no AI label (real footage).  python3 cut.py SRC.mp4"""
import subprocess, sys
from pathlib import Path
out = Path(__file__).resolve().parent / "out/shnuggle_hofr.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", sys.argv[1], "-vf",
    "crop=iw/1.04:ih/1.04:(iw-iw/1.04)/2:0,scale=1080:1920:flags=lanczos,eq=brightness=0.025:contrast=1.03:saturation=0.98,setsar=1,format=yuv420p",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "copy", "-movflags", "+faststart", str(out)], check=True)
print("CUT_DONE", out)
