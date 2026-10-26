"""Calibrate grace/clip_check.py MIN_SCORE: real pairs (ugc/*/stills/SID.png + ugc/*/clips/SID.mp4) vs the same clips
paired with a still from ANOTHER job (what "the model ignored my image" looks like), plus a same-job other-shot set
(info only: same room and product, so it is expected to score high). Writes scores.json + prints the split.
  python3 tools/clipcheck/calibrate.py
"""
import glob, json, os, random, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "grace"))
import clip_check as cc

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(ROOT)
pairs = []
for c in sorted(glob.glob("ugc/*/clips/*.mp4")):
    job, sid = c.split("/clips/")[0], os.path.basename(c)[:-4]
    if os.path.exists(f"{job}/stills/{sid}.png"):
        pairs.append((f"{job}/stills/{sid}.png", c))
rng = random.Random(7)
neg, same = [], []
for s, c in pairs:
    job = c.split("/")[1]
    other = [p[0] for p in pairs if p[0].split("/")[1] != job]
    neg.append((rng.choice(other), c))
    sib = [p[0] for p in pairs if p[0].split("/")[1] == job and p[0] != s]
    if sib: same.append((rng.choice(sib), c))


def run(p):
    try:
        return cc.score(*p)
    except Exception as e:  # unreadable file: report, don't count
        return None


with ThreadPoolExecutor(8) as ex:
    P, N, S = (list(ex.map(run, x)) for x in (pairs, neg, same))
out = {"pos": list(zip(pairs, P)), "neg": list(zip(neg, N)), "same_job": list(zip(same, S))}
json.dump(out, open("tools/clipcheck/scores.json", "w"), indent=0)
import numpy as np
for name, v in (("pos", P), ("neg", N), ("same_job", S)):
    v = np.array([x for x in v if x is not None])
    print(f"{name:9s} n={len(v)} min={v.min():.3f} p5={np.percentile(v,5):.3f} p50={np.median(v):.3f} max={v.max():.3f}")
for t in (0.45, 0.5, 0.55, 0.6, 0.65):
    fp = sum(1 for x in P if x is not None and x < t); tn = sum(1 for x in N if x is not None and x < t)
    print(f"threshold {t}: real pairs flagged {fp}/{len(P)}, mismatches caught {tn}/{len(N)}")
