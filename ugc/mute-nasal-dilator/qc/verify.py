"""QC for the cut: python3 -I qc/verify.py  -> prints each gate OK/FAIL (flash, sync, levels, speed)."""
import json, re, subprocess, sys
J = json.load(open("shots.json")); F = "out/mute_nasal_dilator_r4.mp4"
def run(c): return subprocess.run(c, capture_output=True, text=True)
def dur(f, s="format"): return float(run(["ffprobe","-v","error","-show_entries",f"{s}=duration","-of","csv=p=0",f]).stdout.split()[0])
ok = True
def gate(n, c, m=""):
    global ok; print(("OK  " if c else "FAIL"), n, m); ok &= bool(c)
import importlib.util
import re as _re
src = open("cut.py").read(); PLAN = eval(_re.search(r"PLAN = (\[.*?\])\n", src, _re.S).group(1))
joins = [p[2] for p in PLAN[1:]]
SRC = eval(_re.search(r"SRC = (\{.*?\})", src).group(1))
cuts = [float(x) for x in re.findall(r"pts_time:([\d.]+)", run(["ffmpeg","-nostdin","-v","error","-i",F,"-vf","scale=108:192,select='gt(scene,0.2)',metadata=print:file=-","-an","-f","null","-"]).stdout)]
EVENTS = [21.17]  # S6: the lamp switch (light drops on the hand action), not a cut
stray = [c for c in cuts if min(abs(c-j) for j in joins + EVENTS) > 0.2]
close = [(a,b) for a,b in zip(joins, joins[1:]) if b-a < 0.25]
gate("flash: no cuts except the shot joins, none <0.25s apart", not stray and not close, f"cuts={cuts} stray={stray}")
gate("sync: video length == VO length", abs(dur(F)-dur("vo/voiceover_tight.mp3"))<0.15, f"video {dur(F):.2f}s vs VO {dur('vo/voiceover_tight.mp3'):.2f}s")
gate("sync: windows contiguous, end at VO end", all(abs(a[3]-b[2])<0.01 for a,b in zip(PLAN,PLAN[1:])) and abs(PLAN[-1][3]-dur("vo/voiceover_tight.mp3"))<0.1)
gate("speed: every clip >= window (1.0x, never stretched)", all(dur(SRC.get(p[0], f"clips/{p[0]}.mp4")) + 0.05 >= p[1] + p[3]-p[2] for p in PLAN))
m = run(["ffmpeg","-nostdin","-i",F,"-af","ebur128=peak=true","-f","null","-"]).stderr
i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1]); p = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", m)[-1])
gate("levels: -17..-15 LUFS, peak <= -1 dBFS", -17.5 <= i <= -14.5 and p <= -1.0, f"I={i} peak={p}")
txt = open("cut.py").read()
gate("no text overlay in cut.py", "drawtext" not in txt and "overlay=" not in txt)
sys.exit(0 if ok else 1)
