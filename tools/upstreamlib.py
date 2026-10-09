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

import os
import re
import subprocess
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "upstream.yml"


# ------------------------------------------------------------------- configuration


@lru_cache(maxsize=1)
def config() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def dead_links(cfg: dict | None = None) -> list[str]:
    """Upstream URLs that no longer answer: kept byte-identical in the woven text, skipped by
    linkcheck (conf.py). An entry leaves the list when upstream fixes the link."""
    return [d["url"] for d in (cfg or config()).get("dead_links") or []]


def dead_anchors(cfg: dict | None = None) -> list[str]:
    """Pages upstream links into whose anchor no longer exists (the page answers): linkcheck skips
    the anchor on these base URLs only (conf.py)."""
    return [d["url"].partition("#")[0] for d in (cfg or config()).get("dead_anchors") or []]


def org_root() -> Path:
    return Path(os.environ.get("APS_ORG_ROOT", "/opt/aps-conecta-org"))


def upstream_dir() -> Path:
    """The sparse clone tools/fetch-upstream.sh maintains."""
    return Path(os.environ.get("UPSTREAM_DIR", ROOT / "_generated" / "upstream"))


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
    """The upstream RST of `docname` at `sha` (a partial clone fetches the blob on demand)."""
    return git(updir, "show", f"{sha}:{docname}.rst")


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
    return re.compile(rf"\b{word}\b{guard}")


def rename(text: str, cfg: dict | None = None) -> str:
    """«Nextcloud» → «APS Conecta Gestión», except inside the legal/product names `keep` lists."""
    cfg = cfg or config()
    return _rename_re(cfg).sub(cfg["rename"]["to"], text)


def leftovers(text: str, cfg: dict | None = None) -> list[str]:
    cfg = cfg or config()
    return [
        text[max(0, m.start() - 30) : m.end() + 30]
        for m in _rename_re(cfg).finditer(text)
    ]


# ------------------------------------------------------------------- RST, the upstream side

ADORN = re.compile(r"^([=\-~^\"'`#*+_:.<>])\1{2,}\s*$")
LABEL = re.compile(r"^\.\.\s+_([^:`]+):\s*$")
RST_CODE_DIRECTIVE = re.compile(r"^(\s*)\.\.\s+(?:code-block|code|sourcecode)::.*$")
RST_INLINE_LITERAL = re.compile(r"``(.+?)``")
RST_EXT_LINK = re.compile(r"`[^`<]*<(https?://[^>]+)>`__?")
RST_NAMED_TARGET = re.compile(r"^\.\. _[^:\n]+:\s*(https?://\S+)\s*$", re.M)
URL = re.compile(r"https?://[^\s<>`\"')\]]+")
RST_ROLE = re.compile(r":(doc|ref):`(?:[^`<]*<([^>]+)>|([^`]+))`")


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


def rst_labels(text: str) -> list[tuple[str, int]]:
    """(label, line index) of every `.. _label:` target."""
    return [
        (m.group(1).strip().lower(), i)
        for i, ln in enumerate(text.split("\n"))
        if (m := LABEL.match(ln))
    ]


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


def _indented_block(lines: list[str], i: int) -> tuple[list[str], int]:
    """The indented block starting after line i (blank lines allowed inside)."""
    j = i + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    if j >= len(lines) or not lines[j][:1].isspace():
        return [], i + 1
    indent = len(lines[j]) - len(lines[j].lstrip())
    block = []
    while j < len(lines) and (
        not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) >= indent
    ):
        block.append(lines[j][indent:] if lines[j].strip() else "")
        j += 1
    while block and not block[-1]:
        block.pop()
    return block, j


