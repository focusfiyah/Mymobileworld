"""Free cut for the Horbaach Beet Root+ ad: hand shots = Seedance clips (S1, S3, S5, S6), hand-free shots = slow push-ins on
stills (S2 beets, S4 real label photo, S7 jar). No overlay text of any kind (Ralph 2026-10-02). VO = vo/voiceover_tight.mp3.
  python3 cut.py   -> out/horbaach_beet_root.mp4
Windows come from shots.json (VO word timings); S5 is cut at 2.3s (its label drifts after that) and S6 starts that much early."""
import json, subprocess, os
from pathlib import Path
os.chdir(Path(__file__).parent)
J = json.load(open("shots.json")); T = {s["id"]: s["t"] for s in J["shots"]}
S5_LEN = 2.3
w = {k: list(v) for k, v in T.items()}
shift = (w["S5"][1] - w["S5"][0]) - S5_LEN
w["S5"][1] -= shift; w["S6"][0] -= shift          # S6 picture starts early, VO untouched
FPS = 24
tmp = Path("out/_seg"); tmp.mkdir(parents=True, exist_ok=True)


def dur(k): return round(w[k][1] - w[k][0], 3)


def run(args): subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def clip(k, src):
    run(["-i", src, "-t", str(dur(k)), "-vf", f"fps={FPS},scale=720:1280,setsar=1", "-an", "-c:v", "libx264", "-crf", "17",
         "-pix_fmt", "yuv420p", str(tmp / f"{k}.mp4")])


def push(k, src, crop, z0=1.0, z1=1.12, fx=0.5, fy=0.5):
    """slow push-in on a still: crop (w:h:x:y, 9:16), big scale, zoompan with a faint handheld drift."""
    d = int(round(dur(k) * FPS)); cw, ch, cx, cy = crop
    vf = (f"crop={cw}:{ch}:{cx}:{cy},scale=2160:3840:flags=lanczos,"
          f"zoompan=z='{z0}+({z1}-{z0})*on/{d}':x='(iw-iw/zoom)*{fx}+6*sin(on/9)':y='(ih-ih/zoom)*{fy}+5*sin(on/11)':"
          f"d={d}:s=720x1280:fps={FPS},setsar=1")
    run(["-loop", "1", "-i", src, "-vf", vf, "-frames:v", str(d), "-an", "-c:v", "libx264", "-crf", "17",
         "-pix_fmt", "yuv420p", str(tmp / f"{k}.mp4")])


clip("S1", "clips/S1.mp4")
push("S2", "stills/S2.png", (691, 1228, 0, 0), 1.0, 1.10, 0.35, 0.6)       # crop above the phone date stamp at the bottom
clip("S3", "clips/S3.mp4")
push("S4", "refs/jar_label.png", (458, 814, 31, 0), 1.0, 1.14, 0.5, 0.45)   # the real label photo, label words readable
clip("S5", "clips/S5.mp4")
clip("S6", "clips/S6.mp4")
push("S7", "stills/S7.png", (768, 1365, 0, 0), 1.0, 1.10, 0.4, 0.5)
order = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]
Path(tmp / "list.txt").write_text("".join(f"file '{k}.mp4'\n" for k in order))
run(["-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-i", "vo/voiceover_tight.mp3", "-map", "0:v", "-map", "1:a",
     "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
     "-shortest", "-movflags", "+faststart", "out/horbaach_beet_root.mp4"])
print({k: dur(k) for k in order}, "total", round(sum(dur(k) for k in order), 2))
