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
#   theme     .wy-nav-side computes rgb(83, 21, 168); aps-brand.css declares
#             color-scheme: light; zero prefers-color-scheme in any served CSS
#             every request the load issued resolves to the serving host
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

SIDEBAR_RGB = "rgb(83, 21, 168)"  # #5315a8 — the .wy-nav-side backdrop in aps-brand.css
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
        description="Playwright gate on the served site: docs/brand/fonts/theme/isolation families."
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

            # theme: brand backdrop applied, light color-scheme declared, no dark-mode media.
            errs = []
            sidebar = page.evaluate(
                """() => {
                    const el = document.querySelector('.wy-nav-side');
                    return el ? getComputedStyle(el).backgroundColor : null;
                }"""
            )
            if sidebar is None:
                errs.append("no .wy-nav-side element — the theme sheet did not apply")
            elif sidebar != SIDEBAR_RGB:
                errs.append(f".wy-nav-side background is {sidebar}, expected {SIDEBAR_RGB}")
            css_urls = set(page.evaluate(
                """() => Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
                          .map(l => l.href)"""
            ))
            brand_css_url = urljoin(static_base, BRAND_CSS)
            css_urls.add(brand_css_url)
            served = {}
            for url in sorted(css_urls):
                resp = context.request.get(url)
                served[url] = resp.text() if resp.ok else None
                if not resp.ok:
                    errs.append(f"{url} -> HTTP {resp.status}")
            brand_css = served.get(brand_css_url) or ""
            if not re.search(r"color-scheme:\s*light", brand_css):
                errs.append(f"{BRAND_CSS} does not declare color-scheme: light")
            for url, text in served.items():
                if text and "prefers-color-scheme" in text:
                    errs.append(f"prefers-color-scheme present in {url}")
            check_family("theme", errs)

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
