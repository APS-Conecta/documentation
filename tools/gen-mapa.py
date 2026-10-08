#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Mapa de módulos por repositorio (graphify).

Por cada fila de ``catalogo.yml`` con ``kind`` ∈ MAP_KINDS ejecuta
``python -m graphify update <scan root absoluto> --no-cluster`` con
``GRAPHIFY_OUT`` apuntando a ``_generated/mapa/<repo>/`` y ``GRAPHIFY_FORCE=1``
(contract verificado contra graphifyy 0.8.33), y renderiza
``_generated/mapa/<slug>.md`` como función pura de ``graph.json``.

Decisiones ancladas en la fuente de graphifyy 0.8.33:
- ``save_manifest`` escribe ``graphify-out/manifest.json`` RELATIVO AL CWD del
  proceso, no bajo ``GRAPHIFY_OUT``; el subprocess corre en un scratch dentro
  del out dir y el manifiesto se reubica después (nunca se toca un
  ``graphify-out/`` preexistente del checkout hermano).
- El corpus cero imprime «No code files found - nothing to rebuild.» y sale 1:
  se absorbe como página de degradación («Sin módulos extraídos en este
  repositorio.») con la entrada de toctree intacta; cualquier otro exit ≠ 0
  es error duro.
- ``--no-cluster`` no genera GRAPH_REPORT.md / graph.html / .graphify_labels.json.
- Cada corrida arranca en frío (el out dir se limpia antes de invocar):
    el update sobre un graph.json preexistente re-anexa las aristas
    preservadas sin deduplicar (duplicación progresiva en graphifyy 0.8.33),
    así que la idempotencia de bytes se garantiza por arranque en frío —
    dos corridas frías sobre el mismo corpus son sha256 idénticas.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ORG_ROOT_DEFAULT = "/opt/aps-conecta-org"
ORG = "APS-Conecta"
CATALOGO = REPO_ROOT / "catalogo.yml"
OUT_BASE = REPO_ROOT / "_generated" / "mapa"
BLOB_SEED = REPO_ROOT / "_generated" / "linkcheck-blob.txt"

# Kinds del catálogo que generan mapa. El resto degrada a «sin mapa»:
# sin página, sin entrada de toctree, una línea de registro por fila.
MAP_KINDS = {
    "suite",
    "distribution-fork",
    "nextcloud-app",
    "shared-library",
    "data-corpus",
    "canon-engine",
    "agent-prompts",
    "laboratory-app",
}
NON_MAP_KINDS = {"artifacts-store", "org-defaults", "docs-site"}

# .graphifyignore canónico — mismo conjunto de líneas para cada scan root
# (sintaxis gitignore; al existir .graphifyignore en un directorio, graphify
# ya no lee el .gitignore de ese directorio). Escrito solo si difieren los bytes.
IGNORE_PATTERNS = [
    "node_modules/",
    "vendor/",
    "apps/",
    "l10n/",
    "img/",
    "screenshots/",
    "demo-data/",
    "showcases/",
    ".browser-check/",
    "openapi/",
    "php-cs-fixer.d/",
    ".aps-replay-tree/",
    ".rpiv/",
    "*.png",
]

NO_CODE_SIGNATURE = "No code files found - nothing to rebuild."
PROVENANCE = "Mapa AST del repositorio, extraído con graphify al momento de compilar."

_LINE_RE = re.compile(r"^L?(\d+)$")


def die(msg: str) -> None:
    print(f"[mapa] error: {msg}", file=sys.stderr)
    sys.exit(1)


def org_root() -> Path:
    return Path(os.environ.get("APS_ORG_ROOT", ORG_ROOT_DEFAULT))


def load_roster(path: Path) -> list[dict]:
    """Lee catalogo.yml y valida cada kind contra el enum de 11 valores."""
    try:
        import yaml  # pyyaml: misma dependencia que gen-catalogo.py (fase 5)
    except ImportError:
        die("falta el módulo yaml (pip install pyyaml)")
    if not path.is_file():
        die(f"no existe {path} (fase 5)")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        die(f"catalogo.yml ilegible: {exc}")
    rows = data.get("repos")
    if not isinstance(rows, list) or not rows:
        die("catalogo.yml sin filas en «repos»")
    for row in rows:
        kind = row.get("kind")
        if kind not in MAP_KINDS | NON_MAP_KINDS:
            die(f"kind desconocido «{kind!r}» en la fila {row.get('repo')!r}")
    return rows


# ---------------------------------------------------------------------------
# Invocación de graphify
# ---------------------------------------------------------------------------

