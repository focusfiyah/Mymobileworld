"""Free clip fixes (keep the clean window, play it forward then back; no stretch, no freeze). python3 clip_fix.py V2S5 V2S2 ...
  V2S5: Omni cuts to a front face (eye + mouth) at 1.2 s and the lips enter the top from 0.7 s: keep 0-0.65 s (a top crop cut the bristle head off, so no crop); V2S4 runs 0.5 s longer in cut.py
  V2S2: Seedance turns the hand from 0.9 s (crown ring and makeup gone): keep 0-0.85 s, forward-back-forward
  V2S3: Omni jumps to a macro at 1.96 s: its line uses the macro part 1.99-3.99 s (cut.py START)
  V2S7: the end shot = V2S3 0-1.9 s (push-in on the wet brush leaning on the basin), forward then back
  V3S3: a toilet edge comes in at the right from 2.8 s: keep 0-1.55 s"""
import subprocess, sys
SRC = {"V2S7": "V2S3"}   # V2S7 end shot = V2S3's push-in on the brush leaning on the basin (Ralph: old S7 "not good"; the paid S7 still drew a flared foot)
FIX = {"V2S7": (1.9, "null"), "V2S5": (0.65, "null"), "V2S2": (0.85, "null", 3), "V2S3": (1.05, "null"), "V3S3": (1.55, "null")}
for sid in sys.argv[1:]:
    t, vf, n = (FIX[sid] + (2,))[:3]
    parts = "".join(f"[p{i}]" if i % 2 == 0 else f"[r{i}]" for i in range(n))
    rev = "".join(f"[q{i}]reverse[r{i}];" for i in range(1, n, 2))
    fc = (f"[0:v]trim=0:{t},setpts=PTS-STARTPTS,{vf},split={n}" + "".join(f"[p{i}]" if i % 2 == 0 else f"[q{i}]" for i in range(n)) + ";"
          + rev + parts + f"concat=n={n}:v=1:a=0[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"clips/{SRC.get(sid, sid)}.mp4", "-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", f"clips/{sid}_fix.mp4"], check=True)
    print(sid, "->", f"clips/{sid}_fix.mp4", round(n * t, 2), "s")
