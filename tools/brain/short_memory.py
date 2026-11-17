"""Build Brain/Short memory.md: one line per standing rule, from the rule files themselves.

Ralph 2026-11-17: "If short memory is full ... create a short memory in your brain to pull from always so nothing is
left out." handoff/MEMORY_SHORT.txt (claude.ai memory) is capped at 2,000 characters; this note has no cap. Every
session reads it right after Brain/Index.md. It is generated, never hand-edited, so it can't drift from the rules:
each line is the rule's own bold title (or its first words), its first date, and the file that holds the full text.

usage:
  python3 tools/brain/short_memory.py [--vault /home/user/obsidian-vault]          write the note
  python3 tools/brain/short_memory.py --check [--vault ...]                         SHORT_MEMORY_OK / STALE (exit 1)
tools/brain/check.py runs --check, so a session can't end with a stale note. Sources missing from this container
(a repo not attached) are skipped, not counted as stale.
"""
import argparse, hashlib, pathlib, re, sys

HOME = pathlib.Path("/home/user")
SOURCES = [  # (repo-relative label, path) in reading order
    ("Mymobileworld/CLAUDE.md", HOME / "Mymobileworld/CLAUDE.md"),
    ("Mymobileworld/rules/other-jobs.md", HOME / "Mymobileworld/rules/other-jobs.md"),
    ("Dayone-ai/CLAUDE.md", HOME / "Dayone-ai/CLAUDE.md"),
    ("Dayone-ai/rules/day-one-videos.md", HOME / "Dayone-ai/rules/day-one-videos.md"),
    ("Dayone-ai/rules/rgh-posts.md", HOME / "Dayone-ai/rules/rgh-posts.md"),
    ("Dayone-ai/rules/story-series.md", HOME / "Dayone-ai/rules/story-series.md"),
    ("jean-rameau/CLAUDE.md", HOME / "jean-rameau/CLAUDE.md"),
]
ITEM = re.compile(r"^(?:- |\d+\. )(.*)")
DATE = re.compile(r"20\d\d-\d\d-\d\d")


def strip_quotes(t):
    """Drop top-level (...) groups that only say who said it and when, e.g. (Ralph 2026-10-21: "...")."""
    out, depth, buf = [], 0, ""
    for ch in t:
        if ch == "(":
            if depth == 0:
                buf = ""
            depth += 1
        if depth:
            buf += ch
        else:
            out.append(ch)
        if ch == ")" and depth:
            depth -= 1
            if depth == 0 and not re.match(r"\((Ralph|Grace|Jean|standard|Ralph \+|tested|moved|20\d\d)", buf):
                out.append(buf)
    if depth:  # unclosed group: keep it only if it is not a quote
        if not re.match(r"\((Ralph|Grace|Jean|standard|20\d\d)", buf):
            out.append(buf)
    return re.sub(r"\s+", " ", "".join(out)).replace(" :", ":").replace(" ;", ";").strip()


def clip(t, n):
    return t if len(t) <= n else t[:n - 3].rsplit(" ", 1)[0] + "..."


def line_for(text):
    d = DATE.search(text)
    bold = re.match(r"\*\*(.+?)\*\*:?\s*(.*)", text)
    if bold:
        head, body = strip_quotes(bold.group(1)).rstrip(":"), strip_quotes(bold.group(2)).lstrip(": ")
    else:
        t = strip_quotes(text)
        head, body = t, ""
    body = re.sub(r"\*\*", "", body)
    s = f"**{clip(head, 120)}**" + (f": {clip(body, 260)}" if body else "")
    rest = body[len(clip(body, 260)) - 3:] if len(body) > 260 else ""
    nevers = [clip(x.strip(), 170) for x in re.split(r"(?<=[.;])\s+", rest) if re.search(r"\b(never|Never|NEVER|not|only)\b", x)]
    if nevers:  # the limits a clipped line would lose (e.g. "never mention ... to Jean")
        s += " LIMITS: " + " | ".join(nevers[:4])
    if not bold:
        s = clip(re.sub(r"\*\*", "", head), 300)
    return s + (f" ({d.group(0)})" if d else "")


def digest(paths):
    return {lab: hashlib.sha256(p.read_bytes()).hexdigest()[:12] for lab, p in paths}


def build():
    present = [(lab, p) for lab, p in SOURCES if p.exists()]
    out = ["---", "type: memory", "---", "# Short memory",
           "", "Every standing rule, one line each, built from the rule files by Mymobileworld "
           "`tools/brain/short_memory.py` (Ralph 2026-11-17: \"create a short memory in your brain to pull from "
           "always so nothing is left out\"). Read it at the start of every session, right after [[Index]]. "
           "The full text and the newest date win: open the file named in each heading before acting on a rule. "
           "Do not hand-edit; rerun the script after any rule change. Hub: [[Rules map]].", ""]
    seen = set()  # the same rule is copied in Mymobileworld and Dayone-ai CLAUDE.md: list it once
    for lab, p in present:
        lines = []
        for raw in p.read_text().splitlines():
            m = ITEM.match(raw)
            if m and len(m.group(1)) > 25:
                ln = line_for(m.group(1))
                key = re.sub(r"\W+", "", ln.split(":", 1)[0].lower())[:60]
                if key in seen:
                    continue
                seen.add(key)
                lines.append("- " + ln)
        if lines:
            out += [f"## {lab}", *lines, ""]
    out += ["## Sources", *[f"- {lab}: {h}" for lab, h in digest(present).items()], ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default=str(HOME / "obsidian-vault"))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    note = pathlib.Path(a.vault) / "Brain" / "Short memory.md"
    if a.check:
        if not note.exists():
            print("SHORT_MEMORY_STALE: Brain/Short memory.md missing; run tools/brain/short_memory.py"); return 1
        stored = dict(re.findall(r"^- (\S+): ([0-9a-f]{12})$", note.read_text(), re.M))
        now = digest([(lab, p) for lab, p in SOURCES if p.exists()])
        bad = [lab for lab, h in now.items() if stored.get(lab) != h]
        print("SHORT_MEMORY_OK" if not bad else "SHORT_MEMORY_STALE: changed since last build: " + ", ".join(bad)
              + "; run tools/brain/short_memory.py")
        return 1 if bad else 0
    note.write_text(build())
    print(f"wrote {note} ({note.read_text().count(chr(10) + '- ')} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
