#!/usr/bin/env python3
"""rebrand-check — the built site names the product «APS Conecta Gestión», nowhere «Nextcloud».

Reads every page of _build/html as a reader sees it and fails on any «Nextcloud» outside the
places the rename rule leaves alone: code (<code>, <pre>), scripts and styles, attribution lines
(class `atribucion`), the legal and product names upstream.yml `rename.keep` lists, and the
pages `rename.exempt_pages` names. Proves _ext/rebrand.py from the outside, so a page that
bypasses the transform (a template, a generator writing raw HTML) is caught too.

    python3 tools/rebrand-check.py [html_dir]
"""
from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstreamlib as u  # noqa: E402

SKIP_TAGS = {"code", "pre", "script", "style", "kbd", "samp"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.text = [], []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        classes = (dict(attrs).get("class") or "").split()
        self.stack.append(tag in SKIP_TAGS or "atribucion" in classes)

    def handle_endtag(self, tag):
        if tag not in VOID and self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if not any(self.stack):
            self.text.append(data)


def visible_text(html: str) -> str:
    r = Reader()
    r.feed(html)
    return " ".join(r.text)


def main(argv: list[str]) -> int:
    site = Path(argv[0]) if argv else u.ROOT / "_build" / "html"
    cfg = u.config()
    exempt = {f"{p}.html" for p in cfg["rename"]["exempt_pages"]}
    found = 0
    for page in sorted(site.rglob("*.html")):
        rel = page.relative_to(site).as_posix()
        if rel in exempt or rel.startswith(("_static/", "_sources/")) or rel in ("genindex.html", "search.html"):
            continue
        for hit in u.leftovers(visible_text(page.read_text(encoding="utf-8", errors="replace")), cfg):
            print(f"ERROR {rel}: «…{' '.join(hit.split())}…»")
            found += 1
    print(f"[rebrand-check] {found} leftover(s)")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
