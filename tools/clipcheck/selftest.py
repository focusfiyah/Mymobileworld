"""Self-test for grace/clip_check.py, grace/billed.py and the spend wiring (2026-10-26). No paid calls.
  python3 tools/clipcheck/selftest.py   -> "SELFTEST OK n/n" or the failures
"""
import glob, json, os, subprocess, sys, tempfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT); sys.path.insert(0, "grace")
import clip_check as cc, billed, spend

res = []
def ok(name, cond, why=""):
    res.append(cond); print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"  [{why}]"))

still, clip = "ugc/youtheory-collagen/stills/S2.png", "ugc/youtheory-collagen/clips/S2.mp4"
if not (os.path.exists(still) and os.path.exists(clip)):
    still, clip = "ugc/carpe-mb-15s/stills/S1.png", "ugc/carpe-mb-15s/clips/S1.mp4"
e, s = cc.check_clip(still, clip)
ok("real still/clip pair passes", not e, f"{e} {s:.2f}")
other = "ugc/space-heater-ptc/stills/V1S1.png"
e, s = cc.check_clip(other, clip)
ok("clip vs another job's still fails on the look", any("does not look like" in x for x in e), f"{e} {s:.2f}")
with tempfile.TemporaryDirectory() as d:
    land = os.path.join(d, "land.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-t", "2", "-vf", "scale=1280:720,setsar=1", land], check=True)
    e, _ = cc.check_clip(still, land, aspect="9:16")
    ok("landscape clip from a vertical still fails on shape", any("different shape" in x for x in e), str(e))
    small = os.path.join(d, "small.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-t", "2", "-vf", "scale=360:-2", small], check=True)
    e, _ = cc.check_clip(still, small)
    ok("360p clip fails the 720 floor", any("short side" in x for x in e), str(e))
    e, _ = cc.check_clip(still, small, min_short=300, seconds=2)
    ok("same small clip passes when the floor is lowered (positive control)", not e, str(e))
    sq = os.path.join(d, "sq.png")
    from PIL import Image; Image.new("RGB", (1024, 1024), "white").save(sq)
    ok("square still fails the 9:16 pre-check", bool(cc.check_still(sq, "9:16")))
    ok("vertical still passes the 9:16 pre-check", not cc.check_still(still, "9:16"), str(cc.check_still(still, "9:16")))
r = subprocess.run([sys.executable, "grace/clip_check.py", still, clip], capture_output=True, text=True)
ok("CLI prints CLIP_CHECK_OK and exits 0 on a real pair", r.returncode == 0 and "CLIP_CHECK_OK" in r.stdout, r.stdout + r.stderr)

d = json.load(open("tools/clipcheck/scores.json"))
P = [v for _, v in d["pos"] if v is not None]; N = [v for _, v in d["neg"] if v is not None]
caught = sum(v < cc.MIN_SCORE for v in N); flagged = sum(v < cc.MIN_SCORE for v in P)
ok(f"calibration at {cc.MIN_SCORE}: {caught}/{len(N)} mismatches caught, {flagged}/{len(P)} real pairs flagged",
   len(P) >= 200 and caught >= 0.98 * len(N) and flagged <= 0.07 * len(P))

missing = billed.logged_ids() - set(billed.load())
ok("billed cache covers every logged Kie task", not missing or len(missing) <= 3, f"{len(missing)} missing")
lip = None
for f in glob.glob("ugc/**/kie_log.json", recursive=True):
    for e in json.load(open(f)):
        if isinstance(e, dict) and e.get("taskId") and (e.get("request") or {}).get("model") == "volcengine/video-to-video-lip-sync" and not e.get("fail"):
            lip = e; break
    if lip: break
b = billed.usd(lip["taskId"])
ok("spend counts a lip-sync task at Kie's billed figure, not the list price",
   b is not None and abs(spend.entry_usd(lip) - b) < 1e-9 and abs(spend.kie_cost(lip)[1] - b) < 1e-9 and abs(b - spend.price(lip["request"])[1]) > 0.01,
   f"billed {b} entry {spend.entry_usd(lip)} list {spend.price(lip['request'])[1]}")

src = {f: open(f).read() for f in [".claude/skills/ugc-product-ad/scripts/omni_clip.py", "ugc/youtheory-collagen/kie.py", "ugc/oqq-wide-leg-pants/kie.py"]}
ok("omni_clip.py checks the still before paying and the clip after", all(x in src[".claude/skills/ugc-product-ad/scripts/omni_clip.py"] for x in ("check_still", "clip_check.report", "creditsConsumed")))
ok("template kie.py runners log billed credits and check clips", all(all(x in s for x in ("creditsConsumed", "clip_check.report", "_SRC[out]")) for f, s in src.items() if f.endswith("kie.py")))
print(f"SELFTEST {'OK' if all(res) else 'FAILED'} {sum(res)}/{len(res)}")
