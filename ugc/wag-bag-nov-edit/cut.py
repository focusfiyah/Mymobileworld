"""Cleanwaste Wag Bag November edits (Grace's own footage, 2026-11-19). Reusable for the next 7 (total 10).
Each video = takes of her four script parts (wb1 hook+pain, wb2 demo, wb3 features + which box, wb4 urgency + orange cart),
her own voice. Pauses inside a take over GAP s are cut (jump cut) and alternate shots punch in, so it keeps pace.
Plan: videos.json  {"videos":[{"name","zoom","punch","grade","takes":[{"src","a","b"}]}]}
Usage: python3 cut.py [name ...] [--fast]   (no names = all; --fast = veryfast preset for review renders)
Source cut method from ugc/wag-bag-v2/cut.py (VFR-safe sound per segment, one concat encode)."""
import json, subprocess, sys, hashlib
from pathlib import Path
J = Path(__file__).parent
SRC, OUT, TMP = J / "orig", J / "out", J / "tmp"
FPS, GAP, PAD = 30, 0.45, 0.10
P = json.loads((J / "videos.json").read_text())
FAST = "--fast" in sys.argv

def words(src):
    w = json.loads((J / "tr" / src / "transcript_words.json").read_text())["words"]
    return [x for x in w if x.get("type", "word") == "word"]

def silences(src, a, b, db=-32, d=GAP):
    import re
    e = subprocess.run(["ffmpeg", "-v", "info", "-ss", f"{a}", "-t", f"{b - a}", "-i", str(SRC / f"{src}.mov"), "-vn",
                        "-af", f"highpass=f=120,silencedetect=n={db}dB:d={d}", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) + a for x in re.findall(r"silence_start: ([\d.]+)", e)]
    en = [float(x) + a for x in re.findall(r"silence_end: ([\d.]+)", e)]
    return list(zip(st, en + [b] * (len(st) - len(en))))

def src_cuts(src):
    """hard cuts inside her file (WagBagNClips = several clips joined); cached in tr/<src>/cuts.json"""
    import re
    c = J / "tr" / src / "cuts.json"
    if not c.exists():
        o = subprocess.run(["ffmpeg", "-v", "error", "-i", str(SRC / f"{src}.mov"), "-vf", "scale=270:480,select='gt(scene,0.28)',metadata=print:file=-",
                            "-an", "-f", "null", "-"], capture_output=True, text=True).stdout
        c.write_text(json.dumps([float(x) for x in re.findall(r"pts_time:([\d.]+)", o)]))
    return json.loads(c.read_text())

def snap(src, out):
    """no frame of the neighbouring clip: a piece starting/ending within 0.6 s of a source cut starts/ends at that cut"""
    cs, res = src_cuts(src), []
    for a, b in out:
        for c in cs:
            if a < c <= a + 0.6: a = c - 0.002   # first frame of her next clip
            if b - 0.6 <= c < b: b = c - 0.010
        res.append((a, b))
    return res

def pieces(t):
    """split a take where the audio is silent for more than GAP s; keep PAD s of air each side; trims lead/tail air"""
    if t.get("whole"): return snap(t["src"], [(t["a"], t["b"])])
    a, b = t["a"], t["b"]; out = []
    for s0, s1 in silences(t["src"], a, b, t.get("db", -32)):
        if s0 - a > 0.05: out.append((a, min(s0 + PAD, b)))
        a = max(s1 - PAD, a)
    if b - a > 0.15: out.append((a, b))
    ws = words(t["src"])   # drop bits with no spoken word in them (box rustle)
    out = snap(t["src"], out)
    return [p for p in out if p[1] - p[0] > 0.12 and any(p[0] - 0.25 <= w["start"] <= p[1] for w in ws)]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-2000:])

def segment(v, k, src, a, b, z):
    out = TMP / f"{v['name']}_{k:02d}.mov"
    key = json.dumps([src, a, b, z, v["grade"], FAST], sort_keys=True)
    kf = out.with_suffix(".key")
    if out.exists() and kf.exists() and kf.read_text() == key: return out, b - a   # unchanged: reuse
    b = a + round((b - a) * FPS) / FPS
    vf = [f"scale={round(1080*z/2)*2}:{round(1920*z/2)*2}:flags=lanczos", "crop=1080:1920", v["grade"], f"fps={FPS}", "format=yuv420p"]
    d = b - a; nfr = round(d * FPS); f = SRC / f"{src}.mov"
    fr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-read_intervals", f"{max(a - 0.2, 0):.3f}%+0.4",
                         "-show_entries", "frame=pts_time", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout
    av = min((x for x in (float(l.strip(",")) for l in fr.split() if l.strip(",")) if x >= a - 0.0005), default=a)
    ns = round(d * 48000); wav = out.with_suffix(".wav")
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(f), "-vn", "-af",
         f"atrim=start={av:.4f}:end={av + d:.4f},asetpts=PTS-{av:.4f}/TB,aresample=48000:async=1:first_pts=0,"
         f"asetpts=N/SR/TB,afade=t=in:d=0.02,apad=whole_len={ns},atrim=end_sample={ns},afade=t=out:st={d - 0.03:.4f}:d=0.03",
         "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(wav)])
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{a:.4f}", "-i", str(f), "-i", str(wav), "-vf", ",".join(vf),
         "-map", "0:v", "-map", "1:a", "-frames:v", str(nfr), "-c:v", "libx264", "-preset", "veryfast" if FAST else "medium",
         "-crf", "16", "-threads", "4", "-c:a", "pcm_s16le", str(out)])
    kf.write_text(key)
    return out, d

def build(v):
    segs, k, n = [], 0, 0
    for t in v["takes"]:
        for a, b in pieces(t):
            z = v["zoom"] * (v["punch"] if (n % 2 and not t.get("nopunch")) else 1.0)   # alternate punch-in on jump cuts
            r = segment(v, k, t["src"], a, b, z)
            segs.append({"src": t["src"], "a": round(a, 3), "b": round(b, 3), "zoom": round(z, 3), "file": str(r[0] if isinstance(r, tuple) else r)})
            k += 1; n += 1
    out = OUT / f"wagbag_{v['name']}.mp4"
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y"]
    for s in segs: cmd += ["-i", s["file"]]
    m = len(segs)
    fc = "".join(f"[{i}:v][{i}:a]" for i in range(m)) + f"concat=n={m}:v=1:a=1[v][a0];[a0]loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[a]"
    run(cmd + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast" if FAST else "medium",
               "-crf", "18", "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
    exp = round(sum(round((s["b"] - s["a"]) * FPS) / FPS for s in segs), 3)
    json.dump({"name": v["name"], "segs": segs, "expected": exp}, open(OUT / f"wagbag_{v['name']}.json", "w"), indent=1)
    print(out, exp, "s", m, "segments")

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True); TMP.mkdir(exist_ok=True)
    want = [x for x in sys.argv[1:] if not x.startswith("--")]
    for v in P["videos"]:
        if not want or v["name"] in want: build(v)