def canonical_ignore_text() -> str:
    return "\n".join(IGNORE_PATTERNS) + "\n"


def ensure_graphifyignore(scan_root: Path) -> bool:
    """Escribe el .graphifyignore canónico en el scan root si los bytes difieren."""
    path = scan_root / ".graphifyignore"
    want = canonical_ignore_text()
    try:
        have = path.read_text(encoding="utf-8")
    except OSError:
        have = None
    if have != want:
        path.write_text(want, encoding="utf-8")
        return True
    return False


def run_graphify(repo: str, scan_root: Path, out_dir: Path) -> str:
    """Ejecuta graphify update sobre un repo. Devuelve "ok" | "empty" | "fail"."""
    ensure_graphifyignore(scan_root)
    # Arranque en frío obligatorio: el update de graphifyy 0.8.33, sobre un
    # graph.json preexistente, re-anexa TODAS las aristas preservadas junto a
    # la extracción fresca y su comparación canónica no deduplica — cada
    # corrida tibia duplica aristas (verificado: 40 → 76 → 112 con 40 tríos
    # únicos constantes), rompiendo la idempotencia de bytes e inflando los
    # grados y conteos renderizados. Con el out dir limpio cada corrida es
    # determinista (dos corridas frías: sha256 idénticos).
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    scratch = out_dir / ".mrun"
    shutil.rmtree(scratch, ignore_errors=True)
    scratch.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "graphify", "update", str(scan_root.resolve()), "--no-cluster"]
    env = os.environ.copy()
    env["GRAPHIFY_OUT"] = str(out_dir.resolve())
    env["GRAPHIFY_FORCE"] = "1"
    proc = subprocess.run(cmd, cwd=scratch, env=env, capture_output=True, text=True)
    # manifest.json se escribe relativo al CWD (graphify-out/manifest.json):
    # reubicar al out dir y limpiar el scratch.
    manifest = scratch / "graphify-out" / "manifest.json"
    if manifest.is_file():
        manifest.replace(out_dir / "manifest.json")
    shutil.rmtree(scratch, ignore_errors=True)
    if proc.returncode == 0:
        return "ok"
    if NO_CODE_SIGNATURE in proc.stdout:
        return "empty"
    tail = "\n".join((proc.stdout + "\n" + proc.stderr).splitlines()[-12:])
    print(f"[mapa] {repo}: graphify falló (exit {proc.returncode}):\n{tail}", file=sys.stderr)
    return "fail"


# ---------------------------------------------------------------------------
# Render de la página (función pura de graph.json + repo)
# ---------------------------------------------------------------------------

def blob_anchor(repo: str, source_file, source_location) -> str | None:
    """Ancla GitHub para un nodo; None si la ruta es inutilizable (absoluta,
    con barra invertida o que escape del repo) o está ausente."""
    if not source_file:
        return None
    sf = str(source_file)
    if sf.startswith("/") or "\\" in sf or ".." in sf.split("/"):
        return None
    url = f"https://github.com/{ORG}/{repo}/blob/main/{sf}"
    m = _LINE_RE.fullmatch(str(source_location or "").strip())
    return f"{url}#L{m.group(1)}" if m else url


def extracted_degrees(graph: dict) -> Counter:
    """Grado (aristas incidentes) contando SOLO aristas EXTRACTED."""
    deg: Counter = Counter()
    for link in graph.get("links") or []:
        if link.get("confidence") != "EXTRACTED":
            continue
        s, t = link.get("source"), link.get("target")
        if not s or not t:
            continue
        if s == t:
            deg[s] += 1
        else:
            deg[s] += 1
            deg[t] += 1
    return deg


def dir_counts(graph: dict) -> Counter:
    """Nodos por directorio (dirname posix de source_file; raíz = «.»).
    Las rutas absolutas o con barra invertida no se cuentan."""
    dirs: Counter = Counter()
    for n in graph.get("nodes") or []:
        sf = n.get("source_file")
        if not sf:
            continue
        s = str(sf)
        if s.startswith("/") or "\\" in s:
            continue
        dirs[posixpath.dirname(s) or "."] += 1
    return dirs


