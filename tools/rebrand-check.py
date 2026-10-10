#!/usr/bin/env python3
"""rebrand-check — the built site names the product «APS Conecta Gestión», nowhere «Nextcloud».

Reads every page of _build/html as a reader sees it and fails on any «Nextcloud» outside the
places the rename rule leaves alone: code (<code>, <pre>), scripts and styles, attribution lines
(class `atribucion`), the vendor ({vendor} role, links to `rename.keep_hosts`), the legal and
product names upstream.yml `rename.keep` lists, and the pages `rename.exempt_pages` names. Also
fails on a store client (desktop, Android, iOS) named as the product: client_problems.
Proves _ext/rebrand.py from the outside, so a page that bypasses the transform (a template, a
generator writing raw HTML) is caught too.

    python3 tools/rebrand-check.py [html_dir]
"""
from __future__ import annotations

import html as htmllib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstreamlib as u  # noqa: E402

SKIP_TAGS = {"code", "pre", "script", "style", "kbd", "samp"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Reader(HTMLParser):
    """Collects visible text outside skipped contexts. A link INTO an exempt page (the legal
    notice) is skipped too: the navigation repeats that page's headings, which name the origin.
    So is a link whose text is its own URL (an autolink)."""

    def __init__(self, exempt: tuple[str, ...] = (), cfg: dict | None = None):
        super().__init__(convert_charrefs=True)
        self.stack, self.text, self.exempt, self.cfg = [], [], exempt, cfg
        self.hrefs: list[str | None] = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        attrs = dict(attrs)
        classes = (attrs.get("class") or "").split()
        href = (attrs.get("href") or "").split("#", 1)[0]
        into_exempt = tag == "a" and any(href.endswith(e) for e in self.exempt)
        vendor = "vendor" in classes or (tag == "a" and u.vendor_link(attrs.get("href") or "", self.cfg))
        self.stack.append(tag in SKIP_TAGS or "atribucion" in classes or into_exempt or vendor)
        self.hrefs.append(attrs.get("href") if tag == "a" else None)

    def handle_endtag(self, tag):
        if tag not in VOID and self.stack:
            self.stack.pop()
            self.hrefs.pop()

    def handle_data(self, data):
        # an autolink shows its own URL: URL text, which the build never renames (rebrand.py)
        if not any(self.stack) and not (self.hrefs and self.hrefs[-1] == data.strip()):
            self.text.append(data)


def visible_text(html: str, exempt: tuple[str, ...] = (), cfg: dict | None = None,
                 titles: set[str] = frozenset()) -> str:
    r = Reader(exempt, cfg)
    r.feed(html)
    text = " ".join(" ".join(r.text).split())
    for t in titles:  # plain copies of a vendor title (vendor_titles)
        text = text.replace(t, " ")
    return text


def vendor_titles(pages: list[str]) -> set[str]:
    """Page titles whose h1 marks «Nextcloud» as the vendor ({vendor}`Nextcloud`): Sphinx copies a
    title into <title> and every toctree entry as plain text, so those copies lose the mark."""
    out = set()
    for html in pages:
        m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        if m and 'class="vendor"' in m.group(1):
            inner = re.sub(r'<a class="headerlink".*?</a>', "", m.group(1), flags=re.S)
            out.add(" ".join(htmllib.unescape(re.sub(r"<[^>]+>", "", inner)).split()))
    return out



def client_problems(text: str, cfg: dict) -> list[str]:
    """A store client named as the product: «el cliente de escritorio de APS Conecta Gestión». The
    desktop, Android and iOS clients ship as «Nextcloud», so the source writes {vendor}`Nextcloud`
    (owner, 2026-10-10, documentation#136). HTTP and web clients, accounts and platform libraries
    are the product itself and keep the rename."""
    product = re.escape(cfg["rename"]["to"])
    gap = r"((?:\s+(?!cuenta\b|web\b|HTTP\b)[^\s.;:]+){0,4}?)"
    client = re.compile(r"\b(?:clientes?|aplicaci[oó]n(?:es)? m[oó]vil(?:es)?)\b(?!\s+(?:HTTP|web)\b)" + gap + r"\s+de " + product)
    library = re.compile(r"\bbibliotecas? de (?:Android|iOS) de " + product)
    return [m.group(0) for pat in (client, library) for m in pat.finditer(text)]


def main(argv: list[str]) -> int:
    site = Path(argv[0]) if argv else u.ROOT / "_build" / "html"
    cfg = u.config()
    exempt = {f"{p}.html" for p in cfg["rename"]["exempt_pages"]}
    found = 0
    pages = {}
    for page in sorted(site.rglob("*.html")):
        rel = page.relative_to(site).as_posix()
        if rel in exempt or rel.startswith(("_static/", "_sources/")) or rel in ("genindex.html", "search.html"):
            continue
        pages[rel] = page.read_text(encoding="utf-8", errors="replace")
    titles = vendor_titles(list(pages.values()))
    for rel, html in pages.items():
        text = visible_text(html, tuple(sorted(exempt)), cfg, titles)
        for hit in u.leftovers(text, cfg):
            print(f"ERROR {rel}: «…{' '.join(hit.split())}…»")
            found += 1
        for hit in client_problems(text, cfg):
            print(f"ERROR {rel}: «{hit}» — a store client keeps {{vendor}}`Nextcloud`")
            found += 1
    print(f"[rebrand-check] {found} leftover(s)")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
