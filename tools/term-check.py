#!/usr/bin/env python3
"""term-check — one Spanish across the site (iniciativa scribe, S5).

Fails on:
- a variant glosario.yml lists under `evitar` (terms and tecnicos), anywhere in prose;
- an {upstream} block whose upstream section uses a `tecnicos` term the block does not carry in
  its approved form `es` (`re`, when given, is how the English term is matched);
- tuteo or vosotros: the register is formal, direct and affirmative, «usted» or impersonal, on
  every paragraph, an official Transifex msgstr included (owner, 2026-10-10; upstream-fidelity
  then stops demanding that msgstr verbatim).
Prose excludes code, roles ({guilabel} is the interface's own wording), URLs and «quoted» text
(a message or an example someone types): upstreamlib.prose / style_problems.

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
prose = u.prose  # the tests and the corpus tools read prose the way the gate does


def check_page(text: str, gl: dict, source_of) -> list[str]:
    """source_of(block) → (upstream section RST, official catalog msgid → msgstr) for a block with a doc."""
    found = [p for para in u.myst_paragraphs(text) for p in u.style_problems(para, gl)]
    for block in u.blocks(text):
        section, cat = source_of(block) if block["doc"] else ("", {})
        found += [p for para in u.myst_paragraphs(block["content"]) for p in u.style_problems(para, gl)]
        # upstream prose as the Spanish side reads its own: no code, roles or quoted text
        up = " ".join(x for x in u.rst_paragraphs(section) if x not in cat)  # an official translation is the translators'
        up = re.sub(r"``.+?``|:[\w:-]+:`[^`]*`|`[^`<]*`(?!_)|\"[^\"\n]*\"|“[^”]*”|\*\*[^*]+\*\*", " ", up)  # **label**
        es = " ".join(prose(p) for p in u.myst_paragraphs(block["content"]) + [h for _, h in u.myst_headings(block["content"])])
        for t in (t for t in gl.get("tecnicos", []) if "en" in t):
            en = re.compile(r"(?<![\w-])" + (t.get("re") or re.escape(t["en"]) + "(?:s|es)?") + r"(?![\w-])", re.I)
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
