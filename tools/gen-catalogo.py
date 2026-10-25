#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Generador del catálogo: catalogo.yml (SSOT) → páginas generadas.

Escribe `_generated/catalogo.md` (página de referencia, tabla de dependencias)
y `_generated/linkcheck-private.txt` (una URL raíz por fila privada — la semilla
de `linkcheck_ignore` en conf.py).

Valida: esquema de filas, paridad con la lista de aplicaciones de la suite (las
filas `own` y `fork` de `apps.json`, el manifiesto único del instalador, se pliegan
sobre los nombres canónicos del catálogo y exigen su fila `nextcloud-app`) y que
cada `manuals` resuelva a un .md comprometido del árbol y lleve su repositorio
en `apps`. Versiona por cadena (`version:` explícita →
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
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOGO = REPO_ROOT / "catalogo.yml"
GENERATED = REPO_ROOT / "_generated"
ORG = "APS-Conecta"
ORG_ROOT = Path(os.environ.get("APS_ORG_ROOT", "/opt/aps-conecta-org"))


def manifest_path(org_root: Path) -> Path:
    """La lista de aplicaciones de la suite vive en el manifiesto único del
    instalador (apps.json), no en gestion ni en ninguna fase de provisión: el
    manifiesto es la única lista de aplicaciones que queda."""
    return org_root / "instalador" / "apps.json"


REGISTRY = manifest_path(ORG_ROOT)

KINDS = {
    "suite",
    "distribution-fork",
    "nextcloud-app",
    "shared-library",
    "data-corpus",
    "canon-engine",
    "agent-prompts",
    "laboratory-app",
    "app-in-design",
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
    "app-in-design": "Aplicación sin publicar",
    "artifacts-store": "Almacén de artefactos",
    "org-defaults": "Valores por defecto de la organización",
    "docs-site": "Sitio de documentación",
}
REQUIRED = ("repo", "kind", "role", "manuals", "depends_on", "status")
OPTIONAL = ("version", "soft_depends_on", "readme")
MANUAL_RE = re.compile(r"^(?:usuario|administracion|desarrollo|proyecto)/(?:[a-z0-9_-]+/)*[a-z0-9_-]+\.md$")
# Las filas cuyo cambio ve una persona usuaria o administradora llevan su página de
# novedades (scribe Q4): la escribe 📚 Scribe; el catálogo garantiza que exista.
NOVEDADES_KINDS = {"suite", "distribution-fork", "nextcloud-app"}
MANIFEST_OWN = {"own", "fork"}  # las filas del manifiesto que el catálogo documenta como aplicaciones
SEMVER_RE = re.compile(r"^#{1,3}\s*\[?\s*v?(\d+(?:\.\d+){2}[0-9A-Za-z.+-]*)", re.M)

# Clavijas de --selftest (deriva viva a 2026-10-24).
PINNED_REPOS = {
    "gestion", "instalador", "IntraVox", "farmacia", "estadistica", "epidemiologia",
    "territorio", "aps-common", "Databases", "repo-docs",
    "rpiv-artifacts", ".github", "documentation", "buscador-documental",
    "side_menu", "eurooffice", "desktop_workspace", "totem",
}
PINNED_APPS = {"epidemiologia", "farmacia", "territorio", "IntraVox", "estadistica",
               "side_menu", "eurooffice", "desktop_workspace", "totem"}
PINNED_VERSIONS = {
    "gestion": "0.3.0",
    "instalador": "0.4.0",
    "IntraVox": "3.1.7",
    "farmacia": "0.12.0",
    "estadistica": "0.1.0",
    "epidemiologia": "0.12.0",
    "territorio": "0.80.0",
    "aps-common": "1.0.0",
    "Databases": "",
    "repo-docs": "",
    "rpiv-artifacts": "",
    ".github": "",
    "documentation": "",
    "buscador-documental": "",
    "side_menu": "6.0.1",
    "eurooffice": "11.0.7",
    "desktop_workspace": "0.19.0",
    "totem": "0.3.0",
}
PINNED_PUBLIC = {"gestion", "instalador", "IntraVox", "repo-docs", ".github", "documentation",
                 "buscador-documental", "epidemiologia", "farmacia", "estadistica",
                 "territorio", "aps-common", "side_menu", "eurooffice", "desktop_workspace", "totem"}


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
    if len(set(names)) != len(names):
        fail("filas duplicadas en catalogo.yml")
    if doc.get("org") != ORG:
        fail(f"org: esperaba {ORG!r}, hay {doc.get('org')!r}")
    if doc.get("out_of_scope") != ["aps-conecta-web", "calculadora-ecicep"]:
        fail("out_of_scope: esperaba [aps-conecta-web, calculadora-ecicep]")
    return rows


# -------------------------------------------------------------------- paridad


def own_apps(registry: Path) -> list[str]:
    """Los `id` de las filas `own` y `fork` del manifiesto de la suite (apps.json):
    las aplicaciones cuyo repositorio es de la organización y que por tanto deben
tener su fila en el catálogo."""
    try:
        text = registry.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"registro ausente para la paridad: {registry} "
             "(apps.json vive en el instalador: clonar APS-Conecta/instalador "
             "bajo APS_ORG_ROOT)")
    try:
        rows = json.loads(text)
    except json.JSONDecodeError as exc:
        fail(f"apps.json ilegal ({registry}): {exc}")
    return [r["id"] for r in rows if r.get("source") in MANIFEST_OWN]


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
    if folded - apps:
        fail(
            "paridad apps.json ≠ filas nextcloud-app: "
            f"solo-manifiesto={sorted(folded - apps)} (cada aplicación propia o fork "
            "de la suite lleva su fila en catalogo.yml)"
        )
    return apps


