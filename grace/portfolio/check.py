#!/usr/bin/env python3
"""Gate checks for Grace's UGC portfolio page (grace/portfolio/GATES.md).

  check.py files   every media/ file the page references exists; mp4s are H.264 + AAC, faststart, < 15 MB; each has a poster
  check.py stats   every data-stat number on the page matches videos.json (TikTok numbers pulled 2026-10-28)
  check.py copy    visible copy has no banned words, no dash punctuation, no price, and reads at grade <= 8
Run from the repo root.
"""
import json, re, subprocess, sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
PAGE = (SITE / "index.html").read_text()


def fmt(n):
    """TikTok-style short number: 2,800,000 -> 2.8M, 44,300 -> 44.3K, 4,006 -> 4,006."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}".rstrip("0").rstrip(".") + "M"
    if n >= 10_000:
        return f"{n / 1_000:.1f}".rstrip("0").rstrip(".") + "K"
    return f"{n:,}"


def files():
    bad = []
    refs = sorted(set(re.findall(r"media/[\w.-]+", PAGE)))
    # grid cards build their <video> from data-video ids at tap time
    for vid in set(re.findall(r'data-video="(\d+)"', PAGE)):
        refs += [f"media/{vid}.mp4", f"media/{vid}.jpg"]
    for ref in sorted(set(refs)):
        f = SITE / ref
        if not f.exists():
            bad.append(f"missing {ref}")
            continue
        if f.suffix == ".mp4":
            if f.stat().st_size >= 15_000_000:
                bad.append(f"{ref} is {f.stat().st_size} bytes (>= 15 MB)")
            probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name", "-of", "csv=p=0", str(f)],
                                   capture_output=True, text=True).stdout.split()
            if "h264" not in probe or "aac" not in probe:
                bad.append(f"{ref} codecs {probe}")
            head = f.read_bytes()[:200_000]
            if head.find(b"moov") < 0 or head.find(b"moov") > head.find(b"mdat") > 0:
                bad.append(f"{ref} not faststart")
            if not f.with_suffix(".jpg").exists():
                bad.append(f"{ref} has no poster")
    total = sum(p.stat().st_size for p in (SITE / "media").iterdir())
    print(f"{len(set(refs))} media refs, {total / 1e6:.1f} MB")
    return bad


def stats():
    data = json.loads((ROOT / "videos.json").read_text())
    acct = data["account"]
    by_id = {v["id"]: v for v in data["videos"]}
    bad, n = [], 0
    for key, shown in re.findall(r'data-stat="([\w:]+)">([^<]+)<', PAGE):
        n += 1
        if ":" in key:
            field, vid = key.split(":")
            want = fmt(by_id[vid][field])
        else:
            want = fmt(acct[key])
        if shown.strip() != want:
            bad.append(f"{key}: page {shown!r} vs TikTok {want!r}")
    if n < 10:  # per-video stats only
        bad.append(f"only {n} stats tagged")
    # only self-filmed videos (Ralph 2026-10-28): every id on the page must be in videos.json, none from the AI list
    ai = {"7696231728855223582", "7696617399759555871", "7697844264050511135", "7700400913759980831",
          "7696627904985304351", "7699252578239925535", "7698506471268568351", "7696285070046301470"}
    for vid in set(re.findall(r'data-video="(\d+)"', PAGE)):
        if vid in ai:
            bad.append(f"AI-made video {vid} on the page")
        if vid not in by_id:
            bad.append(f"video {vid} has no TikTok record")
    # Grace 2026-10-30: no "2.8M views" callout (the #1 card's own Views stat stays, Ralph 2026-10-30),
    # no followers / likes / videos-posted account numbers
    for key in re.findall(r'data-stat="(\w+)"', PAGE):
        bad.append(f"account number {key} on the page")
    if PAGE.count("2.8M") != 1 or "views on one of her videos" in PAGE:
        bad.append("2.8M shown outside the #1 card's stats")
    print(f"{n} stats checked")
    return bad


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip, self.out = 0, []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "title"):
            self.skip += 1
        alt = dict(attrs).get("alt") or dict(attrs).get("aria-label")
        if alt:
            self.out.append(alt + ".")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "title"):
            self.skip -= 1

    def handle_data(self, d):
        if not self.skip and d.strip():
            self.out.append(d.strip())


def grade(text):
    sents = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    words = re.findall(r"[A-Za-z']+", text)

    def syl(w):
        w = w.lower()
        g = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith("le") else 0)
        return max(1, g)
    s = sum(syl(w) for w in words)
    return 0.39 * len(words) / len(sents) + 11.8 * s / len(words) - 15.59


def copy():
    p = Text()
    p.feed(PAGE)
    text = " ".join(p.out)
    bad = []
    for pat in [r"\breviewers?\b", r"the label says", r"order it now", r"heads up", r"lorem", r"TODO", r"\$\s?\d",
                r"\d+\s?(usd|dollars)", r" — | – |--", r"\bpackage(s)?\b.*\bprice", r"\bAI\b"]:
        if re.search(pat, text, re.I):
            bad.append(f"banned: {pat}")
    g = grade(re.sub(r"\b[\w.]+@[\w.]+\b|@\w+|\d[\d.,]*[KM]?", "", text))
    print(f"{len(text.split())} words, grade {g:.1f}")
    if g > 8:
        bad.append(f"reading grade {g:.1f} > 8")
    return bad


if __name__ == "__main__":
    mode = sys.argv[1]
    problems = {"files": files, "stats": stats, "copy": copy}[mode]()
    for b in problems:
        print("FAIL", b)
    print({"files": "FILES_OK", "stats": "STATS_OK", "copy": "COPY_OK"}[mode] if not problems else "CHECK_FAILED")
    sys.exit(1 if problems else 0)