def _tarjan_sccs(ids: list[str], adj: dict[str, set[str]]) -> list[list[str]]:
    """Tarjan iterativo; devuelve todas las SCC (incluidas las triviales)."""
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    on_stack: set[str] = set()
    stack: list[str] = []
    sccs: list[list[str]] = []
    counter = 0
    for root in ids:
        if root in index:
            continue
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on_stack.add(root)
        work: list[tuple[str, object]] = [(root, iter(sorted(adj.get(root, ()))))]
        while work:
            v, it = work[-1]
            pushed = False
            for w in it:  # type: ignore[union-attr]
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack.add(w)
                    work.append((w, iter(sorted(adj.get(w, ())))))
                    pushed = True
                    break
                if w in on_stack:
                    low[v] = min(low[v], index[w])
            if pushed:
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[v])
            if low[v] == index[v]:
                scc: list[str] = []
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    scc.append(w)
                    if w == v:
                        break
                sccs.append(scc)
    return sccs


def import_cycles(graph: dict) -> list[list[str]]:
    """SCC de tamaño ≥ 2 sobre las aristas EXTRACTED imports/imports_from."""
    adj: dict[str, set[str]] = {}
    ids: set[str] = set()
    for link in graph.get("links") or []:
        if link.get("confidence") != "EXTRACTED":
            continue
        if link.get("relation") not in ("imports", "imports_from"):
            continue
        s, t = link.get("source"), link.get("target")
        if not s or not t:
            continue
        adj.setdefault(s, set()).add(t)
        ids.add(s)
        ids.add(t)
    sccs = _tarjan_sccs(sorted(ids), adj)
    return [scc for scc in sccs if len(scc) >= 2]


