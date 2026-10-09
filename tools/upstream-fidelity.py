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

import fnmatch
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstreamlib as u  # noqa: E402

AUDIENCES = ("usuario", "administracion", "desarrollo", "proyecto")


def check_block(
    block: dict, page: str, source: str, catalog: dict, cfg: dict, ui: dict | None = None
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

    up_levels = u.relative_levels(
        [lv for lv, _, _ in u.rst_headings(section, u.rst_styles(source))]
    )
    my_levels = u.relative_levels([lv for lv, _ in u.myst_headings(content)])
    if up_levels != my_levels:
        out.append(
            f"{doc}: headings {my_levels} differ from upstream's {up_levels} (count, order, level)"
        )

    directive_fences = [ln.strip() for ln in content.split("\n")
                        if (m := u.FENCE.match(ln)) and m.group(1)[0] == "`" and m.group(2).strip().startswith("{")]
    if directive_fences:
        out.append(f"{doc}: directive in a backtick fence ({directive_fences[0][:40]}); use a colon fence :::{{…}}")
    up_code, my_code = u.rst_code_blocks(section), u.myst_code_blocks(content)
    if up_code != my_code:
        missing = [c.split("\n")[0][:60] for c in up_code if c not in my_code]
        out.append(
            f"{doc}: code blocks differ from upstream ({len(my_code)} vs {len(up_code)}; "
            f"first not byte-identical: {missing[:1] or '(order)'})"
        )
    # an official paragraph's literals are its msgstr's: the Transifex string may translate one
    want = Counter(u.rst_inline_literals(section))
    for para in u.rst_paragraphs(section):
        if catalog.get(para):
            want -= Counter(u.rst_inline_literals(para))
            want += Counter(u.rst_inline_literals(catalog[para]))
    have = Counter(u.myst_inline_literals(content))
    ui = dict(u.ui_strings() if ui is None else ui)
    # a literal this doc's own official msgstr translates is shown that way by the interface
    for para in u.rst_paragraphs(section):
        if catalog.get(para):
            en, es = u.rst_inline_literals(para), u.rst_inline_literals(catalog[para])
            if len(en) == len(es):
                for a, b in zip(en, es):
                    if a != b:
                        ui[a] = set(ui.get(a, ())) | {b}
    swapped = _ui_swaps(want - have, Counter(u.myst_guilabels(content)), ui)
    want -= swapped
    if want != have:
        diff = want - have
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
    # quoted labels of other software (WinSCP, Finder, Thunderbird…) are not Nextcloud's strings
    third_party = any(fnmatch.fnmatch(doc, pat) for pat in cfg.get("ui_third_party", []))
    for quoted in re.findall(r"«([^»\n]+)»|\"([^\"\n]+)\"|“([^”\n]+)”", re.sub(r"`[^`\n]*`", "", u._without_fences(content))):
        text = next(q for q in quoted if q).strip()
        spanish = ui.get(text)
        if spanish and text not in spanish and not third_party:
            out.append(f"{doc}: «{text}» is a UI string the interface shows in Spanish: «{sorted(spanish)[0]}»")
    bare = u.bare_urls(content)
    if bare:
        out.append(f"{doc}: bare URL renders as plain text, write it as <url>: {bare[:2]}")
    labels_up = {u.label_prefix(doc, cfg) + lab for lab, _ in u.rst_labels(section)}
    if not labels_up <= set(u.myst_labels(content)):
        out.append(
            f"{doc}: labels missing as (nc-{u.label_prefix(doc, cfg)}label)=: {sorted(labels_up - set(u.myst_labels(content)))[:3]}"
        )

    # section titles are msgids too; on the page they are headings
    # a lead-in may end in «.» where the «:» introduced a screenshot the page drops
    mine = [u.plain(p).rstrip(":.") for p in u.myst_paragraphs(content)] + [
        u.plain(t).rstrip(":.") for _, t in u.myst_headings(content)
    ]
    ai = 0
    for para in u.rst_paragraphs(section):
        official = catalog.get(para, "")
        if official:
            if u.plain(official).rstrip(":.") not in mine:
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


DROPPED = re.compile(r"^(\s*)\.\. (toctree|figure|image)::")


def _rst_parts(section: str) -> list[str]:
    """The section cut at each heading: what precedes the first one, then one part per heading."""
    lines = section.split("\n")
    cuts = [0] + [
        at - (1 if at and u.ADORN.match(lines[at - 1]) else 0) for _, _, at in u.rst_headings(section)
    ] + [len(lines)]
    return ["\n".join(lines[a:b]) for a, b in zip(cuts, cuts[1:])]


def _myst_parts(content: str) -> list[str]:
    out, cur = [], []
    for ln, fenced in u.fence_walk(content.split("\n")):
        if not fenced and u.MYST_HEADING.match(ln.strip()):
            out.append("\n".join(cur))
            cur = []
        cur.append(ln)
    return out + ["\n".join(cur)]


def _words(paragraphs: list[str]) -> int:
    return sum(len(re.findall(r"[^\W\d_]+", u.plain(p))) for p in paragraphs)


def _rst_prose(part: str) -> list[str]:
    """Prose the page owes: no toctree or figure bodies (the page renders those differently)."""
    keep, skip = [], None
    for ln in part.split("\n"):
        if skip is not None:
            if ln.strip() and len(ln) - len(ln.lstrip()) <= skip:
                skip = None
            else:
                continue
        if m := DROPPED.match(ln):
            skip = len(m.group(1))
            continue
        keep.append(ln)
    return u.rst_paragraphs("\n".join(keep))


def _myst_prose(part: str) -> list[str]:
    body = u._without_fences(part)
    cells = [ln.strip().strip("|").replace("|", " ") for ln in body.split("\n")
             if ln.strip().startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", ln.strip())]
    return u.myst_paragraphs(part) + cells + [t for _, t in u.myst_headings(part)]


def _ui_swaps(missing: Counter, labels: Counter, ui: dict) -> Counter:
    """The upstream UI literals the page wrote as {guilabel} with the interface's own Spanish
    (a menu path `A -> B` as one label per step). Only a swap the catalog backs counts."""
    swapped = Counter()
    for lit, n in missing.items():
        parts = re.split(r"\s*(?:->|→)\s*", lit)
        for _ in range(n):
            picks = [next((es for es in sorted(ui.get(p, ())) if labels[es] > 0), None) for p in parts]
            if None in picks:
                break
            for es in picks:
                labels[es] -= 1
            swapped[lit] += 1
    return swapped


def warnings(content: str, section: str, ui: dict | None = None) -> list[str]:
    """Signals a reviewer reads; never a failure. A section whose Spanish runs well under its
    English (Spanish runs ~1.1x) may have lost text; a lead-in ending in «:» with nothing after
    it introduced something the page dropped (usually a screenshot)."""
    out = []
    up, mine = _rst_parts(section), _myst_parts(content)
    if len(up) == len(mine):
        for i, (a, b) in enumerate(zip(up, mine)):
            en, es = _words(_rst_prose(a)), _words(_myst_prose(b))
            if en >= 40 and es < 0.7 * en:
                title = next((t for _, t in u.myst_headings(b)), "(before the first heading)")
                out.append(f"section «{title}»: {es} Spanish words for {en} English — text may be missing")
    for lit in dict.fromkeys(u.myst_inline_literals(content)):
        parts = re.split(r"\s*(?:->|→)\s*", lit)
        es = [sorted((ui or {}).get(p, ())) for p in parts]
        if all(es) and any(p not in e for p, e in zip(parts, es)):
            out.append(f"`{lit}` is a UI label the interface shows as «{' → '.join(e[0] for e in es)}»: write {{guilabel}}")
    walk = list(u.fence_walk(content.split("\n")))
    for i, (ln, fenced) in enumerate(walk):
        s = ln.strip()
        # a bold label («**MySQL**:») names what follows, like a heading: not a lead-in
        if fenced or not s.endswith(":") or s.startswith((":", "|", "#", "(")) or re.match(r"^\*\*[^*]+\*\*:$", s):
            continue
        nxt = next((x for x, _ in walk[i + 1:] if x.strip()), "")
        # a lead-in may introduce a fence, list, table, admonition or quote; prose, a heading, a
        # sibling list step, an admonition's closing «:::» or the block's end means it is gone
        item = re.match(r"^(\s*)(?:[-*+]|\d+[.)])\s+", ln)
        base = len(item.group(1)) if item else len(ln) - len(ln.lstrip())
        indent = len(nxt) - len(nxt.lstrip())
        opens = re.match(r"^\s*([-*+|>]\s|\d+[.)]\s|:::\{)", nxt)
        closing = re.match(r"^\s*:::\s*$", nxt)
        # code introduced is code wherever it sits (upstream puts some fences between steps)
        # a paragraph of code spans only (a command, a list of keys), or a bold label («**MySQL**:»)
        command = re.match(r"^\s*(?:`[^`]+`[\s,.;:…]*)+$", nxt) or re.match(r"^\s*\*\*[^*]+\*\*:?\s*$", nxt)
        if not nxt or closing or not (u.FENCE.match(nxt) or command or indent > base or (opens and not item and indent >= base)):
            out.append(f"«{s[:60]}» ends in «:» but introduces nothing — a dropped screenshot?")
    return out


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
    problems, notes, woven, ai_total, n_blocks = [], [], set(), 0, 0
    names = u.docnames(updir, cfg)
    problems += [f"upstream.yml: {p}" for p in u.map_problems(names, cfg)]
    problems += [f"upstream.yml: {p}" for p in u.label_collisions(
        {n: (updir / f"{n}.rst").read_text(encoding="utf-8", errors="replace") for n in names}, cfg)]
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
            if block["doc"] and not found:
                notes += [f"{where}: {w}" for w in warnings(block["content"], u.rst_section(source, block["anchor"]), u.ui_strings())]
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
    for n in notes:
        print(f"WARN {n}")
    for p in problems:
        print(f"ERROR {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
