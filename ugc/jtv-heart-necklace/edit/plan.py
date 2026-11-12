"""JTV Pink Heart Necklace: 10 x 16 s edits of Grace's two originals (2026-11-12).
python3 plan.py        -> writes out/plan.json (shots with exact source windows)
python3 plan.py check  -> RULES_OK when Grace's rules hold (msg 466): no take twice in a video, no shared opening or
                          closing take across videos, no two videos with the same order, windows inside the usable range,
                          every video 16.0 s.
A = export_1794449898752.mov (on-body, 42.4 s), B = 788f8e00773c481687702813256f4441.mov (product + selfies, 71.1 s).
Usable windows picked from 1 fps + 3 fps sheets and sharp.py (blurry, whip and blink stretches left out)."""
import json, sys
TAKES = {  # id: (src, start, end, what)
 "a1": ("A", 1.2, 7.9, "low angle, fingers framing the pendant on her chest"),
 "a2": ("A", 12.8, 18.4, "neck close, hand at her collarbone"),
 "a3": ("A", 19.6, 23.4, "tilted close, fingers beside the heart"),
 "a4": ("A", 25.5, 28.6, "ringed hand by the pendant"),
 "a5": ("A", 31.8, 33.9, "pendant close on bare skin"),
 "a6": ("A", 34.4, 36.6, "glossy lips, head tilted back, pendant on her neck"),
 "a7": ("A", 39.4, 42.2, "hand on chest with rings, pendant centre"),
 "b1": ("B", 0.0, 6.6, "heart hanging from her fingers, vanity bulbs behind"),
 "b2": ("B", 8.8, 13.0, "heart hanging from her fingers, later"),
 "b3": ("B", 15.4, 17.4, "heart lowered into frame in front of the round mirror"),
 "b4": ("B", 17.4, 20.6, "heart swinging close in front of the mirror"),
 "b5": ("B", 27.8, 30.7, "heart in her palm, close"),
 "b6": ("B", 34.2, 37.6, "heart in her palm, chain up"),
 "b7": ("B", 37.9, 41.6, "palm wider, rings"),
 "b8": ("B", 43.6, 47.0, "palm wider, other angle"),
 "b9": ("B", 48.4, 51.6, "mirror selfie, face and necklace"),
 "b10": ("B", 53.4, 55.2, "close selfie, chin down"),
 "b11": ("B", 55.4, 60.2, "hand on shoulder, neck and pendant"),
 "b12": ("B", 62.6, 64.3, "wide round mirror, full look"),
 "b13": ("B", 64.3, 66.4, "selfie closer"),
 "b14": ("B", 67.9, 71.0, "hand on shoulder, face turned"),
}
LOOK = {"b7": "palmwide", "b8": "palmwide", "b9": "selfie", "b10": "selfie", "b13": "selfie", "b11": "shoulder", "b14": "shoulder"}
VIDEOS = [  # takes in order; zoom (<=1.08), hflip on product-only shots, grade
 dict(takes="b4 b5 a2 b12 a4 b9 b14", zoom=1.0, flip=False, grade="eq=brightness=0.02:contrast=1.03"),
 dict(takes="b1 a5 b7 a3 b4 b11 b12 b13", zoom=1.05, flip=True, grade="eq=brightness=0.03:contrast=1.02:saturation=1.03"),
 dict(takes="b5 b3 a1 b9 b11 a7", zoom=1.0, flip=False, grade="eq=brightness=0.025:contrast=1.04:saturation=0.98"),
 dict(takes="a5 b6 b2 a2 b12 b14 a1", zoom=1.08, flip=False, grade="eq=brightness=0.035:contrast=1.02"),
 dict(takes="b9 b4 a7 b5 a3 b11 a4 b8", zoom=1.0, flip=True, grade="eq=brightness=0.02:contrast=1.05:saturation=1.04"),
 dict(takes="a4 b1 a5 b6 a2 b12", zoom=1.05, flip=False, grade="eq=brightness=0.03:contrast=1.03:saturation=1.02"),
 dict(takes="b11 b5 b2 a4 b13 a5 b7", zoom=1.0, flip=False, grade="eq=brightness=0.015:contrast=1.04"),
 dict(takes="a2 b4 b8 a7 b9 b1 a3", zoom=1.08, flip=True, grade="eq=brightness=0.03:contrast=1.02:saturation=1.05"),
 dict(takes="b2 a1 b6 b14 a5 b12 b5 b3", zoom=1.05, flip=False, grade="eq=brightness=0.025:contrast=1.03"),
 dict(takes="b6 a3 b4 b11 a4 a6", zoom=1.0, flip=True, grade="eq=brightness=0.02:contrast=1.04:saturation=1.02"),
]
TOTAL, FPS = 16.0, 30

