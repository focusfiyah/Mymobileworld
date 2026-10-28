"""Checks for Ralph's AI consultant site (GATES.md). Usage: python3 verify.py <render|hero|privacy|media|copy|motion|detect|form|live|shots|all>
Site source: /home/user/focusfiyah.github.io (served locally on a free port for browser checks)."""
import sys, os, re, json, glob, subprocess as sp, threading, http.server, socketserver, functools, html

SITE = os.environ.get("SITE", "/home/user/focusfiyah.github.io")  # SITE/PAGE env: run the checks on a mockup folder (r2)
INDEX = os.path.join(SITE, os.environ.get("PAGE", "index.html"))
SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proof")
SKILL = (glob.glob("/root/.claude/skills/synced/*/web-design-stack") + ["/home/user/Mymobileworld/.claude/skills/web-design-stack"])[0]


def fail(msg):
    print("FAIL:", msg); sys.exit(1)


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Quiet, directory=SITE)
    srv = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}/{os.environ.get('PAGE', '')}"


def browser(fn):
    from playwright.sync_api import sync_playwright
    srv, url = serve()
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])
            try:
                return fn(b, url)
            finally:
                b.close()
    finally:
        srv.shutdown()


def visible_text():
    s = open(INDEX).read()
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def render():
    def run(b, url):
        out = []
        for w, h in [(390, 844), (1440, 900)]:
            pg = b.new_page(viewport={"width": w, "height": h})
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(url, wait_until="load", timeout=60000); pg.wait_for_timeout(800)
            sw = pg.evaluate("document.documentElement.scrollWidth")
            if errs: fail(f"{w}px console errors: {errs}")
            if sw > w: fail(f"{w}px page scrolls sideways (scrollWidth {sw})")
            out.append(f"{w}px ok")
            pg.close()
        print(", ".join(out)); print("RENDER_OK")
    browser(run)


def hero():
    def run(b, url):
        pg = b.new_page(viewport={"width": 390, "height": 844})
        pg.goto(url, wait_until="load", timeout=60000); pg.wait_for_timeout(600)
        for sel in [".over h1", ".pitch", ".actions .btn"]:
            r = pg.locator(sel).bounding_box()
            if not r: fail(f"{sel} missing")
            if r["y"] < 0 or r["y"] + r["height"] > 844 or r["x"] < 0 or r["x"] + r["width"] > 390:
                fail(f"{sel} not fully inside the first phone screen: {r}")
        print("HERO_OK")
    browser(run)


# Real names, handles and numbers that must never appear. Positive control: privacy --control.
BANNED_PRIVATE = [r"\bGrace\b", r"Vallon", r"\bJean\b", r"Rameau", r"Diaspo", r"House of Rameau", r"@\w*grace", r"718[\s.-]?576", r"576[\s.-]?2667",
                  r"516[\s.-]?\d{3}", r"786[\s.-]?496", r"945[\s.-]?300", r"Pierre", r"Toussaint", r"\bKie\b", r"Seedance", r"ElevenLabs"]


def privacy():
    files = [INDEX] + glob.glob(os.path.join(SITE, "*.md"))
    if "--control" in sys.argv:
        sample = "Grace sent it; call Diaspo at 718-576-2667"
        hits = [p for p in BANNED_PRIVATE if re.search(p, sample, re.I)]
        if len(hits) < 3: fail("control did not trip the checker")
        print("CONTROL_TRIPPED", hits); return
    for f in files:
        if os.path.basename(f) in ("PRODUCT.md",):  # private brief, not linked from the page
            continue
        s = open(f).read()
        for p in BANNED_PRIVATE:
            m = re.search(p, s, re.I)
            if m: fail(f"{os.path.basename(f)} contains '{m.group(0)}'")
    print("PRIVACY_OK")


def media():
    total = 0
    for f in glob.glob(os.path.join(SITE, "**/*"), recursive=True):
        if "/.git/" in f or os.path.isdir(f): continue
        total += os.path.getsize(f)
    for f in glob.glob(os.path.join(SITE, "media/*.mp4")):
        a = sp.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip()
        if a: fail(f"{os.path.basename(f)} has an audio stream")
        if os.path.getsize(f) > 1.6e6: fail(f"{os.path.basename(f)} is over 1.6 MB")
    used = re.findall(r'(?:src|data-src|poster)="(media/[^"]+)"', open(INDEX).read())
    for u in used:
        if not os.path.exists(os.path.join(SITE, u)): fail(f"missing {u}")
    if total > 15e6: fail(f"site is {total/1e6:.1f} MB")
    print(f"{len(set(used))} media files, site {total/1e6:.2f} MB"); print("MEDIA_OK")


BANNED_WORDS = [r"reviewer", r"order it now", r"heads up", r"\$\s?\d", r"\d+\s?(?:dollars|usd)", r"game[- ]?changer", r"seamless", r"leverage", r"unlock", r"elevate", r"revolutioniz", r"cutting[- ]edge", r"supercharge"]


def copy():
    t = visible_text()
    if re.search(r"\s[—–-]\s|—|–", t): fail("a dash used as punctuation: " + re.search(r".{20}(?:\s[—–-]\s|—|–).{20}", t).group(0))
    for p in BANNED_WORDS:
        m = re.search(p, t, re.I)
        if m: fail(f"banned word/price '{m.group(0)}'")
    words = re.findall(r"[A-Za-z']+", t)
    sents = max(1, len(re.findall(r"[.!?](?:\s|$)", t)))
    def syl(w):
        w = w.lower(); v = re.findall(r"[aeiouy]+", w); n = len(v)
        if w.endswith("e") and n > 1: n -= 1
        return max(1, n)
    s = sum(syl(w) for w in words)
    grade = 0.39 * len(words) / sents + 11.8 * s / len(words) - 15.59
    print(f"{len(words)} words, {sents} sentences, grade {grade:.1f}")
    if grade > 8: fail(f"reading grade {grade:.1f} > 8")
    print("COPY_OK")


