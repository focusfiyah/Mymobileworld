"""Round 4 gate checks for the Always Answered page (GATES_r4.md). Usage: python3 check.py <words|order|plans|bf|banned|graphics|blue|render|all>
render also writes screenshots to SHOTS (phone + desktop, full page, plus reduced-motion and JS-off phone renders)."""
import re, sys, pathlib

PAGE = pathlib.Path("/home/user/always-answered/index.html")
SHOTS = pathlib.Path("/tmp/claude-0/-home-user/5e4b75d3-d0bb-5b18-89a3-48c2214c7dd3/scratchpad/r4")
H = PAGE.read_text()


def visible_text(h):
    b = h[h.index("<body"):]
    b = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", b, flags=re.S)
    return re.sub(r"\s+", " ", html_unescape(re.sub(r"<[^>]+>", " ", b))).strip()


def html_unescape(s):
    import html
    return html.unescape(s)


def words():
    n = len(visible_text(H).split())
    print("WORDS_OK" if n <= 400 else "WORDS_OVER", n)


def order():
    t = visible_text(H)
    i, j = t.find("44%"), t.find("Every call answered")
    k = t.find("Almost half the calls")
    print("STATS_FIRST" if 0 <= k < j and 0 <= i < j else "NOT_FIRST", k, i, j)


def plans():
    t = visible_text(H)
    need = ["$197", "$397", "$597", "$297", "$497", "Most popular", "$0.25", "Calls Only", "Front Desk", "Pro"]
    miss = [x for x in need if x not in t]
    pop = re.search(r'class="plan pop"><span class="badge">Most popular</span><h3>Front Desk', H)
    print("PLANS_OK" if not miss and pop else "PLANS_BAD", miss, bool(pop))


def bf():
    t = visible_text(H)
    need = ["Black Friday", "Half off the setup fee", "testimonial", "November 30"]
    miss = [x for x in need if x not in t]
    print("BF_OK" if not miss else "BF_BAD", miss)


def banned():
    t = visible_text(H).lower()
    bad = [w for w in ["one plan", "founding", "first 3 businesses", "14 days free", "first 14 days", "freeport", "baldwin",
                       "we're new", "brand new business", "just launched", "what a missed call costs you"] if w in t]
    kicker = re.findall(r'class="(?:kick|since|eyebrow)"', H)
    print("WORDING_OK" if not bad and not kicker else "WORDING_BAD", bad, kicker)


def graphics():
    img = re.findall(r'<img [^>]*alt="([^"]{20,})"', H)
    symbols = len(re.findall(r"<symbol ", H))
    marks = H.count('class="mark"')
    dots = re.search(r'<div class="dots"[^>]*>(.*?)</div>', H, re.S).group(1)
    missed, total = dots.count('<i class="m">'), dots.count("<i")
    ok = img and symbols >= 8 and marks >= 1 and missed == 44 and total == 100
    print("GRAPHICS_OK" if ok else "GRAPHICS_BAD", len(img), symbols, marks, missed, total)


def blue():
    h = H.lower()
    print("BLUE_OK" if "#1f4fd8" in h and "#0b1e5b" in h else "BLUE_BAD")


def render():
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(parents=True, exist_ok=True)
    probs = []
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        for w, h, tag in ((390, 844, "phone"), (1440, 900, "desk")):
            for mode in ("normal", "reduce", "nojs"):
                ctx = br.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce" if mode == "reduce" else "no-preference",
                                     java_script_enabled=mode != "nojs", device_scale_factor=2 if tag == "phone" else 1)
                pg = ctx.new_page()
                errs = []
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                pg.on("pageerror", lambda ex: errs.append(str(ex)))
                pg.goto(PAGE.as_uri(), wait_until="networkidle")
                if mode == "normal":
                    gs = pg.evaluate("!!(window.gsap && window.ScrollTrigger)")
                    if not gs:
                        probs.append(f"{tag}: GSAP did not load")
                    # scroll through so the scroll moment plays, then come back
                    for y in range(0, pg.evaluate("document.body.scrollHeight"), 300):
                        pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(60)
                    pg.wait_for_timeout(1800)
                    pg.evaluate("window.scrollTo(0,0)")
                sw = pg.evaluate("document.documentElement.scrollWidth")
                if sw > w:
                    probs.append(f"{tag}/{mode}: side scroll {sw}>{w}")
                op = pg.evaluate("[...document.querySelectorAll('.note')].map(n=>+getComputedStyle(n).opacity)")
                if min(op) < 0.99:
                    probs.append(f"{tag}/{mode}: notes not fully visible {op}")
                fonts = pg.evaluate("document.fonts.check('1em \"DM Serif Display\"')") if mode != "nojs" else True
                if not fonts:
                    probs.append(f"{tag}/{mode}: DM Serif Display not loaded")
                if errs:
                    probs.append(f"{tag}/{mode}: console {errs[:3]}")
                if mode == "normal" or tag == "phone":
                    pg.screenshot(path=str(SHOTS / f"{tag}_{mode}.png"), full_page=True)
                ctx.close()
        br.close()
    print("RENDER_OK" if not probs else "RENDER_BAD", probs)


FINAL_JS = """() => {
  const miss = [...document.querySelectorAll('.dots i')].filter(d => getComputedStyle(d).backgroundColor === 'rgb(255, 138, 107)').length;
  const nums = [...document.querySelectorAll('[data-count]')].map(e => e.textContent.trim());
  const op = s => Math.min(...[...document.querySelectorAll(s)].map(n => +getComputedStyle(n).opacity));
  const draw = getComputedStyle(document.querySelector('.steps')).getPropertyValue('--draw').trim();
  const tr = [...document.querySelectorAll('.steps li > .ic, .msg .stars .ic, .note .mark')].map(n => getComputedStyle(n).transform).filter(x => x !== 'none' && x !== 'matrix(1, 0, 0, 1, 0, 0)');
  return {miss, nums, notes: op('.note'), stars: op('.msg .stars .ic'), terms: op('.cost .term, .cost .op'), draw, tr};
}"""


def final():
    from playwright.sync_api import sync_playwright
    probs = []
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        for w, h in ((390, 844), (1440, 900)):
            for mode in ("normal", "reduce", "nojs"):
                ctx = br.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce" if mode == "reduce" else "no-preference",
                                     java_script_enabled=mode != "nojs")
                pg = ctx.new_page()
                pg.goto(PAGE.as_uri(), wait_until="networkidle")
                if mode == "normal":
                    for y in range(0, pg.evaluate("document.body.scrollHeight"), 250):
                        pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(80)
                    pg.wait_for_timeout(2500)
                r = pg.evaluate(FINAL_JS)
                ok = (r["miss"] == 44 and r["nums"] == ["44%", "$3,900"] and min(r["notes"], r["stars"], r["terms"]) >= 0.99
                      and r["draw"] == "1" and not r["tr"])
                if not ok:
                    probs.append((w, mode, r))
                ctx.close()
        br.close()
    print("FINAL_OK" if not probs else "FINAL_BAD", probs)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    fns = dict(final=final, words=words, order=order, plans=plans, bf=bf, banned=banned, graphics=graphics, blue=blue, render=render)
    for k in (fns if cmd == "all" else [cmd]):
        fns[k]()
