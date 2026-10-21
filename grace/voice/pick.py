"""Rank Grace's TikTok audio for voice cloning (free, local).

Usage: python3 pick.py AUDIO_DIR [N]  -> ranks.json in AUDIO_DIR + the top N printed

Per clip: echo (echo.measure), speech seconds, dynamic range (90th - 10th percentile level in
10 ms frames; voice-only clips sit above ~35 dB, music under the voice pulls it down) and the
level in the gaps between words. Keeps clips with >= 6 s of speech, range >= 32 dB and a
measurable echo, sorted driest first.
"""
import json, os, sys
import numpy as np
from echo import load, measure


def gaps(path):
    x, sr = load(path)
    hop = sr // 100
    n = len(x) // hop
    db = 10 * np.log10(np.array([np.mean(x[i * hop:(i + 1) * hop] ** 2) for i in range(n)]) + 1e-10)
    return float(np.percentile(db, 90) - np.percentile(db, 10)), float(np.percentile(db, 10))


MIN_RANGE = 24


def main(d, top=40):
    rows = []
    for f in sorted(os.listdir(d)):
        if not f.endswith(".wav"):
            continue
        p = os.path.join(d, f)
        try:
            rt, tail, sp, nd = measure(p)
            rng, floor = gaps(p)
        except Exception as e:
            print("skip", f, e)
            continue
        rows.append(dict(id=f[:-4], rt60_est_ms=rt, tail_db=tail, speech_s=sp, range_db=rng, floor_db=floor))
    json.dump(rows, open(os.path.join(d, "ranks.json"), "w"), indent=1)
    ok = [r for r in rows if r["rt60_est_ms"] and r["speech_s"] >= 6 and r["range_db"] >= MIN_RANGE]
    ok.sort(key=lambda r: (r["rt60_est_ms"], r["tail_db"]))
    print(f"{len(rows)} clips, {len(ok)} pass speech/range")
    for r in ok[:top]:
        print(f"{r['id']}  rt={r['rt60_est_ms']:.0f}  tail={r['tail_db']:.1f}  speech={r['speech_s']:.0f}s  range={r['range_db']:.0f}  floor={r['floor_db']:.0f}")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 40)
