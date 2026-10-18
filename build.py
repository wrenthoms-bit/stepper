#!/usr/bin/env python3
"""Wrap stepper.html (artifact-style fragment) into a standalone index.html for GitHub Pages."""
src = open("stepper.fragment.html", encoding="utf-8").read()
cut = src.index("</style>") + len("</style>")
head, body = src[:cut], src[cut:]
reset = (":root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
         "body{margin:0;font:14px system-ui,-apple-system,sans-serif}img{max-width:100%}[hidden]{display:none!important}")
out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>{reset}</style>
{head.strip()}
</head>
<body>
{body.strip()}
</body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(out)
print("index.html", len(out), "bytes")
