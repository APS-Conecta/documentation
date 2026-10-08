#!/usr/bin/env python3
"""Generador de páginas de referencia por aplicación (occ, ajustes, rutas).

Lee `catalogo.yml` (filas `kind: nextcloud-app`), parsea `appinfo/info.xml`
y `appinfo/routes.php` de cada clon bajo `${APS_ORG_ROOT:-/opt/aps-conecta-org}`
y escribe, bajo `_generated/`:

  - `referencia/<slug>.md` — página de referencia (documento descubierto)
  - `attach/<slug>.md`     — fragmento de toctree (fuente de `{include}`)

Contrato: degradar, nunca omitir — toda superficie vacía se declara con una
frase «Sin …»; toda entrada desconocida o no parseable corta la compilación
(exit 1), porque eliminar entradas en silencio es el único resultado
prohibido. Salida determinista: sin fechas ni números de versión.
Solo stdlib: el catálogo se lee con un intérprete mínimo del subconjunto
YAML que `catalogo.yml` usa (escalares, listas de flujo, listas en bloque).
"""

import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORG_ROOT = Path(os.environ.get("APS_ORG_ROOT", "/opt/aps-conecta-org"))
OUT_DIR = ROOT / "_generated" / "referencia"
ATTACH_DIR = ROOT / "_generated" / "attach"

SLOT_ES = {
    "admin": "Administración",
    "admin-section": "Sección de administración",
}
ROUTE_KEYS = {"name", "url", "verb", "requirements"}
TOP_KEYS = {"routes", "ocs"}

# Pines de deriva, verificados contra los clones el 2026-10-07
# (rutas, con requisitos, ocs, comandos occ, ajustes, trabajos, enlaces FQCN).
PINS = {
    "farmacia": (20, 8, 0, 1, 0, 0, 1),
    "territorio": (27, 0, 0, 1, 2, 0, 3),
    "estadistica": (6, 0, 0, 0, 2, 1, 3),
    "epidemiologia": (1, 0, 0, 0, 0, 3, 3),
    "IntraVox": (171, 0, 8, 9, 2, 6, 17),
}


def die(msg: str) -> None:
    sys.exit(f"[referencia] {msg}")


# ---------------------------------------------------------------------------
# catalogo.yml — subconjunto YAML mínimo (solo stdlib)
# ---------------------------------------------------------------------------

_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_.-]*)\s*:\s*(.*)$")
_DASH = re.compile(r"^(\s*)-\s+(.*)$")


def _strip_comment(text: str) -> str:
    """YAML: un `#` precedido de espacio (y fuera de comillas) abre un
    comentario en línea. El subconjunto declarado solo incluía comentarios
    de línea completa, pero el `catalogo.yml` de la Fase 5 aterriza con
    comentarios en línea (p. ej. `soft_depends_on: [Databases] # arista…`),
    así que el lector se ensancha aquí — nunca se silencia."""
    quote = None
    i = 0
    while i < len(text):
        c = text[i]
        if quote:
            if c == "\\":
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in ("'", '"'):
            quote = c
        elif c == "#" and (i == 0 or text[i - 1] in " \t"):
            return text[:i].rstrip()
        i += 1
    return text.rstrip()


def _scalar(text: str) -> str:
    t = text.strip()
    if len(t) >= 2 and t[0] == t[-1] and t[0] in ("'", '"'):
        return t[1:-1]
    return t


def _flow_list(text: str, source: str, lineno: int):
    t = text.strip()
    if not (t.startswith("[") and t.endswith("]")):
        die(f"{source}:{lineno}: lista de flujo malformada: {text!r}")
    inner = t[1:-1].strip()
    if not inner:
        return []
    return [_scalar(part) for part in inner.split(",")]


def _assign(row: dict, key: str, value: str, source: str, lineno: int) -> None:
    v = _strip_comment(value).strip()
    if v.startswith("["):
        row[key] = _flow_list(v, source, lineno)
    else:
        row[key] = _scalar(v)


