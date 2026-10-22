"""G6: the final exists, 12-18 s... (goth skirt): checks out/goth_final.mp4 is 1080x1920, 9-18 s, has a (silent) audio track,
no frozen stretch over 0.5 s, and cut.py draws no text. Prints FINAL_OK."""
import re, subprocess, sys
from pathlib import Path
J = Path(__file__).resolve().parents[1]; F = J / "out/goth_final.mp4"
p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height", "-show_entries", "format=duration",
                    "-of", "json", str(F)], capture_output=True, text=True)
import json; d = json.loads(p.stdout); v = [s for s in d["streams"] if s["codec_type"] == "video"][0]
dur = float(d["format"]["duration"]); errs = []
if (v["width"], v["height"]) != (1080, 1920): errs.append(f"size {v['width']}x{v['height']}")
if not 9 <= dur <= 18: errs.append(f"duration {dur}")
if not any(s["codec_type"] == "audio" for s in d["streams"]): errs.append("no audio track")
fr = subprocess.run(["ffmpeg", "-i", str(F), "-vf", "freezedetect=n=0.001:d=0.5", "-map", "0:v", "-f", "null", "-"], capture_output=True, text=True).stderr
if "freeze_start" in fr: errs.append("frozen stretch over 0.5 s")
if re.search(r"drawtext|subtitles=|ass=", (J / "cut.py").read_text()): errs.append("cut.py draws text")
print("FINAL_OK" if not errs else "FAIL " + "; ".join(errs), f"({dur:.1f}s)"); sys.exit(1 if errs else 0)
