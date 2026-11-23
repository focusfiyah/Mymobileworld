"""QC for the HofR BF silent-B batch. python3 qc.py <check> [jobs...]  (run from houseoframeau/posts/_tools)
checks: silent (sources have no audio stream), script (hook word for word + banned phrases), vo (whisper read-back),
cut (length, size, fps, loudness, HOOK_OK). Prints <CHECK>_OK or <CHECK>_FAIL lines."""
import json, re, subprocess, sys
from pathlib import Path
P = Path(__file__).resolve().parents[1]; R = P.parents[1]
JOBS = {"calmi-ring": "calmi", "cosrx-lip-care": "cosrx", "waterproof-eyeliner": "eyeliner", "wig-milk-spray": "wigmilk", "pinmoco-chair": "pinmoco"}
HOOK = {"calmi-ring": ("H055", ""), "cosrx-lip-care": ("H134", "Christmas"), "waterproof-eyeliner": ("H062", "your eyeliner is gone by lunch"),
        "wig-milk-spray": ("H028", "a tangled wig can be saved"), "pinmoco-chair": ("H061", "sit cross-legged at their desk")}
BANNED = ["order it now", "heads up", "reviewer", "the label says", "$", "dollar", "price", " - ", "—", "–", "buy now", "limited time"]
def sh(*a): return subprocess.run(a, capture_output=True, text=True)
def lines(j): return [l.strip() for l in (P / f"bf-{j}/vo/lines.txt").read_text().splitlines() if l.strip()]
def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " ")).split()
check, jobs = sys.argv[1], sys.argv[2:] or list(JOBS)
bad = 0
for j in jobs:
    if check == "silent":
        st = sh("ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(P / f"_src/{JOBS[j]}.mp4")).stdout.split()
        ok = "audio" not in st and "video" in st; print(j, st)
    elif check == "script":
        hooks = {h["id"]: (h.get("hook") or h.get("text")) for h in (lambda d: d if isinstance(d, list) else d["hooks"])(json.load(open(R / "grace/hooks/hooks.json")))}
        hid, fill = HOOK[j]; want = hooks[hid].replace("__", fill).rstrip("?.") ; L = lines(j)
        txt = " ".join(L).lower()
        probs = [b for b in BANNED if b in txt] + ([] if L[0].rstrip("?.") == want else [f"hook != {want!r}"]) + ([] if L[-1] == "It's in the orange cart." else ["close"])
        ok = not probs; print(j, hid, probs)
    elif check == "vo":
        wj = json.load(open(P / f"bf-{j}/vo/words.json")); probs = []
        for n, t in enumerate(lines(j)):
            heard = norm(wj["lines"][n]["text"]); w = norm(t)
            miss = [x for x in w if x not in heard]
            if len(miss) > max(0, len(w) // 10): probs.append((n, miss))
        ok = not probs; print(j, probs)
    elif check == "cut":
        f = P / f"bf-{j}/out/bf_{j}.mp4"
        v = sh("ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(f)).stdout
        v = json.loads(v); s = v["streams"][0]; dur = float(v["format"]["duration"])
        lu = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", sh("ffmpeg", "-nostats", "-i", str(f), "-af", "ebur128", "-f", "null", "-").stderr)[-1])
        box = json.load(open(P / f"bf-{j}/out/hookbox.json"))["box"]
        hk = sh("python3", str(R / "tools/hookcheck/hook_check.py"), str(f), "--hook", box).stdout.strip()
        fz = re.findall(r"freeze_duration: ([\d.]+)", sh("ffmpeg", "-nostats", "-i", str(f), "-vf", "freezedetect=n=0.003:d=0.7", "-an", "-f", "null", "-").stderr)
        ok = not fz and dur >= 15.0 and (s["width"], s["height"]) == (1080, 1920) and s["r_frame_rate"] == "30/1" and -16.5 <= lu <= -13.5 and "HOOK_OK" in hk
        print(j, f"{dur:.2f}s {s['width']}x{s['height']} {s['r_frame_rate']} {lu} LUFS", hk.splitlines()[-1] if hk else hk, "freezes:", fz)
    bad += not ok
print(f"{check.upper()}_{'OK' if not bad else 'FAIL'} {len(jobs) - bad}/{len(jobs)}")
