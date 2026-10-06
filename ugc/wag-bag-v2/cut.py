"""Wag Bag v2 (Grace, 2026-10-06): 5 real-footage videos = new hook take + new body take + old Part 3 take + old Part 4 take.
Emoji pops on the hook only (Grace/Ralph asked: food, water, poop + question mark). No text. Each video: its own takes,
its own bright grade and framing (rule 6).  Usage: python3 cut.py [1-5 ...]   (no args = all)"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image

J = Path(__file__).parent
SRC, EMO, OUT, TMP = J / "src", J / "emoji", J / "out", J / "tmp"
FPS = 30
P = json.loads((J / "videos.json").read_text())


def pop_frames(png, size, dur, name):
    """RGBA frame sequence: scale 0 -> 1.15 -> 1.0 in 0.22s, then a gentle bob."""
    import math
    d = TMP / f"pop_{name}_{size}"
    if d.exists(): return d
    d.mkdir(parents=True)
    im = Image.open(EMO / png).convert("RGBA")
    box = int(size * 1.3)
    for i in range(int(dur * FPS) + 1):
        t = i / FPS
        s = (t / 0.12) * 1.15 if t < 0.12 else (1.15 - 0.15 * (t - 0.12) / 0.10 if t < 0.22 else 1 + 0.03 * math.sin((t - 0.22) * 5))
        w = max(1, int(size * s))
        fr = Image.new("RGBA", (box, box))
        fr.alpha_composite(im.resize((w, w), Image.LANCZOS), ((box - w) // 2, (box - w) // 2))
        fr.save(d / f"{i:04d}.png")
    return d


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-2000:])


def segment(v, k, seg):
    out = TMP / f"v{v['n']}_{k:02d}.mp4"
    key = json.dumps([seg, v["zoom"], v["grade"]], sort_keys=True)
    kf = out.with_suffix(".key")
    if out.exists() and kf.exists() and kf.read_text() == key: return out   # unchanged segment: reuse
    src, a, b = seg["src"], seg["a"], seg["b"]
    z = v["zoom"]
    vf = (["hflip"] if seg.get("hflip") else []) + [
        f"scale={round(1080*z/2)*2}:{round(1920*z/2)*2}", "crop=1080:1920", v["grade"], f"fps={FPS}", "format=yuv420p"]
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", str(SRC / f"{src}.mov")]
    pops = seg.get("pops", [])
    if pops:
        for p in pops:
            cmd += ["-framerate", str(FPS), "-i", str(pop_frames(p["png"], p["size"], b - a, p["png"][:-4]) / "%04d.png")]
        f = [f"[0:v]{','.join(vf)}[b0]"]
        for i, p in enumerate(pops, 1):
            box = int(p["size"] * 1.3)
            f.append(f"[{i}:v]setpts=PTS-STARTPTS+{p['t'] - a:.3f}/TB[e{i}]")
            f.append(f"[b{i-1}][e{i}]overlay=x={p['x'] - box // 2}:y={p['y'] - box // 2}:eof_action=pass[b{i}]")
        cmd += ["-filter_complex", ";".join(f), "-map", f"[b{len(pops)}]", "-map", "0:a"]
    else:
        cmd += ["-vf", ",".join(vf)]
    d = b - a
    cmd += ["-af", f"loudnorm=I=-16:TP=-1.5:LRA=7,afade=t=in:d=0.02,afade=t=out:st={d - 0.03:.3f}:d=0.03,aresample=48000",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out)]
    run(cmd)
    kf.write_text(key)
    return out


def build(v):
    parts = [segment(v, k, s) for k, s in enumerate(v["segments"])]
    lst = TMP / f"v{v['n']}.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    out = OUT / f"wag_bag_v{v['n']}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "copy",
         "-af", "loudnorm=I=-14:TP=-1.0:LRA=7", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)])
    print(out)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True); TMP.mkdir(exist_ok=True)
    want = {int(x) for x in sys.argv[1:]} or {v["n"] for v in P["videos"]}
    for v in P["videos"]:
        if v["n"] in want: build(v)
