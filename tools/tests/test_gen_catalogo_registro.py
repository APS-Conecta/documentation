"""gen-catalogo: el registro OWN_APPS se lee del instalador, no de gestion."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_upstream import load  # noqa: E402

gc = load("gen-catalogo")


class RegistroTest(unittest.TestCase):
    def test_registro_vive_en_instalador(self):
        raiz = Path("/org")
        self.assertEqual(
            gc.registry_path(raiz),
            raiz / "instalador" / "provisioning" / "phases" / "12-apps.sh")

    def test_gestion_sin_registro_e_instalador_con_registro(self):
        gc.selftest_registro()


if __name__ == "__main__":
    unittest.main()
