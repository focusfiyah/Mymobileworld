#!/usr/bin/env python3
"""Audience question map (free AnswerThePublic-style), Ralph 2026-10-05.

  python3 grace/audience.py <job_dir> "ingrown hair" "razor bumps" [--no-alpha]

Expands each seed the way AnswerThePublic does (questions, prepositions, comparisons, A-Z) through the public
autocomplete of Google, Bing, YouTube, Amazon and TikTok, i.e. what real people type. Free, no login, fixed-arg HTTPS GETs only.
Writes <job_dir>/research/audience/: raw.json, questions.md (grouped, with how many sources agree) and sources.txt.
Then YOU write <job_dir>/research/audience.md (Who / Pain point experience / Communication style / Questions they ask)
from that data, quoting real phrases from raw.json; `grace/gate.py` checks the headings and that the quotes exist.
"""
import json, re, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

QUESTIONS = ["are", "can", "how", "is", "should", "what", "when", "where", "which", "who", "why", "will", "does", "do", "why do", "how to get rid of"]
PREPOSITIONS = ["for", "with", "without", "near", "to", "on", "after", "before", "during", "around", "like", "from"]
COMPARISONS = ["vs", "versus", "or", "and", "better than", "instead of", "alternative"]
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}


def get(url):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15).read().decode("utf-8", "ignore")
        except Exception:
            time.sleep(1 + i)
    return ""


def google(q):
    try: return json.loads(get("https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q=" + urllib.parse.quote(q)))[1]
    except Exception: return []


def youtube(q):
    t = get("https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&hl=en&gl=us&q=" + urllib.parse.quote(q))
    return re.findall(r'\["([^"]+)",0', t.replace("\\u0026", "&").replace("\\u0027", "'"))


def bing(q):
    t = get("https://www.bing.com/AS/Suggestions?mkt=en-us&cvid=1&qry=" + urllib.parse.quote(q))
    return [re.sub(r"\s+", " ", x).strip() for x in re.findall(r'<li class="sa_sg"[^>]*\bquery="([^"]+)"', t)]


def amazon(q):
    try: return [s["value"] for s in json.loads(get("https://completion.amazon.com/api/2017/suggestions?mid=ATVPDKIKX0DER&alias=aps&prefix=" + urllib.parse.quote(q)))["suggestions"]]
    except Exception: return []


def tiktok(q):
    try: return [x["content"] for x in json.loads(get("https://www.tiktok.com/api/search/general/preview/?aid=1988&keyword=" + urllib.parse.quote(q))).get("sug_list", [])]
    except Exception: return []


SOURCES = {"google": google, "bing": bing, "youtube": youtube, "amazon": amazon, "tiktok": tiktok}


def queries(seed, alpha=True):
    out = [("seed", seed)]
    out += [("question", f"{w} {seed}") for w in QUESTIONS]
    out += [("preposition", f"{seed} {w}") for w in PREPOSITIONS]
    out += [("comparison", f"{seed} {w}") for w in COMPARISONS]
    if alpha: out += [("alphabetical", f"{seed} {c}") for c in "abcdefghijklmnopqrstuvwxyz"]
    return out


def run(job, seeds, alpha=True):
    jobs = [(seed, kind, q, src) for seed in seeds for kind, q in queries(seed, alpha) for src in SOURCES]
    def one(j):
        seed, kind, q, src = j
        return [(seed, kind, q, src, s.strip().lower()) for s in SOURCES[src](q)]
    rows = []
    with ThreadPoolExecutor(6) as ex:
        for r in ex.map(one, jobs): rows += r
    d = Path(job) / "research" / "audience"; d.mkdir(parents=True, exist_ok=True)
    (d / "raw.json").write_text(json.dumps([dict(zip(("seed", "kind", "query", "source", "suggestion"), r)) for r in rows], indent=0))
    # group by suggestion: which sources agree, which kind of query found it
    agg = {}
    for seed, kind, q, src, s in rows:
        if s == seed.lower() or len(s) < 6: continue
        a = agg.setdefault(s, {"sources": set(), "kinds": set()}); a["sources"].add(src); a["kinds"].add(kind)
    groups = {"questions": [], "comparisons": [], "preposition and situation phrases": [], "everything else (A-Z)": []}
    for s, a in agg.items():
        first = s.split()[0]
        if first in {w.split()[0] for w in QUESTIONS} and first in {"are", "can", "how", "is", "should", "what", "when", "where", "which", "who", "why", "will", "does", "do"}: g = "questions"
        elif re.search(r"\b(vs|versus|or|better than|instead of|alternative)\b", s): g = "comparisons"
        elif a["kinds"] & {"preposition"}: g = "preposition and situation phrases"
        else: g = "everything else (A-Z)"
        groups[g].append((len(a["sources"]), s, sorted(a["sources"])))
    md = [f"# Audience question map ({time.strftime('%Y-%m-%d')}), seeds: {', '.join(seeds)}",
          f"{len(agg)} distinct phrases from {len(jobs)} autocomplete lookups (Google, Bing, YouTube, Amazon). Higher count = more sources agree.\n"]
    for g, items in groups.items():
        items.sort(key=lambda x: (-x[0], x[1]))
        md.append(f"## {g.capitalize()} ({len(items)})")
        md += [f"- [{n}] {s}  ({', '.join(src)})" for n, s, src in items[:80]]
        md.append("")
    (d / "questions.md").write_text("\n".join(md))
    (d / "sources.txt").write_text("Google, Bing, YouTube and Amazon public autocomplete (US English), expanded the AnswerThePublic way. Run " + time.strftime("%Y-%m-%d %H:%M") + "\n")
    print(f"{len(agg)} phrases -> {d}/questions.md")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) < 2: sys.exit(__doc__)
    run(a[0], a[1:], "--no-alpha" not in sys.argv)