def durations(ids):
    """Split 16 s over the shots: even share, capped by each take's length, rest goes to the longer takes; whole frames."""
    lens = [TAKES[i][2] - TAKES[i][1] for i in ids]; d = [0.0] * len(ids); free = list(range(len(ids))); left = TOTAL
    while free:
        share = left / len(free); capped = [k for k in free if lens[k] < share]
        if not capped:
            for k in free: d[k] = share
            break
        for k in capped: d[k] = lens[k]; left -= lens[k]; free.remove(k)
    f = [int(round(x * FPS)) for x in d]; k = max(range(len(f)), key=lambda j: lens[j] - d[j]); f[k] += int(TOTAL * FPS) - sum(f)
    return [x / FPS for x in f]

def build():
    out = []
    for v, cfg in enumerate(VIDEOS, 1):
        ids = cfg["takes"].split(); shots = []
        for k, (i, d) in enumerate(zip(ids, durations(ids))):
            src, s, e, what = TAKES[i]; frac = ((v * 7 + k * 3) % 10) / 9  # different moment of a shared take per video
            a = round(s + (e - s - d) * frac, 3)
            shots.append(dict(take=i, src=src, start=a, dur=round(d, 4), what=what, flip=cfg["flip"] and i[0] == "b" and LOOK.get(i) not in ("selfie", "shoulder")))
        out.append(dict(video=v, zoom=cfg["zoom"], grade=cfg["grade"], shots=shots))
    return out

def check(plan):
    e = []; opens = [p["shots"][0]["take"] for p in plan]; ends = [p["shots"][-1]["take"] for p in plan]
    if len(set(opens)) != len(opens): e.append(f"shared opening {opens}")
    if len(set(ends)) != len(ends): e.append(f"shared ending {ends}")
    if set(opens) & set(ends): e.append(f"a take opens one video and closes another {set(opens) & set(ends)}")
    orders = [tuple(s["take"] for s in p["shots"]) for p in plan]
    if len(set(orders)) != len(orders): e.append("two videos share an order")
    for p in plan:
        t = [s["take"] for s in p["shots"]]
        if len(set(t)) != len(t): e.append(f"V{p['video']} repeats a take")
        looks = [LOOK[x] for x in t if x in LOOK]
        if len(set(looks)) != len(looks): e.append(f"V{p['video']} has two takes of the same look {looks}")
        if abs(sum(s["dur"] for s in p["shots"]) - TOTAL) > 0.01: e.append(f"V{p['video']} not 16 s")
        if p["zoom"] > 1.1: e.append(f"V{p['video']} zoom {p['zoom']}")
        for s in p["shots"]:
            _, a, b, _ = TAKES[s["take"]]
            if s["start"] < a - 1e-6 or s["start"] + s["dur"] > b + 0.02: e.append(f"V{p['video']} {s['take']} outside its window")
            if s["dur"] < 1.0: e.append(f"V{p['video']} {s['take']} under 1 s")
    print("FAIL " + "; ".join(e) if e else f"RULES_OK {len(plan)} videos"); return not e

if __name__ == "__main__":
    plan = build(); json.dump(plan, open("out/plan.json", "w"), indent=1)
    if sys.argv[1:] == ["check"]: sys.exit(0 if check(plan) else 1)
    for p in plan: print(f"V{p['video']}: " + " ".join(f"{s['take']}({s['dur']:.2f})" for s in p["shots"]))
