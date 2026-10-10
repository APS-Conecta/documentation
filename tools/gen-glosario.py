#!/usr/bin/env python3
"""gen-glosario — publish glosario.yml as proyecto/glosario (generated, never committed)."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def render(doc: dict) -> str:
    avoid = lambda t: ", ".join(f"«{v}»" for v in t.get("evitar", [])) or "—"  # noqa: E731
    rows = "\n".join(f"| {t['es']} | {t['en']} | `{t['source']}/l10n/es.json` | {avoid(t)} |" for t in doc["terms"])
    tech = "\n".join(f"| {t['es']} | {t.get('en', '—')} | {avoid(t)} |" for t in doc.get("tecnicos", []))
    return f"""---
tipo: referencia
audiencia: proyecto
apps: []
resumen: Términos de la interfaz en español que usa toda la documentación, con su fuente.
---
# Glosario

## Resumen

La documentación nombra cada elemento de la interfaz como lo muestra la plataforma en español. Este glosario fija esos nombres para las páginas propias y para las traducciones de la plataforma base; cada término cita el archivo de traducciones del servidor (rama `{doc['server_branch']}`) del que sale.

## Tabla

### Interfaz

| En la interfaz | En inglés | Fuente | Evitar |
|---|---|---|---|
{rows}

### Términos técnicos

Forma aprobada de cada término técnico y las variantes que la documentación no usa; `make term-check` lo exige.

| Forma aprobada | En inglés | Evitar |
|---|---|---|
{tech}
"""


def main() -> int:
    doc = yaml.safe_load((ROOT / "glosario.yml").read_text(encoding="utf-8"))
    out = ROOT / "_generated" / "glosario.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(doc), encoding="utf-8")
    print(f"[gen-glosario] {len(doc['terms'])} términos → {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
