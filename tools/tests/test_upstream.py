"""Tests for the upstream machinery: upstreamlib, upstream-fidelity, rebrand-check (scribe S2b).

Every fidelity rule has a passing fixture and a planted violation, so a rule that stops firing
shows up here before it shows up as a wrong page on the site.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
import upstreamlib as u  # noqa: E402


def load(name):
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_"), TOOLS / f"{name}.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fidelity = load("upstream-fidelity")
rebrand_check = load("rebrand-check")

CFG = {
    "source": {
        "manuals": ["user_manual", "admin_manual"],
        "catalog": "user_manual/locale/es/LC_MESSAGES/{path}.pot",
        "external": {
            "user_manual": "https://docs.example/{major}/u/{path}.html",
            "admin_manual": "https://docs.example/{major}/a/{path}.html",
        },
        "major_from": {"file": "x", "pattern": "x"},
    },
    "rename": {
        "from": "Nextcloud",
        "to": "APS Conecta Gestión",
        "keep": ["Nextcloud GmbH", "Nextcloud Desktop"],
        "exempt_pages": ["aviso"],
    },
    "exclude": ["user_manual/contents"],
    "map": [
        {"from": "user_manual/webinterface", "to": "usuario/interfaz-web.md"},
        {"from": "user_manual/userpreferences", "to": "usuario/perfil.md"},
        {"from": "user_manual/user_2fa", "to": "usuario/perfil.md"},
        {"from": "user_manual/files/*", "to": "usuario/archivos/{path}.md"},
        {
            "from": "admin_manual/installation/*",
            "to": "administracion/instalacion/{path}.md",
            "difiere": "administracion/aio",
        },
    ],
}

UPSTREAM = """\
.. _webgui:

=====================
Using the web interface
=====================

You can access your Nextcloud files with the Nextcloud Web interface.

Navigating
----------

Click a folder name in the file list to open it, then use the
breadcrumb bar at the top. See :doc:`files/sharing` and :ref:`quota`.

.. code-block:: bash
   :caption: list

   ls -la

Run ``occ files:scan`` after a manual copy. Read `the guide <https://example.org/g>`_.

Details
~~~~~~~

The sidebar shows details.
"""

GOOD = """\
### Navegar

Hacer clic en el nombre de una carpeta de la lista para abrirla y usar la barra de ruta superior. Ver {nc-doc}`user_manual/files/sharing` y {nc-ref}`quota`.

```bash
ls -la
```

