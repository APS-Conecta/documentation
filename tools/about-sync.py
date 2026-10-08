#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Sincroniza los `role` de catalogo.yml con las descripciones (About) de la org.

Por fila: leer (`gh api repos/… --jq .description`), comparar, omitir si son
iguales; si no, `gh api -X PATCH … -f description=<role>` y re-leer verificando
la igualdad — cualquier fallo (API o divergencia post-PATCH) ⇒ exit 1. El bucle
leer→PATCH→verificar es el contrato de salida. `--dry-run`: solo reporta, cero
PATCH. El token viaja en el ambiente (`GH_TOKEN`), nunca en argv ni URL.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ORG = "APS-Conecta"


def fail(msg: str) -> None:
    print(f"[about-sync] ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def gh(args: list[str]) -> str:
    # GH_TOKEN va en el ambiente (lo acuña el workflow); jamás en argv o URL.
    proc = subprocess.run(["gh", *args], capture_output=True, text=True)
    if proc.returncode != 0:
        fail(f"gh api {args[1]}…: {proc.stderr.strip()}")
    return proc.stdout.strip()


def main() -> int:
    dry = "--dry-run" in sys.argv[1:]
    doc = yaml.safe_load((REPO_ROOT / "catalogo.yml").read_text(encoding="utf-8"))
    rows = doc["repos"]
    if len(rows) != 15:
        fail(f"catalogo.yml: esperaba 15 filas, hay {len(rows)}")
    cambios = 0
    for row in rows:
        repo, role = row["repo"], row["role"]
        actual = gh(["api", f"repos/{ORG}/{repo}", "--jq", ".description"])
        if actual == role:
            print(f"[about-sync] {repo}: descripción sin cambios")
            continue
        if dry:
            print(f"[about-sync] {repo}: actualizaría la descripción (dry-run)")
            cambios += 1
            continue
        gh(["api", "-X", "PATCH", f"repos/{ORG}/{repo}", "-f", f"description={role}"])
        despues = gh(["api", f"repos/{ORG}/{repo}", "--jq", ".description"])
        if despues != role:
            fail(f"{repo}: tras el PATCH la descripción no coincide ({despues!r} ≠ {role!r})")
        print(f"[about-sync] {repo}: descripción actualizada")
        cambios += 1
    sufijo = " (dry-run)" if dry else ""
    print(f"[about-sync] {len(rows)} repositorios, {cambios} cambio(s){sufijo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
