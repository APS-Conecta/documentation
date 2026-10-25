#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""check-structure — every page under the site dirs is typed and skeleton-correct.

A standard-library port of repo-docs' `site-structure` rule (scribe Q24), without
the opt-in marker this repo never needed: the site is what the rule types, so it
always runs. What one page owes: front matter (`tipo`, `audiencia`, `apps`,
`resumen`), `audiencia` equal to its directory, `apps` naming catalog rows, a
`resumen` of at most 160 characters, and the H2 skeleton of its `tipo` — or of
its `esqueleto` override — in order, required ones present, nothing beside them.
index.md pages owe the front matter only; headings inside fences are examples or
a woven block's own structure, never the page's.

Prints `ERROR <file>: <msg>` per finding and exits 1 with any. The shapes live
in SITE_STRUCTURE (the profile constant); the craft that reads them lives here.

    python3 tools/check-structure.py [page.md …]
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# The site_structure shapes of .github/profiles/aps-conecta.json, as a constant: the
# profile is part of the retired repo-docs footprint, and this port owns the shapes.
# '?'-prefixed H2s are optional; the rest are required, in order, nothing else beside.
SITE_STRUCTURE = {
    "dirs": ["usuario/", "administracion/", "desarrollo/", "proyecto/"],
    "keys": ["tipo", "audiencia", "apps", "resumen"],
    "tipos": ["tutorial", "guia", "referencia", "explicacion"],
    "resumen_max": 160,
    "catalog": "catalogo.yml",
    "skeleton_exempt": ["index.md"],
    "skeletons": {
        "guia": ["Objetivo", "Requisitos", "Pasos", "Verificación", "?Problemas frecuentes"],
        "tutorial": ["Objetivo", "Requisitos", "Recorrido", "Resultado"],
        "referencia": ["Resumen", "Tabla", "?Notas"],
        "explicacion": ["Contexto", "Diseño", "Compromisos y límites"],
    },
    "overrides": {
        "plataforma": ["Resumen", "?En APS Conecta Gestión"],
        "borrador": ["Resumen", "?Secciones previstas"],
        "contratos": [
            "Propósito y diseño",
            "?Contratos de componentes y API",
            "?Transiciones de estado",
            "?Taxonomía de errores",
            "?Concurrencia e invariantes",
            "?Dominios de fallo",
            "Deuda técnica y límites",
        ],
    },
}

# Front matter is the LEADING `---` block only: `\A` anchors at byte zero and the pattern is
# only ever matched, never searched, so a `tipo: guia` block quoted mid-page as an example types
# nothing — the page does not declare it about itself. Three regexes, not a YAML parser: stdlib
# only, and the shapes under check are one key and one heading.
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---[ \t]*\n?", re.S)
FM_LINE = re.compile(r"^([a-z_]+):[ \t]*(.*?)[ \t]*$", re.M)
H2 = re.compile(r"^##[ \t]+(.+?)[ \t]*#*[ \t]*$")

# THE single accent-fold seam: every comparison that must read «Documentación» and
# «Documentacion» as the same word folds through here. Accents are typography, not identity —
# but identity only for COMPARISON; facts record the text as written.
_ACCENTS = str.maketrans("áéíóúñü", "aeiounu")


def _fold(text: str) -> str:
    return text.lower().translate(_ACCENTS)


FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})(.*)$")


def _fence_walk(lines):
    """(line, fenced, code, quoted) per line, fences nesting the CommonMark way: a fence closes only on
    the same character, at least as long, with nothing after it; a fence opens inside a MyST
    directive fence (```{name}), never inside a code fence. `fenced`: inside any fence, or a
    fence line itself. `code`: inside a code fence, or a fence line — a directive's text is
    markup, so a woven `{upstream}` block reads as prose while the code it holds does not."""
    stack = []
    for ln in lines:
        m = FENCE.match(ln)
        if m and stack and m.group(1)[0] == stack[-1][0][0] \
                and len(m.group(1)) >= len(stack[-1][0]) and not m.group(2).strip():
            stack.pop()
            yield ln, True, True, any(info.startswith("{upstream}") for _, info in stack)
        elif m and (not stack or stack[-1][1].startswith("{")):
            stack.append((m.group(1), m.group(2).strip()))
            yield ln, True, True, any(info.startswith("{upstream}") for _, info in stack)
        else:
            yield ln, bool(stack), any(not info.startswith("{") for _, info in stack), \
                any(info.startswith("{upstream}") for _, info in stack)


