"""PRITECH V5-V9 cuts (2026-10-29), from ugc/pritech-15s/cut.py: 8 shots per video on Grace's own VO (vo/voiceover_final.wav,
her audio as posted, no re-levelling: a limiter reshapes word tails and fails the echo gate), no text, every clip at 1.0x, AI finish last.
  python3 cut.py V5 [V6 ...]  -> out/V5_review.mp4 (veryfast) + out/pritech_V5.mp4 (AI finish)
Each shot's window = its beat `t` in shots.json. START = second a shot starts inside its clip (default 0.2: skips the still-like
first frames), CROP = free crop (x, y, w) on the 1080x1920 clip (h follows 9:16) that keeps eyes/lips out after Omni zoomed out."""
import json, subprocess, sys
from pathlib import Path

HOLD = 0.35          # the last shot holds a beat after the voice ends (VO is 20.94 s)
VO = "vo/voiceover_final.wav"
START = {"V5S7": 0.6, "V8S4": 0.85, "V9S4": 0.5, "V9S8": 0.25}   # V8S4: the spray comes at 3 s; V9S4/V9S8: Omni reframes in the first frames
WIN = {"V8S7": (15.35, 18.65), "V8S8": (18.65, 20.95)}   # V8S7 runs 0.3 s into the CTA so V8S8 needs only its clean part
PINGPONG = {"V5S1": (0.10, 1.60), "V8S8": (0.05, 1.40), "V9S5": (0.10, 1.40)}   # clean part played forward then back (V1's approved free fix): V5S1 jumps to an extreme close-up at 2.6 s, V8S8 turns silver-grey after 1.4 s,
                                                          # V9S5's camera jumps to a front view with her eye at 1.5 s
CROP = {"V5S7": (60, 450, 827), "V9S5": (0, 200, 900)}   # Omni zoomed out and her eye came into frame (V5S7 clip check 0.26; V9S5 lashes in the top-right corner); crops keep cheek/jaw + brush
S = json.load(open("shots.json"))
dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)


def cut(v):
    shots = [s for s in S if s["video"] == v]
    edit = []
    for k, s in enumerate(shots):
        a, b = WIN.get(s["id"], s["t"]); d = b - a + (HOLD if k == len(shots) - 1 else 0)
        f = f"clips/{s['id']}.mp4"; st = START.get(s["id"], 0.2)
        if s["id"] in PINGPONG:
            pa, pb = PINGPONG[s["id"]]; assert 2 * (pb - pa) >= d - 1e-3, f"{s['id']} ping-pong {pa}-{pb} too short for {d:.2f} s"
        else:
            assert st + d <= dur(f) + 1e-3, f"{s['id']} window {st:.2f}+{d:.2f} runs past its {dur(f):.2f} s clip"
        x = ""
        if s["id"] in CROP:
            cx, cy, cw = CROP[s["id"]]; ch = round(cw * 16 / 9 / 2) * 2; cw = round(cw / 2) * 2
            x = f"crop={cw}:{ch}:{cx}:{cy},"
        edit.append((s["id"], f, st, d, x))
    end = sum(e[3] for e in edit); Path("out").mkdir(exist_ok=True)
    inputs, chains, cum = [], [], 0.0
    for i, (sid, f, st, d, xvf) in enumerate(edit):   # frame-exact: each segment ends on round(running total * 30)
        nf = round((cum + d) * 30) - round(cum * 30); cum += d
        if sid in PINGPONG:
            pa, pb = PINGPONG[sid]; inputs += ["-i", f]
            chains.append(f"[{i}:v]trim=start={pa}:end={pb},setpts=PTS-STARTPTS,fps=30,split[pf{i}][pr{i}];[pr{i}]reverse[prr{i}];[pf{i}][prr{i}]concat=n=2:v=1:a=0,trim=end_frame={nf},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,{xvf}scale=1080:1920:flags=lanczos,crop=1080:1920,format=yuv420p[v{i}]")
            continue
        inputs += ["-ss", f"{st:.3f}", "-i", f]
        chains.append(f"[{i}:v]setpts=PTS-STARTPTS,fps=30,trim=end_frame={nf},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,{xvf}scale=1080:1920:flags=lanczos,crop=1080:1920,format=yuv420p[v{i}]")
    n = len(edit)
    fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    rev = f"out/{v}_review.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", VO, "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                    "-af", f"apad,atrim=0:{end:.3f}", "-ar", "44100", "-t", f"{end:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", rev], check=True)
    # AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK §6 bitrate cap
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", rev, "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                    "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                    "-c:a", "copy", "-movflags", "+faststart", f"out/pritech_{v}.mp4"], check=True)
    print(f"out/pritech_{v}.mp4", round(end, 2), "s")
    for sid, f, st, d, x in edit: print(" ", sid, f, round(st, 2), round(d, 2), x)


if __name__ == "__main__":
    for v in sys.argv[1:]: cut(v)
