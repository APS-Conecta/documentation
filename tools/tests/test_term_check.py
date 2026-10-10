"""term-check (scribe S5): one approved Spanish form per term, one register, no Spain-only forms."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_upstream import load  # noqa: E402

tc = load("term-check")

GL = {
    "terms": [{"en": "Administration settings", "es": "Configuraciones de administración",
               "evitar": ["ajustes de administración"]}],
    "tecnicos": [{"en": "backend", "es": "backend", "evitar": ["back-end"]},
                 {"en": "log", "re": r"logs?(?![- ](?:in|out)\b)", "es": "registro"},
                 {"es": "computador", "evitar": ["ordenador", "ordenadores"]}],
}


def page(content, doc="admin_manual/x"):
    return f"# T\n\n````{{upstream}} {doc}.rst@3ad9158\n{content}\n````\n"


class TermCheckTest(unittest.TestCase):
    def check(self, text, section="", cat=()):
        return tc.check_page(text, GL, lambda block: (section, dict(cat)))

    def test_an_evitar_variant_fails_anywhere_in_prose(self):
        self.assertEqual(len(self.check("Abrir los ajustes de administración.\n")), 1)
        self.assertEqual(len(self.check(page("Usar un back-end propio."))), 1)
        self.assertEqual(len(self.check(page("Desde su ordenador."))), 1)

    def test_code_roles_and_quoted_messages_are_not_prose(self):
        text = "Ver `back-end`, {guilabel}`ajustes de administración` y «back-end»; [x](https://a.example/back-end).\n"
        self.assertEqual(self.check(text), [])

    def test_a_block_carries_the_approved_form_of_its_sections_terms(self):
        self.assertEqual(len(self.check(page("Usar un motor propio."), "Use your own backend.")), 1)
        self.assertEqual(self.check(page("Usar backends propios."), "Use your own backends."), [])
        # «log in» is no log
        self.assertEqual(self.check(page("Iniciar sesión."), "Log in first."), [])
        self.assertEqual(len(self.check(page("Ver el archivo."), "See the log file.")), 1)

    def test_upstream_code_and_quoted_text_are_not_the_sections_terms(self):
        self.assertEqual(self.check(page("Habilitar la app."), "Enable the ``webhook_listeners`` app with a ``backend``."), [])
        self.assertEqual(self.check(page("El mensaje «Revise los registros»."), 'It says "Look at the backend logs".'), [])

    def test_headings_names_and_bold_labels(self):
        self.assertEqual(self.check(page("### Cambios de backend\n\nTexto."), "Backend changes\n===============\n\nText."), [])
        self.assertEqual(self.check(page("Ver la página."), "See code-backend and backend-x."), [])
        self.assertEqual(self.check(page("Hacer clic en «Open backend»."), "Click **Open backend**."), [])

    def test_an_official_msgstr_is_the_translators_words(self):
        text = page("Desde su ordenador, puedes subir archivos.", "user_manual/x")
        self.assertEqual(self.check(text, cat=[("From your computer you can upload files.", "Desde su ordenador, puedes subir archivos.")]), [])
        # nor does its upstream paragraph demand an approved form
        self.assertEqual(self.check(page("Desde su ordenador, puedes subir archivos.", "user_manual/x"), "Use the server backend.",
                                    cat=[("Use the server backend.", "Desde su ordenador, puedes subir archivos.")]), [])

    def test_the_official_set_is_compared_as_plain_text(self):
        self.assertEqual(tc.official({"m": "Algo que *tienes* y `un enlace <https://a.example>`_."}),
                         {"Algo que tienes y un enlace."})

    def test_tuteo_and_vosotros_fail_impersonal_and_usted_pass(self):
        for bad in ("Haz clic en Guardar.", "Ahora puedes subir tus archivos.", "Si tienes dudas, escribe.",
                    "Vosotros lo veréis."):
            self.assertTrue(self.check(bad + "\n"), bad)
        for ok in ("Hacer clic en Guardar.", "Puede subir sus archivos.", "Se pulsa el botón.",
                   "Ejemplo: «¿Puedes resumir tu correo?»", "El sistema elige un servidor y recuerda la elección."):
            self.assertEqual(self.check(ok + "\n"), [], ok)


if __name__ == "__main__":
    unittest.main()