def load_app_repos(text: str, source: str = "catalogo.yml"):
    """Devuelve los `repo` de las filas `kind: nextcloud-app`, en orden de archivo."""
    rows = []
    mode = "top"
    row = None
    dash_indent = 0
    pending = None  # (fila, clave, indent) esperando una lista en bloque
    for lineno, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if mode == "top":
            m = _KEY.match(line)
            if not m:
                die(f"{source}:{lineno}: clave de nivel superior no reconocida: {line!r}")
            if m.group(1) == "repos":
                if m.group(2).strip():
                    die(f"{source}:{lineno}: 'repos:' esperaba una lista en bloque")
                mode = "repos"
            continue  # org, out_of_scope, … — este generador no los consume
        if indent == 0:
            mode = "top"
            row = None
            continue
        if pending is not None:
            prow, pkey, pindent = pending
            dm = _DASH.match(raw)
            if dm and dm.group(1) and len(dm.group(1)) > pindent:
                prow.setdefault(pkey, []).append(dm.group(2).strip())
                continue
            pending = None
        dm = _DASH.match(raw)
        if dm and (row is None or indent == dash_indent):
            dash_indent = indent
            rest = dm.group(2)
            row = {}
            rows.append(row)
            m = _KEY.match(rest)
            if not m:
                die(f"{source}:{lineno}: fila de 'repos:' sin clave inicial")
            _assign(row, m.group(1), m.group(2), source, lineno)
            continue
        if row is None:
            die(f"{source}:{lineno}: contenido inesperado bajo 'repos:'")
        m = _KEY.match(line)
        if not m:
            die(f"{source}:{lineno}: línea de fila no reconocida: {line!r}")
        if indent <= dash_indent:
            die(f"{source}:{lineno}: indentación de fila inconsistente")
        if m.group(2).strip() == "":
            row[m.group(1)] = []
            pending = (row, m.group(1), indent)
        else:
            _assign(row, m.group(1), m.group(2), source, lineno)
    repos = []
    for r in rows:
        if r.get("kind") == "nextcloud-app":
            repo = str(r.get("repo", "")).strip()
            if not repo:
                die(f"{source}: fila nextcloud-app sin 'repo'")
            repos.append(repo)
    return repos


# ---------------------------------------------------------------------------
# appinfo/info.xml
# ---------------------------------------------------------------------------


def parse_info_xml(path: Path) -> dict:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        die(f"{path}: XML no válido: {exc}")
    appid = (root.findtext("id") or "").strip()
    appname = (root.findtext("name") or "").strip()
    if not appid:
        die(f"{path}: falta <id>")
    commands_el = root.find("commands")
    commands = []
    if commands_el is not None:
        for c in commands_el:
            text = (c.text or "").strip()
            if text:
                commands.append(text)
    settings = {}
    settings_el = root.find("settings")
    if settings_el is not None:
        for child in settings_el:
            settings[child.tag] = (child.text or "").strip()
    jobs = []
    jobs_el = root.find("background-jobs")
    if jobs_el is not None:
        for j in jobs_el:
            text = (j.text or "").strip()
            if text:
                jobs.append(text)
    return {
        "appid": appid,
        "appname": appname or appid,
        "commands": commands,
        "settings": settings,
        "jobs": jobs,
    }


# ---------------------------------------------------------------------------
# appinfo/routes.php — tokenizador + descenso recursivo
# ---------------------------------------------------------------------------


class PhpError(Exception):
    pass


def _tokenize_php(src: str, filename: str):
    toks = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c in " \t\r\n":
            i += 1
            continue
        if src.startswith("<?php", i):  # etiqueta de apertura (sin cierre ?>)
            i += 5
            continue
        if src.startswith("<?", i):  # formas cortas (<?=, <?)
            i += 2
            continue
        if src.startswith("?>", i):
            i += 2
            continue
        if src.startswith("//", i) or src.startswith("/*", i) or c == "#":
            if src.startswith("/*", i):
                j = src.find("*/", i + 2)
                if j < 0:
                    raise PhpError(f"{filename}: comentario de bloque sin cerrar")
                i = j + 2
            else:
                j = src.find("\n", i)
                i = n if j < 0 else j
            continue
        if c in ("'", '"'):
            quote = c
            buf = []
            i += 1
            closed = False
            while i < n:
                ch = src[i]
                if ch == "\\" and i + 1 < n and src[i + 1] in ("\\", quote):
                    buf.append(src[i + 1])
                    i += 2
                    continue
                if ch == quote:
                    i += 1
                    closed = True
                    break
                buf.append(ch)
                i += 1
            if not closed:
                raise PhpError(f"{filename}: cadena {quote} sin cerrar")
            toks.append(("str", "".join(buf)))
            continue
        if src.startswith("=>", i):
            toks.append(("=>", "=>"))
            i += 2
            continue
        if c in "[],;()=":
            toks.append((c, c))
            i += 1
            continue
        if c.isdigit():
            j = i
            while j < n and (src[j].isdigit() or src[j] == "."):
                j += 1
            toks.append(("num", src[i:j]))
            i = j
            continue
        if c.isalpha() or c == "_":
            j = i
            while j < n and (src[j].isalnum() or src[j] == "_"):
                j += 1
            toks.append(("word", src[i:j]))
            i = j
            continue
        raise PhpError(f"{filename}: carácter inesperado {c!r} en la posición {i}")
    return toks


