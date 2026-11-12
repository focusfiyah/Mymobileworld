"""QC for the Chatterbox re-voice (2026-11-12). Each check prints <NAME>_OK or <NAME>_FAIL and exits 1 on fail.
  python3 qc.py vo | cut | out"""
import json, re, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
def fail(m): print(m); sys.exit(1)
def norm(s): return re.sub(r"[^a-z' ]", "", s.lower().replace("-", " ")).split()
what = sys.argv[1]
if what == "vo":   # every line read back by faster-whisper matches the script, and the VO is the Chatterbox file
    lines = (H / "vo/lines.txt").read_text().split("\n"); lines = [l for l in lines if l.strip()]
    rb = json.loads((H / "vo/readback.json").read_text())
    if not (H / "vo/ralph_cbx.wav").is_file() or len(rb) != len(lines): fail("VO_FAIL missing wav or readback")
    for want, got in zip(lines, rb):
        a, b = norm(want), norm(got)
        miss = [w for w in a if w not in b]
        if len(miss) > 0: fail(f"VO_FAIL '{want}' heard as '{got}' missing {miss}")
    print("VO_OK", len(lines), "lines")
elif what == "cut":  # cut.py reads the Chatterbox VO and every shot starts on its line's first word
    src = (H / "cut.py").read_text()
    if '"-i", "vo/ralph.mp3"' in src or '"-i", "vo/ralph_cbx.wav"' not in src: fail("CUT_FAIL cut.py not on ralph_cbx.wav")
    if re.search(r"setpts=[0-9.]+\*", src) or "atempo" in src: fail("CUT_FAIL speed change found")
    starts = json.loads((H / "vo/line_starts.json").read_text())
    seg = [float(x) for x in re.findall(r'"[^"]+",\s*[0-9.]+,\s*([0-9.]+),', src)]
    exp = [0.0] + starts[1:]
    if len(seg) != len(exp) or any(abs(s - e) > 0.06 for s, e in zip(seg, exp)): fail(f"CUT_FAIL starts {seg} vs lines {exp}")
    print("CUT_OK", seg)
elif what == "out":  # final file: >=15 s, 1080x1920, -16..-14 LUFS
    f = str(H / "out/bf_novatabz.mp4")
    p = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration", "-of", "json", f], capture_output=True, text=True).stdout)
    d = float(p["format"]["duration"]); v = [s for s in p["streams"] if "width" in s][0]
    e = subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", e)[-1])
    if d < 15.0 or (v["width"], v["height"]) != (1080, 1920) or not -16 <= lufs <= -14: fail(f"OUT_FAIL {d} {v} {lufs}")
    print(f"OUT_OK {d:.2f}s 1080x1920 {lufs} LUFS")
