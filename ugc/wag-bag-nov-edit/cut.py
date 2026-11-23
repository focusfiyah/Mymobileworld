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

BREATH = 0.06   # air kept on each side of a closed gap: ~0.12 s pause (Grace 2026-11-19: no gaps between her lines)
TGAP = 0.25     # any quiet run longer than this is closed (Grace 2026-11-19; target longest gap <= 0.25 s)

def env(src, a, b):
    """10 ms RMS envelope in dB of the source audio between a and b"""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a}", "-t", f"{b - a}", "-i", str(SRC / f"{src}.mov"), "-vn",
                          "-ac", "1", "-ar", "16000", "-af", "highpass=f=120", "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = len(x) // 160
    return 20 * np.log10(np.sqrt((x[:n * 160].reshape(n, 160) ** 2).mean(1)) + 1e-6)

def edges(src, p, q):
    """where her voice really stops after word p and starts before word q (Whisper word ends drift):
    threshold = floor + 35% of (peak - floor) over both words; returns (speech_end, speech_start)"""
    import numpy as np
    lo = p["start"]; db = env(src, lo, q["end"])
    if len(db) < 10: return p["end"], q["start"]
    fl, pk = np.percentile(db, 10), np.percentile(db, 95); thr = fl + 0.35 * (pk - fl); low = db < thr
    f = lambda t: min(len(db) - 1, max(0, int(round((t - lo) / 0.01))))
    i = f(p["end"] - 0.15); stop = f(p["end"] + 0.30)
    while i < stop and not low[i:i + 5].all(): i += 1
    j = f(q["start"] + 0.15); floor_ = f(q["start"] - 0.30)
    while j > floor_ and not low[max(0, j - 5):j].all(): j -= 1
    return lo + i * 0.01, lo + j * 0.01

def take_words(t):
    """her words inside this take only: never a word from the neighbouring clip"""
    cs = src_cuts(t["src"])
    a = max([t["a"]] + [c for c in cs if t["a"] < c <= t["a"] + 0.6])
    b = min([t["b"]] + [c for c in cs if t["b"] - 0.6 <= c < t["b"]])
    return [w for w in words(t["src"] + "_medfull") if w["start"] >= a - 0.05 and w["start"] < b - 0.30], a, b

KEEP_END, KEEP_START = 0.10, 0.06   # air kept after her voice drops / before it starts (soft word ends stay whole)

def tight(t):
    """V2 (2026-11-19, Grace: no gaps between her lines). Every cut point comes from the audio level of the take:
    her voice = 10 ms RMS above floor + FRAC x (peak - floor); a quiet run longer than TGAP closes to KEEP_END + KEEP_START.
    Whisper words only bound the take (no word of the next clip); their timings drift into silence, so they never decide a cut."""
    import numpy as np
    if t.get("whole") and not t.get("tighten"): return snap(t["src"], [(t["a"], t["b"])])
    if t.get("pieces"):   # set by hand from the audio level (the demo: one piece per action she names)
        return apply_drops(t, [tuple(p) for p in t["pieces"]])
    ws, A, B = take_words(t)
    if not ws: return []
    B = min(B, ws[-1]["end"] + 0.8)
    db = env(t["src"], A, B); db = np.convolve(db, np.ones(3) / 3, "same")
    fl, pk = np.percentile(db, 10), np.percentile(db, 97)
    voice = db > fl + t.get("frac", 0.18) * (pk - fl)
    T = lambda k: A + k * 0.01
    idx = np.flatnonzero(voice)
    if not len(idx): return []
    a = max(A, T(idx[0]) - KEEP_START)
    end = min(B, T(idx[-1] + 1) + KEEP_END + 0.04)
    mids = [(w["start"] + w["end"]) / 2 for w in ws]
    out, k, n = [], idx[0], len(voice)
    while k < idx[-1]:
        if voice[k]: k += 1; continue
        st = k
        while k < n and not voice[k]: k += 1
        if (k - st) * 0.01 > TGAP:
            c0, c1 = T(st) + KEEP_END, T(k) - KEEP_START
            out.append((a, c0)); a = c1
    out.append((a, end))
    return apply_drops(t, out)

def apply_drops(t, out):
    for x, y in t.get("drop", []):   # quiet runs the gap meter found in a render, mapped back to source time (close_gaps.py)
        nxt = []
        for p, q in out:
            if y <= p or x >= q: nxt.append((p, q)); continue
            if x > p: nxt.append((p, x))
            if y < q: nxt.append((y, q))
        out = nxt
    starts_ = [w["start"] for w in words(t["src"] + "_medfull")]
    # no sliver: a piece under 0.3 s with no word starting in it is rustle between drops, and would flash on screen
    return [p for p in snap(t["src"], out) if p[1] - p[0] > 0.3 or (p[1] - p[0] > 0.12 and any(p[0] - 0.05 <= w <= p[1] for w in starts_))]

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
        for a, b in (tight(t) if v.get("tight", True) else pieces(t)):
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