def _table(rows: list[tuple], headers: tuple[str, ...]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out.extend("| " + " | ".join(str(c) for c in row) + " |" for row in rows)
    return out


def render_page(repo: str, graph: dict) -> str:
    """Página <slug>.md — función pura de graph.json (sin marcas de tiempo)."""
    nodes = graph.get("nodes") or []
    links = graph.get("links") or []
    by_id = {n.get("id"): n for n in nodes if n.get("id")}

    L: list[str] = [
        "---",
        "tipo: referencia",
        "---",
        "",
        f"# Mapa de módulos — {repo}",
        "",
        PROVENANCE,
        "",
        "## Resumen",
        "",
        f"- Nodos: {len(nodes)}",
        f"- Aristas: {len(links)}",
        "",
    ]

    ft = Counter(str(n.get("file_type") or "sin clasificar") for n in nodes)
    rel = Counter(str(l.get("relation") or "sin relación") for l in links)
    conf = Counter(str(l.get("confidence") or "sin confianza") for l in links)

    L.append("**Nodos por tipo de archivo**")
    L.append("")
    L += _table(sorted(((k, v) for k, v in ft.items()), key=lambda kv: (-kv[1], kv[0])),
                ("Tipo", "Nodos"))
    L.append("")
    L.append("**Aristas por relación**")
    L.append("")
    L += _table(sorted(((k, v) for k, v in rel.items()), key=lambda kv: (-kv[1], kv[0])),
                ("Relación", "Aristas"))
    L.append("")
    L.append("**Aristas por confianza**")
    L.append("")
    L += _table(sorted(((k, v) for k, v in conf.items()), key=lambda kv: (-kv[1], kv[0])),
                ("Confianza", "Aristas"))
    L.append("")

    L += ["## Núcleos", "", "Grados calculados solo sobre aristas EXTRACTED.", ""]
    deg = extracted_degrees(graph)
    ranked = sorted(
        ((deg[i], by_id[i]) for i in deg if i in by_id),
        key=lambda p: (-p[0], str(p[1].get("label") or p[1].get("id")), str(p[1].get("id"))),
    )
    if ranked:
        rows = []
        for d, n in ranked[:15]:
            label = str(n.get("label") or n.get("id"))
            anchor = blob_anchor(repo, n.get("source_file"), n.get("source_location"))
            sf = n.get("source_file")
            cell = f"[`{sf}`]({anchor})" if anchor and sf else "—"
            rows.append((f"`{label}`", cell, d))
        L += _table(rows, ("Núcleo", "Archivo", "Grado"))
    else:
        L.append("Sin aristas EXTRACTED en este grafo.")
    L.append("")

    L += ["## Por directorio", ""]
    dirs = dir_counts(graph)
    if dirs:
        L += _table(sorted(((k, v) for k, v in dirs.items()), key=lambda kv: (-kv[1], kv[0])),
                    ("Directorio", "Nodos"))
    else:
        L.append("Sin archivos con ruta en este grafo.")
    L.append("")

    L += [
        "## Ciclos de importación",
        "",
        "Componentes fuertemente conexos de tamaño ≥ 2 sobre las aristas EXTRACTED de tipo `imports`/`imports_from`.",
        "",
    ]
    cycles = import_cycles(graph)
    if cycles:
        ordered = sorted(
            ([str(by_id.get(i, {}).get("label") or i) for i in sorted(scc)] for scc in cycles),
            key=lambda members: (-len(members), members),
        )
        L.append(f"Se detectaron {len(ordered)} ciclos.")
        L.append("")
        for members in ordered[:10]:
            L.append("- " + " → ".join(f"`{m}`" for m in members))
        if len(ordered) > 10:
            L.append(f"- … y {len(ordered) - 10} más")
    else:
        L.append("Sin ciclos de importación detectados sobre aristas EXTRACTED.")
    L.append("")
    return "\n".join(L)


def render_empty_page(repo: str) -> str:
    return (
        "---\n"
        "tipo: referencia\n"
        "---\n"
        "\n"
        f"# Mapa de módulos — {repo}\n"
        "\n"
        f"{PROVENANCE}\n"
        "\n"
        "Sin módulos extraídos en este repositorio.\n"
    )


def write_if_changed(path: Path, text: str) -> None:
    try:
        if path.read_text(encoding="utf-8") == text:
            return
    except OSError:
        pass
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Modo principal
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Genera _generated/mapa/<slug>.md por repo del catálogo (graphify --no-cluster)."
    )
    parser.add_argument("--selftest", action="store_true",
                        help="pruebas con fixture sintético + micro-run en vivo opcional (explícito, nunca en make).")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()

    rows = load_roster(CATALOGO)
    root = org_root()
    OUT_BASE.mkdir(parents=True, exist_ok=True)
    wanted: dict[str, str] = {}  # slug -> repo (caso canónico)
    n_pages = 0
    for row in rows:
        repo = row.get("repo")
        if not repo or not isinstance(repo, str):
            die(f"fila sin «repo»: {row!r}")
        kind = row.get("kind")
        if kind not in MAP_KINDS:
            print(f"[mapa] omitido {repo}: kind {kind} no genera mapa")
            continue
        slug = repo.lower()
        wanted[slug] = repo
        scan_root = root / repo
        if not scan_root.is_dir():
            die(f"no existe el checkout {scan_root} (repo {repo})")
        out_dir = OUT_BASE / repo
        status = run_graphify(repo, scan_root, out_dir)
        if status == "fail":
            sys.exit(1)
        page = OUT_BASE / f"{slug}.md"
        if status == "empty":
            # Corpus cero: sin graph.json fresco; uno viejo de una corrida
            # anterior ya no representa el estado y se elimina.
            (out_dir / "graph.json").unlink(missing_ok=True)
            write_if_changed(page, render_empty_page(repo))
            print(f"[mapa] {repo}: sin corpus → {page.name} (degradado)")
        else:
            graph_path = out_dir / "graph.json"
            try:
                graph = json.loads(graph_path.read_text(encoding="utf-8"))
            except Exception as exc:
                die(f"{repo}: graph.json ilegible tras graphify: {exc}")
            write_if_changed(page, render_page(repo, graph))
            n_nodes = len(graph.get("nodes") or [])
            n_links = len(graph.get("links") or [])
            print(f"[mapa] {repo}: {n_nodes} nodos, {n_links} aristas → {page.name}")
        n_pages += 1

    # Podar páginas de slugs que ya no generan mapa: una página suelta sin
    # toctree que la referencie es un documento huérfano (-W fatal).
    for stale in OUT_BASE.glob("*.md"):
        if stale.stem not in wanted:
            stale.unlink()
            print(f"[mapa] poda {stale.name}: sin fila de mapa en el catálogo")

    # Semilla de linkcheck para las anclas blob (respaldo anclado del riesgo
    # r2): las páginas blob de GitHub no exponen anclas #L<n> a un GET simple
    # y el volumen de anclas por mapa vive bajo limitación de tasa de GitHub;
    # las rutas ya se verifican localmente al generarse desde los checkouts.
    # Una regex anclada por repo con mapa, en orden de catálogo; la semilla
    # privada de gen-catalogo (9 URL raíz) no se toca.
    BLOB_SEED.parent.mkdir(parents=True, exist_ok=True)
    blob_lines = "\n".join(
        rf"^https://github\.com/{ORG}/{repo}/blob/" for repo in wanted.values()
    ) + "\n"
    write_if_changed(BLOB_SEED, blob_lines)

    print(f"[mapa] {n_pages} páginas de mapa; {len(rows) - n_pages} filas sin mapa")
    return 0