def _h2s(body: str) -> list:
    """H2 headings outside fenced blocks: a heading inside a code block is an example, and one
    inside a directive fence (a woven `{upstream}` block) is that block's own structure. Fences
    nest the CommonMark way — a fence closes only on the same character, at least as long,
    with nothing after it — so a 4-backtick directive may hold 3-backtick code."""
    return [hm.group(1) for ln, fenced, _, _ in _fence_walk(body.split("\n"))
            if not fenced and (hm := H2.match(ln))]


def catalog_repos() -> list:
    """Repo slugs of catalogo.yml, the site's catalog."""
    cat = REPO_ROOT / SITE_STRUCTURE["catalog"]
    if not cat.is_file():
        return []
    return re.findall(r"^\s*-\s*repo:\s*([A-Za-z0-9._-]+)\s*$", cat.read_text(errors="replace"), re.M)


def problems(rel: str, text: str, catalog: list) -> list:
    """What one page under the site dirs owes (scribe Q24): typed front matter whose audiencia
    is its directory, and an H2 skeleton chosen by tipo (or the esqueleto override) whose
    headings appear in order, required ones present, nothing else beside them."""
    cfg = SITE_STRUCTURE
    m = FRONT_MATTER.match(text)
    if not m:
        return ["no front matter"]
    fm = dict(FM_LINE.findall(m.group(1)))
    missing = [k for k in cfg["keys"] if not fm.get(k)]
    if missing:
        return [f"front matter lacks {', '.join(missing)}"]
    out = []
    if fm["tipo"] not in cfg["tipos"]:
        out.append(f"tipo '{fm['tipo']}' is not one of {', '.join(cfg['tipos'])}")
    top = rel.split("/", 1)[0]
    if fm["audiencia"] != top:
        out.append(f"audiencia '{fm['audiencia']}' does not match the directory '{top}'")
    if not (fm["apps"].startswith("[") and fm["apps"].endswith("]")):
        out.append("apps must be a [list]")
    elif catalog:
        apps = [a.strip() for a in fm["apps"][1:-1].split(",") if a.strip()]
        out += [f"apps names '{a}', not in the catalog" for a in apps if a not in catalog]
    if len(fm["resumen"]) > cfg["resumen_max"]:
        out.append(f"resumen is {len(fm['resumen'])} chars (max {cfg['resumen_max']})")
    if rel.rsplit("/", 1)[-1] in cfg["skeleton_exempt"]:
        return out
    if "esqueleto" in fm:
        if fm["esqueleto"] not in cfg["overrides"]:
            return out + [f"esqueleto '{fm['esqueleto']}' is not one of {', '.join(cfg['overrides'])}"]
        name, shape = fm["esqueleto"], cfg["overrides"][fm["esqueleto"]]
    elif fm["tipo"] in cfg["skeletons"]:
        name, shape = fm["tipo"], cfg["skeletons"][fm["tipo"]]
    else:
        return out
    names = [h.lstrip("?") for h in shape]
    folded = [_fold(n) for n in names]
    got = _h2s(text[m.end():])
    pos = -1
    for h in got:
        if _fold(h) not in folded:
            out.append(f"H2 '{h}' is not in the {name} skeleton")
            continue
        i = folded.index(_fold(h))
        if i < pos:
            out.append(f"H2 '{h}' is out of order for {name} ({', '.join(names)})")
        pos = max(pos, i)
    have = {_fold(h) for h in got}
    out += [f"H2 skeleton for {name}: missing '{n}'"
            for n, raw in zip(names, shape) if not raw.startswith("?") and _fold(n) not in have]
    return out


def tracked_pages() -> list:
    """The tracked .md files under the site dirs (git ls-files): never a straggler."""
    dirs = tuple(SITE_STRUCTURE["dirs"])
    out = subprocess.run(["git", "ls-files", "*.md"], cwd=REPO_ROOT, capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"[check-structure] git ls-files failed: {out.stderr.strip()}")
    return [f for f in out.stdout.splitlines() if f.startswith(dirs)]


def main(argv: list[str]) -> int:
    files = argv or tracked_pages()
    catalog = catalog_repos()
    n = 0
    for rel in files:
        text = (REPO_ROOT / rel).read_text(errors="replace")
        for msg in problems(rel, text, catalog):
            print(f"ERROR {rel}: {msg}")
            n += 1
    print(f"[check-structure] {len(files)} page(s); {n} problem(s)")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