# ------------------------------------------------------------------- manuales


def check_manuals(rows: list[dict]) -> None:
    for row in rows:
        novedades = f"proyecto/novedades/{row['repo'].lower()}.md"
        if row["kind"] in NOVEDADES_KINDS and novedades not in row["manuals"]:
            fail(f"fila {row['repo']}: falta su página de novedades {novedades} en manuals")
        for page in row["manuals"]:
            if not MANUAL_RE.match(page):
                fail(f"fila {row['repo']}: manual mal formado: {page!r}")
            path = REPO_ROOT / page
            if not path.is_file():
                fail(f"fila {row['repo']}: el manual {page} no existe en el árbol comprometido")
            try:
                front = path.read_text(encoding="utf-8").split("---", 2)[1]
                apps = yaml.safe_load(front).get("apps") or []
            except (IndexError, yaml.YAMLError):
                fail(f"fila {row['repo']}: el manual {page} no lleva encabezado legible")
            if row["repo"] not in apps:
                fail(f"fila {row['repo']}: {page} no lleva {row['repo']} en apps")


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
    if "version" in row:  # anulación explícita (p. ej. instalador: aún sin versión publicada)
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


def _gh(path: str, jq: str) -> subprocess.CompletedProcess:
    extra = ["--paginate"] if path.startswith("orgs/") else []
    return subprocess.run(["gh", "api", path, *extra, "--jq", jq], capture_output=True, text=True)


def org_visibility(rows: list[dict], api=_gh) -> tuple[dict[str, bool], bool]:
    """nombre → privado, y si hubo censo de la org. Primero el listado de la org (también halla
    repos que el catálogo no nombra). Una sesión atada a sus repositorios (una rutina de Claude)
    rechaza las rutas de org: entonces cada repo del catálogo responde por sí mismo y el censo
    se omite, con aviso."""
    proc = api(f"orgs/{ORG}/repos", ".[] | [.name, .private] | @tsv")
    if proc.returncode == 0:
        visibility: dict[str, bool] = {}
        for line in proc.stdout.splitlines():
            if line.strip():
                name, private = line.split("\t")[:2]
                visibility[name] = private.strip() == "true"
        if not visibility:
            fail("la consulta de visibilidad devolvió cero repositorios")
        return visibility, True
    warn(f"gh api orgs/{ORG}/repos rechazada ({proc.stderr.strip().splitlines()[0][:90] if proc.stderr.strip() else proc.returncode});"
         " visibilidad repo por repo, sin censo de la org")
    visibility = {}
    for row in rows:
        one = api(f"repos/{ORG}/{row['repo']}", ".private")
        if one.returncode != 0:
            fail(f"{row['repo']}: no existe en la org viva (gh api repos/{ORG}/{row['repo']}: {one.stderr.strip()})")
        visibility[row["repo"]] = one.stdout.strip() == "true"
    return visibility, False


