"""The one reader of upstream.yml, plus the RST/MyST text helpers every upstream consumer shares.

Consumers: _ext/upstream.py (the directive and the nc-doc/nc-ref roles), _ext/rebrand.py (the
site-wide rename), tools/upstream-fidelity.py, tools/rebrand-check.py and the bulk-weave
workflow. None of them reads upstream.yml or parses RST on its own, so a rule changes in one
place (DRY).

The helpers are line-oriented regexes, not a docutils parse: upstream RST uses Sphinx roles and
directives a bare docutils parser rejects, and the facts compared here (heading levels, literal
text, link targets, paragraphs) are visible at the line level.
"""

from __future__ import annotations

import json
import os
import posixpath
import re
import string
import subprocess
import tarfile
import textwrap
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "upstream.yml"


# ------------------------------------------------------------------- configuration


@lru_cache(maxsize=1)
def config() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def woven_urls(pages) -> set[str]:
    """External URLs that appear only inside {upstream} blocks of the given page texts. They are
    upstream's text, kept byte-identical (fidelity); keeping them alive is upstream's job, so
    linkcheck skips them (conf.py) and checks every URL the APS prose writes."""
    inside, outside = set(), set()
    for text in pages:
        rest = text
        for b in blocks(text):
            inside |= myst_links(b["content"])
            rest = rest.replace(b["content"], "")
        outside |= myst_links(rest)
    return inside - outside


def org_root() -> Path:
    return Path(os.environ.get("APS_ORG_ROOT", "/opt/aps-conecta-org"))


def upstream_dir() -> Path:
    """The sparse clone tools/fetch-upstream.sh maintains."""
    return Path(os.environ.get("UPSTREAM_DIR", ROOT / "_generated" / "upstream"))


def server_dir() -> Path:
    """The sparse clone of nextcloud/server's Spanish l10n that tools/fetch-upstream.sh maintains."""
    return Path(os.environ.get("SERVER_DIR", ROOT / "_generated" / "server"))


def major(cfg: dict | None = None) -> str:
    cfg = cfg or config()
    spec = cfg["source"]["major_from"]
    path = org_root() / spec["file"]
    m = re.search(spec["pattern"], path.read_text(encoding="utf-8"))
    if not m:
        raise SystemExit(
            f"upstreamlib: no Nextcloud major in {path} (pattern {spec['pattern']!r})"
        )
    return m.group(1)


def branch(cfg: dict | None = None) -> str:
    cfg = cfg or config()
    return cfg["source"]["branch"].format(major=major(cfg))


def tip(updir: Path | None = None) -> str:
    return git(updir or upstream_dir(), "rev-parse", "HEAD").strip()


def git(updir: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", "-C", str(updir), *args], capture_output=True, text=True
    )
    if out.returncode != 0:
        raise LookupError(out.stderr.strip() or f"git {' '.join(args)} failed")
    return out.stdout


def show(updir: Path, sha: str, docname: str) -> str:
    """The upstream RST of `docname` at `sha`, includes expanded (a partial clone fetches each
    blob on demand)."""
    read = lambda path: git(updir, "show", f"{sha}:{path}")
    return expand_includes(read(f"{docname}.rst"), docname, read)


INCLUDE = re.compile(r"^([ \t]*)\.\.\s+(include|literalinclude)::\s*(\S+)\s*$")
INCLUDE_OPTION = re.compile(r"^[ \t]+:([\w-]+):\s*(.*?)\s*$")


def expand_includes(text: str, docname: str, read) -> str:
    """The doc as Sphinx renders it: each `.. include::` replaced by the file's RST, each
    `.. literalinclude::` by a code-block of the file. `read(path)` returns a file of the
    upstream tree; a path starting with «/» is from the manual's root. Any option but a
    literalinclude's `:language:` is refused: it would change what renders."""
    out, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        m = INCLUDE.match(lines[i])
        i += 1
        if not m:
            out.append(lines[i - 1])
            continue
        indent, kind, target = m.groups()
        opts = {}
        while i < len(lines) and (o := INCLUDE_OPTION.match(lines[i])):
            opts[o.group(1)] = o.group(2)
            i += 1
        if set(opts) - ({"language"} if kind == "literalinclude" else set()):
            raise LookupError(f"{docname}: {kind} {target} with options {sorted(opts)} is not supported")
        manual = docname.split("/", 1)[0]
        path = os.path.normpath(f"{manual}{target}" if target.startswith("/") else os.path.join(os.path.dirname(docname), target))
        body = read(path).rstrip("\n")
        if kind == "include":
            body = expand_includes(body, path, read)
            out += [indent + ln if ln.strip() else "" for ln in body.split("\n")]
        else:
            out += [f"{indent}.. code-block:: {opts.get('language', '')}".rstrip(), ""]
            out += [f"{indent}   {ln}" if ln.strip() else "" for ln in body.split("\n")]
    return "\n".join(out)


# ------------------------------------------------------------------- the map


def slug(path: str) -> str:
    return path.lower().replace("_", "-")


def docnames(updir: Path | None = None, cfg: dict | None = None) -> list[str]:
    """Every upstream document of the three manuals, minus translation catalogs."""
    updir, cfg = updir or upstream_dir(), cfg or config()
    out = []
    for manual in cfg["source"]["manuals"]:
        for f in sorted((updir / manual).rglob("*.rst")):
            rel = f.relative_to(updir).with_suffix("").as_posix()
            if "/locale/" in rel or "/_" in rel:
                continue
            out.append(rel)
    return out


