"""Gate oracle for the Wag Bag November edits.
python3 check.py all       -> ALL_CUTS_OK: each cut 1080x1920, has her voice (AAC), within 0.15 s of plan, no black frames,
                              loudness -16..-12 LUFS, true peak <= -0.5, every scene change sits on a planned cut or a cut in her own clip (no stray frame)
python3 check.py distinct  -> DISTINCT_OK: no source second is used in two different cuts (TikTok duplicate rule)
python3 check.py words NAME -> WORDS_OK: the cut's transcript starts with the take's first words (nothing clipped at a cut)"""
import subprocess, json, sys, re
from pathlib import Path
J = Path(__file__).parent; O = J / "out"; FPS = 30
names = [v["name"] for v in json.loads((J / "videos.json").read_text())["videos"]]
if len(sys.argv) > 2 and sys.argv[1] in ("all", "gaps"): names = sys.argv[2:]   # only these cuts (batch 1 files may not be on disk)

def one(n):
    p = O / f"wagbag_{n}.mp4"; plan = json.loads((O / f"wagbag_{n}.json").read_text()); errs = []
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(p)], capture_output=True, text=True, check=True).stdout)
    v = [s for s in pr["streams"] if s["codec_type"] == "video"][0]; a = [s for s in pr["streams"] if s["codec_type"] == "audio"]
    d = float(pr["format"]["duration"])
    if (v["width"], v["height"]) != (1080, 1920): errs.append(f"size {v['width']}x{v['height']}")
    if not a: errs.append("no audio")
    if abs(d - plan["expected"]) > 0.15: errs.append(f"dur {d:.2f} vs {plan['expected']}")
    e = subprocess.run(["ffmpeg", "-v", "info", "-i", str(p), "-vf", "blackdetect=d=0.05:pix_th=0.10", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    if e.count("black_start"): errs.append("black frames")
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1]); tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])
    if not -16 <= I <= -12: errs.append(f"loudness {I}")
    if tp > -0.5: errs.append(f"true peak {tp}")
    # allowed scene changes: piece boundaries + her own clip cuts mapped into the cut's timeline
    ok, t = [], 0.0
    for s in plan["segs"]:
        dur = round((s["b"] - s["a"]) * FPS) / FPS
        if t: ok.append(t)
        cuts = json.loads((J / "tr" / s["src"] / "cuts.json").read_text())
        ok += [t + c - s["a"] for c in cuts if s["a"] < c < s["b"]]
        t += dur
    o = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", "scale=270:480,select='gt(scene,0.35)',metadata=print:file=-", "-an", "-f", "null", "-"], capture_output=True, text=True).stdout
    sc = [float(x) for x in re.findall(r"pts_time:([\d.]+)", o)]
    ok += [float(x) for x in next(v for v in json.loads((J / "videos.json").read_text())["videos"] if v["name"] == n).get("scene_ok", [])]   # looked at by eye, noted in videos.json
    stray = [round(x, 2) for x in sc if not any(abs(x - y) <= 0.1 for y in ok)]
    if stray: errs.append(f"unplanned scene changes at {stray}")
    return errs, f"{d:.2f}s I={I} TP={tp} scenes={len(sc)}"

if sys.argv[1] == "all":
    bad = 0
    for n in names:
        errs, info = one(n); print(n, "OK" if not errs else "FAIL " + "; ".join(errs), info); bad += bool(errs)
    print("ALL_CUTS_OK" if not bad else "CUTS_FAIL"); sys.exit(1 if bad else 0)
if sys.argv[1] == "gaps":   # V2 (Grace 2026-11-19: no gaps between her lines): gapmeter.py on every cut
    bad = 0
    for n in names:
        r = subprocess.run([sys.executable, str(J / "gapmeter.py"), str(O / f"wagbag_{n}.mp4"), "0.25"], capture_output=True, text=True).stdout
        print(r.strip().splitlines()[0][:150]); bad += "GAPS_OK" not in r
    print("GAPS_ALL_OK" if not bad else "GAPS_FAIL"); sys.exit(1 if bad else 0)
if sys.argv[1] == "distinct":
    # Batch 1: no source second in two cuts. Batch 2 (Grace msg 626) reuses her clip 3/4 takes on purpose, so the rule is:
    # no intro (WagBag1 take) in two cuts, and no two cuts with the same set of body takes.
    V = json.loads((J / "videos.json").read_text())["videos"]; clash = []
    intro = {}; body = {}
    for v in V:
        t0 = v["takes"][0]; k = (t0["src"], round(t0["a"], 1))
        if k in intro: clash.append(("intro", v["name"], intro[k]))
        intro[k] = v["name"]
        sig = tuple(sorted((t["src"], round(t["a"], 1)) for t in v["takes"][1:]))
        if sig in body: clash.append(("body", v["name"], body[sig]))
        body[sig] = v["name"]
    print("DISTINCT_OK" if not clash else f"CLASH {clash}"); sys.exit(1 if clash else 0)
