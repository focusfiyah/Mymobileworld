"""Add Fluent 3D emoji pops (word-timed, pops.json) + the hook card to the HofR cut.
   python3 pops.py SRC.mp4 -> out/hofr_pops.mp4. Same crop/grade as post.json. Emoji never past 1.2x source (256 px)."""
import json, subprocess, sys, math
from pathlib import Path
from PIL import Image
here = Path(__file__).resolve().parent; cfg = json.loads((here / "post.json").read_text()); P = json.loads((here / "pops.json").read_text())
FPS = 30; tmp = Path("/tmp/claude-0/pops"); tmp.mkdir(parents=True, exist_ok=True)
def frames(p, i):
    size = p.get("size", P["size"]); assert size <= 256 * 1.2, size
    src = Image.open(here / "emoji" / p["png"]).convert("RGBA"); box = int(size * 1.2); d = tmp / f"p{i}"; d.mkdir(exist_ok=True)
    n = int(p["d"] * FPS)
    for k in range(n):
        t = k / FPS; s = (t / 0.15) * 1.15 if t < 0.15 else (1.15 - 0.15 * (t - 0.15) / 0.07 if t < 0.22 else 1.0)
        if t > p["d"] - 0.15: s = max(0.01, (p["d"] - t) / 0.15)
        sz = max(2, int(size * s)); im = src.resize((sz, sz), Image.LANCZOS)
        fr = Image.new("RGBA", (box, box)); bob = int(6 * math.sin(2 * math.pi * t / 1.2)) if t >= 0.22 else 0
        fr.paste(im, ((box - sz) // 2, (box - sz) // 2 + bob), im); fr.save(d / f"{k:04d}.png")
    return d, box
ins = ["-i", sys.argv[1], "-i", str(here / "out/hook.png")]; f = [f"[0:v]crop={cfg['crop']},scale=1080:1920:flags=lanczos,{cfg['grade']},format=yuv420p,setsar=1[g]",
      f"[g][1:v]overlay=0:0:enable='lt(t,{cfg['hook_until']})'[b0]"]
for i, p in enumerate(P["pops"], 1):
    d, box = frames(p, i); ins += ["-framerate", str(FPS), "-i", str(d / "%04d.png")]
    f.append(f"[{i + 1}:v]setpts=PTS-STARTPTS+{p['t']}/TB[e{i}]")
    f.append(f"[b{i - 1}][e{i}]overlay=x={p['x'] - box // 2}:y={p['y'] - box // 2}:eof_action=pass[b{i}]")
n = len(P["pops"])
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(f), "-map", f"[b{n}]", "-map", "0:a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "copy", "-movflags", "+faststart", str(here / "out/hofr_pops.mp4")], check=True)
print("POPS_DONE", n)