def destination(docname: str, cfg: dict | None = None) -> tuple[str, dict] | None:
    """(APS page, rule) for an upstream docname; None when the map excludes it."""
    cfg = cfg or config()
    if docname in cfg.get("exclude", ()):
        return None
    for rule in cfg["map"]:
        src = rule["from"]
        if src.endswith("/*"):
            prefix = src[:-1]
            if docname.startswith(prefix):
                return rule["to"].format(path=slug(docname[len(prefix) :])), rule
        elif docname == src:
            return rule["to"], rule
    raise LookupError(f"{docname}: no map rule")


def map_problems(names: list[str], cfg: dict | None = None) -> list[str]:
    """Every document lands somewhere, and two documents share a page only through a rule
    that names the page outright (a deliberate weave), never by two {path} expansions."""
    cfg = cfg or config()
    out, seen = [], {}
    for name in names:
        try:
            hit = destination(name, cfg)
        except LookupError as error:
            out.append(str(error))
            continue
        if hit is None:
            continue
        page, rule = hit
        if "{path}" in rule["to"] and page in seen:
            out.append(f"{name}: page {page} already holds {seen[page]}")
        seen.setdefault(page, name)
    return out


def external_url(docname: str, anchor: str = "", cfg: dict | None = None) -> str:
    cfg = cfg or config()
    manual, path = docname.split("/", 1)
    url = cfg["source"]["external"][manual].format(major=major(cfg), path=path)
    return f"{url}#{anchor}" if anchor else url


# ------------------------------------------------------------------- the rename


def _rename_re(cfg: dict) -> re.Pattern:
    keep = sorted(cfg["rename"]["keep"], key=len, reverse=True)
    word = re.escape(cfg["rename"]["from"])
    guard = "".join(
        f"(?!{re.escape(k[len(cfg['rename']['from']) :])})"
        for k in keep
        if k.startswith(cfg["rename"]["from"])
    )
    # a path component keeps its name: $HOME/.config/Nextcloud/ is where the client really writes
    return re.compile(rf"(?<![/\\])\b{word}\b(?![/\\]){guard}")


def _forms_re(cfg: dict) -> re.Pattern | None:
    """The inflected forms `rename.forms` maps («Nextclouds»), each a whole word."""
    forms = cfg["rename"].get("forms") or {}
    if not forms:
        return None
    alt = "|".join(re.escape(f) for f in sorted(forms, key=len, reverse=True))
    return re.compile(rf"(?<![/\\])\b(?:{alt})\b(?![/\\])")


def rename(text: str, cfg: dict | None = None) -> str:
    """«Nextcloud» → «APS Conecta Gestión», except inside the legal/product names `keep` lists;
    an inflected form («Nextclouds») takes its own wording from `rename.forms`."""
    cfg = cfg or config()
    if forms := _forms_re(cfg):
        text = forms.sub(lambda m: cfg["rename"]["forms"][m.group(0)], text)
    return _rename_re(cfg).sub(cfg["rename"]["to"], text)


# A casing variant of the name as a whole word («NextCloud», «NEXTCLOUD», «NextClouds»): the rename
# never matches it, so it shows the vendor's name. Lower case is a path or a database name.
CASE_VARIANT = re.compile(r"(?<![\w/\\.-])(?i:nextclouds?)(?![\w/\\.-])")


def vendor_link(url: str, cfg: dict | None = None) -> bool:
    """A link to the vendor's own site (rename.keep_hosts): its text names the vendor, never the
    suite — «la página de descargas de Nextcloud» points at nextcloud.com, which APS does not run."""
    cfg = cfg or config()
    where = re.sub(r"^https?://(www\.)?", "", url or "")
    host = re.split(r"[/#?]", where, maxsplit=1)[0]
    return any(where == h or where.startswith((h + "/", h + "#", h + "?"))
               or ("/" not in h and host.endswith("." + h))  # apps.nextcloud.com, docs.nextcloud.com
               for h in cfg["rename"].get("keep_hosts") or [])


def leftovers(text: str, cfg: dict | None = None) -> list[str]:
    cfg = cfg or config()
    word, forms = cfg["rename"]["from"], cfg["rename"].get("forms") or {}
    hits = list(_rename_re(cfg).finditer(text))
    if f := _forms_re(cfg):
        hits += f.finditer(text)
    hits += [m for m in CASE_VARIANT.finditer(text)
             if not m.group(0).islower() and m.group(0) != word and m.group(0) not in forms]
    return [text[max(0, m.start() - 30) : m.end() + 30] for m in sorted(hits, key=lambda m: m.start())]


# ------------------------------------------------------------------- RST, the upstream side

