"""Gate checks for the done-for-you service research (ralph/dfy-service). Usage: python3 verify.py <gate>"""
import re, subprocess, sys, pathlib
HERE = pathlib.Path(__file__).parent
R = HERE / "REPORT.md"

def fail(msg):
    print("FAIL:", msg); sys.exit(1)

def report():
    if not R.exists(): fail("REPORT.md missing")
    return R.read_text()

def sections(text):
    # each ranked pick is a "## #N" heading
    parts = re.split(r"(?m)^## #(\d) ", text)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}

g = sys.argv[1]
if g == "videos":
    for n in ("tiktok_part1.txt", "tiktok_part2.txt"):
        t = (HERE / "research" / n).read_text()
        if len(t) < 2000: fail(f"{n} short ({len(t)} chars)")
    print("VIDEOS_OK")
elif g == "thoughts":
    t = report()
    m = re.search(r"(?ms)^## My take on the video\n(.*?)(?=^## )", t)
    if not m or len(m.group(1).split()) < 120: fail("video take missing or under 120 words")
    print("THOUGHTS_OK")
elif g == "top3":
    s = sections(report())
    if sorted(s) != [1, 2, 3]: fail(f"ranked picks found: {sorted(s)}")
    need = ["**Who has it:**", "**Proof it hurts:**", "**The offer:**", "**Price:**", "**How we deliver it:**", "**First client:**"]
    for k, body in s.items():
        for n in need:
            if n not in body: fail(f"#{k} lacks {n}")
        urls = set(re.findall(r"https?://[^\s)\]]+", body))
        if len(urls) < 3: fail(f"#{k} has {len(urls)} source links, needs 3")
    print("TOP3_OK")
elif g == "better":
    t = report()
    if not re.search(r"(?m)^## Is done-for-you the best model\?", t): fail("model comparison section missing")
    if "**My pick:**" not in t: fail("no recommendation line")
    print("BETTER_OK")
elif g == "readability":
    t = report()
    body = re.sub(r"https?://\S+", "", t)
    body = re.sub(r"[#*|`>\[\]()]", " ", body)
    words = re.findall(r"[A-Za-z']+", body)
    sents = max(1, len(re.findall(r"[.!?](\s|$)", body)))
    syl = sum(max(1, len(re.findall(r"[aeiouy]+", w.lower())) - (1 if w.lower().endswith("e") and len(w) > 3 else 0)) for w in words)
    grade = 0.39 * len(words) / sents + 11.8 * syl / len(words) - 15.59
    print(f"grade {grade:.1f}")
    if grade > 9: fail("reading grade above 9")
    print("READ_OK")
else:
    fail("unknown gate")