# ---------------------------------------------------------------------------
# Selftest (explícito, offline; micro-run en vivo solo si hay checkout + graphify)
# ---------------------------------------------------------------------------

def selftest() -> int:
    fixture = {
        "nodes": [
            {"id": "a", "label": "Alpha", "file_type": "code",
             "source_file": "lib/x/a.php", "source_location": "L1"},
            {"id": "b", "label": "Beta", "file_type": "code",
             "source_file": "lib/x/b.php", "source_location": "L2"},
            {"id": "c", "label": "Gamma", "file_type": "code",
             "source_file": "lib/y/c.php", "source_location": "L3"},
            {"id": "d", "label": "Delta", "file_type": "document",
             "source_file": "README.md", "source_location": "2.4.0"},
        ],
        "links": [
            {"source": "a", "target": "b", "relation": "imports", "confidence": "EXTRACTED"},
            {"source": "b", "target": "c", "relation": "imports", "confidence": "EXTRACTED"},
            {"source": "c", "target": "a", "relation": "imports", "confidence": "EXTRACTED"},
            {"source": "a", "target": "d", "relation": "contains", "confidence": "EXTRACTED"},
            {"source": "b", "target": "a", "relation": "references", "confidence": "INFERRED"},
        ],
    }

    # Grados: EXTRACTED a-b, b-c, c-a, a-d → a=3, b=2, c=2, d=1;
    # la arista INFERRED b→a no debe inflar el grado.
    deg = extracted_degrees(fixture)
    assert deg["a"] == 3 and deg["b"] == 2 and deg["c"] == 2 and deg["d"] == 1, deg

    dirs = dir_counts(fixture)
    assert dirs["lib/x"] == 2 and dirs["lib/y"] == 1 and dirs["."] == 1, dirs

    cycles = import_cycles(fixture)
    assert len(cycles) == 1 and set(cycles[0]) == {"a", "b", "c"}, cycles

    base = f"https://github.com/{ORG}/farmacia/blob/main"
    assert blob_anchor("farmacia", "lib/X.php", "L27") == f"{base}/lib/X.php#L27"
    assert blob_anchor("farmacia", "lib/X.php", "2") == f"{base}/lib/X.php#L2"
    assert blob_anchor("farmacia", "lib/X.php", "2.4.0") == f"{base}/lib/X.php"
    assert blob_anchor("farmacia", "/abs/x.py", "L1") is None
    assert blob_anchor("farmacia", "a\\b.php", "L1") is None
    assert blob_anchor("farmacia", None, "L1") is None

    page = render_page("Prueba", fixture)
    assert page.startswith("---\ntipo: referencia\n---\n"), page[:40]
    for section in ("## Resumen", "## Núcleos", "## Por directorio", "## Ciclos de importación"):
        assert section in page, section
    assert PROVENANCE in page
    assert f"{base.replace('farmacia', 'Prueba')}/lib/x/a.php#L1" in page
    assert "`Alpha`" in page and "| 3 |" in page
    assert "/tmp" not in page

    empty = render_empty_page("Prueba")
    assert "Sin módulos extraídos en este repositorio." in empty
    assert empty.startswith("---\ntipo: referencia\n---\n")
    assert "|" not in empty

    assert canonical_ignore_text().splitlines() == IGNORE_PATTERNS
    assert canonical_ignore_text().endswith("\n")

    print("[mapa][selftest] fixture sintético: correcto")

    ps = org_root() / "pi-sandbox"
    if ps.is_dir() and importlib.util.find_spec("graphify") is not None:
        with tempfile.TemporaryDirectory(prefix="mapa-selftest-") as td:
            out = Path(td) / "g"
            status = run_graphify("pi-sandbox", ps, out)
            assert status == "ok", status
            for name in ("graph.json", "manifest.json", ".graphify_root"):
                assert (out / name).is_file(), name
            assert (out / "cache").is_dir(), "cache/"
            assert not (out / ".mrun").exists(), "scratch sin limpiar"
            g = json.loads((out / "graph.json").read_text(encoding="utf-8"))
            for n in g.get("nodes") or []:
                sf = str(n.get("source_file") or "")
                assert not sf.startswith("/"), f"ruta absoluta: {sf}"
                assert "\\" not in sf, f"barra invertida: {sf}"
            live = render_page("pi-sandbox", g)
            assert "## Resumen" in live and "/opt/" not in live
        print("[mapa][selftest] micro-run en vivo de pi-sandbox: correcto")
    else:
        print("[mapa][selftest] micro-run en vivo omitido (sin checkout o sin graphify instalado)")

    print("[mapa][selftest] OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