ADORN = re.compile(r"^([!-/:-@\[-`{-~])\1{2,}\s*$")  # docutils: any non-alphanumeric printable ASCII
LABEL = re.compile(r"^\.\.\s+_([^:`]+):\s*$")
RST_CODE_DIRECTIVE = re.compile(r"^(\s*)\.\.\s+(?:code-block|code|sourcecode)\s*::.*$")  # docutils allows «code-block ::»
# may wrap a line, never a paragraph; it closes on a «``» no backtick follows, as docutils does
RST_INLINE_LITERAL = re.compile(r"``((?:[^\n]|\n(?!\s*\n))+?)``(?!`)")
RST_EXT_LINK = re.compile(r"`[^`<]*<(https?://[^>]+)>`__?")
RST_NAMED_TARGET = re.compile(r"^\.\. _[^:\n]+:\s*(https?://\S+)\s*$", re.M)
# «'» may sit inside (…/wiki/FAQ's), and balanced «(…)» too (…-encryption-(HTTPS)); a closing «)» alone ends it
URL = re.compile(r"https?://(?:[^\s<>`\"()\]{}]|\([^\s<>`\"(){}]*\))+")  # «{ns}name»: docutils stops at «}»
# docutils' end-string: a backtick followed by a word character does not close the role
# (upstream's «:ref:`… core `Text-To-Speech Task type<t2s-consumer-apps>`» links t2s-consumer-apps)
RST_ROLE = re.compile(r":(doc|ref):`((?:[^`]|`(?=\w))+?)`(?![\w`])")


def _rst_titles(text: str):
    """(adornment style, title, line index) per section title: "o=" overlined, "u-" underlined."""
    lines, i = text.split("\n"), 0
    while i < len(lines) - 1:
        over = ADORN.match(lines[i])
        if (
            over
            and i + 2 < len(lines)
            and lines[i + 1].strip()
            and ADORN.match(lines[i + 2])
            and lines[i + 2][0] == lines[i][0]
            # docutils: an overline under 4 characters and shorter than the text is text («```»)
            and (len(lines[i].strip()) >= 4 or len(lines[i].strip()) >= len(lines[i + 1].strip()))
        ):
            yield "o" + lines[i][0], lines[i + 1].strip(), i + 1
            i += 3
        elif (
            lines[i].strip()
            and not lines[i].startswith((" ", "\t", ".."))
            and ADORN.match(lines[i + 1])
            and len(lines[i + 1].rstrip()) >= len(lines[i].rstrip())
        ):
            yield "u" + lines[i + 1][0], lines[i].strip(), i
            i += 2
        else:
            i += 1


def rst_styles(text: str) -> list[str]:
    """The adornment styles in the order they first appear — docutils' section ranks."""
    return list(dict.fromkeys(style for style, _, _ in _rst_titles(text)))


def rst_headings(text: str, styles: list[str] | None = None) -> list[tuple[int, str, int]]:
    """(level, title, line index) per section title, ranked by `styles` (default: the order the
    styles first appear in `text`). Rank a section with its whole document's `rst_styles`: a
    section alone can meet its styles in another order than docutils does."""
    order = list(styles or [])
    out = []
    for style, title, at in _rst_titles(text):
        if style not in order:
            order.append(style)
        out.append((order.index(style) + 1, title, at))
    return out


def label_prefix(doc: str, cfg: dict | None = None) -> str:
    """What follows «nc-» in a woven label of `doc`'s manual. Each upstream manual is its own
    Sphinx project, so a label is unique only inside it; upstream.yml `label_prefix` gives the
    manuals that share labels with another one a prefix of their own."""
    cfg = cfg or config()
    return (cfg["source"].get("label_prefix") or {}).get(doc.split("/", 1)[0], "")


def label_collisions(texts: dict[str, str], cfg: dict | None = None) -> list[str]:
    """Upstream labels that two manuals define under the same woven name `(nc-<prefix><label>)=`."""
    seen, out = {}, []
    for doc, text in texts.items():
        manual = doc.split("/", 1)[0]
        for label, _ in rst_labels(text):
            name = label_prefix(doc, cfg) + label.lower()
            other = seen.setdefault(name, manual)
            if other != manual:
                out.append(f"label {label!r} is in {other} and {manual}: give one a label_prefix")
                seen[name] = manual
    return sorted(set(out))


def rst_labels(text: str) -> list[tuple[str, int]]:
    """(label, line index) of every `.. _label:` target. A target whose URL sits on the next,
    indented line is an external hyperlink target (docutils), not a label."""
    lines = text.split("\n")
    return [
        (m.group(1).strip().lower(), i)
        for i, ln in enumerate(lines)
        if (m := LABEL.match(ln))
        and not (i + 1 < len(lines) and re.match(r"^\s+https?://", lines[i + 1]))
    ]


def title_labels(text: str) -> list[str]:
    """The labels above the doc's first title (`.. _occ:` on line 1): they name the whole doc."""
    starts = [at - (style[0] == "o") for style, _, at in _rst_titles(text)]
    first = min(starts) if starts else len(text.split("\n"))
    return [label for label, at in rst_labels(text) if at < first]


def rst_section(text: str, anchor: str = "") -> str:
    """Without `anchor`: the whole document below its title (every top-level section — a few
    upstream docs carry more than one). With `anchor`: the section that label `anchor` (or the
    heading whose slug is `anchor`) opens, up to the next heading at the same or a higher level."""
    lines, heads = text.split("\n"), rst_headings(text)
    if not heads:
        return text
    if anchor:
        labels = {lab: i for lab, i in rst_labels(text)}
        if anchor in labels:
            start = next((h for h in heads if h[2] > labels[anchor]), None)
        else:
            start = next((h for h in heads if make_id(h[1]) == anchor), None)
        if start is None:
            raise LookupError(f"anchor {anchor!r} not found")
        level, _, at = start
        end = next((h[2] for h in heads if h[2] > at and h[0] <= level), len(lines))
    else:
        level, _, at = heads[0]
        end = len(lines)
    # a title line `at` is followed by its underline; an overlined title starts one line earlier
    chunk = lines[at + 2:end]
    if end < len(lines) and end > 0 and ADORN.match(lines[end - 1] or " "):
        chunk = chunk[:-1]          # the next section's overline
    while chunk and (not chunk[-1].strip() or LABEL.match(chunk[-1])):
        chunk.pop()                 # a trailing label belongs to the next section
    return "\n".join(chunk)


