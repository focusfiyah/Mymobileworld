"""python3 captions_check.py FILE -> CAPTIONS_OK when the 4 sections exist, 5 hooks + 5 captions, hashtags present, no dashes, no $ or price numbers (ctw weights allowed), never diamond or solid gold."""
import re, sys
t = open(sys.argv[1]).read(); e = []
for s in ["Text overlay hook options", "Video caption options", "SEO phrases", "Hashtags"]:
    if s not in t: e.append("missing " + s)
sec = lambda a, b: t.split(a)[1].split(b)[0] if a in t and b in t else ""
if len(re.findall(r"(?m)^\d\. ", sec("Text overlay hook options", "Video caption options"))) < 5: e.append("hooks<5")
if len(re.findall(r"(?m)^\d\. ", sec("Video caption options", "SEO phrases"))) < 5: e.append("captions<5")
if len(re.findall(r"#\w+", t)) < 5: e.append("hashtags<5")
if re.search(r"[–—]| - ", t): e.append("dash")
if re.search(r"\$|\d+\s*(dollars|bucks)|\d+\.\d\d(?!\s*ctw)", t): e.append("price")
if re.search(r"diamond|solid gold|real gold", t.split("Notes for Grace")[0], re.I): e.append("diamond/solid gold claim")
print("FAIL " + "; ".join(e) if e else "CAPTIONS_OK"); sys.exit(1 if e else 0)
