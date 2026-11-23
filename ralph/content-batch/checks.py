"""Gate checks for a weekly batch. python3 checks.py scripts|kits|faceless|carousels WEEK"""
import sys, json, re, glob, pathlib, subprocess
HERE = pathlib.Path(__file__).parent; what, week = sys.argv[1], sys.argv[2]; D = HERE / week
S = json.load(open(D / "scripts.json")); bad = []

if what == "scripts":
    W = lambda s: re.findall(r"[a-z0-9']+", s.lower())
    src = [W(open(f, errors="ignore").read()) for f in ["/home/user/Mymobileworld/grace/PLAYBOOK.md", "/home/user/Mymobileworld/grace/hooks/HOOKS.md"]
           + glob.glob("/home/user/Mymobileworld/.claude/skills/ugc-product-ad/**/*.md", recursive=True)]
    G = {tuple(w[i:i + 6]) for w in src for i in range(len(w) - 5)}
    txt = " ".join([s["line"] for t in S["twin"] for s in t["shots"]] + [l["say"] for f in S["faceless"] for l in f["lines"]]
                   + [x["head"] + ". " + x["sub"] for c in S["carousel"] for x in c["slides"]])
    w = W(txt); shared = [" ".join(w[i:i + 6]) for i in range(len(w) - 5) if tuple(w[i:i + 6]) in G]
    if shared: bad.append(f"shared 6-word runs {shared}")
    hooks = [t["shots"][0]["line"] for t in S["twin"]] + [f["lines"][0]["say"] for f in S["faceless"]] + [c["slides"][0]["head"] for c in S["carousel"]]
    json.dump({"hooks": [{"hook": h} for h in hooks]}, open(D / "hooks.json", "w"))
    r = subprocess.run(["python3", "-I", "/home/user/Dayone-ai/products/ai-video-kit/tools/hook_similarity.py", str(D / "hooks.json")], capture_output=True, text=True).stdout
    if "too_close=0" not in r: bad.append("hook close to Grace's: " + r.strip()[:200])
    if re.search(r"\$\s?\d|\bdollars?\b", txt): bad.append("price in script")
    sents = [x for x in re.split(r"[.!?]+", txt) if x.strip()]; ws = re.findall(r"[A-Za-z']+", txt)
    syl = lambda x: max(1, len(re.findall(r"[aeiouy]+", x.lower())) - (1 if x.lower().endswith("e") else 0))
    grade = 0.39 * len(ws) / len(sents) + 11.8 * sum(syl(x) for x in ws) / len(ws) - 15.59
    if grade > 6: bad.append(f"grade {grade:.1f}")
    print(f"words={len(w)} grade={grade:.1f}"); print("SCRIPTS_OK" if not bad else f"BAD {bad}")

elif what == "kits":
    for t in S["twin"]:
        k = json.load(open(D / "kits" / t["id"] / "kit.json"))
        if len(k) != 4: bad.append(f"{t['id']} has {len(k)} shots")
        if len({x["angle"] for x in k}) != len(k): bad.append(f"{t['id']} repeats an angle")
        for x in k:
            if not (D / "kits" / t["id"] / x["room"]).exists(): bad.append(f"missing room {x['room']}")
            if "KIT" in x["prompt"]: bad.append(f"{x['shot']} capital KIT in prompt")
            if "counting on his fingers" in x["prompt"]: bad.append(f"{x['shot']} asks for finger counting")
            if "Image 3" not in x["prompt"]: bad.append(f"{x['shot']} no room reference")
    print("KITS_OK" if not bad else f"BAD {bad}")

elif what == "faceless":
    for f in S["faceless"]:
        v = D / "faceless" / f["id"] / f"{f['id']}_final.mp4"
        try: d = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(v)], capture_output=True, text=True).stdout)
        except Exception: bad.append(f"{v} unreadable"); continue
        vs = [s for s in d.get("streams", []) if s["codec_type"] == "video"]; au = [s for s in d.get("streams", []) if s["codec_type"] == "audio"]
        dur = float(d.get("format", {}).get("duration", 0))
        if not vs or (vs[0]["width"], vs[0]["height"]) != (1080, 1920): bad.append(f"{f['id']} size")
        if not au: bad.append(f"{f['id']} no audio")
        if not 10 <= dur <= 45: bad.append(f"{f['id']} duration {dur}")
        heard = {x["w"].lower().strip(".,?!") for x in json.load(open(D / "faceless" / f["id"] / "words.json"))}
        heard |= {p for x in heard for p in x.split("-")}
        miss = [x for x in re.findall(r"[a-z']+", " ".join(l["say"] for l in f["lines"]).lower().replace("dm", "dm")) if x not in heard]
        if miss: bad.append(f"{f['id']} not heard {miss}")
    print("FACELESS_OK" if not bad else f"BAD {bad}")

elif what == "carousels":
    from PIL import Image
    for c in S["carousel"]:
        fs = sorted(glob.glob(str(D / "carousel" / c["id"] / "*.png")))
        if len(fs) != len(c["slides"]): bad.append(f"{c['id']} {len(fs)} slides vs {len(c['slides'])}")
        bad += [f"{f} size" for f in fs if Image.open(f).size != (1080, 1350)]
    print("CAROUSELS_OK" if not bad else f"BAD {bad}")