def motion():
    r = sp.run([sys.executable, os.path.join(SKILL, "scripts/motion_check.py"), SITE], capture_output=True, text=True)
    print(r.stdout.strip()[-800:], r.stderr.strip()[-400:])
    if r.returncode or "MOTION_OK" not in r.stdout: fail("motion_check did not pass")


def detect():
    env = dict(os.environ, IMPECCABLE_NO_TELEMETRY="1")
    r = sp.run(["sh", os.path.join(SKILL, "impeccable/scripts/impeccable"), "detect", "--json", INDEX], capture_output=True, text=True, env=env, cwd=SITE)
    out = r.stdout.strip()
    try:
        data = json.loads(out[out.index("["):]) if "[" in out else json.loads(out)
    except Exception:
        print(out[-1500:], r.stderr[-500:]); fail("could not read detector output")
    findings = data if isinstance(data, list) else data.get("findings", [])
    allowed = set(json.load(open(os.path.join(os.path.dirname(__file__), "detect_allow.json")))) if os.path.exists(os.path.join(os.path.dirname(__file__), "detect_allow.json")) else set()
    left = [f for f in findings if (f.get("rule") or f.get("id") or f.get("antipattern")) not in allowed]
    for f in findings: print("-", json.dumps(f)[:300])
    if left: fail(f"{len(left)} detector finding(s) not named in detect_allow.json")
    print("DETECT_OK")


def form():
    s = open(INDEX).read()
    for need in ['id="f-name"', 'id="f-email"', 'id="f-msg"', 'formsubmit.co/ajax/life22watch@gmail.com', 'action="https://formsubmit.co/life22watch@gmail.com"', 'name="_honey"']:
        if need not in s: fail("form is missing " + need)
    def run(b, url):
        pg = b.new_page(viewport={"width": 390, "height": 844})
        sent = []
        def handler(route):
            sent.append(route.request.post_data)
            route.fulfill(status=200, content_type="application/json", body='{"success":"true","message":"ok"}') if not os.environ.get("FAILMODE") else route.fulfill(status=500, body="{}")
        pg.route("https://formsubmit.co/**", handler)
        pg.goto(url, wait_until="load", timeout=60000); pg.wait_for_timeout(800)
        pg.click("#f-send"); pg.wait_for_timeout(200)
        if "fill in" not in pg.inner_text("#f-status"): fail("empty form shows no error")
        pg.fill("#f-name", "Test"); pg.fill("#f-email", "not-an-email"); pg.fill("#f-msg", "hello")
        pg.click("#f-send"); pg.wait_for_timeout(200)
        if "email" not in pg.inner_text("#f-status").lower(): fail("bad email shows no error")
        pg.fill("#f-email", "test@example.com"); pg.click("#f-send"); pg.wait_for_timeout(1500)
        if not sent: fail("nothing was posted")
        if not pg.is_visible("#f-done"): fail("success state not shown")
        body = json.loads(sent[0])
        if body.get("email") != "test@example.com" or body.get("message") != "hello": fail("posted body wrong: " + sent[0])
        pg2 = b.new_page(viewport={"width": 390, "height": 844})
        pg2.route("https://formsubmit.co/**", lambda r: r.fulfill(status=500, body="{}"))
        pg2.goto(url, wait_until="load", timeout=60000); pg2.wait_for_timeout(800)
        pg2.fill("#f-name", "Test"); pg2.fill("#f-email", "test@example.com"); pg2.fill("#f-msg", "hello")
        pg2.click("#f-send"); pg2.wait_for_timeout(1200)
        if "didn't send" not in pg2.inner_text("#f-status"): fail("server error shows no error message")
        if pg2.is_disabled("#f-send"): fail("button stays disabled after an error")
        print("FORM_OK")
    browser(run)


def live():
    import urllib.request
    s = urllib.request.urlopen("https://focusfiyah.github.io/?v=" + str(os.getpid()), timeout=30).read().decode()
    local = open(INDEX).read()
    if "<title>Ralph, AI Consultant</title>" not in s: fail("live page is not this site")
    if s.strip() != local.strip(): fail("live page differs from the local index.html (not deployed yet?)")
    print("LIVE_OK")


def shots():
    os.makedirs(SHOTS, exist_ok=True)
    def run(b, url):
        for w, h, tag in [(390, 844, "phone"), (1440, 900, "desktop")]:
            for rm in ["no-preference", "reduce"]:
                pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2 if w < 500 else 1, reduced_motion=rm)
                pg.goto(url, wait_until="load", timeout=60000); pg.wait_for_timeout(1500)
                pg.evaluate("Promise.all([...document.querySelectorAll('video')].map(v=>{if(v.dataset.src&&!v.src)v.src=v.dataset.src;return new Promise(r=>{if(v.readyState>=2)r();else{v.addEventListener('loadeddata',r,{once:true});setTimeout(r,3000)}})}))")
                pg.wait_for_timeout(500)
                suffix = "" if rm == "no-preference" else "_reduced"
                pg.screenshot(path=f"{SHOTS}/{tag}{suffix}.png", full_page=True)
                pg.screenshot(path=f"{SHOTS}/{tag}_first{suffix}.png")
                pg.close()
        print("SHOTS_OK", SHOTS)
    browser(run)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "all":
        for c in [render, hero, privacy, media, copy, motion, detect, form]:
            print("==", c.__name__);
            try: c()
            except SystemExit as e:
                if e.code: print("(continuing)")
    else:
        globals()[cmd]()
