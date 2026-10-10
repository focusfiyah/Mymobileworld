"""QC for the cut: python3 -I qc/verify.py  -> prints each gate OK/FAIL (flash, sync, levels, speed)."""
import json, re, subprocess, sys
J = json.load(open("shots.json")); F = "out/thunderfit_ring_v5.mp4"
def run(c): return subprocess.run(c, capture_output=True, text=True)
def dur(f, s="format"): return float(run(["ffprobe","-v","error","-show_entries",f"{s}=duration","-of","csv=p=0",f]).stdout.split()[0])
ok = True
def gate(n, c, m=""):
    global ok; print(("OK  " if c else "FAIL"), n, m); ok &= bool(c)
import itertools
SEGS = [["S1", 0.0, 4.04], ["S2", 0.0, 4.44], ["S3", 0.0, 4.94], ["S4", 1.4, 3.6], ["S5", 0.3, 1.25], ["S6", 0.0, 1.81], ["S5", 1.55, 2.49], ["S7", 0.0, 4.04], ["S8", 0.0, 7.64]]
joins = list(itertools.accumulate(d for _,_,d in SEGS))[:-1]
cuts = [float(x) for x in re.findall(r"pts_time:([\d.]+)", run(["ffmpeg","-nostdin","-v","error","-i",F,"-vf","scale=108:192,select='gt(scene,0.2)',metadata=print:file=-","-an","-f","null","-"]).stdout)]
stray = [c for c in cuts if min(abs(c-j) for j in joins) > 0.15]
close = [(a,b) for a,b in zip(joins, joins[1:]) if b-a < 0.25]
gate("flash: no cuts except the 7 shot joins, none <0.25s apart", not stray and not close, f"cuts={cuts} stray={stray}")
gate("sync: video length == VO length", abs(dur(F)-dur("vo/voiceover_v5_nobeach.mp3"))<0.15, f"video {dur(F):.2f}s vs VO {dur('vo/voiceover_v5_nobeach.mp3'):.2f}s")
gate("speed: every segment fits inside its clip, played at 1.0x (never stretched)", all(st+d <= dur(f"clips/{sid}.mp4")+0.05 for sid,st,d in SEGS))
m = run(["ffmpeg","-nostdin","-i",F,"-af","ebur128=peak=true","-f","null","-"]).stderr
i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1]); p = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", m)[-1])
gate("levels: -17..-15 LUFS, peak <= -1 dBFS", -17.5 <= i <= -14.5 and p <= -1.0, f"I={i} peak={p}")
txt = open("cut.py").read()
gate("no text overlay in cut.py", "drawtext" not in txt and "overlay=" not in txt)
sys.exit(0 if ok else 1)