def relative_levels(levels: list[int]) -> list[int]:
    base = min(levels) if levels else 0
    return [lv - base for lv in levels]


def _indented_block(lines: list[str], i: int, base: int | None = None) -> tuple[list[str], int]:
    """The literal block after line i, as docutils reads it: every line indented deeper than
    `base` (line i's own indent unless a directive passes its own), blank lines allowed inside,
    with the smallest indent stripped."""
    j = i + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    if base is None:
        # the paragraph's own indent; past a list marker («#. Edit it::» is column 3) when the
        # block sits deeper than that, so the item's next paragraph is not swallowed
        base = len(lines[i]) - len(lines[i].lstrip())
        m = re.match(r"^\s*(?:[-*+]|#\.|\d+[.)]|\(\d+\))\s+", lines[i])
        if m and j < len(lines) and len(lines[j]) - len(lines[j].lstrip()) > len(m.group(0)):
            base = len(m.group(0))
    if j >= len(lines) or len(lines[j]) - len(lines[j].lstrip()) <= base:
        return [], i + 1
    block = []
    while j < len(lines) and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > base):
        block.append(lines[j])
        j += 1
    while block and not block[-1].strip():
        block.pop()
    cut = min(len(ln) - len(ln.lstrip()) for ln in block if ln.strip())
    return [ln[cut:] if ln.strip() else "" for ln in block], j


def _quoted_block(lines: list[str], i: int) -> tuple[list[str], int]:
    """RST quoted literal block after line i's «::»: unindented contiguous lines that all start
    with the same punctuation character («# netstat -pant»). Docutils renders it as code."""
    pad = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
    j = i + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    lead = lines[j][len(pad) : len(pad) + 1] if j < len(lines) and lines[j].startswith(pad) else ""
    if not lead or lead not in string.punctuation:
        return [], i + 1
    block = []
    while j < len(lines) and lines[j].startswith(pad + lead):
        block.append(lines[j][len(pad) :])
        j += 1
    return block, j


RST_COMMENT = re.compile(r"^\s*\.\.(\s|$)")  # explicit markup; «...» opening a sentence is prose


def _rst_code_ranges(text: str) -> list[tuple[int, int, list[str]]]:
    """(first line, end line, body) of each code-block/code/sourcecode directive and `::` literal
    block, in order. Callers drop code BY POSITION: a code line equal to a prose literal
    (``[Install]``, ``freshclam``) must not erase that literal."""
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        ln = lines[i]
        if RST_CODE_DIRECTIVE.match(ln):
            j = i + 1
            while j < len(lines) and re.match(r"^\s+:[\w-]+:", lines[j]):
                j += 1
            block, nxt = _indented_block(lines, j - 1, base=len(ln) - len(ln.lstrip()))
            out.append((i, nxt, block))
            i = nxt
            continue
        if ln.rstrip().endswith("::") and not RST_COMMENT.match(ln):
            block, nxt = _indented_block(lines, i)
            if not block:
                block, nxt = _quoted_block(lines, i)
            if block:
                out.append((i + 1, nxt, block))
                i = nxt
                continue
        i += 1
    return out


GRID_BORDER = re.compile(r"^\s*\+(?:[-=]+\+)+\s*$")


def _grid_cells(lines: list[str], i: int) -> tuple[list[tuple[int, str]], int]:
    """(row's first line, cell text) of the grid table opening at line i, row by row and left to
    right as docutils orders them, and the line after the table. Spanning cells are read as
    their columns: none of upstream's code-holding tables spans."""
    cols = [k for k, c in enumerate(lines[i].rstrip()) if c == "+"]
    rows, cur, first, j = [], [[] for _ in cols[1:]], i + 1, i + 1
    while j < len(lines) and lines[j].strip().startswith(("|", "+")):
        if GRID_BORDER.match(lines[j]):
            rows += [(first, textwrap.dedent("\n".join(c))) for c in cur]
            cur, first = [[] for _ in cols[1:]], j + 1
        else:
            for k in range(len(cols) - 1):
                cur[k].append(lines[j][cols[k] + 1 : cols[k + 1]].rstrip())
        j += 1
    return rows, j


def rst_code_blocks(text: str) -> list[str]:
    """Contents of code-block/code/sourcecode directives and `::` literal blocks, in order,
    those inside grid-table cells included (developer WebDAV/basic)."""
    found = [(start, normalize_code(block)) for start, _, block in _rst_code_ranges(text)]
    lines, i = text.split("\n"), 0
    while i < len(lines):
        if GRID_BORDER.match(lines[i]):
            cells, i = _grid_cells(lines, i)
            found += [(start, code) for start, cell in cells for code in rst_code_blocks(cell)]
        else:
            i += 1
    return [code for _, code in sorted(found, key=lambda x: x[0])]


def normalize_code(block: list[str]) -> str:
    return "\n".join(ln.rstrip() for ln in block).strip("\n")


