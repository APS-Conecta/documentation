#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Generador del catálogo: catalogo.yml (SSOT) → páginas generadas.

Escribe `_generated/catalogo.md` (página de referencia, 15 filas, tabla de
dependencias) y `_generated/linkcheck-private.txt` (una URL raíz por fila
privada — la semilla de `linkcheck_ignore` en conf.py).

Valida: esquema de filas, nómina (15 filas), paridad con OWN_APPS (el pliegue
case-insensitive de repo-docs census.py: la mitad variable de cada entrada
`nombre=url` de gestion `provisioning/phases/12-apps.sh` se pliega sobre los
nombres canónicos del catálogo) y que cada `manuals` resuelva a un .md
comprometido del árbol. Versiona por cadena (`version:` explícita →
`appinfo/info.xml <version>` → `composer.json`/`package.json` `.version` →
primera entrada versionada de `CHANGELOG.md` → vacío) leyendo los checkouts
bajo `${APS_ORG_ROOT:-/opt/aps-conecta-org}`. La visibilidad se consulta viva
con `gh api orgs/APS-Conecta/repos` (gh en el ambiente; GH_TOKEN nunca en
argv/URL). Determinista: sin marcas de tiempo.

`--selftest` clavija la deriva (nómina, paridad, versiones, visibilidad,
semilla privada) y es explícito — nada lo invoca desde el Makefile.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOGO = REPO_ROOT / "catalogo.yml"
GENERATED = REPO_ROOT / "_generated"
ORG = "APS-Conecta"
ORG_ROOT = Path(os.environ.get("APS_ORG_ROOT", "/opt/aps-conecta-org"))
REGISTRY = ORG_ROOT / "gestion" / "provisioning" / "phases" / "12-apps.sh"

KINDS = {
    "suite",
    "distribution-fork",
    "nextcloud-app",
    "shared-library",
    "data-corpus",
    "canon-engine",
    "agent-prompts",
    "laboratory-app",
    "artifacts-store",
    "org-defaults",
    "docs-site",
}
# El enum `kind` es machine (EN); la página renderiza estas etiquetas y ningún
# valor del enum llega a la superficie construida.
KIND_ES = {
    "suite": "Suite",
    "distribution-fork": "Fork de distribución",
    "nextcloud-app": "Aplicación Nextcloud",
    "shared-library": "Biblioteca compartida",
    "data-corpus": "Corpus de datos",
    "canon-engine": "Motor del canon",
    "agent-prompts": "Prompts de agentes",
    "laboratory-app": "Aplicación de laboratorio",
    "artifacts-store": "Almacén de artefactos",
    "org-defaults": "Valores por defecto de la organización",
    "docs-site": "Sitio de documentación",
}
REQUIRED = ("repo", "kind", "role", "manuals", "depends_on", "status")
OPTIONAL = ("version", "soft_depends_on", "readme")
MANUAL_RE = re.compile(r"^(?:usuario|administracion|desarrollo|proyecto)/[a-z0-9-]+\.md$")
OWN_APPS_RE = re.compile(r'^OWN_APPS="(.*)"$', re.M)
SEMVER_RE = re.compile(r"^#{1,3}\s*\[?\s*v?(\d+(?:\.\d+){2}[0-9A-Za-z.+-]*)", re.M)

# Clavijas de --selftest (deriva viva a 2026-10-07).
PINNED_REPOS = {
    "gestion", "AIO", "IntraVox", "farmacia", "estadistica", "epidemiologia",
    "territorio", "aps-common", "Databases", "repo-docs", "agents",
    "pi-sandbox", "rpiv-artifacts", ".github", "documentation",
}
PINNED_APPS = {"epidemiologia", "farmacia", "territorio", "IntraVox", "estadistica"}
PINNED_VERSIONS = {
    "gestion": "0.3.0",
    "AIO": "",
    "IntraVox": "3.1.7",
    "farmacia": "0.11.1",
    "estadistica": "0.1.0",
    "epidemiologia": "0.11.3",
    "territorio": "0.77.0",
    "aps-common": "1.0.0",
    "Databases": "",
    "repo-docs": "",
    "agents": "",
    "pi-sandbox": "0.1.0",
    "rpiv-artifacts": "",
    ".github": "",
    "documentation": "",
}
PINNED_PUBLIC = {"gestion", "AIO", "IntraVox", "repo-docs", ".github", "documentation"}


