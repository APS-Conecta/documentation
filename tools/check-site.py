#!/usr/bin/env python3
# check-site — the c10 Playwright gate on served HTML.
#
# Serves the built site at a /documentation/ subpath (stylesheet-relative assets
# must survive the real base URL https://aps-conecta.github.io/documentation/),
# then asserts five families. --url skips the local server and reuses the same
# assertions against a deployed site (the owner's post-merge check).
#
# families, evaluated in order; exit 1 names the first failed family:
#   docs      documentElement.lang == 'es'; a visible Spanish <h1>; <link rel="icon">
#   brand     HTTP 200 x11 under _static/ — 4 woff2 + 3 logo SVG + 4 favicon files
#             (delivery, via context.request; the page only fetches faces in use)
#   fonts     after document.fonts.ready, fonts.check('400 1em "Nunito Sans"') and
#             ('600 1em "Fraunces"') are both true, and both faces are loaded —
#             use, not just delivery (check() alone is vacuously true with no
#             @font-face declared, so the face status is asserted too)
#   theme     the Furo sidebar computes rgb(83, 21, 168); aps-brand.css declares
#             color-scheme: light; with the browser asking for dark mode the page
#             still renders light (body[data-theme="light"], white background)
#   responsive at 360x800 no page scrolls sideways (index, legal notice, catalog) and
#             the navigation drawer opens
#   search    Pagefind answers a Spanish query with the expected page, and the
#             audiencia filter narrows it
#   isolation every request the load issued resolves to the serving host
#             (127.0.0.1 locally; the deployed origin under --url) — the
#             no-third-party rule as a mechanical gate

import argparse
import functools
import os
import re
import shutil
import sys
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright

# The 11 brand assets (gestion themes/apsconecta/core — the fetch-brand contract):
# 4 variable woff2 faces + the 3 logo SVGs + the 4 favicon files.
BRAND_ASSETS = (
    "fonts/Fraunces.woff2",
    "fonts/Fraunces-Italic.woff2",
    "fonts/NunitoSans.woff2",
    "fonts/NunitoSans-Italic.woff2",
    "img/logo/logo.svg",
    "img/logo/logo-mark.svg",
    "img/logo/logo-header.svg",
    "img/favicon.svg",
    "img/favicon.ico",
    "img/favicon-mask.svg",
    "img/favicon-touch.png",
)

SIDEBAR_RGB = "rgb(83, 21, 168)"  # #5315a8 — Furo's --color-sidebar-background (conf.py)
NARROW_PAGES = ("", "aviso.html", "_generated/catalogo.html")
SEARCH_QUERY, SEARCH_EXPECT, SEARCH_FILTER = "vademécum", "usuario/farmacia", "usuario"
BRAND_CSS = "css/aps-brand.css"


