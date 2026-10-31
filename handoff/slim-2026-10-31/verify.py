"""Checks for the 2026-10-31 CLAUDE.md slim. Usage: verify.py lossless|pointers|phrases|refs|size"""
import pathlib, re, sys

H = pathlib.Path(__file__).parent
M, D = pathlib.Path("/home/user/Mymobileworld"), pathlib.Path("/home/user/Dayone-ai")
SHARED = [M / "tools/camofox/README.md", M / "tools/broll/SOURCE.md", M / "tools/media/README.md",
          M / "handoff/history/SETUP_NOTES.md"]
CORPUS = {
    "mmw": (H / "orig_mmw_CLAUDE.md.txt", [M / "CLAUDE.md", *sorted((M / "rules").glob("*.md")), *SHARED,
                                            M / "handoff/history/JOBS_LOG.md", M / "handoff/history/SKILL_INSTALL_LOG.md"]),
    "d1": (H / "orig_d1_CLAUDE.md.txt", [D / "CLAUDE.md", *sorted((D / "rules").glob("*.md")), *SHARED,
                                          D / "handoff/history/STATUS_LOG.md"]),
}
# Sentences changed on purpose after the move (stale pointers only), as (repo, old fragment, why).
CHANGED = [("mmw", "Full rule: Dayone-ai CLAUDE.md.", "the posting rule moved to Dayone-ai rules/rgh-posts.md")]


def norm(s): return re.sub(r"\s+", " ", s).strip()


def frags(text):
    for line in text.split("\n"):
        line = re.sub(r"^\s*(- |\d+\. |#+ )", "", line)
        for f in re.split(r"(?<=[.;!?])\s+", line):
            f = norm(f)
            if len(f) > 3:
                yield f


def lossless():
    bad = 0
    for k, (orig, files) in CORPUS.items():
        corpus = norm("\n".join(p.read_text() for p in files if p.exists()))
        allowed = [c[1] for c in CHANGED if c[0] == k]
        miss = [f for f in frags(orig.read_text()) if f not in corpus and not any(a in f or f in a for a in allowed)]
        print(k, "fragments missing:", len(miss))
        for f in miss[:5]: print("   ", f[:140])
        bad += len(miss)
    print("LOSSLESS_OK" if not bad else "LOSSLESS_FAIL")


def pointers():
    ok = True
    for repo in (M, D):
        text = (repo / "CLAUDE.md").read_text()
        for f in sorted((repo / "rules").glob("*.md")):
            rel = f"rules/{f.name}"
            if rel not in text: print("CLAUDE.md does not point to", repo.name, rel); ok = False
            if f.stat().st_size < 1000: print("too small", f); ok = False
        for rel in re.findall(r"`(rules/[\w-]+\.md)`", text):
            if not (repo / rel).exists(): print("dead pointer", repo.name, rel); ok = False
    for p in SHARED:
        if "Moved from CLAUDE.md (2026-10-31)" not in p.read_text(): print("no moved section", p); ok = False
    print("POINTERS_OK" if ok else "POINTERS_FAIL")


def phrases():
    # what the repos' own checks look for in CLAUDE.md (tools/camofox, tools/broll, grace/tests/docs.py,
    # grace/voice/r5, tools/clipcheck, looks/check_round2), plus the job index lines
    need = {M / "CLAUDE.md": ["BOOK.md", "she does", "2026-10-28", "broll", "camofox", "playwright", "backup",
                              "Clip check + real Kie cost", "thumbnail-looks", "Rule 0: the SCRIPT GATE",
                              "Hard rules for every ad", "House of Rameau (@houseoframeau)", "rules/other-jobs.md"],
            D / "CLAUDE.md": ["formats/shorts.md", "broll", "camofox", "playwright", "backup", "thumbnail-looks",
                              "Never make a video public", "rules/day-one-videos.md", "rules/rgh-posts.md",
                              "Ralph's own look in AI", "Model: Opus"]}
    miss = [(p.parent.name, w) for p, ws in need.items() for w in ws if w.lower() not in p.read_text().lower()]
    print("missing:", miss)
    print("PHRASES_OK" if not miss else "PHRASES_FAIL")


def refs():
    # no file may still send a reader to a CLAUDE.md section that moved
    moved = ["Numbers rules v2", "Original value rules", "What works", "Posting volume", "Content = 2027", "Social growth",
             "Instagram", "Pipeline", "pipeline step", "step 2", "Daily list"]
    pat = re.compile(r"CLAUDE\.md[\"'“ ,(]*(?:" + "|".join(re.escape(m) for m in moved) + ")")
    hits = []
    for root in (D, M, pathlib.Path("/home/user/claude-skills/skills")):
        for p in root.rglob("*"):
            if p.suffix not in (".md", ".py", ".txt") or any(x in p.parts for x in ("node_modules", "history", ".git")):
                continue
            if "slim-2026-10-31" in str(p) or "usage-audit" in str(p) or p.name in ("REMEMBER_ME.txt", "REMEMBER_ME_paste.txt", "GLOBAL_MEMORY.md", "CLAUDE_PREFERENCES.txt", "DAILY_ROUTINE.txt"):
                continue
            try:
                t = p.read_text()
            except Exception:
                continue
            for i, line in enumerate(t.split("\n"), 1):
                if pat.search(line): hits.append(f"{p}:{i}: {line.strip()[:110]}")
    print("\n".join(hits))
    print("REFS_OK" if not hits else f"REFS_FAIL {len(hits)}")


def size():
    tot0 = tot1 = 0
    for name, o, n in [("Mymobileworld", H / "orig_mmw_CLAUDE.md.txt", M / "CLAUDE.md"),
                       ("Dayone-ai", H / "orig_d1_CLAUDE.md.txt", D / "CLAUDE.md")]:
        a, b = len(o.read_text()), len(n.read_text())
        tot0 += a; tot1 += b
        print(f"{name}: {a} -> {b} chars (~{a // 4} -> ~{b // 4} tokens), {100 - 100 * b // a}% smaller")
    print(f"both: ~{tot0 // 4} -> ~{tot1 // 4} tokens, {100 - 100 * tot1 // tot0}% smaller")
    print("SIZE_OK" if tot1 < 0.75 * tot0 else "SIZE_FAIL")


globals()[sys.argv[1]]()
