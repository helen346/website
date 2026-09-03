#!/usr/bin/env python3
"""Assemble the static pages from src/pages/*.html and src/layout.html.

Usage:  python3 tools/build.py
Each page file starts with a small front-matter block:
    ---
    title: Services
    description: ...
    path: /services/
    ---
followed by the page body HTML. Output goes to the repository root as
index.html, services/index.html, etc. so the site can be hosted anywhere.
"""
import re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
layout = (SRC / "layout.html").read_text()
wordmark = (SRC / "wordmark-inline.svg").read_text().strip()
stacked = (SRC / "stacked-inline.svg").read_text().strip()

SITE = "https://imaginationpr.co.uk"

def render(page: pathlib.Path):
    text = page.read_text()
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    meta = dict(line.split(":", 1) for line in m.group(1).splitlines())
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    body = m.group(2)
    path = meta["path"]
    out = ROOT / (path.strip("/") + "/index.html" if path != "/" else "index.html")
    html = layout
    for key, val in {
        "title": meta["title"],
        "description": meta["description"],
        "canonical": SITE + path,
        "body": body,
        "wordmark": wordmark,
        "stacked": stacked,
        "nav_current": path,
        "year": str(datetime.date.today().year),
        "body_class": meta.get("class", ""),
    }.items():
        html = html.replace("{{" + key + "}}", val)
    # mark the current nav link
    html = re.sub(r'(<a class="nav-link" href="%s")' % re.escape(path), r'\1 aria-current="page"', html)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("wrote", out.relative_to(ROOT))

for page in sorted((SRC / "pages").glob("*.html")):
    render(page)
