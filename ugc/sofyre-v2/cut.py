"""Free cut: shots on the trimmed Grace B voiceover, no text overlay (Ralph has not asked for one).
  python3 cut.py V1 [V2 V3]  -> out/<V>_raw.mp4 (720x1280, 24fps); then ai_finish.sh -> out/<V>.mp4
Windows come from shots.json (vo.py). Real clip footage, never slower than 1.0x (speed-ups only).
SRC[id] = (start, end) of the source used; None end = start + window at 1.0x. BOUND[id] = new start time of that shot
(moves the cut point, e.g. picture keeps running a beat into the next line)."""
import json, subprocess, sys
from pathlib import Path
J = json.loads(Path("shots.json").read_text())
SRC = {"V1S1": (0.0, 3.6), "V3S1": (2.0, 4.0), "V1S4": (0.0, 1.6), "V1S5": (0.0, 1.0), "V1S6": (0.5, 5.0),
       "V2S1": (0.0, 4.7), "V2S5": (0.5, 3.3), "V2S6": (0.2, 4.0),
       "V3S2": (3.4, 4.03), "V3S5": (0.0, 1.4), "V3S6": (0.0, 1.5), "V3S8": (0.8, 2.9)}   # chosen after the clip check
BOUND = {"V1S2": 3.5, "V2S2": 2.6}
for V in sys.argv[1:]:
    S = [s for s in J["shots"] if s["vid"] == V]
    for s in S:
        if s["id"] in BOUND:
            k = S.index(s); S[k - 1]["t"][1] = BOUND[s["id"]]; s["t"][0] = BOUND[s["id"]]
    inputs, chains, labels = [], [], []
    for i, s in enumerate(S):
        t0, t1 = s["t"]; win = t1 - t0; src = f"clips/{s['id']}.mp4"
        clip_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
        a, b = SRC.get(s["id"], (0.0, None)); b = b or a + win
        assert b <= clip_len + 0.05, f"{s['id']} needs {b:.2f}s of a {clip_len:.2f}s clip"
        speed = (b - a) / win; assert speed >= 0.999, f"{s['id']} would be slowed to {speed:.2f}x"
        inputs += ["-i", src]
        chains.append(f"[{i}:v]trim=start={a:.3f}:end={b:.3f},setpts=(PTS-STARTPTS)/{speed:.4f},scale=720:1280,setsar=1,fps=24,trim=duration={win:.3f}[v{i}]")
        labels.append(f"[v{i}]"); print(s["id"], f"src {a:.2f}-{b:.2f}  win {win:.2f}  speed {speed:.2f}x")
    n = len(S); total = S[-1]["t"][1]
    chains.append(f"{''.join(labels)}concat=n={n}:v=1:a=0[c0]"); chains.append("[c0]format=yuv420p[vout]")
    inputs += ["-i", f"vo/{V}_tight.mp3"]
    chains.append(f"[{n}:a]apad,atrim=duration={total},loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
    Path("out").mkdir(exist_ok=True); out = f"out/{V}_raw.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains), "-map", "[vout]", "-map", "[aout]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-threads", "4", "-c:a", "aac", "-b:a", "160k", "-t", str(total), "-movflags", "+faststart", out], check=True)
    print(out, total)
