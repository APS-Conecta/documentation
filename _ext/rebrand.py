"""Site-wide rename: «Nextcloud» → «APS Conecta Gestión» (iniciativa scribe, Q21).

Runs on every page as it is read, before Sphinx collects titles, so page text, headings, the
navigation and the search index all carry the product's name. The rule lives in upstream.yml
(`rename`) and the text function in tools/upstreamlib.py; this module only decides WHERE it
applies. Never renamed: code (literal, literal_block), raw HTML, URL text, attribution lines
(class `atribucion`), the vendor (role `{vendor}`, link text into `rename.keep_hosts`), the
legal and product names `rename.keep` lists, and the pages `rename.exempt_pages` names — the
legal notice keeps «Nextcloud» because it explains the origin.
"""

from __future__ import annotations

import sys
from pathlib import Path

from docutils import nodes

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import upstreamlib as u  # noqa: E402

SKIP = (nodes.literal, nodes.literal_block, nodes.raw, nodes.comment, nodes.target)


def _skipped(node) -> bool:
    parent = node.parent
    while parent is not None:
        if isinstance(parent, SKIP) or {"atribucion", "vendor"} & set(parent.get("classes", ())):
            return True
        if isinstance(parent, nodes.reference) and u.vendor_link(parent.get("refuri", "")):
            return True
        if (
            isinstance(parent, nodes.reference)
            and parent.get("refuri") == node.astext()
        ):
            return True
        parent = parent.parent
    return False


def rebrand(app, doctree):
    cfg = u.config()
    if app.env.docname in cfg["rename"]["exempt_pages"]:
        return
    word = cfg["rename"]["from"]
    for text in list(doctree.findall(nodes.Text)):
        if word not in text or _skipped(text):
            continue
        new = u.rename(str(text), cfg)
        if new != str(text):
            text.parent.replace(text, nodes.Text(new))


def vendor_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """{vendor}`Nextcloud`: the vendor as the subject of a sentence («Nextcloud ofrece…»,
    «no Nextcloud»). The rename leaves it alone; the reader sees plain text."""
    return [nodes.inline(rawtext, text, classes=["vendor"])], []


def setup(app):
    app.add_role("vendor", vendor_role)
    # Before the title collector (priority 500): navigation and <title> get the new name too.
    app.connect("doctree-read", rebrand, priority=100)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
