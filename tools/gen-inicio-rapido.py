#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Generador de inicio rápido: README de registro → páginas incluidas.

Recorre la nómina de catalogo.yml (menos `documentation`, que es este sitio)
y busca en el README de registro de cada repositorio la sección H2
«Inicio rápido de desarrollo» (H2 solamente, tolerante a tilde). Cada acierto
se emite como `_generated/inicio-rapido/<slug>.md`: una página MyST cuyo
cuerpo es un `{include}` del tramo `[línea del título .. línea del siguiente
H2)` con `:start-line:`/`:end-line:` — los límites derivan de números de
línea recalculados en cada compilación, así que la deriva del README de
origen no rompe la página. El índice
`_generated/inicio-rapido/index.md` se emite SIEMPRE: toctree sobre los
acierto cuando hay al menos uno; sin directiva toctree (un toctree vacío es
fatal con -W) y con la frase de degradación cuando no hay ninguno.

El README de registro es la clave opcional `readme` de cada fila (por
defecto `README.md`; IntraVox registra `.github/README.md`), resuelto
bajo `${APS_ORG_ROOT:-/opt/aps-conecta-org}` — sin rutas alternativas: si
no existe, el repositorio se omite con línea de bitácora. Fallos duros
(exit 1, nombrando el repositorio): clon ausente, fila malformada o hub
`desarrollo/<slug>.md` ausente. Determinista: sin marcas de tiempo.
"""
from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path

import yaml

import upstreamlib as u

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOGO = REPO_ROOT / "catalogo.yml"
OUT_DIR = REPO_ROOT / "_generated" / "inicio-rapido"
ORG_ROOT = Path(os.environ.get("APS_ORG_ROOT", "/opt/aps-conecta-org"))
EXCLUDED = "documentation"  # este sitio: su propio README no es contenido de desarrollo

# H2 solamente: dos almohadillas exactas, «rápido» con o sin tilde.
HEADING_RE = re.compile(r"^##\s+Inicio r[áa]pido de desarrollo\s*$")
NEXT_H2_RE = re.compile(r"^##\s")

# Repositorios cuya sección de inicio rápido el sitio no puede perder: si un README
# la retira o la traduce, la compilación falla (la página es la puerta de entrada
# de quien desarrolla sobre ese repositorio).
REQUIRED = {"aps-common", "Databases", "epidemiologia", "estadistica", "farmacia"}


def fail(msg: str) -> None:
    print(f"[inicio-rapido] ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def note(msg: str) -> None:
    print(f"[inicio-rapido] {msg}")


def slug_for(repo: str) -> str:
    """Regla de slug de los hubs (Fase 3): repo.lower(); `.github` → github-org."""
    return "github-org" if repo == ".github" else repo.lower()


def load_roster() -> list[dict]:
    """catalogo.yml → filas menos `documentation`, validando lo consumido."""
    try:
        doc = yaml.safe_load(CATALOGO.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"no existe {CATALOGO}")
    except (yaml.YAMLError, UnicodeDecodeError) as exc:
        fail(f"catalogo.yml no parsea: {exc}")
    rows = doc.get("repos") if isinstance(doc, dict) else None
    if not isinstance(rows, list) or not rows:
        fail("catalogo.yml: falta la lista `repos`")
    roster: list[dict] = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("repo"), str) or not row["repo"].strip():
            fail(f"fila malformada en catalogo.yml: {row!r}")
        readme = row.get("readme", "README.md")
        if not isinstance(readme, str) or not readme.strip():
            fail(f"fila {row['repo']}: clave `readme` malformada: {readme!r}")
        if row["repo"] != EXCLUDED:
            roster.append({"repo": row["repo"], "readme": readme})
    return roster


def scan(repo: str, readme: Path) -> tuple[int, int] | None:
    """Tramo [título .. siguiente H2) en líneas 1-basadas, o None si no hay título."""
    try:
        lines = readme.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        fail(f"{repo}: no se puede leer {readme}: {exc}")
    for i, line in enumerate(lines):
        if HEADING_RE.match(line):
            end = len(lines) + 1  # hasta el fin del archivo…
            for j in range(i + 1, len(lines)):
                if NEXT_H2_RE.match(lines[j]):
                    end = j + 1  # …o exclusivo en el siguiente H2
                    break
            return i + 1, end
    return None


def classify(row: dict) -> tuple[str, Path, tuple[int, int] | None]:
    """'missing' | 'no-heading' | 'hit', con el README y el tramo cuando acierta."""
    repo = row["repo"]
    clone = ORG_ROOT / repo
    if not clone.is_dir():
        fail(f"checkout ausente: {clone}")
    hub = REPO_ROOT / "desarrollo" / f"{slug_for(repo)}.md"
    if not hub.is_file():
        fail(f"hub ausente para {repo}: {hub}")
    readme = clone / row["readme"]
    if not readme.is_file():
        return "missing", readme, None
    span = scan(repo, readme)
    if span is None:
        return "no-heading", readme, None
    return "hit", readme, span


def span_reads_english(span_text: str) -> str | None:
    """El primer párrafo del tramo que se lee como inglés, o None. Un inicio
    rápido publicado en español que un README reescribe en inglés rompe la
    página que lo incluye: se detecta antes de emitir."""
    for paragraph in u.myst_paragraphs(span_text):
        if u.reads_english(paragraph):
            first = paragraph.strip().splitlines()[0]
            return first[:120]
    return None


def emit_page(repo: str, readme: Path, span: tuple[int, int]) -> None:
    """Página por acierto: front matter, H1 sintetizado y el tramo incluido."""
    heading_ln, end_ln = span
    rel = os.path.relpath(os.path.abspath(readme), os.path.abspath(OUT_DIR))
    page = (
        "---\n"
        "tipo: guia\n"
        "---\n"
        "\n"
        f"# Inicio rápido — {repo}\n"
        "\n"
        "El texto proviene del README de registro del repositorio, incluido al momento de compilar el sitio.\n"
        "\n"
        f"```{{include}} {rel}\n"
        f":start-line: {heading_ln - 1}\n"
        f":end-line: {end_ln}\n"
        "```\n"
    )
    (OUT_DIR / f"{slug_for(repo)}.md").write_text(page, encoding="utf-8")


def emit_index(hits: list[str]) -> None:
    """Índice siempre emitido: toctree con aciertos, o la frase de degradación."""
    page = (
        "---\n"
        "tipo: guia\n"
        "---\n"
        "\n"
        "# Inicio rápido de desarrollo\n"
        "\n"
    )
    if hits:
        page += (
            "Secciones de arranque por repositorio, incluidas de los README de registro del catálogo.\n"
            "\n"
            "```{toctree}\n"
            ":maxdepth: 1\n"
            "\n"
        )
        for repo in hits:
            page += f"{repo} <{slug_for(repo)}>\n"
        page += "```\n"
    else:
        page += "Ningún repositorio del catálogo declara aún la sección.\n"
    (OUT_DIR / "index.md").write_text(page, encoding="utf-8")


def main() -> int:
    roster = load_roster()
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)
    hits: list[str] = []
    for row in roster:
        kind, readme, span = classify(row)
        if kind == "missing":
            note(f"omitido {row['repo']}: {row['readme']} no existe")
        elif kind == "no-heading":
            note(f"omitido {row['repo']}: {row['readme']} sin sección «Inicio rápido de desarrollo»")
        else:
            assert span is not None
            heading_ln, end_ln = span
            span_text = "\n".join(
                readme.read_text(encoding="utf-8").splitlines()[heading_ln - 1 : end_ln - 1])
            english = span_reads_english(span_text)
            if english is not None:
                fail(f"{row['repo']}: un párrafo del inicio rápido se lee como inglés: «{english}»")
            emit_page(row["repo"], readme, span)
            note(f"incluido {row['repo']}: {row['readme']}:{span[0]}-{span[1] - 1}")
            hits.append(row["repo"])
    perdidos = REQUIRED - set(hits)
    if perdidos:
        fail(f"inicio rápido ausente en {sorted(perdidos)}: su README perdió la sección "
             "«Inicio rápido de desarrollo» o el clon está ausente bajo APS_ORG_ROOT")
    emit_index(hits)
    note(f"{len(hits)}/{len(roster)} incluyen; {len(roster) - len(hits)} omitidos")
    return 0



if __name__ == "__main__":
    sys.exit(main())
