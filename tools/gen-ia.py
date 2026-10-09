#!/usr/bin/env python3
"""gen-ia — the AI-use table of the legal notice, from ia.yml (generated, never committed)."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def render(doc: dict) -> str:
    def cell(t) -> str:
        return str(t).replace("|", "\\|")

    lines = ["| Herramienta | Proveedor | Modelos | Uso | Desde | Revisión |", "|---|---|---|---|---|---|"]
    for t in doc["tools"]:
        models = ", ".join(f"`{m}`" if m[:1].islower() else m for m in t["models"])
        use = t["use"] + (f" {t['note']}" if t.get("note") else "")
        lines.append(f"| {cell(t['tool'])} | {cell(t['provider'])} | {cell(models)} | {cell(use)} | "
                     f"{t['since']} | {cell(t['review'])} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    doc = yaml.safe_load((ROOT / "ia.yml").read_text(encoding="utf-8"))
    out = ROOT / "_generated" / "ia.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(doc), encoding="utf-8")
    print(f"[gen-ia] {len(doc['tools'])} herramientas → {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
