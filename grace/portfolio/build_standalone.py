"""Build Grace's portfolio as a standalone site for Netlify (no Claude wrapper).
Source stays site/index.html (the Artifact version). Writes dist/: index.html with a full head, and only the media it uses.
Run: python3 build_standalone.py"""
import re, shutil, pathlib
here = pathlib.Path(__file__).parent; src = here / "site"; out = here / "dist"
shutil.rmtree(out, ignore_errors=True); (out / "media").mkdir(parents=True)
html = (src / "index.html").read_text()
html = re.sub(r'<meta name="claude:[^>]*>\n?', "", html)
html = html.replace("// captions ship inline (artifacts do not serve .vtt files)", "// captions ship inline")
title = re.search(r"<title>(.*?)</title>", html).group(1)
html = html.replace(f"<title>{title}</title>", "", 1)
desc = "Grace With The Glow: New York-based UGC and TikTok Shop creator. See her videos and send your brief."
head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} | UGC Creator">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="media/photo-hero-v2.jpg">
<meta property="og:type" content="website">
<style>[hidden]{{display:none!important}}</style>
"""
body_start = html.find("<body")
if body_start == -1:
    # Artifact source has no <body>: everything before the first section-level tag is head content
    m = re.search(r"</style>\s*", html); cut = m.end()
    html = head + html[:cut] + "</head>\n<body>\n" + html[cut:] + "\n</body>\n</html>\n"
else:
    html = head + html
(out / "index.html").write_text(html)
used = set(re.findall(r"media/([A-Za-z0-9._-]+\.(?:jpg|png|mp4))", html))
ids = set(re.findall(r"\b(7\d{18})\b", html))
used |= {f"{i}.mp4" for i in ids} | {f"{i}.jpg" for i in ids}
for f in sorted(used):
    shutil.copy2(src / "media" / f, out / "media" / f)
print(len(used), "media files,", sum((out/'media'/f).stat().st_size for f in used)//1_000_000, "MB")
