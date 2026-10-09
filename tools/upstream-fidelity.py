#!/usr/bin/env python3
"""upstream-fidelity — every woven {upstream} block says what its upstream source says.

The weave (an AI translator) may change the words, never the facts a reader acts on. For each
block, against the upstream document section at the block's own SHA:

  structure   heading count, order and relative level are upstream's
  literals    code blocks and inline literals are byte-identical, in order
  links       external URLs and :doc:/:ref: targets are upstream's (as {nc-doc}/{nc-ref})
  labels      every upstream `.. _label:` in the section exists as `(nc-label)=`
  wording     user manual: a paragraph whose source still matches an official catalog msgid
              with a msgstr IS that msgstr (markup-normalised); every other paragraph is
              AI-translated and only counted
  language    no paragraph reads as English
  marker      the SHA resolves upstream, the docname is mapped, the block sits on its mapped
              page, and a `difiere` rule's documents carry `:difiere:`

Coverage (every mapped document has a block somewhere) is reported always and enforced with
--require-coverage, which the last bulk-weave run switches on.

    python3 tools/upstream-fidelity.py [--require-coverage] [page.md …]
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstreamlib as u  # noqa: E402

AUDIENCES = ("usuario", "administracion", "desarrollo", "proyecto")


def check_block(
    block: dict, page: str, source: str, catalog: dict, cfg: dict
) -> tuple[list[str], int]:
    """(problems, AI-translated paragraph count) for one block against its upstream section."""
    if not block["doc"]:
        return [
            f"argument {block['arg']!r} is not <manual>/<path>.rst@<sha>[#<anchor>]"
        ], 0
    doc = block["doc"]
    try:
        hit = u.destination(doc, cfg)
    except LookupError:
        return [f"{doc} is not in upstream.yml"], 0
    if hit is None:
        return [f"{doc} is excluded in upstream.yml"], 0
    want_page, rule = hit
    out = []
    if want_page != page:
        out.append(f"{doc} belongs on {want_page}, not here")
    if rule.get("difiere") and not block["options"].get("difiere"):
        out.append(f"{doc} needs :difiere: (APS differs: {rule['difiere']})")
    try:
        section = u.rst_section(source, block["anchor"])
    except LookupError as error:
        return out + [f"{doc}: {error}"], 0
    content = block["content"]

    up_levels = u.relative_levels([lv for lv, _, _ in u.rst_headings(section)])
    my_levels = u.relative_levels([lv for lv, _ in u.myst_headings(content)])
    if up_levels != my_levels:
        out.append(
            f"{doc}: headings {my_levels} differ from upstream's {up_levels} (count, order, level)"
        )

    up_code, my_code = u.rst_code_blocks(section), u.myst_code_blocks(content)
    if up_code != my_code:
        missing = [c.split("\n")[0][:60] for c in up_code if c not in my_code]
        out.append(
            f"{doc}: code blocks differ from upstream ({len(my_code)} vs {len(up_code)}; "
            f"first not byte-identical: {missing[:1] or '(order)'})"
        )
    if Counter(u.rst_inline_literals(section)) != Counter(
        u.myst_inline_literals(content)
    ):
        diff = Counter(u.rst_inline_literals(section)) - Counter(
            u.myst_inline_literals(content)
        )
        out.append(
            f"{doc}: inline literals differ from upstream (missing or altered: {sorted(diff)[:3]})"
        )

    if u.rst_links(section) != u.myst_links(content):
        out.append(
            f"{doc}: external links differ: missing {sorted(u.rst_links(section) - u.myst_links(content))[:3]}, "
            f"extra {sorted(u.myst_links(content) - u.rst_links(section))[:3]}"
        )
    if Counter(u.rst_xrefs(section, doc)) != Counter(u.myst_xrefs(content)):
        out.append(
            f"{doc}: cross-references differ: missing "
            f"{sorted(Counter(u.rst_xrefs(section, doc)) - Counter(u.myst_xrefs(content)))[:3]}"
        )
    labels_up = {lab for lab, _ in u.rst_labels(section)}
    if not labels_up <= set(u.myst_labels(content)):
        out.append(
            f"{doc}: labels missing as (nc-label)=: {sorted(labels_up - set(u.myst_labels(content)))[:3]}"
        )

    mine = [u.plain(p) for p in u.myst_paragraphs(content)]
    ai = 0
    for para in u.rst_paragraphs(section):
        official = catalog.get(para, "")
        if official:
            if u.plain(official) not in mine:
                out.append(
                    f"{doc}: official Spanish not used verbatim: «{u.plain(official)[:70]}…»"
                )
        else:
            ai += 1
    for para in u.myst_paragraphs(content):
        if u.reads_english(para):
            out.append(f"{doc}: paragraph reads as English: «{u.plain(para)[:70]}…»")
            break
    return out, ai


def pages(paths: list[str] | None) -> list[Path]:
    if paths:
        return [Path(p) for p in paths]
    return sorted(p for a in AUDIENCES for p in (u.ROOT / a).rglob("*.md"))


def main(argv: list[str]) -> int:
    require = "--require-coverage" in argv
    paths = [a for a in argv if not a.startswith("--")]
    cfg, updir = u.config(), u.upstream_dir()
    if not (updir / ".git").exists():
        print(
            f"[upstream-fidelity] no upstream clone at {updir} — run make upstream",
            file=sys.stderr,
        )
        return 2
    problems, woven, ai_total, n_blocks = [], set(), 0, 0
    names = u.docnames(updir, cfg)
    problems += [f"upstream.yml: {p}" for p in u.map_problems(names, cfg)]
    for path in pages(paths):
        page = (
            path.relative_to(u.ROOT).as_posix()
            if path.is_absolute()
            else path.as_posix()
        )
        for block in u.blocks(path.read_text(encoding="utf-8")):
            n_blocks += 1
            where = f"{page}:{block['line']}"
            if block["doc"]:
                try:
                    source = u.show(updir, block["sha"], block["doc"])
                except LookupError as error:
                    problems.append(
                        f"{where}: {block['doc']}@{block['sha']} does not resolve upstream ({error})"
                    )
                    continue
                cat = u.catalog(updir, block["doc"], cfg)
            else:
                source, cat = "", {}
            found, ai = check_block(block, page, source, cat, cfg)
            problems += [f"{where}: {p}" for p in found]
            ai_total += ai
            if block["doc"]:
                woven.add(block["doc"])
    mapped = [n for n in names if u.destination(n, cfg)]
    missing = [n for n in mapped if n not in woven]
    print(
        f"[upstream-fidelity] {n_blocks} block(s); coverage {len(mapped) - len(missing)}/{len(mapped)} "
        f"documents; {ai_total} AI-translated paragraph(s) counted"
    )
    if require and missing and not paths:
        problems += [f"coverage: {n} has no block" for n in missing]
    for p in problems:
        print(f"ERROR {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
