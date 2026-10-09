"""The {upstream} directive and the nc-doc / nc-ref roles (iniciativa scribe, Q19–Q20).

A woven block is upstream text — translated prose, verbatim code — placed inside an APS page:

    ````{upstream} admin_manual/configuration_user/user_configuration.rst@3ad9158
    :difiere: administracion/aio
    …translated MyST, upstream's own headings…
    ````

The directive is the block's marker, its attribution and its reading context at once: it renders
a «Fuente» line (class `atribucion`, which the rename skips) and, with `:difiere:`, a notice that
APS Conecta Gestión departs from upstream. Its headings join the page's table of contents.

Cross-references inside a block keep upstream's targets: {nc-doc}`user_manual/files/sharing` and
{nc-ref}`label`. They resolve to the APS page where that document is woven, and until it is, to
docs.nextcloud.com — so a half-woven site never has a dead link.
"""

from __future__ import annotations

import sys
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util import logging
from sphinx.util.nodes import nested_parse_with_titles

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import upstreamlib as u  # noqa: E402

logger = logging.getLogger(__name__)
SOURCE_URL = "https://github.com/{repo}/blob/{sha}/{doc}.rst"


class UpstreamDirective(SphinxDirective):
    required_arguments = 1
    has_content = True
    option_spec = {"difiere": directives.unchanged_required}

    def run(self):
        m = u.BLOCK_ARG.match(self.arguments[0])
        if not m:
            raise self.error(
                f"{{upstream}} needs <manual>/<path>.rst@<sha>[#<anchor>], got {self.arguments[0]!r}"
            )
        doc, sha = m.group("doc"), m.group("sha")
        cfg = u.config()
        anchor_id = "upstream-" + u.make_id(
            doc + ("-" + m.group("anchor") if m.group("anchor") else "")
        )
        target = nodes.target("", "", ids=[anchor_id])
        source = nodes.reference(
            "",
            f"«{doc}»",
            refuri=SOURCE_URL.format(repo=cfg["source"]["repo"], sha=sha, doc=doc),
        )
        credit = nodes.paragraph("", "", classes=["atribucion"])
        credit += nodes.Text("Fuente: documentación de Nextcloud, ")
        credit += source
        credit += nodes.Text(
            f", versión {sha[:7]}, licencia CC BY 3.0; traducida y adaptada para APS Conecta Gestión."
        )
        out = [target, credit]
        if "difiere" in self.options:
            note = nodes.admonition(classes=["difiere"])
            note += nodes.title("", "En APS Conecta Gestión esto difiere")
            para = nodes.paragraph()
            ref = nodes.reference("", "", internal=True)
            ref["nc_kind"], ref["nc_target"] = "page", self.options["difiere"]
            ref += nodes.Text("Ver la página de APS Conecta Gestión")
            para += ref
            para += nodes.Text(".")
            note += para
            out.append(note)
        # Headings in the content open sections straight in the page's section tree, so the
        # attribution and the text before the first heading go into the page first; returning
        # them instead would place them after the block's own subsections.
        parent = self.state_machine.node
        parent += out
        nested_parse_with_titles(self.state, self.content, parent, self.content_offset)
        # The title of the section the block sits in: a bare {nc-doc} link to a page holding
        # several documents shows this one's own heading (resolve()).
        head = parent[0].astext() if isinstance(parent, nodes.section) and len(parent) and \
            isinstance(parent[0], nodes.title) else ""
        blocks = self.env.domaindata.setdefault("upstream", {}).setdefault("blocks", {})
        blocks.setdefault(doc, (self.env.docname, anchor_id, u.rename(head, cfg)))
        return []


class NcRole(SphinxRole):
    """{nc-doc}`[title <]docname[>]` and {nc-ref}`[title <]label[>]`."""

    def __init__(self, kind: str):
        self.kind = kind

    def run(self):
        text = self.text
        if text.endswith(">") and "<" in text:
            title, target = (
                text[: text.rindex("<")].strip(),
                text[text.rindex("<") + 1 : -1].strip(),
            )
        else:
            title, target = "", text.strip()
        ref = nodes.reference(self.rawtext, title or target, internal=False)
        # no text given: resolve() writes the woven page's title (doc) or section title (ref),
        # so a title lives in one place
        ref["nc_auto_title"] = not title
        ref["nc_kind"], ref["nc_target"] = (
            self.kind,
            target if self.kind == "doc" else target.lower(),
        )
        return [ref], []


def _labels(app) -> dict:
    """upstream label → (docname, anchor id), read once from the clone."""
    if not hasattr(app, "_nc_labels"):
        found = {}
        updir = u.upstream_dir()
        if (updir / ".git").exists():
            for doc in u.docnames(updir):
                text = (updir / f"{doc}.rst").read_text(
                    encoding="utf-8", errors="replace"
                )
                for label, _ in u.rst_labels(text):
                    found.setdefault(label, (doc, u.make_id(label)))
        app._nc_labels = found
    return app._nc_labels


def resolve(app, doctree, fromdocname):
    env, builder = app.env, app.builder
    blocks = env.domaindata.get("upstream", {}).get("blocks", {})
    std_labels = env.domaindata["std"]["labels"]
    for ref in list(doctree.findall(nodes.reference)):
        kind = ref.get("nc_kind")
        if not kind:
            continue
        target = ref["nc_target"]
        if kind == "page":
            page, _, anchor = target.partition("#")
            ref["refuri"] = builder.get_relative_uri(fromdocname, page) + (
                f"#{anchor}" if anchor else ""
            )
        elif kind == "doc":
            if target in blocks:
                page, anchor, head = blocks[target]
                ref["refuri"] = (
                    builder.get_relative_uri(fromdocname, page) + f"#{anchor}"
                )
                if ref.get("nc_auto_title"):
                    several = sum(1 for p, _, _ in blocks.values() if p == page) > 1
                    title = head if several and head else (
                        env.titles[page].astext() if page in env.titles else "")
                    if title:
                        ref.children = [nodes.Text(title)]
            else:
                ref["refuri"] = u.external_url(target)
        else:
            label = f"nc-{target}"
            if label in std_labels:
                page, anchor, section = std_labels[label]
                ref["refuri"] = (
                    builder.get_relative_uri(fromdocname, page) + f"#{anchor}"
                )
                if ref.get("nc_auto_title") and section:
                    ref.children = [nodes.Text(section)]
            elif target in _labels(app):
                doc, anchor = _labels(app)[target]
                ref["refuri"] = u.external_url(doc, anchor)
            else:
                ref["refuri"] = u.external_url("admin_manual/index")
                logger.warning(
                    f"nc-ref: unknown upstream label {target!r}", location=ref
                )


def purge(app, env, docname):
    blocks = env.domaindata.get("upstream", {}).get("blocks", {})
    for doc in [d for d, (page, *_) in blocks.items() if page == docname]:
        del blocks[doc]


def merge(app, env, docnames, other):
    mine = env.domaindata.setdefault("upstream", {}).setdefault("blocks", {})
    for doc, where in other.domaindata.get("upstream", {}).get("blocks", {}).items():
        if where[0] in docnames:
            mine.setdefault(doc, where)


def setup(app):
    app.add_directive("upstream", UpstreamDirective)
    app.add_role("nc-doc", NcRole("doc"))
    app.add_role("nc-ref", NcRole("ref"))
    app.connect("doctree-resolved", resolve)
    app.connect("env-purge-doc", purge)
    app.connect("env-merge-info", merge)
    return {"parallel_read_safe": True, "parallel_write_safe": True, "env_version": 3}