def fail(msg: str) -> None:
    print(f"[gen-catalogo] ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def note(msg: str) -> None:
    print(f"[gen-catalogo] {msg}")


def warn(msg: str) -> None:
    print(f"[gen-catalogo] AVISO: {msg}", file=sys.stderr)


# ---------------------------------------------------------------- schema/nómina


def load_rows() -> list[dict]:
    try:
        doc = yaml.safe_load(CATALOGO.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"no existe {CATALOGO}")
    except yaml.YAMLError as exc:
        fail(f"catalogo.yml no parsea: {exc}")
    rows = doc.get("repos") or []
    names = [r.get("repo") for r in rows]
    for row in rows:
        keys = set(row)
        missing = [k for k in REQUIRED if k not in keys]
        unknown = keys - set(REQUIRED) - set(OPTIONAL)
        if missing:
            fail(f"fila {row.get('repo', '?')}: faltan claves requeridas {sorted(missing)}")
        if unknown:
            fail(f"fila {row.get('repo')}: claves desconocidas {sorted(unknown)}")
        if not str(row["role"]).strip():
            fail(f"fila {row['repo']}: `role` vacío")
        if row["kind"] not in KINDS:
            fail(f"fila {row['repo']}: kind {row['kind']!r} fuera del enum ({sorted(KINDS)})")
        if not isinstance(row["manuals"], list) or not row["manuals"]:
            fail(f"fila {row['repo']}: `manuals` debe ser una lista no vacía")
        for key in ("depends_on", "soft_depends_on"):
            for dep in row.get(key, []) or []:
                if dep not in names:
                    fail(f"fila {row['repo']}: {key} apunta fuera de la nómina: {dep!r}")
    if len(rows) != 15:
        fail(f"esperaba 15 filas, hay {len(rows)}")
    if len(set(names)) != len(names):
        fail("filas duplicadas en catalogo.yml")
    if doc.get("org") != ORG:
        fail(f"org: esperaba {ORG!r}, hay {doc.get('org')!r}")
    if doc.get("out_of_scope") != ["aps-conecta-web", "calculadora-ecicep"]:
        fail("out_of_scope: esperaba [aps-conecta-web, calculadora-ecicep]")
    return rows


# -------------------------------------------------------------------- paridad


def own_apps(registry: Path) -> list[str]:
    """La mitad variable de cada entrada `nombre=url` de OWN_APPS (como
    repo-docs census.py `own_apps()`)."""
    try:
        text = registry.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"registro ausente para la paridad: {registry}")
    m = OWN_APPS_RE.search(text)
    if not m:
        fail(f"OWN_APPS no encontrado en {registry}")
    return [entry.split("=", 1)[0] for entry in m.group(1).split() if entry]


def resolve(name: str, canonical: list[str]) -> str:
    """Pliega `name` sobre la clave canónica que coincida case-insensitivamente;
    sin coincidencia devuelve `name` intacto (el tripwire de onboarding
    sobrevive el pliegue) — census.py `resolve()`."""
    for key in canonical:
        if key.lower() == name.lower():
            return key
    return name


def parity(rows: list[dict]) -> set[str]:
    names = [r["repo"] for r in rows]
    folded = {resolve(n, names) for n in own_apps(REGISTRY)}
    apps = {r["repo"] for r in rows if r["kind"] == "nextcloud-app"}
    if apps != folded:
        fail(
            "paridad OWN_APPS ≠ filas nextcloud-app: "
            f"solo-catálogo={sorted(apps - folded)} solo-OWN_APPS={sorted(folded - apps)}"
        )
    return apps


# ------------------------------------------------------------------- manuales


def check_manuals(rows: list[dict]) -> None:
    for row in rows:
        for page in row["manuals"]:
            if not MANUAL_RE.match(page):
                fail(f"fila {row['repo']}: manual mal formado: {page!r}")
            if not (REPO_ROOT / page).is_file():
                fail(f"fila {row['repo']}: el manual {page} no existe en el árbol comprometido")


# ------------------------------------------------------------------ versiones


