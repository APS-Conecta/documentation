"""gen-catalogo: la lista de aplicaciones se lee del manifiesto del instalador."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_upstream import load  # noqa: E402

gc = load("gen-catalogo")


class RegistroTest(unittest.TestCase):
    def test_el_manifiesto_vive_en_instalador(self):
        raiz = Path("/org")
        self.assertEqual(
            gc.manifest_path(raiz),
            raiz / "instalador" / "apps.json")

    def test_gestion_sin_manifiesto_e_instalador_con_manifiesto(self):
        gc.selftest_registro()


if __name__ == "__main__":
    unittest.main()
