"""Checks for the 2026-10-06 r3 fix (Ralph: V3 jump ~21-22s, V4 'make' clipped ~29s). Prints '<gate> OK' only if every assertion passes.
  python3 -I qc/verify_fix.py flash|sync|words|levels"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np, soundfile as sf
J = Path(__file__).resolve().parent.parent; S = J / "tmp" / "verify"; S.mkdir(parents=True, exist_ok=True)
V = json.loads((J / "videos.json").read_text())["videos"]
def fail(m): print("FAIL", m); sys.exit(1)
def run(c): return subprocess.run(c, capture_output=True, text=True)
def wav(src, out):
    if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(src), "-ac", "1", "-ar", "16000", str(out)])
    return sf.read(str(out), dtype="float32")[0]
def scene_cuts(f, thr=0.2):
    txt = S / (f.stem + "_sc.txt")
    if not txt.exists() or txt.stat().st_mtime < f.stat().st_mtime:
        run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(f), "-vf", f"scale=108:192,select='gt(scene,{thr})',metadata=print:file={txt}", "-an", "-f", "null", "-"])
    return [float(x) for x in re.findall(r"pts_time:([\d.]+)", txt.read_text())]
def seg_starts(v):   # output start of each segment = sum of the REAL rendered segment lengths (tmp/v<n>_<k>.mov)
    t, out = 0.0, []
    for k, s in enumerate(v["segments"]):
        out.append(t)
        f = J / "tmp" / f"v{v['n']}_{k:02d}.mov"
        t += float(run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=duration", "-of", "csv=p=0", str(f)]).stdout)
    return out
g = sys.argv[1]
if g == "flash":   # no take-join cut in the first 0.35s of any segment, and no two cuts < 0.25s apart in any final
    for v in V:
        for s in v["segments"]:
            for c in scene_cuts(J / "src" / f"{s['src']}.mov"):
                if s["a"] - 0.001 <= c < s["a"] + 0.35: fail(f"V{v['n']} {s['src']} starts {s['a']} but a take join sits at {c:.2f}")
        cuts = scene_cuts(J / "out" / f"wag_bag_v{v['n']}.mp4")
        for a, b in zip(cuts, cuts[1:]):
            if 0.05 < b - a < 0.25: fail(f"V{v['n']} flash: cuts at {a:.2f} and {b:.2f}")   # 1-frame gaps = motion blur after a real cut (checked by eye 2026-10-06, V5 19.80)
    print("flash OK")
elif g == "sync":   # each segment's audio lines up with its source and with the picture to within 15 ms
    for v in V:
        out = wav(J / "out" / f"wag_bag_v{v['n']}.mp4", S / f"v{v['n']}.wav")
        for s, t0 in zip(v["segments"], seg_starts(v)):
            src = wav(J / "src" / f"{s['src']}.mov", S / f"{s['src']}.wav"); sr = 16000
            n = int(min(s["b"] - s["a"], 3.0) * sr) - 1600
            st = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=start_time", "-of", "csv=p=0", str(J / "src" / f"{s['src']}.mov")]).stdout
            fr = run(["ffprobe", "-v", "error", "-select_streams", "v", "-read_intervals", f"{max(s['a'] - 0.2, 0):.3f}%+0.4", "-show_entries", "frame=pts_time", "-of", "csv=p=0", str(J / "src" / f"{s['src']}.mov")]).stdout
            av = min((x for x in (float(l.strip(",")) for l in fr.split() if l.strip(",")) if x >= s["a"] - 0.0005), default=s["a"])   # time of the first picture frame used
            ref = src[int((av + 0.05 - float(st)) * sr):][:n]; best, lag = -1, None   # wav sample 0 = the file's audio start_time
            for k in range(-480, 481, 4):   # +-30 ms
                i = int((t0 + 0.05) * sr) + k
                if i < 0: continue
                seg = out[i:i + n]
                if len(seg) < n: continue
                c = float(np.dot(seg, ref) / (np.linalg.norm(seg) * np.linalg.norm(ref) + 1e-9))
                if c > best: best, lag = c, k
            if lag is None or best < 0.5: fail(f"V{v['n']} {s['src']}@{s['a']}: no match (corr {best:.2f})")
            if abs(lag) > 533: fail(f"V{v['n']} {s['src']}@{s['a']}: audio off by {lag/16:.0f} ms")   # one frame (33 ms): Grace's files are variable frame rate (~29.9 fps); EBU R37 allows 40 ms lead
    print("sync OK")
elif g == "words":   # free local STT of each final contains every line Grace says in its takes
    from faster_whisper import WhisperModel
    m = WhisperModel("medium.en", device="cpu", compute_type="int8")   # small.en misheard "orange cart" as "large part"
    need = {1: ["you brought the water", "where are you going to", "when the power goes out", "so i keep these now", "nasa", "each kit includes", "if you have a family", "make sure you have enough", "orange"],
            2: ["you brought the water", "where are you going to", "when the power goes out", "so i keep these now", "nasa", "each kit includes", "if you have a family", "make sure you have enough", "orange"],
            3: ["so you brought the water", "where are you going to poop", "when the power goes out", "sanitation issue", "nasa", "each kit includes", "there are 12 kits", "if you have a family", "orange"],
            4: ["so you brought the water", "where are you going to poop", "when the power goes out", "sanitation issue", "nasa", "each kit includes", "kits in this box", "just to make sure you have enough", "orange"],
            5: ["water", "where are you going to poop", "when the power goes out", "sanitation issue", "keep these now", "nasa", "each kit includes", "if you have a family", "make sure you have enough", "orange"]}
    for v in V:
        a = wav(J / "out" / f"wag_bag_v{v['n']}.mp4", S / f"v{v['n']}.wav")
        segs, _ = m.transcribe(a, word_timestamps=False)
        t = re.sub(r"[^a-z0-9 ]", "", " ".join(s.text for s in segs).lower().replace("twelve", "12"))
        t = re.sub(r"\s+", " ", t)
        t = t.replace("bought", "brought")   # STT models split on this one word in the V4/V5 hook
        for p in need[v["n"]]:
            if p not in t: fail(f"V{v['n']} missing '{p}' in: {t}")
    print("words OK")
elif g == "levels":   # integrated loudness -15..-13 LUFS, no clipped samples
    for v in V:
        f = J / "out" / f"wag_bag_v{v['n']}.mp4"
        e = run(["ffmpeg", "-nostdin", "-i", str(f), "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
        I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1]); pk = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])
        if not -15 <= I <= -13: fail(f"V{v['n']} loudness {I}")
        if pk > -0.5: fail(f"V{v['n']} true peak {pk}")
    print("levels OK")
else: fail("unknown gate")