def rst_inline_literals(text: str) -> list[str]:
    lines = _without_code_blocks_rst(text).split("\n")
    # a title's backtick adornment («`````````», developer basics/events) is no literal; a
    # Markdown fence in prose is one, as docutils renders it (weave contract)
    for style, _, at in _rst_titles(text):
        lines[at + 1] = ""
        if style[0] == "o":
            lines[at - 1] = ""
    return [" ".join(x.split()) for x in RST_INLINE_LITERAL.findall("\n".join(lines))]


DROPPED_DIRECTIVE = re.compile(r"^(\s*)\.\.\s+(?:mermaid|graphviz|raw)::")
# a comment: «.. text» that is no directive, target, substitution or footnote («.. code-block: php»)
COMMENT_BLOCK = re.compile(r"^(\s*)\.\.\s+(?![_|\[])(?![\w:+.-]+::)\S")


def _without_code_blocks_rst(text: str) -> str:
    """The text with every code line blanked in place (line count and paragraph breaks kept),
    and the bodies of the directives the contract drops (diagrams, raw HTML) and of comments:
    none is prose."""
    lines = text.split("\n")
    for start, end, _ in _rst_code_ranges(text):
        lines[start:end] = [""] * (end - start)
    for i in [i for i, ln in enumerate(lines) if DROPPED_DIRECTIVE.match(ln) or COMMENT_BLOCK.match(ln)]:
        _, end = _indented_block(lines, i)
        lines[i:end] = [""] * (end - i)
    return "\n".join(lines)


def _urls(paragraphs: list[str]) -> set[str]:
    """Every http(s) URL in prose: inline, embedded, autolinked or bare (trailing punctuation off)."""
    return {m.rstrip(".,;:*'") for p in paragraphs for m in URL.findall(p)}  # «**url**», «'url'»: markup


RST_REL_LINK = re.compile(r"`[^`<]*<([^>`\s:]+)>`__?")


def link_target(docname: str, target: str, cfg: dict | None = None) -> str:
    """Where a relative embedded link points: upstream's built site, beside the doc's own page
    (`<../../_static/openapi.html>` from developer client_apis/OCS/index)."""
    cfg = cfg or config()
    manual, path = docname.split("/", 1)
    base = cfg["source"]["external"][manual].split("{path}")[0].format(major=major(cfg))
    return base + posixpath.normpath(posixpath.join(posixpath.dirname(path), target))


def rst_links(text: str, docname: str = "", cfg: dict | None = None) -> set[str]:
    """External URLs: `text <url>`_, named targets (`.. _Name: url`) and bare URLs in prose; with
    `docname`, a relative embedded link too, as the address it points to (link_target), and a
    visible toctree's URL entry (`Title <url>`), which Sphinx lists as a link.
    An embedded URL that wraps a line is one URL: docutils drops the line break."""
    text = RST_EXT_LINK.sub(lambda m: m.group(0).replace(m.group(1), re.sub(r"\s+", "", m.group(1))), text)
    relative = {link_target(docname, t, cfg) for t in RST_REL_LINK.findall(text)
                if docname and not t.endswith("_") and not t.startswith("#")}
    return (
        relative
        | set(RST_EXT_LINK.findall(text))
        | set(RST_NAMED_TARGET.findall(text))
        | {m for body in TOCTREE.findall(text + "\n") if ":hidden:" not in body for m in TOCTREE_URL.findall(body)}
        # an embedded URL is read whole above; its «)» or «#…» never reaches the bare-URL scan
        | _urls(rst_paragraphs(re.sub(r"<https?://[^>]+>", " ", text)))
    )


TOCTREE = re.compile(r"^[ \t]*\.\. toctree::[^\n]*\n((?:[ \t]+[^\n]*\n|[ \t]*\n)*)", re.M)
TOCTREE_URL = re.compile(r"^[ \t]+(?:[^<\n]*<)?(https?://[^>\s]+)>?[ \t]*$", re.M)


_ALL_DOCS: list[str] | None = None


def _all_docs() -> list[str]:
    """Every upstream docname, once; empty without a clone (a glob then names nothing)."""
    global _ALL_DOCS
    if _ALL_DOCS is None:
        _ALL_DOCS = docnames() if (upstream_dir() / ".git").exists() else []
    return _ALL_DOCS


def _glob(pattern: str) -> re.Pattern:
    """Sphinx's toctree glob: «*» and «?» never cross a «/»."""
    return re.compile("".join("[^/]*" if c == "*" else "[^/]" if c == "?" else re.escape(c) for c in pattern) + "$")


def rst_toctree(text: str, docname: str, all_docs: list[str] | None = None) -> list[str]:
    """Absolute docnames a visible toctree lists, in order. Upstream renders a toctree as a list
    of links on the page, so the woven page carries that list; a :hidden: toctree shows nothing,
    `self` and URLs name no document. Under :glob:, a pattern lists every matching document as
    Sphinx does: sorted, minus the toctree's own page and the entries already listed."""
    out = []
    for body in TOCTREE.findall(text + "\n"):
        lines = [ln.strip() for ln in body.split("\n") if ln.strip()]
        if ":hidden:" in lines:
            continue
        glob, seen = ":glob:" in lines, {docname}
        for ln in lines:
            if ln.startswith(":"):
                continue
            target = re.sub(r"\.rst$", "", re.sub(r"^[^<]*<([^>]+)>$", r"\1", ln).strip())  # Sphinx drops the suffix
            if target == "self" or "://" in target:
                continue
            if "*" in target or "?" in target:
                if glob:
                    pat = _glob(absolute_doc(docname, target))
                    hits = [d for d in sorted(_all_docs() if all_docs is None else all_docs)
                            if pat.match(d) and d not in seen]
                    seen.update(hits)
                    out += hits
                continue
            doc = absolute_doc(docname, target)
            seen.add(doc)
            out.append(doc)
    return out