Ejecutar `occ files:scan` tras una copia manual. Leer [la guía](https://example.org/g).

#### Detalles

Puede acceder a sus archivos en Nextcloud con la interfaz web de Nextcloud.
"""


def block(content, arg="user_manual/webinterface.rst@3ad9158", options=None):
    return u.blocks(
        f"````{{upstream}} {arg}\n"
        + "".join(f":{k}: {v}\n" for k, v in (options or {}).items())
        + content
        + "````\n"
    )[0]


CATALOG = {
    "You can access your Nextcloud files with the Nextcloud Web interface.": "Puede acceder a sus archivos en Nextcloud con la interfaz web de Nextcloud."
}


class MapTest(unittest.TestCase):
    def test_prefix_rule_slugs_the_path(self):
        self.assertEqual(
            u.destination("user_manual/files/access_webgui", CFG)[0],
            "usuario/archivos/access-webgui.md",
        )

    def test_exact_rule_and_exclusion(self):
        self.assertEqual(
            u.destination("user_manual/webinterface", CFG)[0], "usuario/interfaz-web.md"
        )
        self.assertIsNone(u.destination("user_manual/contents", CFG))
        with self.assertRaises(LookupError):
            u.destination("user_manual/unknown", CFG)

    def test_deliberate_weave_is_allowed_a_path_collision_is_not(self):
        self.assertEqual(
            u.map_problems(
                ["user_manual/userpreferences", "user_manual/user_2fa"], CFG
            ),
            [],
        )
        clash = dict(
            CFG,
            map=CFG["map"]
            + [{"from": "user_manual/talk/*", "to": "usuario/archivos/{path}.md"}],
        )
        self.assertEqual(
            u.map_problems(["user_manual/files/x", "user_manual/talk/x"], clash),
            [
                "user_manual/talk/x: page usuario/archivos/x.md already holds user_manual/files/x"
            ],
        )


class RenameTest(unittest.TestCase):
    def test_renames_the_product_and_keeps_legal_names(self):
        self.assertEqual(
            u.rename(
                "Nextcloud lo gestiona Nextcloud GmbH; instalar Nextcloud Desktop.", CFG
            ),
            "APS Conecta Gestión lo gestiona Nextcloud GmbH; instalar Nextcloud Desktop.",
        )
        self.assertEqual(
            u.rename("nextcloud.com y NextcloudPi", CFG), "nextcloud.com y NextcloudPi"
        )

    def test_rebrand_check_reads_only_visible_prose(self):
        html = (
            "<p>Abrir Nextcloud.</p><pre>nextcloud Nextcloud</pre><code>Nextcloud</code>"
            '<p class="atribucion">documentación de Nextcloud</p><p>Nextcloud GmbH</p>'
        )
        text = rebrand_check.visible_text(html)
        self.assertEqual(len(u.leftovers(text, CFG)), 1)


class RstTest(unittest.TestCase):
    def test_headings_levels_follow_first_seen_style(self):
        self.assertEqual(
            [(lv, t) for lv, t, _ in u.rst_headings(UPSTREAM)],
            [(1, "Using the web interface"), (2, "Navigating"), (3, "Details")],
        )

    def test_section_by_label_and_by_slug(self):
        self.assertIn("Navigating", u.rst_section(UPSTREAM, "webgui"))
        self.assertNotIn("Using the web interface", u.rst_section(UPSTREAM))
        self.assertTrue(
            u.rst_section(UPSTREAM, "details").strip().startswith("The sidebar")
        )
        with self.assertRaises(LookupError):
            u.rst_section(UPSTREAM, "nope")

    def test_code_literals_links_and_xrefs(self):
        self.assertEqual(u.rst_code_blocks(UPSTREAM), ["ls -la"])
        self.assertEqual(u.rst_inline_literals(UPSTREAM), ["occ files:scan"])
        self.assertEqual(u.rst_links(UPSTREAM), {"https://example.org/g"})
        self.assertEqual(
            u.rst_xrefs(UPSTREAM, "user_manual/webinterface"),
            [("doc", "user_manual/files/sharing"), ("ref", "quota")],
        )
        self.assertEqual(u.absolute_doc("admin_manual/a/b", "../c"), "admin_manual/c")

    def test_literal_block_after_double_colon(self):
        self.assertEqual(
            u.rst_code_blocks("Run this::\n\n   occ status\n   occ check\n\nThen."),
            ["occ status\nocc check"],
        )


class BlockTest(unittest.TestCase):
    def test_four_backtick_block_holds_code_and_options(self):
        b = block(GOOD, options={"difiere": "administracion/aio"})
        self.assertEqual(
            (b["doc"], b["sha"], b["anchor"]),
            ("user_manual/webinterface", "3ad9158", ""),
        )
        self.assertEqual(b["options"], {"difiere": "administracion/aio"})
        self.assertEqual(u.myst_code_blocks(b["content"]), ["ls -la"])
        self.assertEqual([lv for lv, _ in u.myst_headings(b["content"])], [3, 4])

    def test_bad_argument_is_reported(self):
        found, _ = fidelity.check_block(
            block(GOOD, arg="webinterface@zz"), "usuario/interfaz-web.md", "", {}, CFG
        )
        self.assertIn("is not <manual>/<path>.rst@<sha>", found[0])


class FidelityTest(unittest.TestCase):
    def check(
        self,
        content,
        page="usuario/interfaz-web.md",
        arg="user_manual/webinterface.rst@3ad9158",
        options=None,
        catalog=CATALOG,
    ):
        return fidelity.check_block(
            block(content, arg, options), page, UPSTREAM, catalog, CFG
        )

    def test_faithful_block_passes(self):
        found, ai = self.check(GOOD)
        self.assertEqual(found, [])
        self.assertGreaterEqual(
            ai, 1
        )  # the paragraphs with no official string are counted

    def test_misplaced_and_unmapped(self):
        self.assertIn(
            "belongs on usuario/interfaz-web.md",
            self.check(GOOD, page="usuario/x.md")[0][0],
        )
        self.assertIn(
            "not in upstream.yml",
            self.check(GOOD, arg="user_manual/nope.rst@3ad9158")[0][0],
        )

    def test_difiere_required(self):
        found, _ = fidelity.check_block(
            block(GOOD, "admin_manual/installation/x.rst@3ad9158"),
            "administracion/instalacion/x.md",
            UPSTREAM,
            {},
            CFG,
        )
        self.assertTrue(any("needs :difiere:" in f for f in found), found)

    def test_heading_structure(self):
        found, _ = self.check(GOOD.replace("#### Detalles", "### Detalles"))
        self.assertTrue(any("headings" in f for f in found), found)

    def test_code_must_be_byte_identical(self):
        found, _ = self.check(GOOD.replace("ls -la", "ls -l"))
        self.assertTrue(any("code blocks differ" in f for f in found), found)

    def test_inline_literal_translated(self):
        found, _ = self.check(
            GOOD.replace("`occ files:scan`", "`occ archivos:escanear`")
        )
        self.assertTrue(any("inline literals" in f for f in found), found)

    def test_links_and_xrefs(self):
        found, _ = self.check(
            GOOD.replace("https://example.org/g", "https://example.org/otra")
        )
        self.assertTrue(any("external links" in f for f in found), found)
        found, _ = self.check(GOOD.replace("{nc-ref}`quota`", "la cuota"))
        self.assertTrue(any("cross-references" in f for f in found), found)

    def test_official_wording_is_verbatim(self):
        found, _ = self.check(
            GOOD.replace("Puede acceder a sus archivos", "Usted accede a sus archivos")
        )
        self.assertTrue(
            any("official Spanish not used verbatim" in f for f in found), found
        )

    def test_english_paragraph(self):
        found, _ = self.check(
            GOOD
            + "\nYou can open the file in the sidebar and then share it with your team.\n",
            catalog={},
        )
        self.assertTrue(any("reads as English" in f for f in found), found)

    def test_labels_kept(self):
        up = UPSTREAM.replace(
            "Details\n~~~~~~~", ".. _details-label:\n\nDetails\n~~~~~~~"
        )
        found, _ = fidelity.check_block(
            block(GOOD), "usuario/interfaz-web.md", up, CATALOG, CFG
        )
        self.assertTrue(any("labels missing" in f for f in found), found)
        ok, _ = fidelity.check_block(
            block(GOOD.replace("#### Detalles", "(nc-details-label)=\n#### Detalles")),
            "usuario/interfaz-web.md",
            up,
            CATALOG,
            CFG,
        )
        self.assertEqual(ok, [])


class CatalogTest(unittest.TestCase):
    def test_reads_multiline_msgid_and_msgstr(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "user_manual/locale/es/LC_MESSAGES"
            p.mkdir(parents=True)
            (p / "webinterface.pot").write_text(
                'msgid ""\nmsgstr ""\n"Language: es\\n"\n\n#: ../../webinterface.rst:3\n'
                'msgid ""\n"You can access your Nextcloud files "\n"with it."\n'
                'msgstr ""\n"Puede acceder "\n"con ella."\n',
                encoding="utf-8",
            )
            self.assertEqual(
                u.catalog(Path(d), "user_manual/webinterface", CFG),
                {
                    "You can access your Nextcloud files with it.": "Puede acceder con ella."
                },
            )


if __name__ == "__main__":
    unittest.main()
