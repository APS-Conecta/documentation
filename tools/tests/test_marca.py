"""The «Marca» page and the site's stylesheet take the brand from the suite's brand token file."""

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_upstream import load  # noqa: E402

gm = load("gen-marca")
ROOT = Path(__file__).resolve().parents[2]

# The brand manual's palette (Manual de Marca v2.0): role, value and contrast on white. The manual prints ink at
# 17.8:1, its 17.75 rounded again; the WCAG 2 ratio is 17.747, so one decimal is 17.7.
MANUAL = {
    "violet": ("#7f21fe", "5,9:1"),
    "violet-dark": ("#5315a8", "10,3:1"),
    "violet-hover": ("#6c1bd9", "7,5:1"),
    "ink": ("#101828", "17,7:1"),
    "muted": ("#485363", "7,8:1"),
    "error": ("#ea003e", "4,6:1"),
    "error-text": ("#cc0033", "5,8:1"),
    "warning": ("#f34700", "3,7:1"),
    "success": ("#009764", "3,7:1"),
    "info": ("#0082ce", "4,1:1"),
    "warning-text": ("#9a4c00", "6,2:1"),
    "logo-gold": ("#f28f36", "2,4:1"),
}

TOKENS = """:root {
  --aps-violet: #7f21fe;  /* primary */
  --aps-violet-dark: #5315a8;
  --aps-violet-hover: #6c1bd9;
  --aps-violet-tint: #ece6ff;
  --aps-violet-tint-hover: #d9cdff;
  --aps-violet-wash: #faf8fe;
  --aps-logo-gold: #f28f36;
  --aps-ink: #101828;
  --aps-muted: #485363;
  --aps-canvas: #f1f2f4;
  --aps-border: #e2e5e9;
  --aps-paper: white;
  --aps-error: #ea003e;
  --aps-error-text: #cc0033;
  --aps-warning: #f34700;
  --aps-warning-text: #9a4c00;
  --aps-success: #009764;
  --aps-info: #0082ce;
  --aps-night-violet: #a66bff;
  --aps-font-display: "Fraunces", Georgia, serif;
}
"""

COLOUR_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(")


def rows(table: str) -> dict[str, list[str]]:
    cells = [[c.strip() for c in line.strip("|").split("|")] for line in table.splitlines()[2:] if line]
    return {c[0].strip("`").removeprefix("--aps-"): c[1:] for c in cells}


class PaletteTableTest(unittest.TestCase):
    def test_every_light_colour_role_of_the_token_file_is_a_row(self):
        table = rows(gm.render(TOKENS))
        self.assertEqual(
            set(table),
            {"violet", "violet-dark", "violet-hover", "violet-tint", "violet-tint-hover", "violet-wash",
             "logo-gold", "ink", "muted", "canvas", "border", "paper", "error", "error-text", "warning",
             "warning-text", "success", "info"})

    def test_values_and_contrast_on_white_are_the_manuals(self):
        table = rows(gm.render(TOKENS))
        for role, (value, contrast) in MANUAL.items():
            with self.subTest(role=role):
                self.assertEqual(table[role][:2], [f"`{value}`", contrast])

    def test_a_background_role_shows_no_contrast(self):
        table = rows(gm.render(TOKENS))
        self.assertEqual(table["paper"][:2], ["`white`", "—"])
        self.assertEqual(table["canvas"][:2], ["`#f1f2f4`", "—"])

    def test_the_value_is_the_token_files(self):
        table = rows(gm.render(TOKENS.replace("#7f21fe", "#7f21ff")))
        self.assertEqual(table["violet"][0], "`#7f21ff`")

    def test_a_colour_role_without_a_use_fails(self):
        with self.assertRaisesRegex(ValueError, "--aps-violet-glow"):
            gm.render(TOKENS.replace("}", "  --aps-violet-glow: #b0f;\n}"))

    def test_a_role_missing_from_the_token_file_fails(self):
        with self.assertRaisesRegex(ValueError, "--aps-info"):
            gm.render(TOKENS.replace("  --aps-info: #0082ce;\n", ""))

    def test_a_token_inside_a_comment_is_not_a_role(self):
        table = rows(gm.render(TOKENS.replace("/* primary */", "/* not --aps-violet-glow: #b0f; */")))
        self.assertNotIn("violet-glow", table)

    def test_empty_input_fails(self):
        with self.assertRaises(ValueError):
            gm.render("")


class SiteStylesheetTest(unittest.TestCase):
    def test_the_site_stylesheet_has_no_colour_literal(self):
        for name in ("_static/css/aps-brand.css", "conf.py"):
            with self.subTest(file=name):
                text = (ROOT / name).read_text(encoding="utf-8")
                self.assertEqual(COLOUR_LITERAL.findall(text), [])


if __name__ == "__main__":
    unittest.main()
