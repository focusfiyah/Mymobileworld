"""Twin assembly after speech-to-speech (week 3, 2026-11-23): trim each shot to its speech, join each video's shots,
then build silence islands for pace.py (whisper word gaps hid 1.5 s pauses; real silences don't).
  python3 assemble.py TWIN_DIR VIDEO_ID [VIDEO_ID ...]
TWIN_DIR holds map.json {shot: raw clip}, raw/<clip>.mp4, sts/<shot>.mp3; optional seg.json {shot: [[start,end],...]} overrides.
Writes cut/<shot>.mkv, cut/<VID>raw.mkv, cut/<VID>raw_isl.json. Then: pace.py cut/<VID>raw.mkv cut/<VID>raw_isl.json cut/<VID>.mkv"""
import json, re, subprocess, sys, pathlib
D = pathlib.Path(sys.argv[1]); vids = sys.argv[2:]
m = json.load(open(D / "map.json")); segf = D / "seg.json"; seg = json.load(open(segf)) if segf.exists() else {}
def sil(f, d):
    o = subprocess.run(["ffmpeg", "-v", "info", "-i", str(f), "-vn", "-af", f"silencedetect=n=-35dB:d={d}", "-f", "null", "-"], capture_output=True, text=True).stderr
    return [float(x) for x in re.findall(r"silence_start: ([\d.]+)", o)], [float(x) for x in re.findall(r"silence_end: ([\d.]+)", o)]
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout)
for k, c in m.items():
    if k.split("_")[0] not in vids: continue
    if k not in seg:
        ss, se = sil(D / "sts" / f"{k}.mp3", 0.12); T = dur(D / "raw" / f"{c}.mp4")
        st = se[0] - 0.08 if ss and ss[0] == 0 else 0.0; en = ss[-1] + 0.15 if ss and ss[-1] > st + 1 else T
        seg[k] = [[round(max(0, st), 2), round(min(T, en), 2)]]
    parts = []
    for i, (a, b) in enumerate(seg[k]):
        f = D / "cut" / f"{k}_{i}.mkv"; parts.append(f)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(round(b - a, 2)), "-i", str(D / "raw" / f"{c}.mp4"), "-ss", str(a), "-t", str(round(b - a, 2)), "-i", str(D / "sts" / f"{k}.mp3"),
                        "-map", "0:v", "-map", "1:a", "-vf", "fps=25,scale=1080:1920", "-af", "aresample=48000", "-ac", "1", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-c:a", "pcm_s16le", str(f)], check=True)
    (D / "cut" / "tmp.txt").write_text("".join(f"file '{p.name}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(D / "cut" / "tmp.txt"), "-c", "copy", str(D / "cut" / f"{k}.mkv")], check=True)
json.dump(seg, open(segf, "w"), indent=0)
for v in vids:
    shots = sorted(k for k in m if k.split("_")[0] == v)
    (D / "cut" / f"{v}.txt").write_text("".join(f"file '{s}.mkv'\n" for s in shots))
    raw = D / "cut" / f"{v}raw.mkv"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(D / "cut" / f"{v}.txt"), "-c", "copy", str(raw)], check=True)
    ss, se = sil(raw, 0.08); T = dur(raw); s2 = []
    for a, b in zip(ss, se + [T]):
        if s2 and a - s2[-1][1] < 0.06: s2[-1][1] = b
        else: s2.append([a, b])
    s2 = [x for x in s2 if x[1] - x[0] > 0.3]; isl = []; t = 0.0
    for a, b in s2:
        if a > t: isl.append({"w": "_", "s": round(t, 2), "e": round(a, 2)})
        t = b
    if t < T - 0.05: isl.append({"w": "_", "s": round(t, 2), "e": round(T, 2)})
    json.dump(isl, open(D / "cut" / f"{v}raw_isl.json", "w")); print("ASSEMBLE_OK", v, round(T, 2), len(isl))
