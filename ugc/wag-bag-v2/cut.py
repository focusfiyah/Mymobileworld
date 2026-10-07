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
    out = TMP / f"v{v['n']}_{k:02d}.mov"
    import hashlib   # sticker files are part of the cache key (r5: a new outline reused old clips)
    stk = [hashlib.md5((EMO / q["png"]).read_bytes()).hexdigest() for q in seg.get("pops", [])]
    key = json.dumps([seg, v["zoom"], v["grade"], stk], sort_keys=True)
    kf = out.with_suffix(".key")
    if out.exists() and kf.exists() and kf.read_text() == key: return out   # unchanged segment: reuse
    src, a = seg["src"], seg["a"]
    b = a + round((seg["b"] - a) * FPS) / FPS   # whole frames, so picture and sound end together
    z = v["zoom"]
    vf = (["hflip"] if seg.get("hflip") else []) + [
        f"scale={round(1080*z/2)*2}:{round(1920*z/2)*2}", "crop=1080:1920", v["grade"], f"fps={FPS}", "format=yuv420p"]
    d = b - a
    nfr = round(d * FPS)
    # Grace's phone files run ~30.3 fps (variable): start the sound at the first real picture frame at/after a
    fr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-read_intervals", f"{max(a - 0.2, 0):.3f}%+0.4",
                         "-show_entries", "frame=pts_time", "-of", "csv=p=0", str(SRC / f"{src}.mov")], capture_output=True, text=True).stdout
    av = min((x for x in (float(l.strip(",")) for l in fr.split() if l.strip(",")) if x >= a - 0.0005), default=a)
    ns = round(d * 48000)
    # sound first, on the file's own timeline (iPhone audio starts 16 ms after the picture), padded to the exact clip length
    wav = out.with_suffix(".wav")
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(SRC / f"{src}.mov"), "-vn", "-af",
         f"atrim=start={av:.4f}:end={av + d:.4f},asetpts=PTS-{av:.4f}/TB,aresample=48000:async=1:first_pts=0,loudnorm=I=-16:TP=-1.5:LRA=7,aresample=48000,"
         f"asetpts=N/SR/TB,afade=t=in:d=0.02,apad=whole_len={ns},atrim=end_sample={ns},afade=t=out:st={d - 0.03:.4f}:d=0.03",   # sample counts: loudnorm shifts timestamps
         "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(wav)])
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{a:.4f}", "-i", str(SRC / f"{src}.mov")]
    pops = seg.get("pops", [])
    for p in pops:
        cmd += ["-framerate", str(FPS), "-i", str(pop_frames(p["png"], p["size"], d, p["png"][:-4].replace("/", "_")) / "%04d.png")]
    cmd += ["-i", str(wav)]
    if pops:
        f = [f"[0:v]{','.join(vf)}[b0]"]
        for i, p in enumerate(pops, 1):
            box = int(p["size"] * 1.3)
            f.append(f"[{i}:v]setpts=PTS-STARTPTS+{p['t'] - a:.3f}/TB[e{i}]")
            f.append(f"[b{i-1}][e{i}]overlay=x={p['x'] - box // 2}:y={p['y'] - box // 2}:eof_action=pass[b{i}]")
        cmd += ["-filter_complex", ";".join(f), "-map", f"[b{len(pops)}]"]
    else:
        cmd += ["-vf", ",".join(vf), "-map", "0:v"]
    cmd += ["-map", f"{len(pops) + 1}:a", "-frames:v", str(nfr), "-c:v", "libx264", "-preset", "medium", "-crf", "16",
            "-c:a", "pcm_s16le", str(out)]
    run(cmd)
    kf.write_text(key)
    return out


def build(v):
    parts = [segment(v, k, s) for k, s in enumerate(v["segments"])]
    out = OUT / f"wag_bag_v{v['n']}.mp4"
    # one concat filter + one encode keeps every segment's sound locked to its picture
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y"]
    for p in parts: cmd += ["-i", str(p)]
    n = len(parts)
    fc = "".join(f"[{i}:v][{i}:a]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a0];[a0]loudnorm=I=-14:TP=-1.0:LRA=7,aresample=48000[a]"
    run(cmd + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
               "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
    print(out)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True); TMP.mkdir(exist_ok=True)
    want = {int(x) for x in sys.argv[1:]} or {v["n"] for v in P["videos"]}
    for v in P["videos"]:
        if v["n"] in want: build(v)
