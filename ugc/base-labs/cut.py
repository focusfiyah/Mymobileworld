"""Free cut for the two Base Laboratories videos (silent: Grace records her own VO).
  python3 cut.py pads|oil [A|B|C]   -> <job>/out/<job>_<opt>.mp4 (720x1280, 24fps, silent track)
Pieces are (clip, start, dur), hard cuts, every piece at 1.0x (never stretched). Pain beat = the clean parts of the two hands-free steam shots
(Seedance added a mismatched hand after ~2.3s / ~0.9s). Pop-up = the brand's real packshot over the label shot (hides AI label garble).
Hook text = TikTok Classic style (classic_caption.py), one text per script option so each post has its own.
"""
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/ugc-product-ad/scripts"))
from classic_caption import classic_png
job, opt = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "A")
TEXT = {"pads": {"A": "step after shaving", "B": "the step everyone skips", "C": "step two"},
        "oil": {"A": "oil for ingrown hairs?", "B": "your skin after shaving", "C": "shave, then this"}}[job][opt]
P = {"pads": [("pads/clips/S1.mp4", 0, 5.0), ("oil/clips/S2.mp4", 0, 2.3), ("pads/clips/S2.mp4", 0, 0.9), ("pads/clips/S3.mp4", 0, 4.0),
              ("pads/clips/S4a.mp4", 0, 4.0), ("pads/clips/S4b.mp4", 0, 2.0), ("pads/clips/S5.mp4", 0, 5.0), ("pads/clips/S6.mp4", 0, 6.0)],
     "oil": [("oil/clips/S1.mp4", 0, 5.0), ("pads/clips/S2.mp4", 0, 0.9), ("oil/clips/S2.mp4", 0, 2.3), ("oil/clips/S3.mp4", 0, 4.0),
             ("oil/clips/S4a.mp4", 0, 4.0), ("oil/clips/S4b.mp4", 0, 4.0), ("oil/clips/S5.mp4", 0, 5.0), ("oil/clips/S6.mp4", 0, 6.0)]}[job]
total = sum(p[2] for p in P); pop_t = total - 6 - 5   # label shot = 5th from the end
inputs, ch = [], []
for i, (f, s, d) in enumerate(P):
    inputs += ["-i", f]
    ch.append(f"[{i}:v]trim=start={s}:duration={d},setpts=PTS-STARTPTS,scale=720:1280,setsar=1,fps=24[v{i}]")
ch.append("".join(f"[v{i}]" for i in range(len(P))) + f"concat=n={len(P)}:v=1:a=0[c0]")
capf = Path(job) / "out" / f"_hook_{opt}.png"; capf.parent.mkdir(exist_ok=True); classic_png(TEXT, 720, 1280).save(capf)
popf = f"{job}/refs/popup.png"
inputs += ["-loop", "1", "-i", str(capf), "-loop", "1", "-i", popf]
n = len(P)
ch.append(f"[c0][{n}:v]overlay=0:0:enable='between(t,0,3.0)'[c1]")
PW, PY = {"pads": (400, 820), "oil": (250, 760)}[job]
ch.append(f"[{n+1}:v]format=rgba,scale=w='{PW}*min(1,0.9+t*0.8)':h=-1:eval=frame,fade=t=in:st=0:d=0.15:alpha=1,fade=t=out:st=2.05:d=0.15:alpha=1,setpts=PTS-STARTPTS+{pop_t+1.0}/TB[bn]")
ch.append(f"[c1][bn]overlay=x=30:y={PY}:enable='between(t,{pop_t+1.0},{pop_t+3.2})':eof_action=pass,format=yuv420p[vout]")
inputs += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
out = f"{job}/out/{job}_{opt}.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(ch), "-map", "[vout]", "-map", f"{n+2}:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "64k", "-t", f"{total:.3f}", "-movflags", "+faststart", out], check=True)
print(out, f"{total:.1f}s")