class QuietHandler(SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler with the per-request log line silenced —
    the family lines are the output contract, not the access log."""

    def log_message(self, format, *args):
        pass


# "Reads as Spanish": an accented letter or a Spanish function word.
SPANISH_RE = re.compile(r"[áéíóúñÁÉÍÓÚÑ]|\b(?:de|del|la|el|y|en|para|con)\b", re.IGNORECASE)


def check_family(name, errors):
    """Report one family; exit 1 naming it on the first failure."""
    if errors:
        print(f"check-site: family '{name}' FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    print(f"check-site: {name} ok")


def serve(root, base):
    """Serve root under a /<base>/ subpath on a free loopback port.

    The symlink layout reproduces the deployed /documentation/ subpath, so
    stylesheet-relative asset URLs resolve the way they will in production.
    """
    serve_dir = tempfile.mkdtemp(prefix="check-site-")
    os.symlink(os.path.abspath(root), os.path.join(serve_dir, base))
    handler = functools.partial(QuietHandler, directory=serve_dir)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}/{base}/", serve_dir


def main():
    ap = argparse.ArgumentParser(
        description="Playwright gate on the served site: docs/brand/fonts/theme/responsive/search/isolation."
    )
    ap.add_argument("--root", default="_build/html",
                    help="built site root (default: %(default)s)")
    ap.add_argument("--base", default="documentation",
                    help="subpath name the site is served under (default: %(default)s)")
    ap.add_argument("--url", default=None,
                    help="skip the local server; run the same assertions against this deployed base URL")
    args = ap.parse_args()

    serve_dir = None
    httpd = None
    if args.url:
        base_url = args.url if args.url.endswith("/") else args.url + "/"
    else:
        if not os.path.isdir(args.root):
            print(f"check-site: build root '{args.root}' does not exist — run make html first",
                  file=sys.stderr)
            return 1
        httpd, base_url, serve_dir = serve(args.root, args.base)
    host = urlparse(base_url).hostname

    requests_seen = []
    try:
        with sync_playwright() as p:
            # --no-sandbox: the build-og idiom — chromium runs as root in containers
            browser = p.chromium.launch(args=["--no-sandbox"])
            context = browser.new_context()
            page = context.new_page()
            page.on("request", lambda r: requests_seen.append(r.url))
            page.goto(base_url, wait_until="networkidle")

            static_base = urljoin(base_url, "_static/")

            # docs: language, a visible Spanish <h1>, and a favicon link.
            doc = page.evaluate(
                """() => {
                    const h1 = document.querySelector('h1');
                    return {
                        lang: document.documentElement.lang || '',
                        h1: h1 ? h1.textContent.trim() : '',
                        h1Visible: !!h1 && !!(h1.offsetParent || h1.getClientRects().length),
                        icon: !!document.querySelector('link[rel~="icon"]'),
                    };
                }"""
            )
            errs = []
            if doc["lang"] != "es":
                errs.append(f"documentElement.lang is {doc['lang']!r}, expected 'es'")
            if not doc["h1"] or not doc["h1Visible"]:
                errs.append("no visible <h1> on the landing page")
            elif not SPANISH_RE.search(doc["h1"]):
                errs.append(f"<h1> {doc['h1']!r} does not read as Spanish")
            if not doc["icon"]:
                errs.append('no <link rel="icon"> on the landing page')
            check_family("docs", errs)

            # brand: all 11 assets deliver (the browser only fetches faces in use).
            errs = []
            for asset in BRAND_ASSETS:
                url = urljoin(static_base, asset)
                resp = context.request.get(url)
                if not resp.ok:
                    errs.append(f"{asset} -> HTTP {resp.status}")
                elif not resp.body():
                    errs.append(f"{asset} -> HTTP 200 but empty body")
            check_family("brand", errs)

            # fonts: the declared faces exist, loaded, and the check() calls hold
            # (check() alone is vacuously true when no @font-face is declared at all).
            fonts = page.evaluate(
                """() => document.fonts.ready.then(() => {
                    const faces = {};
                    for (const f of document.fonts) {
                        if (f.status === 'loaded') faces[f.family] = 'loaded';
                        else if (!(f.family in faces)) faces[f.family] = f.status;
                    }
                    return {
                        nunito: document.fonts.check('400 1em "Nunito Sans"'),
                        fraunces: document.fonts.check('600 1em "Fraunces"'),
                        nunitoFace: faces['Nunito Sans'] || null,
                        frauncesFace: faces['Fraunces'] || null,
                    };
                })"""
            )
            errs = []
            if not fonts["nunito"]:
                errs.append("document.fonts.check('400 1em \"Nunito Sans\"') is false after fonts.ready")
            if not fonts["fraunces"]:
                errs.append("document.fonts.check('600 1em \"Fraunces\"') is false after fonts.ready")
            if fonts["nunitoFace"] != "loaded":
                errs.append(f'no loaded "Nunito Sans" face (status: {fonts["nunitoFace"]!r})')
            if fonts["frauncesFace"] != "loaded":
                errs.append(f'no loaded "Fraunces" face (status: {fonts["frauncesFace"]!r})')
            check_family("fonts", errs)

            # theme: brand sidebar, light declared, and light even when the browser asks for dark.
            errs = []
            sidebar = page.evaluate(
                """() => {
                    const el = document.querySelector('.sidebar-drawer');
                    return el ? getComputedStyle(el).backgroundColor : null;
                }"""
            )
            if sidebar is None:
                errs.append("no .sidebar-drawer element — the Furo theme did not render")
            elif sidebar != SIDEBAR_RGB:
                errs.append(f".sidebar-drawer background is {sidebar}, expected {SIDEBAR_RGB}")
            brand_css_url = urljoin(static_base, BRAND_CSS)
            resp = context.request.get(brand_css_url)
            if not resp.ok:
                errs.append(f"{brand_css_url} -> HTTP {resp.status}")
            elif not re.search(r"color-scheme:\s*light", resp.text()):
                errs.append(f"{BRAND_CSS} does not declare color-scheme: light")
            dark = browser.new_context(color_scheme="dark")
            dpage = dark.new_page()
            dpage.goto(base_url, wait_until="networkidle")
            look = dpage.evaluate(
                """() => ({theme: document.body.dataset.theme,
                          bg: getComputedStyle(document.body).backgroundColor})"""
            )
            dark.close()
            if look["theme"] != "light":
                errs.append(f'with a dark preference body[data-theme] is {look["theme"]!r}, expected "light"')
            if look["bg"] != "rgb(255, 255, 255)":
                errs.append(f"with a dark preference the body background is {look['bg']}, expected white")
            check_family("theme", errs)

            # responsive: nothing scrolls sideways at phone width; the navigation drawer opens.
            errs = []
            narrow = browser.new_context(viewport={"width": 360, "height": 800})
            npage = narrow.new_page()
            npage.on("request", lambda r: requests_seen.append(r.url))
            for rel in NARROW_PAGES:
                npage.goto(urljoin(base_url, rel), wait_until="networkidle")
                over = npage.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
                if over > 0:
                    errs.append(f"/{rel or ''} scrolls sideways by {over}px at 360px wide")
            npage.goto(base_url, wait_until="networkidle")
            npage.click(".mobile-header label[for='__navigation']")
            npage.wait_for_timeout(400)
            left = npage.evaluate(
                "() => document.querySelector('.sidebar-drawer').getBoundingClientRect().left"
            )
            if left < 0:
                errs.append(f"the navigation drawer did not open at 360px (left edge at {left}px)")
            narrow.close()
            check_family("responsive", errs)

            # search: Pagefind answers a Spanish query, and the audiencia filter narrows it.
            errs = []
            found = page.evaluate(
                """async ([q, f]) => {
                    const pf = await import(new URL('pagefind/pagefind.js', document.baseURI
                        .replace(/[^/]*$/, '')).href);
                    await pf.init();
                    const all = await pf.search(q);
                    const narrowed = await pf.search(q, {filters: {audiencia: f}});
                    const urls = async (r) => Promise.all(r.results.slice(0, 5).map(x => x.data().then(d => d.url)));
                    return {all: await urls(all), narrowed: await urls(narrowed),
                            allCount: all.results.length, narrowedCount: narrowed.results.length};
                }""",
                [SEARCH_QUERY, SEARCH_FILTER],
            )
            if not any(SEARCH_EXPECT in u for u in found["all"]):
                errs.append(f"query {SEARCH_QUERY!r} did not return {SEARCH_EXPECT} (got {found['all']})")
            if found["narrowedCount"] == 0 or found["narrowedCount"] > found["allCount"]:
                errs.append(f"filter audiencia={SEARCH_FILTER} did not narrow ({found['narrowedCount']} of {found['allCount']})")
            if any(f"/{SEARCH_FILTER}/" not in u for u in found["narrowed"]):
                errs.append(f"filter audiencia={SEARCH_FILTER} let other audiences through: {found['narrowed']}")
            check_family("search", errs)

            # isolation: nothing the load issued left the serving host.
            errs = []
            for url in requests_seen:
                if urlparse(url).hostname != host:
                    errs.append(f"request left the serving host {host}: {url}")
                    if len(errs) >= 5:
                        errs.append("(further violations suppressed)")
                        break
            check_family("isolation", errs)

            browser.close()
    finally:
        if httpd:
            httpd.shutdown()
        if serve_dir:
            shutil.rmtree(serve_dir, ignore_errors=True)

    print(f"check-site: all families pass on {base_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
