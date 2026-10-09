#!/usr/bin/env python3
"""weave — deterministic helper for weaving the Nextcloud manuals into the site (scribe W-runs).

The AI translator never decides WHAT to weave or WHERE: this script does, from upstream.yml.

    python3 tools/weave.py batches [--done]     JSON: batches still to weave (or all), in Q11 order
    python3 tools/weave.py brief <docname>      Markdown: everything a translator needs for one doc
    python3 tools/weave.py prepare <batch-id>   create the folder index pages the batch's pages need
                                                but no upstream document provides

A batch is one upstream directory, at most BATCH documents, never split across two directories,
so a batch's pages share one chapter folder and two batches never edit the same file.
"""

from __future__ import annotations

import json
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstreamlib as u  # noqa: E402

BATCH = 10
ORDER = (
    "user_manual",
    "admin_manual",
    "developer_manual",
)  # usuario → administración → desarrollo (Q11)
AUDIENCE = {
    "usuario": "usuario",
    "administracion": "administracion",
    "desarrollo": "desarrollo",
}
TOCTREE = "```{toctree}\n:maxdepth: 1\n:glob:\n\n*\n*/index\n```\n"


def woven_docs() -> set[str]:
    done = set()
    for aud in ("usuario", "administracion", "desarrollo", "proyecto"):
        for page in (u.ROOT / aud).rglob("*.md"):
            done |= {
                b["doc"] for b in u.blocks(page.read_text(encoding="utf-8")) if b["doc"]
            }
    return done


def batches(include_done: bool = False) -> list[dict]:
    cfg, updir = u.config(), u.upstream_dir()
    done = set() if include_done else woven_docs()
    groups: "OrderedDict[str, list]" = OrderedDict()
    names = sorted(
        u.docnames(updir, cfg), key=lambda n: (ORDER.index(n.split("/", 1)[0]), n)
    )
    for name in names:
        hit = u.destination(name, cfg)
        if hit is None or name in done:
            continue
        page, rule = hit
        groups.setdefault(name.rsplit("/", 1)[0], []).append(
            {
                "doc": name,
                "page": page,
                "difiere": rule.get("difiere", ""),
                "exists": (u.ROOT / page).exists(),
            }
        )
    out = []
    for directory, docs in groups.items():
        for i in range(0, len(docs), BATCH):
            chunk = docs[i : i + BATCH]
            out.append(
                {
                    "id": f"{u.slug(directory).replace('/', '-')}-{i // BATCH + 1}",
                    "dir": directory,
                    "docs": chunk,
                }
            )
    return out


def brief(docname: str) -> str:
    cfg, updir = u.config(), u.upstream_dir()
    page, rule = u.destination(docname, cfg)
    sha = u.tip(updir)
    source = (updir / f"{docname}.rst").read_text(encoding="utf-8", errors="replace")
    body = u.rst_section(source)
    title = u.rst_headings(source)[0][1] if u.rst_headings(source) else docname
    catalog = u.catalog(updir, docname, cfg)
    official = [(p, catalog[p]) for p in u.rst_paragraphs(body) if catalog.get(p)]
    target = u.ROOT / page
    lines = [
        f"# Brief: `{docname}`",
        "",
        f"- **Upstream:** `{cfg['source']['repo']}` `{docname}.rst` at `{sha}` (branch tip).",
        f"- **Upstream title:** {title}",
        f"- **Target page:** `{page}` — {'EXISTS: keep its front matter and APS sections, add the block(s) at the end, before any toctree' if target.exists() else 'NEW: create it'}.",
        f"- **Block opening line:** ````` ````{{upstream}} {docname}.rst@{sha} `````",
        f"- **`:difiere:` required:** {'yes — `:difiere: ' + rule['difiere'] + '`' if rule.get('difiere') else 'no'}",
        f"- **Folder index:** {'yes — end the page with the toctree block below' if page.endswith('/index.md') else 'no'}",
        f"- **Official Spanish wording to reuse verbatim:** {len(official)} paragraph(s) below; every other paragraph is yours to translate.",
        "",
    ]
    if page.endswith("/index.md"):
        lines += [
            "Toctree block for a folder index:",
            "",
            "`````",
            TOCTREE.rstrip("\n"),
            "`````",
            "",
        ]
    if official:
        lines += ["## Official Spanish (msgid → msgstr)", ""]
        for en, es in official:
            lines += [f"- EN: {en}", f"  ES: {es}"]
        lines.append("")
    lines += [
        "## Upstream source (body below the title)",
        "",
        "`````rst",
        body,
        "`````",
        "",
    ]
    if target.exists():
        lines += [
            "## Current target page",
            "",
            "`````markdown",
            target.read_text(encoding="utf-8"),
            "`````",
            "",
        ]
    return "\n".join(lines)


def prepare(batch_id: str) -> list[str]:
    """Create the index page of every folder this batch's pages live in when no upstream doc of
    the whole map provides it — so every woven page sits in a toctree."""
    cfg = u.config()
    batch = next((b for b in batches(include_done=True) if b["id"] == batch_id), None)
    if batch is None:
        raise SystemExit(f"weave: no batch {batch_id!r}")
    mapped = {
        u.destination(n, cfg)[0]
        for n in u.docnames(u.upstream_dir(), cfg)
        if u.destination(n, cfg)
    }
    made = []
    for doc in batch["docs"]:
        parts = doc["page"].split("/")
        for depth in range(2, len(parts)):
            index = "/".join(parts[:depth]) + "/index.md"
            path = u.ROOT / index
            if index in mapped or path.exists():
                continue
            name = parts[depth - 1].replace("-", " ").capitalize()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f"---\ntipo: referencia\nesqueleto: borrador\naudiencia: {parts[0]}\napps: [gestion]\n"
                f'resumen: "{name}: páginas de la plataforma base."\n---\n# {name}\n\n## Resumen\n\n'
                f"Las páginas de esta sección derivan de la documentación de la plataforma base.\n\n{TOCTREE}",
                encoding="utf-8",
            )
            made.append(index)
    return made


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    cmd = argv[0]
    if cmd == "batches":
        print(json.dumps(batches("--done" in argv), ensure_ascii=False, indent=1))
    elif cmd == "brief" and len(argv) == 2:
        print(brief(argv[1]))
    elif cmd == "prepare" and len(argv) == 2:
        for p in prepare(argv[1]):
            print(f"[weave] created {p}")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
