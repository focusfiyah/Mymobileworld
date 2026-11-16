"""Faster AI-twin pacing (Ralph 2026-11-16: "the pacing is kind of slow ... pick up the pace"; tapped "Trim pauses + 1.1x").
Cuts every pause between words longer than GAP down to KEEP seconds, then speeds picture + voice together by SPEED (lips stay synced),
and maps a cut plan's times (plan + pops) onto the new clock.
  python3 pace.py TALK.mkv WORDS.json OUT.mkv [--plan PLAN.json --plan-out NEW.json] [--speed 1.1 --gap 0.3 --keep 0.15]
TALK.mkv = talking clip with the final voice (before edit.py). Prints PACE_OK old_s new_s."""
import json, subprocess, sys, argparse
ap = argparse.ArgumentParser(); ap.add_argument("talk"); ap.add_argument("words"); ap.add_argument("out")
ap.add_argument("--plan"); ap.add_argument("--plan-out"); ap.add_argument("--speed", type=float, default=1.1)
ap.add_argument("--gap", type=float, default=0.3); ap.add_argument("--keep", type=float, default=0.15)
a = ap.parse_args()
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.talk], capture_output=True, text=True).stdout)
w = json.load(open(a.words)); cuts = []          # (start, end) of removed spans
for x, y in zip(w, w[1:]):
    g = y["s"] - x["e"]
    if g > a.gap: m = (x["e"] + y["s"]) / 2; cuts.append((m - (g - a.keep) / 2, m + (g - a.keep) / 2))
keep, t = [], 0.0
for c0, c1 in cuts: keep.append((t, c0)); t = c1
keep.append((t, dur))
def newt(x):                                       # old time -> new time
    if x >= 90: return x
    acc = 0.0
    for k0, k1 in keep:
        if x <= k1: return round((acc + max(0, x - k0)) / a.speed, 3)
        acc += k1 - k0
    return round(acc / a.speed, 3)
sel = "+".join(f"between(t,{k0:.3f},{k1:.3f})" for k0, k1 in keep)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.talk, "-vf", f"select='{sel}',setpts=N/25/TB/{a.speed},fps=25",
                "-af", f"aselect='{sel}',asetpts=N/SR/TB,atempo={a.speed}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
                "-c:a", "pcm_s16le", a.out], check=True)
if a.plan:
    p = json.load(open(a.plan))
    p["plan"] = [[newt(s[0]), newt(s[1])] + s[2:] for s in p["plan"]]; p["pops"] = [[newt(s[0]), newt(s[1])] + s[2:] for s in p["pops"]]
    json.dump(p, open(a.plan_out, "w"))
nd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.out], capture_output=True, text=True).stdout)
print("PACE_OK", round(dur, 2), round(nd, 2), "cuts", len(cuts))
