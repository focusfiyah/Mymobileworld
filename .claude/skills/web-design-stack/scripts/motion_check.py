#!/usr/bin/env python3
"""Motion budget check for a page or project: prints MOTION_OK, or the problems and exits 1.

Usage: python3 motion_check.py PATH [--scroll-max 2] [--tween-max 12]

Errors (fail): more scroll-driven GSAP effects than --scroll-max; animation without a
prefers-reduced-motion path; `transition: all` / Tailwind `transition-all`; `will-change: all`.
Warnings (listed, do not fail): infinite loops, elastic/bounce eases, press scale under 0.95,
more GSAP tweens than --tween-max. Reads .html .css .scss .js .mjs .jsx .ts .tsx .vue .svelte,
skipping node_modules, dist, build, .git and minified files.
"""
import argparse, pathlib, re, sys

EXT = {".html", ".htm", ".css", ".scss", ".js", ".mjs", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro"}
SKIP = {"node_modules", "dist", "build", ".git", ".next", ".impeccable"}

def files(root):
    p = pathlib.Path(root)
    if p.is_file():
        return [p]
    return [f for f in p.rglob("*") if f.suffix in EXT and not SKIP & set(f.parts) and ".min." not in f.name]

def strip_comments(t):
    return re.sub(r"/\*.*?\*/|<!--.*?-->", "", t, flags=re.S)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--scroll-max", type=int, default=2)
    ap.add_argument("--tween-max", type=int, default=12)
    a = ap.parse_args()
    errors, warns = [], []
    scroll = tweens = 0
    animates = reduced = False
    for f in files(a.path):
        t = strip_comments(f.read_text(errors="ignore"))
        n = len(re.findall(r"scrollTrigger\s*:", t)) + len(re.findall(r"ScrollTrigger\.create\s*\(", t)) \
            + len(re.findall(r"ScrollSmoother\.create\s*\(", t))
        scroll += n
        tw = len(re.findall(r"\b(?:gsap|tl|timeline)\s*\.\s*(?:to|from|fromTo)\s*\(", t))
        tweens += tw
        if n or tw or re.search(r"@keyframes|animation\s*:|transition\s*:|\btransition-\w|gsap\.", t):
            animates = True
        if re.search(r"prefers-reduced-motion|motion-reduce:|useReducedMotion", t):
            reduced = True
        for m in re.finditer(r"transition\s*:\s*all\b|\btransition-all\b", t):
            errors.append(f"{f}: `{m.group(0)}`: name the properties instead (polish/GUIDE.md #14)")
        if re.search(r"will-change\s*:\s*all", t):
            errors.append(f"{f}: `will-change: all` (polish/GUIDE.md #15)")
        for m in re.finditer(r"[\w.-]*\s*\{[^{}]*animation[^{}]*infinite[^{}]*\}|repeat\s*:\s*-1", t):
            if not re.search(r"load|spin|shimmer|skeleton|pulse|progress", m.group(0), re.I):
                warns.append(f"{f}: endless loop outside a loader: {m.group(0)[:60]!r}")
        for m in re.finditer(r"ease\s*:\s*['\"](?:elastic|bounce|back)[^'\"]*['\"]", t):
            warns.append(f"{f}: {m.group(0)}: no bounce/elastic by reflex (impeccable animate.md)")
        for m in re.finditer(r"scale\(\s*0?\.(\d+)\s*\)|scale-\[0?\.(\d+)\]", t):
            v = float("0." + (m.group(1) or m.group(2)))
            if 0.5 < v < 0.95 and re.search(r":active|active:", t[max(0, m.start() - 120):m.start()]):
                warns.append(f"{f}: press scale {v}: use 0.96 (polish/GUIDE.md #12)")
    if scroll > a.scroll_max:
        errors.append(f"{scroll} scroll-driven effects; budget is {a.scroll_max}: keep the one authored moment")
    if animates and not reduced:
        errors.append("motion found but no prefers-reduced-motion path (CSS media query or gsap.matchMedia)")
    if tweens > a.tween_max:
        warns.append(f"{tweens} GSAP tweens; budget hint is {a.tween_max}: is every one earning its place?")
    print(f"scroll-driven: {scroll}/{a.scroll_max}  gsap tweens: {tweens}  reduced-motion path: {reduced}")
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    if errors:
        sys.exit(1)
    print("MOTION_OK")

if __name__ == "__main__":
    main()
