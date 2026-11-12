"""Gate oracle for one HofR Black Friday silent-video post. python3 check.py POST  -> CHECK_OK POST or CHECK_FAIL lines.
Checks: final mp4 is 1080x1920, 15.0-23.0 s, has audio at -16..-13.5 LUFS integrated, HOOK_OK (whole hook from frame 0,
held 2 s) in the declared hook box, VO read back right (vo/readback.txt ends READBACK_OK), script has no banned phrase
(dash, 'order it now', '$' / price, 'reviewer', 'the label says'), ends on "It's in the orange cart.", first line is a
HOOKS.md hook word for word (blanks filled), every b-roll clip logged in broll/SOURCES.md, REMOVED.md items absent."""
import json, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
post = Path(sys.argv[1]).resolve(); name = post.name.replace("bf-", "")
cfg = json.loads((post / "post.json").read_text()); fail = []
mp4 = post / "out" / f"bf_{name}.mp4"
p = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration", "-of", "json", str(mp4)], capture_output=True, text=True).stdout)
v = [s for s in p["streams"] if s["codec_type"] == "video"][0]; a = [s for s in p["streams"] if s["codec_type"] == "audio"]
dur = float(p["format"]["duration"])
if (v["width"], v["height"]) != (1080, 1920): fail.append(f"size {v['width']}x{v['height']}")
if not 15.0 <= dur <= 23.0: fail.append(f"length {dur:.2f}s")
if not a: fail.append("no audio")
else:
    o = subprocess.run(["ffmpeg", "-nostats", "-i", str(mp4), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
    if not -16.0 <= lufs <= -13.5: fail.append(f"loudness {lufs} LUFS")
hc = subprocess.run([sys.executable, str(ROOT / "tools/hookcheck/hook_check.py"), str(mp4), "--hook", cfg["hook_box"]], capture_output=True, text=True).stdout
if "HOOK_OK" not in hc: fail.append("hook: " + hc.strip()[-120:])
rb = (post / "vo/readback.txt").read_text() if (post / "vo/readback.txt").exists() else ""
if "READBACK_OK" not in rb: fail.append("VO read-back not OK")
lines = [l.strip() for l in (post / "vo/lines.txt").read_text().splitlines() if l.strip()]
txt = " ".join(lines)
for bad in ["—", "–", " - ", "order it now", "$", "reviewer", "the label says", "heads up"]:
    if bad.lower() in txt.lower(): fail.append(f"banned '{bad}'")
if re.search(r"\b\d+\s*(dollars|bucks)\b", txt.lower()): fail.append("price")
if lines[-1] != "It's in the orange cart.": fail.append("close line")
hooks = {h["id"]: h for h in json.loads((ROOT / "grace/hooks/hooks.json").read_text())["hooks"]}
tmpl = hooks[cfg["hook_id"]]["hook"]
pat = "^" + re.escape(tmpl.rstrip(".?!")).replace("__", ".+?") + r"[.?!]?$"
if not re.match(pat, lines[0]): fail.append(f"hook not word for word {cfg['hook_id']}: {tmpl!r} vs {lines[0]!r}")
src = (post / "broll/SOURCES.md").read_text() if (post / "broll/SOURCES.md").exists() else ""
for b in cfg.get("broll", []):
    if b not in src: fail.append(f"b-roll {b} not in SOURCES.md")
for r in cfg.get("removed_terms", []):
    if r.lower() in txt.lower(): fail.append(f"REMOVED item '{r}' in script")
print(f"{name}: {dur:.2f}s" + (f", {lufs} LUFS" if a else ""))
print("CHECK_OK " + name if not fail else "CHECK_FAIL " + name + ": " + "; ".join(fail))
