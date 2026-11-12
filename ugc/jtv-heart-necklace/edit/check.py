"""Gate oracle: python3 check.py all|N... -> ALL_CUTS_OK when every cut is 1080x1920, silent, 16.0 s (+-0.15), 480 frames +-3, no black frames."""
import subprocess, json, sys
plan = json.load(open("out/plan.json")); ids = [p["video"] for p in plan] if sys.argv[1:] in ([], ["all"]) else [int(a) for a in sys.argv[1:]]
bad = []
for v in ids:
    p = f"out/necklace_V{v}.mp4"
    try: pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", p], capture_output=True, text=True, check=True).stdout)
    except Exception: bad.append(f"V{v} missing"); continue
    vs = [s for s in pr["streams"] if s["codec_type"] == "video"][0]; d = float(pr["format"]["duration"]); n = int(vs["nb_read_frames"])
    bl = subprocess.run(["ffmpeg", "-v", "info", "-i", p, "-vf", "blackdetect=d=0.05:pix_th=0.10", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr.count("black_start")
    e = []
    if (vs["width"], vs["height"]) != (1080, 1920): e.append("size")
    if any(s["codec_type"] == "audio" for s in pr["streams"]): e.append("audio")
    if abs(d - 16.0) > 0.15 or abs(n - 480) > 3: e.append(f"len {d:.2f}s {n}f")
    if bl: e.append(f"{bl} black")
    print(f"V{v}: {d:.2f}s {n}f " + (" ".join(e) or "ok"))
    if e: bad.append(f"V{v}")
print("FAIL " + " ".join(bad) if bad else "ALL_CUTS_OK"); sys.exit(1 if bad else 0)