def _info_xml_version(repo_dir: Path) -> str:
    path = repo_dir / "appinfo" / "info.xml"
    if not path.is_file():
        return ""
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        fail(f"{repo_dir.name}: info.xml ilegal: {exc}")
    return (root.findtext("version") or "").strip()


def _json_version(repo_dir: Path, name: str) -> str:
    path = repo_dir / name
    if not path.is_file():
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        fail(f"{repo_dir.name}: {name} ilegal: {exc}")
    return str(data.get("version") or "").strip()


def _changelog_version(repo_dir: Path) -> str:
    path = repo_dir / "CHANGELOG.md"
    if not path.is_file():
        return ""
    m = SEMVER_RE.search(path.read_text(encoding="utf-8", errors="replace"))
    return m.group(1) if m else ""


def version_for(row: dict) -> str:
    if "version" in row:  # anulación explícita (AIO: la única <version> es la app interna upstream)
        return str(row["version"]).strip()
    repo_dir = ORG_ROOT / row["repo"]
    if not repo_dir.is_dir():
        fail(f"checkout ausente para versionar: {repo_dir}")
    for probe in (
        _info_xml_version,
        lambda d: _json_version(d, "composer.json"),
        lambda d: _json_version(d, "package.json"),
        _changelog_version,
    ):
        value = probe(repo_dir)
        if value:
            return value
    return ""


# ---------------------------------------------------------------- visibilidad