def rst_code_blocks(text: str) -> list[str]:
    """Contents of code-block/code/sourcecode directives and `::` literal blocks, in order."""
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        ln = lines[i]
        if RST_CODE_DIRECTIVE.match(ln):
            j = i + 1
            while j < len(lines) and re.match(r"^\s+:[\w-]+:", lines[j]):
                j += 1
            block, i = _indented_block(lines, j - 1)
            out.append(normalize_code(block))
            continue
        if ln.rstrip().endswith("::") and not ln.lstrip().startswith(".."):
            block, nxt = _indented_block(lines, i)
            if block:
                out.append(normalize_code(block))
                i = nxt
                continue
        i += 1
    return out


def normalize_code(block: list[str]) -> str:
    return "\n".join(ln.rstrip() for ln in block).strip("\n")


def rst_inline_literals(text: str) -> list[str]:
    return RST_INLINE_LITERAL.findall(_without_code_blocks_rst(text))


def _without_code_blocks_rst(text: str) -> str:
    blocks = rst_code_blocks(text)
    for b in blocks:
        for ln in b.split("\n"):
            if ln.strip():
                text = text.replace(ln, "", 1)
    return text


def _urls(paragraphs: list[str]) -> set[str]:
    """Every http(s) URL in prose: inline, embedded, autolinked or bare (trailing punctuation off)."""
    return {m.rstrip(".,;:") for p in paragraphs for m in URL.findall(p)}


def rst_links(text: str) -> set[str]:
    """External URLs: `text <url>`_, named targets (`.. _Name: url`) and bare URLs in prose."""
    return (
        set(RST_EXT_LINK.findall(text))
        | set(RST_NAMED_TARGET.findall(text))
        | _urls(rst_paragraphs(text))
    )


def rst_xrefs(text: str, docname: str) -> list[tuple[str, str]]:
    """(kind, target) of every :doc: and :ref:, :doc: targets made absolute docnames."""
    out = []
    for kind, explicit, bare in RST_ROLE.findall(text):
        target = (explicit or bare).strip()
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
            parts.pop()
        elif p and p != ".":
            parts.append(p)
    return "/".join(parts)


def rst_paragraphs(text: str) -> list[str]:
    """Prose paragraphs, list markers stripped and whitespace collapsed — the shape Sphinx
    gettext extracts as msgids."""
    out, cur = [], []
    code = {ln.strip() for b in rst_code_blocks(text) for ln in b.split("\n") if ln.strip()}
    for ln in text.split("\n") + [""]:
        s = ln.strip()
        if (
            not s
            or ADORN.match(s)
            or s.startswith(".. ")
            or s.startswith(":")
            or s in code
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
MYST_SPAN = re.compile(r"(\{[\w-]+\})?(?<!`)`([^`\n]+)`(?!`)")  # a role or a code span
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


def _without_fences(content: str) -> str:
    lines, keep, opener = content.split("\n"), [], None
    for ln in lines:
        m = FENCE.match(ln)
        if opener is None:
            if m:
                opener = m.group(1)
            else:
                keep.append(ln)
        elif (
            m
            and m.group(1)[0] == opener[0]
            and len(m.group(1)) >= len(opener)
            and not m.group(2).strip()
        ):
            opener = None
    return "\n".join(keep)


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
        code
        for role, code in MYST_SPAN.findall(_without_fences(content))
        if not role
    ]


def myst_links(content: str) -> set[str]:
    """External URLs anywhere outside code fences: [text](url), <url>, reference definitions,
    table cells and bare URLs."""
    return _urls([_without_fences(content)])


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
    """Untranslated prose: English stopwords ≥ 15 % of 8+ words. A quoted message («…» or "…")
    is not prose: upstream quotes some UI and error strings in English only."""
    text = re.sub(r"«[^»]*»|\"[^\"]*\"|“[^”]*”", " ", plain(paragraph))
    words = re.findall(r"[a-záéíóúñü]+", text.lower())
    if len(words) < 8:
        return False
    return sum(w in EN_STOPWORDS for w in words) / len(words) >= 0.15


def make_id(title: str) -> str:
    """docutils' id shape: lowercase ASCII, runs of anything else become one hyphen."""
    t = title.lower().translate(str.maketrans("áéíóúñü", "aeiounu"))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")