def rst_xrefs(text: str, docname: str) -> list[tuple[str, str]]:
    """(kind, target) of every :doc: and :ref: and every visible toctree entry, :doc: targets
    made absolute docnames."""
    out = [("doc", t) for t in rst_toctree(text, docname)]
    for kind, content in RST_ROLE.findall(text):
        m = re.match(r"(?s)^(.*?)\s*<([^<>]+)>$", content)
        target = (m.group(2) if m else content).strip()
        if kind == "doc":
            target = absolute_doc(docname, target)
        else:
            target = target.lower()
        out.append((kind, target))
    return out


def absolute_doc(docname: str, target: str) -> str:
    manual = docname.split("/", 1)[0]
    if target.startswith("/"):
        return f"{manual}{target}"
    base = docname.rsplit("/", 1)[0]
    parts = []
    for p in f"{base}/{target}".split("/"):
        if p == "..":
            if len(parts) > 1:  # each manual is its own Sphinx project: «..» stops at its root
                parts.pop()
        elif p and p != ".":
            parts.append(p)
    return "/".join(parts)


def rst_paragraphs(text: str) -> list[str]:
    """Prose paragraphs, list markers stripped and whitespace collapsed — the shape Sphinx
    gettext extracts as msgids."""
    out, cur = [], []
    for ln in _without_code_blocks_rst(text).split("\n") + [""]:
        s = ln.strip()
        if (
            not s
            or ADORN.match(s)
            or s.startswith(".. ")
            or s == ".."  # an empty comment
            or re.match(r"^:[^:`\s][^:`]*:(\s|$)", s)  # a field or option; a role (:code:`…`) is text
        ):
            if cur:
                out.append(" ".join(" ".join(cur).split()))
                cur = []
            continue
        cur.append(re.sub(r"^(?:[-*+]|#\.|\d+\.)\s+", "", s))
    return [p for p in out if p]


# ------------------------------------------------------------------- catalogs


def catalog(updir: Path, docname: str, cfg: dict | None = None) -> dict[str, str]:
    """msgid → msgstr (both whitespace-collapsed) of the official Spanish catalog, user manual only."""
    cfg = cfg or config()
    manual, path = docname.split("/", 1)
    if manual != "user_manual":
        return {}
    f = updir / cfg["source"]["catalog"].format(path=path)
    if not f.is_file():
        return {}
    out = {}
    for block in re.split(r"\n\s*\n", f.read_text(encoding="utf-8", errors="replace")):
        mid = re.search(r"^msgid (.*?)(?=^msgstr )", block, re.S | re.M)
        mst = re.search(r"^msgstr (.*)", block, re.S | re.M)
        if not mid or not mst:
            continue
        a, b = _po_string(mid.group(1)), _po_string(mst.group(1))
        if a:
            out[" ".join(a.split())] = " ".join(b.split())
    return out


def _po_string(raw: str) -> str:
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', raw)
    return "".join(parts).replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")


# ------------------------------------------------------------------- MyST, the woven side

FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})(.*)$")  # any indent: fences nest in list items
BLOCK_OPEN = re.compile(r"^[ \t]{0,3}(`{3,})\{upstream\}\s+(\S+)\s*$")
BLOCK_ARG = re.compile(
    r"^(?P<doc>(?:user|admin|developer)_manual/[A-Za-z0-9_./-]+?)\.rst"
    r"@(?P<sha>[0-9a-f]{7,40})(?:#(?P<anchor>[A-Za-z0-9_.-]+))?$"
)
MYST_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
# a role or a code span, opened and closed by the same run of one or two backticks (CommonMark:
# ``` `` ` x ` `` ``` holds a backtick); may wrap a line
MYST_SPAN = re.compile(r"(\{[\w-]+\})?(?<!`)(``?)(?!`)((?:[^\n]|\n(?!\s*\n))+?)(?<!`)\2(?!`)")
MYST_ROLE = re.compile(r"\{nc-(doc|ref)\}`(?:[^`<]*<([^>]+)>|([^`]+))`")
MYST_LABEL = re.compile(r"^\(nc-([^)]+)\)=\s*$")


def blocks(markdown: str) -> list[dict]:
    """Every {upstream} block of a page: its argument parts, options and raw content."""
    lines, out, i = markdown.split("\n"), [], 0
    while i < len(lines):
        m = BLOCK_OPEN.match(lines[i])
        if not m:
            i += 1
            continue
        fence, arg, start = m.group(1), m.group(2), i
        i += 1
        options = {}
        while i < len(lines) and (om := re.match(r"^:([\w-]+):\s*(.*)$", lines[i])):
            options[om.group(1)] = om.group(2).strip()
            i += 1
        body = []
        while i < len(lines):
            fm = FENCE.match(lines[i])
            if (
                fm
                and fm.group(1)[0] == "`"
                and len(fm.group(1)) >= len(fence)
                and not fm.group(2).strip()
            ):
                break
            body.append(lines[i])
            i += 1
        am = BLOCK_ARG.match(arg)
        out.append(
            {
                "arg": arg,
                "line": start + 1,
                "options": options,
                "content": "\n".join(body),
                "doc": am.group("doc") if am else None,
                "sha": am.group("sha") if am else None,
                "anchor": (am.group("anchor") or "") if am else None,
            }
        )
        i += 1
    return out


