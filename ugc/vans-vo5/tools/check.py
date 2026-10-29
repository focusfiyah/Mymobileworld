"""Gate checks for GATES.md (Vans V13-V17). python3 tools/check.py vo|truth|shots|book|stills|clips|cuts"""
import json, subprocess, sys
from pathlib import Path
J = Path(__file__).resolve().parent.parent


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout.strip() or 0)


def vo():
    f = J / "vo/grace_vo.wav"; ref = dur(J / "ref/grace_ref.mp4"); d = dur(f) if f.exists() else 0
    samples = json.loads((J.parent.parent / "grace/voice/r5/samples.json").read_text())["samples"]
    logged = any(s["video_id"] == "7699252578239925535" for s in samples)
    music = J / "vo/sep/htdemucs/grace_vo_raw/no_vocals.wav"
    ok = d > 0 and abs(d - ref) < 0.2 and logged and music.exists()
    return ok, f"vo {d:.2f}s vs ref {ref:.2f}s, sample logged {logged}"


def truth():
    t = json.loads((J / "product_truth.json").read_text())
    missing = [p for p in t["photos"] if not (J / p).exists()]
    return bool(t["facts"]) and bool(t["forbid"]) and not missing, f"missing {missing}"


def shots():
    S = json.loads((J / "shots.json").read_text()); errs = []
    vids = sorted({s["video"] for s in S.values()})
    if len(vids) != 5: errs.append(f"{len(vids)} videos")
    ideas = {}
    for v in vids:
        rows = sorted((s for s in S.values() if s["video"] == v), key=lambda s: s["window"][0])
        if len(rows) != 11: errs.append(f"{v}: {len(rows)} shots")
        if rows[0]["window"][0] != 0 or abs(rows[-1]["window"][1] - 27.6) > 0.01: errs.append(f"{v}: does not span 0-27.6")
        for a, b in zip(rows, rows[1:]):
            if abs(a["window"][1] - b["window"][0]) > 1e-6: errs.append(f"{v}: gap {a['window']} {b['window']}")
        places = {s["place"] for s in rows}
        if any(not p.startswith(v) for p in places): errs.append(f"{v}: borrows another video's place {places}")
        for s in rows:
            if len(s["still_refs"]) > 8: errs.append(f"{v}{s['beat']}: {len(s['still_refs'])} refs")
            for r in s["still_refs"] + s["clip_refs"][1:]:
                if not (J / r).exists(): errs.append(f"missing {r}")
            key = s["scene"]
            if key in ideas: errs.append(f"same scene in {ideas[key]} and {v}{s['beat']}")
            ideas[key] = f"{v}{s['beat']}"
    return not errs, "; ".join(errs[:8])


def book():
    b = (J / "BOOK.md").read_text()
    sent = [l for l in b.splitlines() if l.startswith("Sent to Ralph:")]
    ok = b.count("\nTOTAL: $") == 1 and sent and "claude.ai" in sent[0]
    return ok, sent[0] if sent else "no Sent line"


def stills():
    S = json.loads((J / "shots.json").read_text())
    miss = [k for k in S if not (J / f"stills/{k}.png").exists()]
    qc = J / "qc/stills_qc.json"
    passed = json.loads(qc.read_text()) if qc.exists() else {}
    bad = [k for k in S if passed.get(k) != "PASS"]
    return not miss and not bad, f"missing {miss[:5]} not passed {bad[:5]}"


def clips():
    S = json.loads((J / "shots.json").read_text())
    miss = [k for k in S if not (J / f"clips/{k}.mp4").exists()]
    return not miss, f"missing {miss[:8]}"


def cuts():
    ref = dur(J / "vo/grace_vo.wav"); errs = []
    for v in ["V13", "V14", "V15", "V16", "V17"]:
        f = J / f"out/{v}.mp4"
        if not f.exists(): errs.append(f"{v} missing"); continue
        wh = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(f)],
                            capture_output=True, text=True).stdout.strip()
        if wh != "1080,1920": errs.append(f"{v} {wh}")
        if abs(dur(f) - ref) > 0.2: errs.append(f"{v} {dur(f):.2f}s vs {ref:.2f}s")
    return not errs, "; ".join(errs)


if __name__ == "__main__":
    k = sys.argv[1]
    ok, why = globals()[k]()
    print(f"{k.upper()}_OK" if ok else f"{k.upper()} FAILED: {why}")
    sys.exit(0 if ok else 1)
