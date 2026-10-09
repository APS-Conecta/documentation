"""Page metadata for search and sharing (iniciativa scribe, Q23–Q24).

Turns each page's front matter into Pagefind filters (`audiencia`, one per `apps` entry) for
_templates/page.html, and its `resumen` into the description meta tag.
"""
from __future__ import annotations

from html import escape

from docutils import nodes


def _apps(value) -> list[str]:
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value or "").strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    return [v.strip().strip("'\"") for v in text.split(",") if v.strip().strip("'\"")]


def context(app, pagename, templatename, ctx, doctree):
    meta = app.env.metadata.get(pagename, {}) if pagename in app.env.found_docs else {}
    filters = []
    if meta.get("audiencia"):
        filters.append(("audiencia", str(meta["audiencia"])))
    filters += [("apps", a) for a in _apps(meta.get("apps"))]
    ctx["pagefind_filters"] = filters
    if meta.get("resumen"):
        ctx["metatags"] = ctx.get("metatags", "") + f'\n<meta name="description" content="{escape(str(meta["resumen"]))}">'


def abstract_to_metadata(app, doctree):
    """docutils reads a Spanish `resumen:` field as the bibliographic *abstract* and renders it
    as a box above the title, outside the metadata. The page already opens with its own
    «Resumen» section, so the box goes; its text returns to the metadata for search and the
    description tag."""
    for topic in list(doctree.findall(nodes.topic)):
        if "abstract" in topic.get("classes", ()):
            text = " ".join(p.astext() for p in topic.findall(nodes.paragraph))
            app.env.metadata[app.env.docname].setdefault("resumen", text)
            topic.parent.remove(topic)


def setup(app):
    # After the metadata collector (priority 500), which would otherwise reset the entry.
    app.connect("doctree-read", abstract_to_metadata, priority=900)
    app.connect("html-page-context", context)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