def _array_literal(items: dict, positional: list, filename: str):
    """Un literal de array PHP: mapa si todas sus entradas tienen clave,
    lista si todas son posicionales; mezclar ambas es error."""
    if positional and items:
        raise PhpError(f"{filename}: array que mezcla claves y posición")
    return items if items else positional


def _parse_value(toks, pos, filename):
    kind, val = toks[pos]
    if kind == "str":
        return val, pos + 1
    if kind == "[":
        items, positional, pos = _parse_array(toks, pos, filename)
        return _array_literal(items, positional, filename), pos
    if kind == "word" and val in ("TRUE", "FALSE", "NULL", "true", "false", "null"):
        return {"TRUE": True, "true": True, "FALSE": False, "false": False,
                "NULL": None, "null": None}[val], pos + 1
    if kind == "num":
        return int(val) if "." not in val else float(val), pos + 1
    raise PhpError(f"{filename}: valor inesperado {val!r}")


def _parse_array(toks, pos, filename):
    pos += 1  # consume '['
    items = {}
    positional = []
    while True:
        if pos >= len(toks):
            raise PhpError(f"{filename}: array sin cerrar")
        if toks[pos][0] == "]":
            return items, positional, pos + 1
        value, pos = _parse_value(toks, pos, filename)
        if pos < len(toks) and toks[pos][0] == "=>":
            if not isinstance(value, str):
                raise PhpError(f"{filename}: clave de array no textual: {value!r}")
            pos += 1
            value2, pos = _parse_value(toks, pos, filename)
            items[value] = value2
        else:
            positional.append(value)
        if pos < len(toks) and toks[pos][0] == ",":
            pos += 1
        elif pos < len(toks) and toks[pos][0] != "]":
            raise PhpError(f"{filename}: token inesperado {toks[pos][1]!r} tras una entrada")


def parse_routes_php(path: Path) -> dict:
    """Devuelve el array de nivel superior de `return […]` ya validado."""
    filename = str(path)
    src = path.read_text(encoding="utf-8")
    try:
        toks = _tokenize_php(src, filename)
        start = None
        for idx, (kind, val) in enumerate(toks):
            if kind == "word" and val == "return" and idx + 1 < len(toks) and toks[idx + 1][0] == "[":
                start = idx + 1
                break
        if start is None:
            raise PhpError(f"{filename}: no se encontró 'return ['")
        items, positional, _ = _parse_array(toks, start, filename)
        if positional:
            raise PhpError(
                f"{filename}: entrada posicional en el array de nivel superior: "
                f"{positional[0]!r}")
    except PhpError as exc:
        die(str(exc))
    for key in items:
        if key not in TOP_KEYS:
            die(
                f"{filename}: clave de nivel superior no reconocida: {key!r} "
                f"(esperadas: {sorted(TOP_KEYS)})")
    for section in ("routes", "ocs"):
        entries = items.get(section)
        if entries is None:
            continue
        if not isinstance(entries, list):
            die(f"{filename}: la clave {section!r} no es una lista")
        for entry in entries:
            if not isinstance(entry, dict):
                die(f"{filename}: entrada de {section!r} que no es un array asociativo")
            name = entry.get("name")
            for key in entry:
                if key not in ROUTE_KEYS:
                    die(
                        f"{filename}: clave de entrada de ruta no reconocida: {key!r} "
                        f"(en {name!r}, sección {section!r})")
            for required in ("name", "url", "verb"):
                if not isinstance(entry.get(required), str) or not entry[required]:
                    die(f"{filename}: la entrada {name!r} de {section!r} falta '{required}'")
            reqs = entry.get("requirements")
            if reqs is not None:
                if not isinstance(reqs, dict) or not all(
                        isinstance(k, str) and isinstance(v, str) for k, v in reqs.items()):
                    die(f"{filename}: 'requirements' inválidos en {name!r} de {section!r}")
    return items


