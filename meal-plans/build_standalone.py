"""Wrap tiny-table-app.html (written as an Artifact page, no <head>) into a page that runs on its own.
Usage: python3 build_standalone.py  -> tiny-table.html (open in any browser or host it anywhere)."""
import pathlib
here = pathlib.Path(__file__).parent
src = (here / "tiny-table-app.html").read_text()
head_end = src.index("</style>") + len("</style>")          # title, font links and styles go in <head>
head, body = src[:head_end], src[head_end:]
page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#F8F8F1">
{head}
<style>
:root {{ padding-top: env(safe-area-inset-top, 0px); }}
img {{ max-width: 100%; }}
</style>
</head>
<body>
{body.strip()}
</body>
</html>
"""
(here / "tiny-table.html").write_text(page)
print("wrote tiny-table.html", len(page), "bytes")