def check_visibility(rows: list[dict], out_of_scope: list[str]) -> dict[str, bool]:
    visibility, census = org_visibility(rows)
    for row in rows:
        if row["repo"] not in visibility:
            fail(f"{row['repo']}: no existe en la org viva (gh api orgs/{ORG}/repos)")
    if census:
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
        "Los repositorios que documenta este sitio, con su tipo, versión "
        "vigente, visibilidad, rol, manuales propios y estado. La versión y la "
        "visibilidad se consultan en vivo al compilar; el resto vive en "
        "`catalogo.yml`.",
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
    note(f"{len(rows)} filas; {out.relative_to(REPO_ROOT)} + "
         f"_generated/linkcheck-private.txt ({privadas} privadas)")
    return 0


def selftest_registro() -> None:
    """La lista de aplicaciones se lee del manifiesto del instalador, nunca de
    gestion: una raíz donde gestion NO tiene `apps.json` e instalador SÍ,
    resuelve; sin el manifiesto, el error nombra la ruta del instalador."""
    rel = Path("apps.json")
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        (raiz / "gestion").mkdir(parents=True)
        (raiz / "instalador").mkdir(parents=True)
        (raiz / "instalador" / rel).write_text(
            '[{"id": "intravox", "source": "fork"}, '
            '{"id": "farmacia", "source": "own"}, '
            '{"id": "calendar", "source": "store"}]\n', encoding="utf-8")
        assert manifest_path(raiz) == raiz / "instalador" / rel, manifest_path(raiz)
        assert own_apps(manifest_path(raiz)) == ["intravox", "farmacia"]
        (raiz / "instalador" / rel).unlink()
        try:
            own_apps(manifest_path(raiz))
        except SystemExit:
            pass
        else:
            raise AssertionError("sin apps.json en instalador la paridad debe fallar")


def selftest() -> int:
    selftest_registro()
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
    # Una rutina de Claude no puede listar la org: repo por repo da la misma visibilidad.
    def refused(path, jq):
        if path.startswith("orgs/"):
            return subprocess.CompletedProcess([], 1, "", "HTTP 403: sessions are bound to their configured repositories")
        return _gh(path, jq)
    per_repo, census = org_visibility(rows, refused)
    assert not census and per_repo == {r["repo"]: visibility[r["repo"]] for r in rows}, per_repo
    page = render(rows, versions, visibility)
    for row in rows:
        assert row["repo"] in page, row["repo"]
    used_labels = {KIND_ES[r["kind"]] for r in rows}
    for label in used_labels:  # cada etiqueta usada llega a la página
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
    assert len(main_rows) == len(rows), (len(main_rows), len(rows))
    tipo_cells = {ln.split("|")[2].strip() for ln in main_rows}
    assert tipo_cells <= set(KIND_ES.values()), tipo_cells - set(KIND_ES.values())
    for enum in KINDS - {"suite"}:  # «suite» es también common noun; cubierto por la columna
        assert enum not in page, enum
    privadas = [f"https://github.com/{ORG}/{r['repo']}" for r in rows if visibility[r["repo"]]]
    assert len(privadas) == 2, privadas  # Databases y rpiv-artifacts son los únicos privados de la nómina
    print("[gen-catalogo] selftest OK (nómina, paridad, versiones, visibilidad, "
          "visibilidad sin listado de org, etiquetas, semilla privada)")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
