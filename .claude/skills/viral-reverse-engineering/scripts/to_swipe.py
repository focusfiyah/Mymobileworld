#!/usr/bin/env python3
"""to_swipe.py - turn TikTok or YouTube Shorts data into the TSV that swipe.py ranks.

  python3 to_swipe.py tiktok tag-creatine.json [more.json] > captured.tsv
      Rows from tiktok-shop-coach (tiktok.py tag/discover/viral output). The baseline is
      each account's median views when every account has 3+ rows, else followers for all rows.
  python3 to_swipe.py shorts @handle [@handle ...] --n 30 > captured.tsv
      Each channel's last N Shorts through yt-dlp (uvx yt-dlp==2026.10.26 if not installed).
      The baseline is that channel's median views.

The hook column is the caption (TikTok, hashtags removed) or the title (Shorts), not the
spoken first line: Shorts captions need a sign-in from the cloud (tested 2026-11-07). For the
top rows, get the spoken hook with tiktok.py video and edit it into the TSV before ranking.
"""
import json, re, shutil, statistics, subprocess, sys

def clean(t):
    t = re.sub(r"#\S+", "", (t or "").split("\n")[0])
    return re.sub(r"\s+", " ", t).strip().replace("\t", " ")

def emit(rows):
    print("account\tfollowers\tmedian\tviews\thook")
    for r in rows:
        if r["hook"]:
            print(f"{r['account']}\t{r['followers'] or ''}\t{r['median'] or ''}\t{r['views']}\t{r['hook']}")

def tiktok(paths):
    rows = [x for p in paths for x in json.load(open(p, encoding="utf-8"))]
    by = {}
    for x in rows:
        by.setdefault(x.get("author"), []).append(x.get("views") or 0)
    use_med = all(len(v) >= 3 for v in by.values())
    if not use_med:
        print("baseline: follower count for every row (some accounts have under 3 videos here; "
              "mixing medians and followers would rank on two scales)", file=sys.stderr)
    out = []
    for x in rows:
        v = by[x.get("author")]
        out.append({"account": "@" + str(x.get("author")), "followers": x.get("author_followers"),
                    "median": int(statistics.median(v)) if use_med else None,
                    "views": x.get("views") or 0, "hook": clean(x.get("caption"))})
    emit(out)

def shorts(handles, n):
    ytdlp = [shutil.which("yt-dlp")] if shutil.which("yt-dlp") else ["uvx", "yt-dlp==2026.10.26"]
    out = []
    for h in handles:
        h = h if h.startswith("@") else "@" + h
        r = subprocess.run(ytdlp + ["--flat-playlist", "--playlist-end", str(n), "--print",
                           "%(view_count)s\t%(title)s", f"https://www.youtube.com/{h}/shorts"],
                           capture_output=True, text=True)
        vids = [l.split("\t", 1) for l in r.stdout.splitlines() if "\t" in l and l.split("\t")[0].isdigit()]
        if not vids:
            print(f"no Shorts read for {h}: {r.stderr.strip()[-200:]}", file=sys.stderr)
            continue
        med = int(statistics.median(int(v) for v, _ in vids))
        out += [{"account": h, "followers": None, "median": med, "views": int(v), "hook": clean(t)} for v, t in vids]
    emit(out)

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2 or a[0] not in ("tiktok", "shorts"):
        sys.exit(__doc__)
    if a[0] == "tiktok":
        tiktok(a[1:])
    else:
        n = 30
        if "--n" in a:
            i = a.index("--n"); n = int(a[i + 1]); del a[i:i + 2]
        shorts(a[1:], n)
