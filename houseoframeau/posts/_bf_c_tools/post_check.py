"""QC for one HofR BF silent-C post (Ralph 2026-11-12 rules). Run from the post folder:  python3 ../_bf_c_tools/post_check.py <name> <hook id>
Checks out/<name>.mp4: 1080x1920, >= 15.0 s, 30 fps, audio present, integrated loudness -16..-13.5 LUFS, true peak <= -1.0,
no black frames, no frozen stretch >= 0.7 s (freezedetect); hook text = hooks.json <id> with only the blanks filled;
vo/lines.txt: first line = hook, last line "It's in the orange cart.", no banned words (order it now, heads up, dashes,
$ / price numbers, reviewer, "the label says"); every VO line heard back (vo/words.json from vo.py check).
Prints POST_OK <name> or POST_FAIL <name> with the reasons."""
import json, re, subprocess, sys
from pathlib import Path
name, hid = sys.argv[1], sys.argv[2]
V = Path(f"out/{name}.mp4"); bad = []
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration",
                                "-of", "json", str(V)], capture_output=True, text=True).stdout)
vs = [s for s in pr["streams"] if s["codec_type"] == "video"][0]; d = float(pr["format"]["duration"])
if (vs["width"], vs["height"]) != (1080, 1920): bad.append(f"size {vs['width']}x{vs['height']}")
if vs["r_frame_rate"] != "30/1": bad.append(f"fps {vs['r_frame_rate']}")
if d < 15.0: bad.append(f"length {d:.2f} < 15")
if not any(s["codec_type"] == "audio" for s in pr["streams"]): bad.append("no audio")
ln = subprocess.run(["ffmpeg", "-nostats", "-i", str(V), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", ln)[-1]); tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", ln)[-1])
if not -16.0 <= I <= -13.5: bad.append(f"loudness {I}")
if tp > -1.0: bad.append(f"true peak {tp}")
ev = subprocess.run(["ffmpeg", "-nostats", "-i", str(V), "-vf", "blackdetect=d=0.1:pix_th=0.08,freezedetect=n=0.003:d=0.7", "-an", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
if "black_start" in ev: bad.append("black frames")
if "freeze_start" in ev: bad.append("frozen stretch: " + ";".join(re.findall(r"freeze_start: ([\d.]+)", ev)))
lines = [l.strip() for l in Path("vo/lines.txt").read_text().splitlines() if l.strip()]
hooks = {h["id"]: h["hook"] for h in (lambda d: d["hooks"] if isinstance(d, dict) else d)(json.loads(Path(__file__).resolve().parents[3].joinpath("grace/hooks/hooks.json").read_text()))}
pat = "^" + re.escape(hooks[hid]).replace("__", ".+?") + r"[.!?]?$"
if not re.match(pat, lines[0]): bad.append(f"hook not word for word {hid}: {lines[0]!r} vs {hooks[hid]!r}")
plan = json.loads(Path(f"out/{name}_plan.json").read_text())
if plan["hook"].rstrip(".?!").lower() != lines[0].rstrip(".?!").lower().replace("’", "'"): bad.append("on-screen hook differs from spoken hook")
if lines[-1] != "It's in the orange cart.": bad.append("close line")
txt = " ".join(lines).lower()
for w in ["order it now", "heads up", "reviewer", "the label says", "$", "—", "–", " - ", "dollar", "price"]:
    if w in txt: bad.append(f"banned: {w!r}")
if re.search(r"\d", txt): bad.append("number in script (check it is not a price)")
words = json.loads(Path("vo/words.json").read_text())
norm = lambda s: re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("’", "'")).split()
ok_heard = json.loads(Path("vo/heard_ok.json").read_text()) if Path("vo/heard_ok.json").exists() else {}
for w in words:
    if norm(w["heard"]) != norm(w["text"]) and ok_heard.get(str(w["n"])) != w["heard"]:
        bad.append(f"L{w['n']} misheard: {w['heard']!r}")
print(f"len {d:.2f}s loud {I} LUFS tp {tp}")
print(f"POST_OK {name}" if not bad else f"POST_FAIL {name}: " + " | ".join(bad))
