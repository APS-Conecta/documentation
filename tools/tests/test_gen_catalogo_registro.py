"""gen-catalogo: la lista de aplicaciones se lee del manifiesto del repositorio de la suite (gestion-aio)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_upstream import load  # noqa: E402

gc = load("gen-catalogo")


class RegistroTest(unittest.TestCase):
    def test_el_manifiesto_vive_en_gestion_aio(self):
        raiz = Path("/org")
        self.assertEqual(
            gc.manifest_path(raiz),
            raiz / "gestion-aio" / "aps" / "provisionador" / "apps.json")

    def test_gestion_aio_sin_manifiesto_falla(self):
        gc.selftest_registro()


if __name__ == "__main__":
    unittest.main()
