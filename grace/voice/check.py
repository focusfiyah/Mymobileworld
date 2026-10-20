"""Gate checks for the Grace voice re-clone (GATES.md). Usage: python3 grace/voice/check.py sources|train|clone|account|refs"""
import json, os, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get("GV_SCRATCH", "")
OLD = ["P8OUGBCvq8OBS4xlb65A", "bGrsdLmwBbYUgHRuMFOI"]


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
        for o in OLD:
            if o in t:
                bad.append((f, o))
    assert not bad, bad
    pm = open(os.path.join(root, "grace/PLAYBOOK.md")).read()
    assert new in pm, "PLAYBOOK lacks new id"
    print("rule files name only", new, "\nREFS OK")


if __name__ == "__main__":
    globals()[sys.argv[1]]()
