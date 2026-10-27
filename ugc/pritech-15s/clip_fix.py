"""Free clip fixes (keep the clean window, play it forward then back; no stretch, no freeze). python3 clip_fix.py V2S5 V2S2 ...
  V2S5: Omni cuts to a front face (eye + mouth) at 1.2 s and the lips enter the top from 0.7 s: keep 0-0.65 s (a top crop cut the bristle head off, so no crop); V2S4 runs 0.5 s longer in cut.py
  V2S2: Seedance turns the hand at 1.3 s (crown ring and makeup gone): keep 0-1.2 s
  V2S3: Omni jumps to a macro at 1.7 s: keep 0-1.05 s
  V3S3: a toilet edge comes in at the right from 2.8 s: keep 0-1.55 s"""
import subprocess, sys
FIX = {"V2S5": (0.65, "null"), "V2S2": (1.2, "null"), "V2S3": (1.05, "null"), "V3S3": (1.55, "null")}
for sid in sys.argv[1:]:
    t, vf = FIX[sid]
    fc = f"[0:v]trim=0:{t},setpts=PTS-STARTPTS,{vf},split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0[v]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"clips/{sid}.mp4", "-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", f"clips/{sid}_fix.mp4"], check=True)
    print(sid, "->", f"clips/{sid}_fix.mp4", 2 * t, "s")
