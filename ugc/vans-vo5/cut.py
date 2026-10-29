"""Cuts V13-V17 on Grace's own VO (vo/grace_vo.wav), 2026-10-29. Free (ffmpeg).
  python3 cut.py V13 [V14 ...]   -> out/<V>_raw.mp4 (review render), then ai_finish -> out/<V>.mp4
Edit = Grace's style (grace/winners/STYLE_pritech.md): hand shot from frame 0, cuts on the first word of each phrase
(each window start snapped to the quietest 20 ms within +-0.25 s of the transcript time), the last line closes on a quick
run of that video's own hand shots. Per-shot trims from QC live in cut.json {"V13A": {"from": 0.4}, ...}.
Each video gets its own mild grade (hard rule 6), all bright and neutral."""
import json, subprocess, sys
from pathlib import Path
import numpy as np

J = Path(__file__).resolve().parent
S = json.loads((J / "shots.json").read_text())
CUT = json.loads((J / "cut.json").read_text()) if (J / "cut.json").exists() else {}
VO = J / "vo/grace_vo.wav"
GRADE = {"V13": "eq=brightness=0.02:saturation=1.02", "V14": "eq=brightness=0.03:saturation=0.98,colorbalance=bs=0.02",
         "V15": "eq=brightness=0.02:contrast=1.03:saturation=1.0", "V16": "eq=brightness=0.025:saturation=1.04",
         "V17": "eq=brightness=0.035:saturation=0.97,colorbalance=rs=-0.01:bs=0.015"}
FPS = 30


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-2000:])
    return r.stdout


def dur(f):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]))


def snap_points():
    """Window starts moved to the quietest 20 ms near each transcript time (cut on the first word)."""
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(VO), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                                     capture_output=True).stdout, np.int16).astype(float)
    hop = 320; rms = np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, "same")[::hop])
    beats = sorted({tuple(s["window"]) for s in S.values()})
    pts = [0.0]
    for (st, _) in beats[1:]:
        i0, i1 = int((st - 0.25) * 50), int((st + 0.25) * 50)
        pts.append(round((i0 + int(np.argmin(rms[i0:i1]))) / 50, 3))
    pts.append(round(dur(VO), 3))
    return pts


def clip(k):
    """Seedance first-frame take (Ralph 2026-10-29: "Ok on seed") unless QC picked another file in cut.json."""
    f = CUT.get(k, {}).get("file")
    return J / f if f else J / f"clips/{k}_sd.mp4"


def piece(src, start, length, out, grade, zoom=None):
    """zoom = (factor, x-centre 0..1, y-centre 0..1): a free crop from cut.json, e.g. to keep a removed item out of frame."""
    pre = f"crop=iw/{zoom[0]}:ih/{zoom[0]}:(iw-iw/{zoom[0]})*{zoom[1]}:(ih-ih/{zoom[0]})*{zoom[2]}," if zoom else ""
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-i", str(src), "-t", f"{length:.3f}", "-an",
         "-vf", f"{pre}scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps={FPS},{grade},setsar=1",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", str(out)])


def build(v):
    pts = snap_points(); tmp = J / f"out/tmp_{v}"; tmp.mkdir(parents=True, exist_ok=True)
    rows = sorted((k for k, s in S.items() if s["video"] == v), key=lambda k: S[k]["window"][0])
    for n, k in enumerate(rows):   # cut.json "max": a shot that is only clean for N s starts later (the shot before it runs longer)
        mx = CUT.get(k, {}).get("max")
        if mx and pts[n + 1] - pts[n] > mx: pts[n] = round(pts[n + 1] - mx, 3)
    hands = [k for k in rows if S[k]["kind"] == "HAND" and S[k]["beat"] not in ("K",)]
    parts, plan = [], []
    for n, k in enumerate(rows):
        a, b = pts[n], pts[n + 1]; length = b - a; src = clip(k); t0 = CUT.get(k, {}).get("from", 0.0)
        if S[k]["beat"] == "K":   # Grace's close: the K hold, then a quick run of this video's own hand shots (their unused tails)
            runs = [v + b for b in CUT.get("_run", {}).get(v, [])] or hands[-3:]   # tails QC'd: her hand still holds the moving shoe
            head = max(0.9, length - len(runs) * 0.42); run_len = (length - head) / len(runs)
            plan += [(src, t0, head)] + [(clip(h), min(dur(clip(h)), 4.0) - run_len - 0.15, run_len) for h in runs]
        else:
            plan.append((src, t0, length))
    plan_main = {k: i for i, k in enumerate(rows)}   # piece index of each shot's main use (zoom applies there only)
    for i, (src, st, ln) in enumerate(plan):
        if st + ln > dur(src) + 1e-3: sys.exit(f"{src.name}: needs {st + ln:.2f}s, has {dur(src):.2f}s (fix cut.json)")
        z = next((CUT[k].get("zoom") for k in CUT if isinstance(CUT[k], dict) and src.name == f"{k}_sd.mp4" and i == plan_main.get(k)), None)
        out = tmp / f"{i:02d}.mp4"; piece(src, st, ln, out, GRADE[v], z); parts.append(out)
    (tmp / "list.txt").write_text("".join(f"file '{p}'\n" for p in parts))
    raw = J / f"out/{v}_raw.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-i", str(VO),
         "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(raw)])
    fin = J / f"out/{v}.mp4"
    run(["bash", str(J.parents[1] / ".claude/skills/ugc-product-ad/scripts/ai_finish.sh"), str(raw), str(fin)])
    json.dump({"cuts": pts, "pieces": [(p[0].name, round(p[1], 3), round(p[2], 3)) for p in plan]}, open(J / f"out/{v}_edl.json", "w"), indent=1)
    print(v, "ok", f"{dur(fin):.2f}s", len(plan), "pieces")


if __name__ == "__main__":
    for v in sys.argv[1:]: build(v)
