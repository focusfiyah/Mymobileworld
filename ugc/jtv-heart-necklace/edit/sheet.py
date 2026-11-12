"""python3 sheet.py N -> sheets/V{N}_6fps.png (every 1/6 s, 12 per row) for frame QC."""
import subprocess, sys
v = sys.argv[1]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"out/necklace_V{v}.mp4", "-vf",
  "fps=6,scale=120:-1,drawtext=text='%{pts\\:flt}':x=2:y=2:fontsize=13:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=16x6",
  "-frames:v", "1", f"sheets/V{v}_6fps.png"], check=True)
