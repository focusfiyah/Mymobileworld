"""QC for the cut: python3 -I qc/verify.py  -> prints each gate OK/FAIL (flash, sync, levels, speed)."""
import json, re, subprocess, sys
J = json.load(open("shots.json")); F = "out/mute_nasal_dilator_r1.mp4"
def run(c): return subprocess.run(c, capture_output=True, text=True)
def dur(f, s="format"): return float(run(["ffprobe","-v","error","-show_entries",f"{s}=duration","-of","csv=p=0",f]).stdout.split()[0])
ok = True
def gate(n, c, m=""):
    global ok; print(("OK  " if c else "FAIL"), n, m); ok &= bool(c)
import importlib.util
JOIN = {"S1": (0.0, 5.22), "S2": (5.22, 10.26), "S3": (10.26, 15.30), "S4": (15.30, 19.34), "S5": (19.34, 25.38), "S6": (25.38, 29.42), "S7": (29.42, 34.81)}
for s in J["shots"]: s["t"] = list(JOIN.get(s["id"], s["t"]))
joins = [s["t"][0] for s in J["shots"][1:]]
cuts = [float(x) for x in re.findall(r"pts_time:([\d.]+)", run(["ffmpeg","-nostdin","-v","error","-i",F,"-vf","scale=108:192,select='gt(scene,0.2)',metadata=print:file=-","-an","-f","null","-"]).stdout)]
EVENTS = [25.79]  # S6: the lamp switch (light drops on the hand action), not a cut
stray = [c for c in cuts if min(abs(c-j) for j in joins + EVENTS) > 0.15]
close = [(a,b) for a,b in zip(joins, joins[1:]) if b-a < 0.25]
gate("flash: no cuts except the 7 shot joins, none <0.25s apart", not stray and not close, f"cuts={cuts} stray={stray}")
gate("sync: video length == VO length", abs(dur(F)-dur("vo/voiceover_tight.mp3"))<0.15, f"video {dur(F):.2f}s vs VO {dur('vo/voiceover_tight.mp3'):.2f}s")
gate("sync: windows contiguous, end at VO end", all(abs(a["t"][1]-b["t"][0])<0.01 for a,b in zip(J["shots"],J["shots"][1:])) and abs(J["shots"][-1]["t"][1]-dur('vo/voiceover_tight.mp3'))<0.1)
gate("speed: every clip >= window (1.0x, never stretched)", all(dur(f"clips/{s['id']}.mp4") + 0.05 >= (s["t"][1]-s["t"][0])  for s in J["shots"]))
m = run(["ffmpeg","-nostdin","-i",F,"-af","ebur128=peak=true","-f","null","-"]).stderr
i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1]); p = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", m)[-1])
gate("levels: -17..-15 LUFS, peak <= -1 dBFS", -17.5 <= i <= -14.5 and p <= -1.0, f"I={i} peak={p}")
txt = open("cut.py").read()
gate("no text overlay in cut.py", "drawtext" not in txt and "overlay=" not in txt)
sys.exit(0 if ok else 1)
