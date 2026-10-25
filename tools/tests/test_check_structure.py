"""check-structure (scribe Q24, ported): typed front matter and the H2 skeleton of each page."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_upstream import load  # noqa: E402

cs = load("check-structure")

CATALOG = ["gestion", "instalador", "territorio"]


def page(tipo, audiencia, apps, resumen, body="", esqueleto=None):
    extra = f"esqueleto: {esqueleto}\n" if esqueleto else ""
    return (
        "---\n"
        f"tipo: {tipo}\n"
        f"audiencia: {audiencia}\n"
        f"apps: {apps}\n"
        f'{extra}resumen: {resumen}\n'
        "---\n"
        "# Título\n\n"
        f"{body}"
    )


GUIA_BODY = "## Objetivo\n\nUno.\n\n## Requisitos\n\nDos.\n\n## Pasos\n\nTres.\n\n## Verificación\n\nCuatro.\n"


class CheckStructureTest(unittest.TestCase):
    def problems(self, rel, text):
        return cs.problems(rel, text, CATALOG)

    def test_a_well_formed_guia_has_no_problems(self):
        self.assertEqual(self.problems("administracion/x.md", page("guia", "administracion", "[gestion]", '"Corta."', GUIA_BODY)), [])

    def test_a_161_character_resumen_fails(self):
        text = page("guia", "administracion", "[gestion]", "x" * 161, GUIA_BODY)
        self.assertIn("resumen is 161 chars (max 160)", self.problems("administracion/x.md", text))

    def test_apps_naming_a_repo_outside_the_catalog_fails(self):
        text = page("guia", "administracion", "[AIO]", "Corta.", GUIA_BODY)
        self.assertIn("apps names 'AIO', not in the catalog", self.problems("administracion/x.md", text))

    def test_a_guia_without_verificacion_fails(self):
        body = "## Objetivo\n\nUno.\n\n## Requisitos\n\nDos.\n\n## Pasos\n\nTres.\n"
        self.assertIn(
            "H2 skeleton for guia: missing 'Verificación'",
            self.problems("administracion/x.md", page("guia", "administracion", "[gestion]", "Corta.", body)),
        )

    def test_an_out_of_order_h2_fails(self):
        body = "## Requisitos\n\nDos.\n\n## Objetivo\n\nUno.\n\n## Pasos\n\nTres.\n\n## Verificación\n\nCuatro.\n"
        self.assertIn(
            "H2 'Objetivo' is out of order for guia (Objetivo, Requisitos, Pasos, Verificación, Problemas frecuentes)",
            self.problems("administracion/x.md", page("guia", "administracion", "[gestion]", "Corta.", body)),
        )

    def test_an_audiencia_different_from_the_directory_fails(self):
        self.assertIn(
            "audiencia 'usuario' does not match the directory 'administracion'",
            self.problems("administracion/x.md", page("guia", "usuario", "[gestion]", "Corta.", GUIA_BODY)),
        )

    def test_index_md_owes_the_front_matter_only(self):
        self.assertEqual(self.problems("administracion/index.md", page("guia", "administracion", "[gestion]", "Corta.", "")), [])

    def test_an_h2_inside_a_fence_is_an_example_not_the_page(self):
        body = (
            "## Objetivo\n\nUno.\n\n## Requisitos\n\nDos.\n\n## Pasos\n\nTres.\n\n## Verificación\n\nCuatro.\n\n"
            "````{upstream} admin_manual/x.rst@sha\n"
            "## Fenced heading\n\nProse.\n"
            "````\n"
        )
        self.assertEqual(self.problems("administracion/x.md", page("guia", "administracion", "[gestion]", "Corta.", body)), [])

    def test_no_front_matter_fails(self):
        self.assertEqual(self.problems("administracion/x.md", "# Título\n\nProsa.\n"), ["no front matter"])

    def test_the_esqueleto_override_replaces_the_skeleton(self):
        body = "## Propósito y diseño\n\nUno.\n\n## Deuda técnica y límites\n\nDos.\n"
        self.assertEqual(
            self.problems("desarrollo/x.md", page("referencia", "desarrollo", "[territorio]", "Corta.", body, esqueleto="contratos")),
            [],
        )

    def test_an_unknown_esqueleto_fails(self):
        self.assertIn(
            "esqueleto 'x' is not one of plataforma, borrador, contratos",
            self.problems("desarrollo/x.md", page("referencia", "desarrollo", "[territorio]", "Corta.", "", esqueleto="x")),
        )


if __name__ == "__main__":
    unittest.main()
