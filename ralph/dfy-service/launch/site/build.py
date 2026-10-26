"""Wrap page.html (the Artifact preview fragment) into a standalone index.html for hosting. Usage: python3 build.py"""
import pathlib
here = pathlib.Path(__file__).parent
frag = (here / "page.html").read_text()
head_end = frag.index("</style>") + len("</style>")
head, body = frag[:head_end], frag[head_end:]
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
       'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
       + head + "\n</head>\n<body>" + body + "</body>\n</html>\n")
(here / "index.html").write_text(doc)
print("BUILT", len(doc))