# ---------------------------------------------------------------------------
# FQCN → enlace blob
# ---------------------------------------------------------------------------


def lib_relpath(fqcn: str):
    """OCA\\<Ns>\\Resto → lib/Resto.php; None si no es un FQCN OCA."""
    parts = fqcn.split("\\")
    if len(parts) < 3 or parts[0] != "OCA":
        return None
    return "/".join(parts[2:]) + ".php"


def fqcn_cell(fqcn: str, repo: str, scan_root: Path) -> str:
    rel = lib_relpath(fqcn)
    if rel and (scan_root / "lib" / rel).is_file():
        return f"[`{fqcn}`](https://github.com/APS-Conecta/{repo}/blob/main/lib/{rel})"
    return f"`{fqcn}`"


def n_fqcn_links(info: dict, repo: str, scan_root: Path) -> int:
    fq = list(info["commands"]) + list(info["settings"].values()) + list(info["jobs"])
    return sum(
        1 for f in fq
        if lib_relpath(f) and (scan_root / "lib" / lib_relpath(f)).is_file())


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------


def _route_table(entries, appid: str) -> list:
    lines = ["| Nombre | URL | Verbo | Requisitos |", "| --- | --- | --- | --- |"]
    for entry in entries:
        dotted = f"{appid}.{entry['name'].replace('#', '.')}"
        reqs = entry.get("requirements") or {}
        req_cell = ", ".join(f"`{k}: {v}`" for k, v in reqs.items())
        lines.append(f"| `{dotted}` | `{entry['url']}` | {entry['verb']} | {req_cell} |")
    return lines


def render_page(repo: str, info: dict, routes_items: dict, scan_root: Path) -> str:
    appid = info["appid"]
    out = [
        "---",
        "tipo: referencia",
        "---",
        "",
        f"# Referencia de {info['appname']}",
        "",
        "Esta página se genera al compilar a partir de `appinfo/info.xml` y "
        "`appinfo/routes.php` del repositorio; no incluye números de versión "
        "ni fechas.",
        "",
        "## Comandos occ",
        "",
    ]
    if info["commands"]:
        out.append("| Clase |")
        out.append("| --- |")
        for fq in info["commands"]:
            out.append(f"| {fqcn_cell(fq, repo, scan_root)} |")
    else:
        out.append("Sin comandos occ.")
    out += ["", "## Ajustes", ""]
    if info["settings"]:
        out.append("| Sección | Clase |")
        out.append("| --- | --- |")
        for slot, fq in info["settings"].items():
            label = SLOT_ES.get(slot, slot)
            out.append(f"| {label} | {fqcn_cell(fq, repo, scan_root)} |")
    else:
        out.append("Sin ajustes.")
    out += ["", "## Trabajos en segundo plano", ""]
    if info["jobs"]:
        out.append("| Clase |")
        out.append("| --- |")
        for fq in info["jobs"]:
            out.append(f"| {fqcn_cell(fq, repo, scan_root)} |")
    else:
        out.append("Sin trabajos en segundo plano.")
    if "ocs" in routes_items:
        out += ["", "## Superficie OCS", ""]
        out.append(
            "Superficie externa (autenticación básica): rutas para el acceso "
            "programático desde fuera de la instancia.")
        out.append("")
        ocs_entries = routes_items.get("ocs") or []
        if ocs_entries:
            out += _route_table(ocs_entries, appid)
        else:
            out.append("Sin entradas OCS.")
    out += ["", "## Rutas", ""]
    routes_entries = routes_items.get("routes") or []
    if not routes_entries:
        out.append("Sin rutas.")
    else:
        out.append(
            "Los nombres se derivan del identificador de la app y del nombre "
            "declarado en `appinfo/routes.php`.")
        out.append("")
        by_controller = {}
        for entry in routes_entries:
            controller = entry["name"].split("#", 1)[0]
            by_controller.setdefault(controller, []).append(entry)
        for controller, entries in by_controller.items():
            out.append(f"### {controller}")
            out.append("")
            out += _route_table(entries, appid)
            out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def render_attach(slug: str) -> str:
    return (
        "```{toctree}\n"
        ":maxdepth: 1\n"
        f"Referencia (occ, ajustes, rutas) <../_generated/referencia/{slug}>\n"
        "```\n"
    )