def org_visibility() -> dict[str, bool]:
    proc = subprocess.run(
        ["gh", "api", f"orgs/{ORG}/repos", "--paginate",
         "--jq", ".[] | [.name, .private] | @tsv"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        fail(f"gh api orgs/{ORG}/repos: {proc.stderr.strip()}")
    visibility: dict[str, bool] = {}
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        name, private = line.split("\t")[:2]
        visibility[name] = private.strip() == "true"
    if not visibility:
        fail("la consulta de visibilidad devolvió cero repositorios")
    return visibility


def check_visibility(rows: list[dict], out_of_scope: list[str]) -> dict[str, bool]:
    visibility = org_visibility()
    for row in rows:
        if row["repo"] not in visibility:
            fail(f"{row['repo']}: no existe en la org viva (gh api orgs/{ORG}/repos)")
    known = {r["repo"] for r in rows} | set(out_of_scope)
    for name in sorted(visibility):
        if name not in known:
            warn(f"repo de la org fuera del catálogo y de out_of_scope: {name}")
    return visibility


# --------------------------------------------------------------------- render


def render(rows: list[dict], versions: dict[str, str], visibility: dict[str, bool]) -> str:
    lines = [
        "---",
        "tipo: referencia",
        "---",
        "",
        "# Catálogo de repositorios",
        "",
        "Los repositorios de la organización APS-Conecta, con su tipo, versión "
        "vigente, visibilidad, rol, manuales propios y estado. La versión y la "
        "visibilidad se consultan en vivo al compilar; el resto vive en "
        "`catalogo.yml`, la fuente única de la organización.",
        "",
        "| Repositorio | Tipo | Versión | Visibilidad | Rol | Manuales | Estado |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        repo = row["repo"]
        manuals = " · ".join(f"[{p[:-3]}](../{p})" for p in row["manuals"])
        lines.append(
            f"| [{repo}](https://github.com/{ORG}/{repo}) | {KIND_ES[row['kind']]} "
            f"| {versions[repo]} | {'Público' if not visibility[repo] else 'Privado'} "
            f"| {row['role']} | {manuals} | {row['status']} |"
        )
    lines += [
        "",
        "## Dependencias",
        "",
        "| Repositorio | Depende de |",
        "| --- | --- |",
    ]
    for row in rows:
        edges = [f"[{dep}](https://github.com/{ORG}/{dep})" for dep in row["depends_on"]]
        soft = [f"[{dep}](https://github.com/{ORG}/{dep}) (doctrinal)"
                for dep in row.get("soft_depends_on", []) or []]
        if edges or soft:
            lines.append(f"| [{row['repo']}](https://github.com/{ORG}/{row['repo']}) "
                         f"| {' · '.join(edges + soft)} |")
    lines += [
        "",
        "Las aristas marcadas *(doctrinal)* no son de construcción: unen una "
        "aplicación con el corpus de datos que fija su doctrina, sin enlace de "
        "empaquetado.",
        "",
        "Página generada al compilar por `tools/gen-catalogo.py` a partir de "
        "`catalogo.yml`; las versiones provienen de los checkouts de la "
        "organización y la visibilidad de la API en vivo. No editar a mano.",
        "",
    ]
    return "\n".join(lines)


def write_outputs(rows: list[dict], visibility: dict[str, bool], page: str) -> Path:
    GENERATED.mkdir(parents=True, exist_ok=True)
    seed = GENERATED / "linkcheck-private.txt"
    private = [f"https://github.com/{ORG}/{r['repo']}\n"
               for r in rows if visibility[r["repo"]]]
    seed.write_text("".join(private), encoding="utf-8")
    out = GENERATED / "catalogo.md"
    out.write_text(page, encoding="utf-8")
    return out


# --------------------------------------------------------------------- main


def gather(rows: list[dict], out_of_scope: list[str]):
    visibility = check_visibility(rows, out_of_scope)
    versions = {row["repo"]: version_for(row) for row in rows}
    return versions, visibility


def main() -> int:
    rows = load_rows()
    doc = yaml.safe_load(CATALOGO.read_text(encoding="utf-8"))
    parity(rows)
    check_manuals(rows)  # tras las validaciones duras: la página nunca se escribe con manuales colgando
    versions, visibility = gather(rows, doc["out_of_scope"])
    out = write_outputs(rows, visibility, render(rows, versions, visibility))
    privadas = sum(1 for r in rows if visibility[r["repo"]])
    note(f"15 filas; {out.relative_to(REPO_ROOT)} + "
         f"_generated/linkcheck-private.txt ({privadas} privadas)")
    return 0


def selftest() -> int:
    doc = yaml.safe_load(CATALOGO.read_text(encoding="utf-8"))
    rows = load_rows()
    assert {r["repo"] for r in rows} == PINNED_REPOS
    assert all(str(r.get("role", "")).strip() for r in rows)
    apps = parity(rows)
    assert apps == PINNED_APPS, f"paridad: {sorted(apps)}"
    for row in rows:  # forma de los manuales (la existencia la gatea la corrida completa)
        for page in row["manuals"]:
            assert MANUAL_RE.match(page), page
    versions, visibility = gather(rows, doc["out_of_scope"])
    assert versions == PINNED_VERSIONS, "deriva de versiones:\n" + "\n".join(
        f"  {k}: {versions[k]!r} ≠ {PINNED_VERSIONS[k]!r}" for k in PINNED_VERSIONS
        if versions[k] != PINNED_VERSIONS[k])
    publicos = {r["repo"] for r in rows if not visibility[r["repo"]]}
    assert publicos == PINNED_PUBLIC, f"visibilidad: {sorted(publicos)}"
    page = render(rows, versions, visibility)
    for row in rows:
        assert row["repo"] in page, row["repo"]
    for label in KIND_ES.values():
        assert label in page, label
    # Ningún valor del enum EN llega a la página: columna Tipo estrictamente en
    # español, y ningún enum con guion como subcadena en ninguna parte.
    lines = page.splitlines()
    header = "| Repositorio | Tipo | Versión | Visibilidad | Rol | Manuales | Estado |"
    main_rows = []
    for ln in lines[lines.index(header) + 2:]:  # salta cabecera y separador
        if not ln.startswith("|"):
            break
        main_rows.append(ln)
    assert len(main_rows) == 15, len(main_rows)
    tipo_cells = {ln.split("|")[2].strip() for ln in main_rows}
    assert tipo_cells <= set(KIND_ES.values()), tipo_cells - set(KIND_ES.values())
    for enum in KINDS - {"suite"}:  # «suite» es también common noun; cubierto por la columna
        assert enum not in page, enum
    privadas = [f"https://github.com/{ORG}/{r['repo']}" for r in rows if visibility[r["repo"]]]
    assert len(privadas) == 9, privadas
    print("[gen-catalogo] selftest OK (nómina, paridad, versiones, visibilidad, "
          "etiquetas, semilla privada)")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
