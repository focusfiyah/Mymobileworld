"""Gate checks for the Grace voice re-clone (GATES.md). Usage: python3 grace/voice/check.py sources|train|clone|account|refs"""
import json, os, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get("GV_SCRATCH", "")
OLD = ["P8OUGBCvq8OBS4xlb65A", "bGrsdLmwBbYUgHRuMFOI", "3dmagVYZFvrGkBbWWmGC"]


def api(path):
    return json.load(urllib.request.urlopen("https://api.elevenlabs.io" + path))


def sources():
    s = json.load(open(os.path.join(HERE, "sources.json")))
    assert s["account"] == "@shewiththeglow" and s["clips"], "no clips"
    for c in s["clips"]:
        assert c["posted"] < "2026-09-25", c
        assert int(c["id"]) >> 32 < 1790294400, c  # id timestamp < 2026-09-25 UTC
        assert c["speaker_loo"] >= 0.87, c
    print(f"{len(s['clips'])} clips, all before 2026-09-25, speaker >= 0.87\nSOURCES OK")


def train():
    sys.path.insert(0, HERE)
    from echo import measure
    d = os.path.join(SCRATCH, "train")
    tot = 0
    for f in sorted(os.listdir(d)):
        rt, tail, sp, _ = measure(os.path.join(d, f))
        assert rt is not None and rt <= 160, (f, rt)
        tot += sp
    assert 60 <= tot <= 180, tot
    print(f"speech {tot:.0f}s, every file rt60_est <= 160 ms\nTRAIN OK")


def clone():
    sys.path.insert(0, HERE)
    from echo import measure
    new = json.load(open(os.path.join(HERE, "grace.json")))["voice_id"]
    assert new in [v["voice_id"] for v in api("/v2/voices?page_size=100&voice_type=personal")["voices"]]
    from echo import phrase_end
    rn = measure(os.path.join(HERE, "test_new.mp3"))[0]
    ro = measure(os.path.join(HERE, "test_oldC.mp3"))[0]
    pn, kn = phrase_end(os.path.join(HERE, "test_new.mp3"))
    po, ko = phrase_end(os.path.join(HERE, "test_oldC.mp3"))
    pb, _ = phrase_end(os.path.join(HERE, "test_B.mp3"))
    pc, _ = phrase_end(os.path.join(HERE, "test_C.mp3"))
    print(f"pause decay: new {pn:.0f} ms ({kn}) | old C {po:.0f} ms ({ko}) | control C {pc:.0f} > B {pb:.0f}")
    print(f"fast-decay rt: new {rn:.0f} | old C {ro:.0f}")
    assert pc > pb, "meter control failed (old C test should read echoier than B)"
    assert kn >= 4 and pn <= 0.7 * po and rn <= ro, "new voice not drier"
    print("CLONE OK")


def account():
    new = json.load(open(os.path.join(HERE, "grace.json")))["voice_id"]
    vs = api("/v2/voices?page_size=100&voice_type=personal")["voices"]
    ids = [v["voice_id"] for v in vs]
    grace = [v for v in vs if "grace" in v["name"].lower()]
    assert new in ids and not any(o in ids for o in OLD) and len(grace) == 1, [(v["name"], v["voice_id"]) for v in vs]
    print("only Grace voice:", grace[0]["name"], new, "\nACCOUNT OK")


def refs():
    root = os.path.abspath(os.path.join(HERE, "..", ".."))
    files = ["CLAUDE.md", "grace/PLAYBOOK.md", "grace/voice/README.md", ".claude/skills/ugc-product-ad/SKILL.md",
             "handoff/GLOBAL_MEMORY.md", "handoff/MEMORY_SHORT.txt", "handoff/REMEMBER_ME.txt", "handoff/CLAUDE_PREFERENCES.txt"]
    new = json.load(open(os.path.join(HERE, "grace.json")))["voice_id"]
    bad = []
    for f in files:
        p = os.path.join(root, f)
        if not os.path.exists(p):
            continue
        t = open(p).read()
        t = t.split("## Retired")[0]  # the README's history section names the deleted voices on purpose
        for o in OLD:
            if o in t:
                bad.append((f, o))
    assert not bad, bad
    pm = open(os.path.join(root, "grace/PLAYBOOK.md")).read()
    assert new in pm, "PLAYBOOK lacks new id"
    print("rule files name only", new, "\nREFS OK")


def accent():
    a = json.load(open(os.path.join(HERE, "accent_rank.json")))
    used = [r for r in a["ranked"] if r["used"]]
    assert len(used) >= 5 and all(r["posted"] < "2026-09-25" for r in used), used
    assert min(r["sim_to_example"] for r in used) > a["controls"]["round1_train_mean"] + 0.05
    print(f"{len(used)} clips, closeness to Ralph's example {min(r['sim_to_example'] for r in used)}+ vs round-1 set {a['controls']['round1_train_mean']}\nACCENT OK")


def round2():
    sys.path.insert(0, HERE)
    from echo import load
    import numpy as np
    text = "Okay so I was skeptical about this one, but I've been using it every single morning for two weeks and honestly? I'm obsessed. It's in the orange cart."
    files = {"test_A_v2.mp3": len(text), "test_D_tag.mp3": len(text) + len("[Haitian accent] "),
             "test_C_accent.mp3": len(text), "test_E_accent_v2.mp3": len(text)}
    for f in files:
        x, _ = load(os.path.join(HERE, f))
        assert len(x) > 16000 * 5, f
    chars = sum(files.values())
    print(f"4 test lines rendered, {chars} characters of text billed")
    assert chars <= 500, f"over the ~450 quote: {chars}"
    print("ROUND2 OK")


if __name__ == "__main__":
    globals()[sys.argv[1]]()