# ---------------------------------------------------------------------------
# Generación
# ---------------------------------------------------------------------------


def generate_all(repos, org_root: Path, out_dir: Path, attach_dir: Path):
    for target in (out_dir, attach_dir):
        shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
    pages = 0
    for repo in repos:
        scan_root = org_root / repo
        info_path = scan_root / "appinfo" / "info.xml"
        if not info_path.is_file():
            die(f"falta appinfo/info.xml de {repo} (clon esperado en {scan_root})")
        info = parse_info_xml(info_path)
        routes_path = scan_root / "appinfo" / "routes.php"
        routes_items = parse_routes_php(routes_path) if routes_path.is_file() else {}
        slug = repo.lower()
        page = render_page(repo, info, routes_items, scan_root)
        (out_dir / f"{slug}.md").write_text(page, encoding="utf-8")
        # La página siempre existe (degradar, nunca omitir): siempre hay algo
        # que conectar; el fragmento vacío queda como salvaguarda del contrato.
        attach = render_attach(slug) if page else ""
        (attach_dir / f"{slug}.md").write_text(attach, encoding="utf-8")
        n_routes = len(routes_items.get("routes") or [])
        n_ocs = len(routes_items.get("ocs") or [])
        print(
            f"[referencia] {repo}: {n_routes} rutas, {len(info['commands'])} "
            f"comandos occ, {len(info['settings'])} ajustes, "
            f"{len(info['jobs'])} trabajos, {n_ocs} entradas OCS")
        pages += 1
    return pages


def summarize(repo: str, info: dict, routes_items: dict, scan_root: Path):
    routes = routes_items.get("routes") or []
    ocs = routes_items.get("ocs") or []
    n_req = sum(1 for e in routes if e.get("requirements"))
    return (
        len(routes), n_req, len(ocs),
        len(info["commands"]), len(info["settings"]), len(info["jobs"]),
        n_fqcn_links(info, repo, scan_root),
    )


def _roster_from_catalogo():
    catalogo = ROOT / "catalogo.yml"
    if not catalogo.is_file():
        die(f"falta {catalogo}")
    return load_app_repos(catalogo.read_text(encoding="utf-8"))


def selftest() -> int:
    repos = _roster_from_catalogo()
    if sorted(repos) != sorted(PINS):
        die(f"selftest: el roster no coincide con los pines: {sorted(repos)}")
    ok = True
    for repo in repos:
        scan_root = ORG_ROOT / repo
        info_path = scan_root / "appinfo" / "info.xml"
        if not info_path.is_file():
            die(f"selftest: falta appinfo/info.xml de {repo} (en {scan_root})")
        info = parse_info_xml(info_path)
        routes_path = scan_root / "appinfo" / "routes.php"
        routes_items = parse_routes_php(routes_path) if routes_path.is_file() else {}
        got = summarize(repo, info, routes_items, scan_root)
        want = PINS[repo]
        if got == want:
            print(f"[selftest] {repo}: {got} ok")
        else:
            print(f"[selftest] {repo}: deriva: obtenido {got}, fijado {want}")
            ok = False
    if not ok:
        die("selftest: deriva respecto de los pines (actualiza PINS con los nuevos datos verificados)")
    return 0


def main(argv) -> int:
    if "--selftest" in argv:
        return selftest()
    repos = _roster_from_catalogo()
    if not repos:
        die("catalogo.yml no declara ninguna fila kind: nextcloud-app")
    generate_all(repos, ORG_ROOT, OUT_DIR, ATTACH_DIR)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