def myst_code_blocks(content: str) -> list[str]:
    lines, out, i = content.split("\n"), [], 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        fence, body = m.group(1), []
        indent = len(lines[i]) - len(lines[i].lstrip())  # the body loses the fence's indent
        i += 1
        while i < len(lines):
            fm = FENCE.match(lines[i])
            if (
                fm
                and fm.group(1)[0] == fence[0]
                and len(fm.group(1)) >= len(fence)
                and not fm.group(2).strip()
            ):
                break
            ln = lines[i]
            body.append(ln[min(indent, len(ln) - len(ln.lstrip())):])
            i += 1
        i += 1
        out.append(normalize_code(body))
    return out


def fence_walk(lines: list[str]):
    """(line, fenced) per line: fenced is True on a code fence's own lines and on the lines it
    holds. A fence closes only on the same character, at least as long, with nothing after it."""
    opener = None
    for ln in lines:
        m = FENCE.match(ln)
        if opener is None:
            if m:
                opener = m.group(1)
            yield ln, bool(m)
        else:
            if m and m.group(1)[0] == opener[0] and len(m.group(1)) >= len(opener) \
                    and not m.group(2).strip():
                opener = None
            yield ln, True


def _without_fences(content: str) -> str:
    """The page outside code fences, a «%» comment line blanked: MyST renders it as nothing."""
    return "\n".join("" if ln.lstrip().startswith("%") else ln
                     for ln, fenced in fence_walk(content.split("\n")) if not fenced)


MYST_GUILABEL = re.compile(r"\{guilabel\}`([^`]+)`")


def myst_guilabels(content: str) -> list[str]:
    return MYST_GUILABEL.findall(_without_fences(content))


_UI: dict | None = None


def ui_strings() -> dict[str, set[str]]:
    """English UI string → the Spanish the interface shows: glosario.yml (server strings) and the
    l10n/es.json of every app the suite ships, read from the exact tarballs gestion installs
    (provisioning/apps/*/*.tar.gz), and of the server and every app it bundles (server_dir()).
    Without those checkouts, the glossary alone."""
    global _UI
    if _UI is None:
        out: dict[str, set[str]] = {}
        for t in (yaml.safe_load((ROOT / "glosario.yml").read_text(encoding="utf-8")) or {}).get("terms", []):
            out.setdefault(t["en"], set()).add(t["es"])
        srv = server_dir()
        for f in sorted(srv.glob("apps/*/l10n/es.json")) + sorted(srv.glob("core/l10n/es.json")):
            for en, es in json.loads(f.read_text(encoding="utf-8")).get("translations", {}).items():
                if isinstance(es, str) and es.strip():
                    out.setdefault(en, set()).add(es)
        for tgz in sorted((org_root() / "gestion" / "provisioning" / "apps").glob("*/*.tar.gz")):
            with tarfile.open(tgz) as tf:
                for m in tf.getmembers():
                    if m.name.endswith("/l10n/es.json") and m.name.count("/") == 2:
                        data = json.load(tf.extractfile(m)).get("translations", {})
                        for en, es in data.items():
                            if isinstance(es, str) and es.strip():
                                out.setdefault(en, set()).add(es)
        _UI = out
    return _UI


def bare_urls(content: str) -> list[str]:
    """URLs written as plain text outside code: with no linkify on this site they render
    unclickable, so the contract writes them as autolinks <url>."""
    text = _without_fences(content)
    text = re.sub(r"`[^`\n]*`", " ", text)  # code spans
    text = re.sub(r"<https?://[^>\s]+>", " ", text)  # autolinks
    text = re.sub(r"\]\(https?://[^)\s]*\)", "]", text)  # [text](url)
    text = re.sub(r"(?m)^\[[^\]\n]+\]:\s*\S+", " ", text)  # [Name]: url
    # a host never starts with «[» or «<»: `http://[user@pass:]<server>` is an argument shape
    return [m.rstrip(".,;:*'") for m in URL.findall(text) if re.match(r"https?://\w", m)]


def myst_headings(content: str) -> list[tuple[int, str]]:
    return [
        (len(m.group(1)), m.group(2))
        for ln in _without_fences(content).split("\n")
        if (m := MYST_HEADING.match(ln))
    ]


def myst_inline_literals(content: str) -> list[str]:
    """Inline code spans; a {role}`…` span is not code. One left-to-right scan, so a brace inside
    a code span (`Call {user}`) can never open a role."""
    return [
        " ".join(code.split())
        for role, _, code in MYST_SPAN.findall(_without_fences(content))
        if not role
    ]


def myst_links(content: str) -> set[str]:
    """External URLs anywhere outside code fences: [text](url), <url>, reference definitions,
    table cells and bare URLs."""
    text = _without_fences(content)
    # inside <…> a URL is whole, «)» included (…#L52-L74)); bare URLs end at markup. A <url> inside
    # a code span is code (the Link header in client_apis/activity-api), as rst_links reads it
    autolinks = re.findall(r"<(https?://[^>\s]+)>", MYST_SPAN.sub(" ", text))
    return set(autolinks) | _urls([re.sub(r"<https?://[^>\s]+>", " ", text)])


