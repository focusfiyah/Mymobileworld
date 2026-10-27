"""PRITECH V2-V4 cuts (2026-10-27), from ugc/pritech-cleansing-brush/cut.py: clip windows on Grace's voiceover, no text, every clip at 1.0x, AI finish last.
  python3 cut.py V2 [V3 V4]  -> out/<V>_review.mp4 (veryfast) + out/pritech_<V>.mp4 (AI finish)
Each shot's window = its line's time in vo/<V>/windows.json. FIX picks a fixed clip file, START the second a shot's window begins in its clip,
SHIFT moves a cut later (+) so a long line borrows time from the next shot."""
import json, subprocess, sys
from pathlib import Path

HOLD = 0.6                       # hold the last shot a beat after the voice ends
VO = {"V2": "vo/V2/voiceover_final.mp3", "V3": "vo/V3/voiceover_paced.mp3", "V4": "vo/V4/voiceover_paced.mp3"}
FIX = {}                         # shot -> clips/<file>.mp4 (free fixes)
START = {}                       # shot -> start second inside its clip
SHIFT = {"V2S1": -0.22}          # V2S1's line runs 4.20 s, its clip 4.04 s: cut to V2S2 0.22 s early (hands show under "Yeah")
S = json.load(open("shots.json"))
dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)


def cut(v):
    win = json.load(open(f"vo/{v}/windows.json")); shots = [s for s in S if s["video"] == v]
    edit = []
    for k, s in enumerate(shots):
        a, b = win[s["id"]]
        d = b - a + (HOLD if k == len(shots) - 1 else 0) + SHIFT.get(s["id"], 0) - (SHIFT.get(shots[k - 1]["id"], 0) if k else 0)
        f = f"clips/{FIX.get(s['id'], s['id'])}.mp4"; st = START.get(s["id"], 0.0)
        assert st + d <= dur(f) + 1e-3, f"{s['id']} window {st:.2f}+{d:.2f} runs past its {dur(f):.2f} s clip"
        edit.append((s["id"], f, st, d))
    end = sum(e[3] for e in edit); Path("out").mkdir(exist_ok=True)
    inputs, chains, cum = [], [], 0.0
    for i, (sid, f, st, d) in enumerate(edit):   # frame-exact: each segment ends on round(running total * 30)
        nf = round((cum + d) * 30) - round(cum * 30); cum += d
        inputs += ["-ss", f"{st:.3f}", "-i", f]
        chains.append(f"[{i}:v]setpts=PTS-STARTPTS,fps=30,trim=end_frame={nf},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,format=yuv420p[v{i}]")
    n = len(edit)
    fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    rev = f"out/{v}_review.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", VO[v], "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                    "-af", f"apad,atrim=0:{end:.3f},loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-t", f"{end:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", rev], check=True)
    # AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK §6 bitrate cap
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", rev, "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                    "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                    "-c:a", "copy", "-movflags", "+faststart", f"out/pritech_{v}.mp4"], check=True)
    print(f"out/pritech_{v}.mp4", round(end, 2), "s")
    for sid, f, st, d in edit: print(" ", sid, f, st, round(d, 2))


if __name__ == "__main__":
    for v in sys.argv[1:]: cut(v)
