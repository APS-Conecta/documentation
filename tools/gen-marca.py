#!/usr/bin/env python3
"""gen-marca — the palette table of desarrollo/marca, from the suite's brand token file (generated, never committed).

The token file is gestion-aio's aps/brand/tokens.css, which `make brand` fetches. Every light colour role of the file
is a row, with its value as the file writes it and, for a colour that is drawn on white, its contrast by the WCAG 2
formula. A colour role the page has no use for, or a use whose role the file lacks, fails the build.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = ROOT / "_generated" / "brand" / "brand" / "tokens.css"
OUT = ROOT / "_generated" / "marca-paleta.md"

# The brand manual's allowed use of each role, and whether the role is drawn on white (its contrast is shown).
USES = {
    "violet": ("Texto, botones y enlaces", True),
    "violet-dark": ("Títulos, el fondo del inicio de sesión y la barra superior", True),
    "violet-hover": ("El color primario al pasar el puntero", True),
    "violet-tint": ("Fondo de los elementos seleccionados, con texto en `--aps-violet-dark`", False),
    "violet-tint-hover": ("Fondo de un elemento seleccionado al pasar el puntero, con texto en `--aps-violet-dark`",
                          False),
    "violet-wash": ("Fondo de una navegación", False),
    "ink": ("Texto principal", True),
    "muted": ("Texto secundario", True),
    "canvas": ("Fondos al pasar el puntero", False),
    "border": ("Bordes decorativos, nunca el borde de un campo", False),
    "error": ("Bordes, iconos y texto grande; nunca texto de cuerpo", True),
    "error-text": ("Texto de error", True),
    "warning": ("Bordes, iconos y rellenos; nunca texto", True),
    "warning-text": ("Texto de advertencia", True),
    "success": ("Bordes, iconos y rellenos; nunca texto", True),
    "info": ("Bordes, iconos y rellenos; nunca texto", True),
    "logo-gold": ("Solo el logotipo", True),
    "paper": ("Fondos, y texto sobre violeta", False),
}
# The token file's roles that are not light colours: the font pairing and the dark theme of AIO's page.
NOT_PALETTE = ("font-", "night-")

COMMENT = re.compile(r"/\*.*?\*/", re.S)
TOKEN = re.compile(r"--aps-([a-z0-9-]+)\s*:\s*([^;]+?)\s*;")
HEX = re.compile(r"#([0-9a-fA-F]{6})")


def tokens(css: str) -> dict[str, str]:
    return dict(TOKEN.findall(COMMENT.sub("", css)))


def contrast_on_white(value: str) -> str:
    match = HEX.fullmatch(value)
    if not match:
        raise ValueError(f"a colour drawn on white needs a #rrggbb value, not {value!r}")
    channels = [int(match[1][i:i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = (c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return f"{1.05 / (luminance + 0.05):.1f}".replace(".", ",") + ":1"


def render(css: str) -> str:
    found = {role: value for role, value in tokens(css).items() if not role.startswith(NOT_PALETTE)}
    unused = sorted(set(found) - set(USES))
    missing = [role for role in USES if role not in found]
    if unused or missing:
        raise ValueError("palette and token file differ: "
                         + ", ".join([f"--aps-{r} has no use" for r in unused]
                                     + [f"--aps-{r} is missing" for r in missing]))
    lines = ["| Rol | Valor | Contraste sobre blanco | Uso permitido |", "|---|---|---|---|"]
    for role, (use, on_white) in USES.items():
        value = found[role]
        lines.append(f"| `--aps-{role}` | `{value}` | {contrast_on_white(value) if on_white else '—'} | {use} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    if not TOKENS.is_file():
        print(f"[gen-marca] no token file at {TOKENS.relative_to(ROOT)} — run make brand")
        return 1
    OUT.write_text(render(TOKENS.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"[gen-marca] {len(USES)} roles → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
