"""QC for the Boo-Boo Gel HofR BF cut (GATES.md). python3 qc.py size|lufs|freeze VIDEO ; qc.py words|sync|sources"""
import json, re, subprocess, sys
from pathlib import Path
def probe(v, *a): return subprocess.run(["ffprobe", "-v", "error", *a, "-of", "json", v], capture_output=True, text=True).stdout
cmd = sys.argv[1]
if cmd == "size":
    s = json.loads(probe(sys.argv[2], "-show_streams"))["streams"]
    vs = [x for x in s if x["codec_type"] == "video"][0]; au = [x for x in s if x["codec_type"] == "audio"]
    ok = vs["width"] == 1080 and vs["height"] == 1920 and vs["r_frame_rate"] == "30/1" and au and au[0]["codec_name"] == "aac"
    print("SIZE_OK" if ok else "SIZE_BAD", vs["width"], vs["height"], vs["r_frame_rate"], [a["codec_name"] for a in au])
elif cmd == "lufs":
    e = subprocess.run(["ffmpeg", "-i", sys.argv[2], "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1]); print("LUFS_OK" if -16 <= i <= -13.5 else "LUFS_BAD", i)
elif cmd == "freeze":
    e = subprocess.run(["ffmpeg", "-i", sys.argv[2], "-vf", "freezedetect=n=0.001:d=0.3", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    fr = re.findall(r"freeze_start: ([\d.]+)", e); print("FREEZE_OK" if not fr else "FREEZE_BAD", fr)
elif cmd == "words":
    want = [l["say"] for l in json.loads(Path("vo/lines.json").read_text())]; got = json.loads(Path("vo/heard.json").read_text())
    norm = lambda s: re.sub(r"[^a-z ]", "", s.lower().replace("-", "")).split()
    bad = [(w, g) for w, g in zip(want, got) if norm(w) != norm(g)]
    print("WORDS_OK" if not bad and len(want) == len(got) else "WORDS_BAD", bad)
elif cmd == "sync":
    L = json.loads(Path("vo/starts.json").read_text())["starts"]; seg = json.loads(Path("out/seg_times.json").read_text())
    starts = {round(t, 3) for _, t in seg}; miss = [x for x in L if not any(abs(x - s) <= 0.15 for s in starts)]
    print("SYNC_OK" if not miss else "SYNC_BAD", miss)
elif cmd == "sources":
    src = Path("broll/SOURCES.md").read_text(); clips = [p.name for p in Path("broll").glob("*.mp4")]
    miss = [c for c in clips if not re.search(re.escape(c) + r".*pexels\.com/video/", src)]
    print("SOURCES_OK" if clips and not miss else "SOURCES_BAD", miss)
