"""End-to-end test of the Shot Cam page in headless Chromium with a fake camera.

Serves tools/shotcam/site on localhost, opens the sample list at phone size, records one
take of shot 1, keeps it, and checks the take is stored, named by shot, and that the page
never scrolls sideways. Prints SHOTCAM_TEST_OK only when every check passes.
Run: python3 tools/shotcam/test_shotcam.py
"""
import functools, http.server, os, socketserver, sys, threading

from playwright.sync_api import sync_playwright

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    h = functools.partial(Quiet, directory=SITE)
    srv = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

# Netlify's free plan pins a "Powered by Netlify" badge at the bottom right (about 170x40 px,
# Ralph's OnePlus 2026-11-11). No button may sit in that corner on any screen.
BADGE_JS = """() => {
  const zone = {l: innerWidth - 200, t: innerHeight - 64, r: innerWidth, b: innerHeight};
  return [...document.querySelectorAll('button')].filter(b => b.offsetParent !== null).map(b => {
    const r = b.getBoundingClientRect();
    return (r.right > zone.l && r.left < zone.r && r.bottom > zone.t && r.top < zone.b) ? (b.id || b.textContent.trim()) : null;
  }).filter(Boolean);
}"""


def badge_clear(pg, screen, fails):
    hit = pg.evaluate(BADGE_JS)
    if hit:
        fails.append(f"{screen}: buttons under the Netlify badge corner: {hit}")


def main():
    srv = serve()
    url = f"http://127.0.0.1:{srv.server_address[1]}/?list=sample"
    fails = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("SHOTCAM_CHROME", "/opt/pw-browsers/chromium"), args=["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream", "--autoplay-policy=no-user-gesture-required"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True,
                            permissions=["camera", "microphone"])
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(url)
        pg.wait_for_selector(".shot")
        n_shots = pg.locator(".shot").count()
        if n_shots != 3:
            fails.append(f"expected 3 shots in the sample list, saw {n_shots}")
        if pg.evaluate("document.documentElement.scrollWidth > innerWidth"):
            fails.append("list view scrolls sideways")
        badge_clear(pg, "list", fails)
        pg.locator(".shot").first.click()
        pg.wait_for_function("document.getElementById('preview').videoWidth > 0", timeout=10000)
        card = pg.text_content("#cardK")
        if card != "Shot 1 of 3":
            fails.append(f"card shows {card!r}")
        badge_clear(pg, "camera", fails)
        pg.click("#recBtn")
        pg.wait_for_selector("#countdown:not([hidden])", timeout=2000)
        pg.wait_for_function("window.__shotcam.state().recording", timeout=6000)
        pg.wait_for_timeout(2200)
        pg.click("#recBtn")
        pg.wait_for_selector("#reviewView:not([hidden])", timeout=8000)
        meta = pg.inner_text("#reviewMeta")
        badge_clear(pg, "review", fails)
        pg.click("#keepBtn")
        pg.wait_for_selector("#camView:not([hidden])")
        pg.wait_for_timeout(400)
        nxt = pg.text_content("#cardK")
        if nxt != "Shot 2 of 3":
            fails.append(f"after keep, card shows {nxt!r} (should move to shot 2)")
        pg.click("#backBtn")
        pg.wait_for_selector("#listView:not([hidden])")
        pg.wait_for_selector(".shot.done")
        takes = pg.evaluate("window.__shotcam.allTakes().then(t => t.map(x => ({name: x.name, size: x.size, n: x.n})))")
        if len(takes) != 1 or takes[0]["n"] != 1:
            fails.append(f"stored takes wrong: {takes}")
        elif not takes[0]["name"].startswith("shotcam-test S01 take1") or takes[0]["size"] < 20000:
            fails.append(f"take name/size wrong: {takes[0]}")
        pg.click("#sendBtn")
        pg.wait_for_selector("#sendView:not([hidden])")
        rows = pg.locator(".take").count()
        if rows != 1:
            fails.append(f"send screen lists {rows} takes")
        badge_clear(pg, "send", fails)
        for v in ("#sendView",):
            if pg.evaluate("document.documentElement.scrollWidth > innerWidth"):
                fails.append(f"{v} scrolls sideways")
        if os.environ.get("SHOTCAM_SHOT"):
            pg.screenshot(path=os.environ["SHOTCAM_SHOT"])
        if errs:
            fails.append("page errors: " + "; ".join(errs))
        b.close()
    srv.shutdown()
    print("review:", meta)
    print("takes:", takes)
    if fails:
        print("FAILED:\n- " + "\n- ".join(fails))
        sys.exit(1)
    print("SHOTCAM_TEST_OK")


if __name__ == "__main__":
    main()
