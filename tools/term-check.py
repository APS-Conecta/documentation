#!/usr/bin/env python3
"""term-check — one Spanish across the site (iniciativa scribe, S5).

Fails on:
- a variant glosario.yml lists under `evitar` (terms and tecnicos), anywhere in prose;
- an {upstream} block whose upstream section uses a `tecnicos` term the block does not carry in
  its approved form `es` (`re`, when given, is how the English term is matched);
- tuteo or vosotros: the contract's register is «usted» on official strings, impersonal elsewhere.
Prose excludes code, roles ({guilabel} is the interface's own wording), URLs and «quoted» text
(a message or an example someone types). A paragraph that is an official Transifex msgstr is the
translators' wording, which the contract copies verbatim: not ours to check.

    python3 tools/term-check.py [page.md …]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstreamlib as u  # noqa: E402

AUDIENCES = ("usuario", "administracion", "desarrollo")
# unambiguous tú/vosotros forms; «pulsa», «elige», «recuerda» are also usted/él indicatives
REGISTER = re.compile(
    r"\b(?:puedes|tienes|debes|quieres|necesitas|sabes|haces|deberías|podrás|tendrás|asegúrate|"
    r"haz|tú|tu|tus|ti|contigo|vosotr[oa]s|vuestr[oa]s?)\b", re.I)


def prose(paragraph: str) -> str:
    text = u.MYST_SPAN.sub(" ", paragraph)  # code spans and roles
    text = re.sub(r"\]\([^)]*\)|<https?://[^>]+>|https?://\S+", " ", text)
    return re.sub(r"«[^»]*»", " ", u.plain(text))


def _word(s: str) -> re.Pattern:
    return re.compile(r"(?<!\w)" + re.escape(s) + r"(?!\w)", re.I)


def check_paragraph(text: str, gl: dict) -> list[str]:
    out = []
    for t in gl.get("terms", []) + gl.get("tecnicos", []):
        out += [f"«{m.group(0)}» → «{t['es']}» (glosario.yml)" for v in t.get("evitar", []) for m in _word(v).finditer(text)]
    out += [f"«{m.group(0)}»: register is «usted» or impersonal (weave-contract §3)" for m in REGISTER.finditer(text)]
    return out


def official(cat: dict) -> set[str]:
    """The catalog's msgstrs as a page paragraph reads them (plain text, whitespace collapsed)."""
    return {" ".join(u.plain(v).split()) for v in cat.values()}


def check_page(text: str, gl: dict, source_of) -> list[str]:
    """source_of(block) → (upstream section RST, official catalog msgid → msgstr) for a block with a doc."""
    found = [p for para in u.myst_paragraphs(text) for p in check_paragraph(prose(para), gl)]
    for block in u.blocks(text):
        section, cat = source_of(block) if block["doc"] else ("", {})
        mine = official(cat)
        paras = [para for para in u.myst_paragraphs(block["content"]) if " ".join(u.plain(para).split()) not in mine]
        found += [p for para in paras for p in check_paragraph(prose(para), gl)]
        # upstream prose as the Spanish side reads its own: no code, roles or quoted text
        up = " ".join(x for x in u.rst_paragraphs(section) if x not in cat)  # an official translation is the translators'
        up = re.sub(r"``.+?``|:[\w:-]+:`[^`]*`|`[^`<]*`(?!_)|\"[^\"\n]*\"|“[^”]*”", " ", up)
        es = " ".join(prose(p) for p in u.myst_paragraphs(block["content"]))
        for t in (t for t in gl.get("tecnicos", []) if "en" in t):
            en = re.compile(r"(?<!\w)" + (t.get("re") or re.escape(t["en"]) + "(?:s|es)?") + r"(?!\w)", re.I)
            if en.search(up) and not re.search(r"(?<!\w)" + re.escape(t["es"]), es, re.I):
                found.append(f"block line {block['line']}: upstream says «{t['en']}», the block lacks «{t['es']}» (glosario.yml)")
    return found


def main(argv: list[str]) -> int:
    gl = yaml.safe_load((u.ROOT / "glosario.yml").read_text(encoding="utf-8"))
    updir, cfg = u.upstream_dir(), u.config()
    if not (updir / ".git").exists():
        print(f"[term-check] no upstream clone at {updir} — run make upstream", file=sys.stderr)
        return 2

    def source_of(block):
        source = u.show(updir, block["sha"], block["doc"])
        return u.rst_section(source, block["anchor"]), u.catalog(updir, block["doc"], cfg)

    paths = [Path(a) for a in argv] or sorted(p for a in AUDIENCES for p in (u.ROOT / a).rglob("*.md"))
    n = 0
    for path in paths:
        for problem in check_page(path.read_text(encoding="utf-8"), gl, source_of):
            print(f"ERROR {path.relative_to(u.ROOT) if path.is_absolute() else path}: {problem}")
            n += 1
    print(f"[term-check] {len(paths)} page(s); {n} problem(s)")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