def myst_xrefs(content: str) -> list[tuple[str, str]]:
    return [
        (
            kind,
            (explicit or bare).strip().lower()
            if kind == "ref"
            else (explicit or bare).strip(),
        )
        for kind, explicit, bare in MYST_ROLE.findall(content)
    ]


def myst_labels(content: str) -> list[str]:
    return [
        m.group(1).strip().lower()
        for ln in content.split("\n")
        if (m := MYST_LABEL.match(ln))
    ]


def myst_paragraphs(content: str) -> list[str]:
    out, cur = [], []
    for ln in _without_fences(content).split("\n") + [""]:
        s = ln.strip()
        if (
            not s
            or MYST_HEADING.match(s)
            or MYST_LABEL.match(s)
            or s.startswith(("|", ":::", ":"))
        ):
            if cur:
                out.append(" ".join(" ".join(cur).split()))
                cur = []
            continue
        cur.append(re.sub(r"^(?:[-*+]|\d+\.)\s+", "", s))
    return [p for p in out if p]


# ------------------------------------------------------------------- comparison helpers


def plain(text: str) -> str:
    """Markup-free, whitespace-collapsed text: what the reader sees, for msgstr comparison."""
    t = re.sub(
        r":(?:[\w-]+:)?[\w-]+:`([^`<]*?)\s*<[^>]+>`", r"\1", text
    )  # :role:`text <target>`
    t = re.sub(r":(?:[\w-]+:)?[\w-]+:`([^`]+)`", r"\1", t)  # :role:`text`
    t = re.sub(r"\{[\w-]+\}`([^`<]*?)\s*<[^>]+>`", r"\1", t)  # {role}`text <target>`
    t = re.sub(r"\{nc-(?:doc|ref)\}`[^`<]+`", "", t)  # a bare link shows its target's title, not this
    t = re.sub(r"\{[\w-]+\}`([^`]+)`", r"\1", t)  # {role}`text`
    t = re.sub(r"`([^`<]*?)\s*<[^>]+>`__?", r"\1", t)  # `text <url>`_
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)  # [text](url)
    t = re.sub(r"\[([^\]]*)\]\[[^\]]*\]", r"\1", t)  # [text][Name]
    t = re.sub(r"<(https?://[^>\s]+)>", r"\1", t)  # <url>
    t = re.sub(r"``(.+?)``", r"\1", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"(?<=\w)__?(?=[\s.,;:)]|$)", "", t)  # `Name`_ and Name_ (named references)
    t = re.sub(r"\*\*(.+?)\*\*|\*(.+?)\*", lambda m: m.group(1) or m.group(2), t)
    t = " ".join(t.split())
    # RST's literal-block marker: "text::" reads "text:", "text ::" and a bare "::" read nothing
    return re.sub(r"(?<=\S)::$", ":", re.sub(r"\s*(?<!\S)::$", "", t))


EN_STOPWORDS = {
    "the",
    "and",
    "of",
    "to",
    "is",
    "are",
    "with",
    "for",
    "you",
    "your",
    "this",
    "that",
    "be",
    "on",
    "in",
    "can",
    "will",
    "it",
    "or",
    "an",
    "by",
    "from",
    "if",
    "as",
    "not",
}


def reads_english(paragraph: str) -> bool:
    """Untranslated prose, word by word: an English function word (EN_STOPWORDS) left in the
    text. Not prose: code, «quoted» messages (upstream quotes some UI and error strings in English
    only, and the contract keeps them), *italics* (identifiers, log lines), an all-caps keyword
    (FROM, SQL), [Name]: url definitions, and a word inside a capitalised run, which is a name
    or a title («Extra Packages for Enterprise Linux», «The Movie Database»)."""
    code_free = MYST_SPAN.sub(lambda m: m.group(0) if m.group(1) else " ", paragraph)
    code_free = re.sub(r"(?<![*\w])\*(?!\*)[^*\n]+?(?<!\*)\*(?![*\w])", " ", code_free)
    code_free = re.sub(r"(?m)^\s*\[[^\]\n]+\]:\s*\S+.*$", " ", code_free)  # [Name]: url definitions
    # quotes, URLs, addresses, PHP written as text ($this->inc('x')), command-line flags (-it, --force)
    text = re.sub(r"«[^»]*»|<?https?://\S+|\S+@\S+|\$\w+(?:->\w+|\([^)]*\))*|(?<![\w-])--?\w[\w-]*", " ", plain(code_free))
    # a hyphenated compound is one word (plug-and-play, AGPL-3.0-or-later)
    words = re.findall(r"[A-Za-zÁÉÍÓÚÑÜáéíóúñü0-9]+(?:[-_.:/][A-Za-zÁÉÍÓÚÑÜáéíóúñü0-9]+)*", text)
    for i, w in enumerate(words):
        if w.lower() in EN_STOPWORDS and not (len(w) > 1 and w.isupper()):
            before = i > 0 and words[i - 1][0].isupper()
            after = i < len(words) - 1 and words[i + 1][0].isupper()
            # «Packages for Enterprise»; a capitalised one opens or closes a title («The Movie Database»)
            name = (before and after) or (w[0].isupper() and (before or after))
            if not name:
                return True
    return False


def make_id(title: str) -> str:
    """docutils' id shape: lowercase ASCII, runs of anything else become one hyphen."""
    t = title.lower().translate(str.maketrans("áéíóúñü", "aeiounu"))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")
