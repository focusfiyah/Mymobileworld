"""Gate checks for the launch kit (ralph/dfy-service/launch). Usage: python3 verify.py <gate>"""
import re, sys, pathlib, html
HERE = pathlib.Path(__file__).parent

def fail(m): print("FAIL:", m); sys.exit(1)
def read(n):
    p = HERE / n
    if not p.exists(): fail(n + " missing")
    return p.read_text()

def grade(text):
    words = re.findall(r"[A-Za-z']+", text)
    sents = max(1, len(re.findall(r"[.!?](\s|$)", text)))
    syl = sum(max(1, len(re.findall(r"[aeiouy]+", w.lower())) - (1 if w.lower().endswith("e") and len(w) > 3 else 0)) for w in words)
    return 0.39 * len(words) / sents + 11.8 * syl / max(1, len(words)) - 15.59

g = sys.argv[1]
if g == "offer":
    t = read("OFFER.md")
    for k in ["$397 a month", "$497", "Founding offer", "500 call minutes", "**Calls", "**Reviews", "Month to month", "never pretends", "never calls anyone", "every customer"]:
        if k not in t: fail("OFFER.md lacks " + k)
    rows = re.findall(r"(?m)^\| (?!Name|---)([^|]+)\| ([^|]+)\|", t)
    usable = [r for r in rows if "TAKEN" not in r[1]]
    if len(usable) < 3: fail(f"{len(usable)} usable names")
    print("OFFER_OK")
elif g == "page":
    src = read("site/page.html"); idx = read("site/index.html")
    if not idx.startswith("<!doctype html>") or src.split("</style>")[1] not in idx: fail("index.html stale: run site/build.py")
    for k in ['id="call-btn"', 'id="book-btn"', "$397", "Questions", "justcall.io", "beside.com", "brightlocal.com"]:
        if k not in src: fail("page lacks " + k)
    body = re.sub(r"(?s)<style>.*?</style>|<script>.*?</script>|<[^>]+>", " ", src)
    gr = grade(html.unescape(body)); print(f"grade {gr:.1f}")
    if gr > 8: fail("page grade above 8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium" if pathlib.Path("/opt/pw-browsers/chromium").exists() else None); pg = b.new_page(viewport={"width": 390, "height": 844})
        pg.route("**/*", lambda r: r.abort() if "fonts.g" in r.request.url else r.continue_())
        pg.goto((HERE / "site/index.html").as_uri()); w = pg.evaluate("document.documentElement.scrollWidth"); b.close()
    print("scrollWidth", w)
    if w > 390: fail("side scroll at 390px")
    print("PAGE_OK")
elif g == "agent":
    t = read("AGENT.md")
    for k in ["inbound only", "may be recorded", "AI assistant", "transfer", "$397", "$497", "never say or suggest that you are a person", "Never make outgoing calls"]:
        if k.lower() not in t.lower(): fail("AGENT.md lacks " + k)
    print("AGENT_OK")
elif g == "channels":
    t = read("CHANNELS.md")
    for h in ["## Jean's network", "## Freeport and Baldwin", "## Reddit", "## Online"]:
        if h not in t: fail("missing " + h)
    if len(set(re.findall(r"https?://[^\s)]+", t))) < 6: fail("needs 6+ links")
    if re.search(r"(?i)cold call|we call them|you call them", t) and "No cold calls" not in t: fail("cold call found")
    if "Rules checked" not in t: fail("Reddit rules not recorded")
    print("CHANNELS_OK")
elif g == "plan":
    t = read("PLAN.md")
    if len(re.findall(r"(?m)^TOTAL: \$", t)) != 1: fail("needs exactly one TOTAL line")
    if "## Decisions" not in t: fail("no decisions section")
    if not re.search(r"\$1\.15", t): fail("phone number cost missing")
    print("PLAN_OK")
else: fail("unknown gate")
