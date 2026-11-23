"""G3: both final cuts are 1080x1920, 15-40 s, with an audio stream. Prints CUTS_OK."""
import json, subprocess, sys
bad = []
for f in ["final/twin_kit7_A.mp4", "final/twin_kit7_B.mp4"]:
    try: d = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", f], capture_output=True, text=True).stdout)
    except Exception: bad.append(f"{f} unreadable"); continue
    v = [s for s in d.get("streams", []) if s["codec_type"] == "video"]; au = [s for s in d.get("streams", []) if s["codec_type"] == "audio"]
    dur = float(d.get("format", {}).get("duration", 0))
    if not v or (v[0]["width"], v[0]["height"]) != (1080, 1920): bad.append(f"{f} size")
    if not au: bad.append(f"{f} no audio")
    if not 15 <= dur <= 40: bad.append(f"{f} duration {dur}")
print("CUTS_OK" if not bad else f"BAD {bad}")
