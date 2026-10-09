"""Tests for the upstream machinery: upstreamlib, upstream-fidelity, rebrand-check (scribe S2b).

Every fidelity rule has a passing fixture and a planted violation, so a rule that stops firing
shows up here before it shows up as a wrong page on the site.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

from docutils import nodes

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
        nav = '<a href="../aviso.html#origen">Origen: distribución derivada de Nextcloud</a><a href="x.html">Nextcloud</a>'
        self.assertEqual(len(u.leftovers(rebrand_check.visible_text(nav, ("aviso.html",)), CFG)), 1)


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

    def test_directive_needs_a_colon_fence(self):
        found, _ = self.check(GOOD + "\n```{note}\nUna nota.\n```\n")
        self.assertTrue(any("colon fence" in f for f in found), found)
        ok, _ = self.check(GOOD + "\n:::{note}\nUna nota.\n:::\n")
        self.assertEqual(ok, [])

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


SHARING = """\
==============
File sharing
==============

Share files with others.

Public links
------------

Go to your ``Files`` page.

==============
Federated shares
==============

Share across servers.

Creating
--------

Open the sidebar.
"""

SHARING_PAGE = """\
### Enlaces públicos

Vaya a su página de `Archivos`.

## Recursos compartidos en federación

Compartir entre servidores.

### Crear

Abrir la barra lateral.
"""


OFFICIAL = {"Go to your ``Files`` page.": "Vaya a su página de ``Archivos``."}


class PilotTest(unittest.TestCase):
    """What the first weave batches (user-manual-talk-3, user-manual-files-2) found in the gate."""

    def sharing(self, content, catalog):
        return fidelity.check_block(
            block("Compartir archivos con otras personas.\n\n" + content,
                  "user_manual/files/sharing.rst@3ad9158"),
            "usuario/archivos/sharing.md", SHARING, catalog, CFG,
        )[0]

    def test_an_official_section_title_is_a_heading(self):
        found, _ = self.check_title()
        self.assertEqual(found, [])

    def check_title(self):
        return fidelity.check_block(
            block(GOOD.replace("### Navegar", "### Navegación")),
            "usuario/interfaz-web.md", UPSTREAM,
            dict(CATALOG, Navigating="Navegación"), CFG,
        )

    def test_levels_rank_styles_over_the_whole_document(self):
        # «Federated shares» reuses the title's overline: a sibling of the title, above «Public links».
        self.assertEqual(self.sharing(SHARING_PAGE, OFFICIAL), [])
        flat = SHARING_PAGE.replace("## Recursos", "### Recursos")
        self.assertTrue(any("headings" in f for f in self.sharing(flat, OFFICIAL)))

    def test_an_official_msgstr_may_translate_a_literal(self):
        self.assertEqual(self.sharing(SHARING_PAGE, OFFICIAL), [])
        # without the official string the literal stays byte-identical
        self.assertTrue(any("inline literals" in f for f in self.sharing(SHARING_PAGE, {})))


    def test_a_brace_inside_code_is_not_a_role(self):
        # user_manual/talk/call_from_anywhere: ``Call {user}`` followed by real roles
        self.assertEqual(
            u.myst_inline_literals(
                "Seleccionar `Call {user}`.\n\nVer {nc-doc}`Llamar <user_manual/talk/call>` y `otro`."
            ),
            ["Call {user}", "otro"],
        )

class ContractV2Test(unittest.TestCase):
    """Constructs the first batches met that the contract and gate did not name (user-manual-desktop-1)."""

    RST = (
        "See the `Admin manual`_ and https://b.example/y.\n\n"
        "Read `the guide <https://c.example/g>`_.\n\n"
        ".. _Admin manual: https://a.example/x\n"
    )

    def test_named_and_bare_links_are_links(self):
        self.assertEqual(
            u.rst_links(self.RST), {"https://a.example/x", "https://b.example/y", "https://c.example/g"}
        )

    def test_reference_links_and_autolinks_match(self):
        page = (
            "Ver el [manual de administración][Admin manual] y <https://b.example/y>.\n\n"
            "Leer [la guía](https://c.example/g).\n\n"
            "[Admin manual]: https://a.example/x\n"
        )
        self.assertEqual(u.myst_links(page), u.rst_links(self.RST))
        # a URL dropped from the page is caught
        self.assertNotEqual(u.myst_links(page.replace(" y <https://b.example/y>", "")), u.rst_links(self.RST))

    def test_an_indented_code_line_is_not_prose(self):
        rst = "the command line would be::\n\n  $ cmd --path /Music \\\n        https://server/nextcloud\n\nDone.\n"
        self.assertEqual(u.rst_links(rst), set())
        self.assertNotIn("https://server/nextcloud", " ".join(u.rst_paragraphs(rst)))

    def test_plain_reads_rst_and_myst_shapes_the_same(self):
        # user-manual-files-1: msgstrs end in "::" and carry named references and bare URLs
        self.assertEqual(u.plain("Por ejemplo::"), "Por ejemplo:")
        self.assertEqual(u.plain("Monte el recurso ::"), "Monte el recurso")
        self.assertEqual(u.plain("Use `WinHTTP`_ y KB2123563_."), "Use WinHTTP y KB2123563.")
        self.assertEqual(u.plain("Use [WinHTTP][WinHTTP] y [KB2123563][KB2123563]."), "Use WinHTTP y KB2123563.")
        self.assertEqual(
            u.plain("en un enlace <https://example.com/s/kFy9>, abra"), "en un enlace https://example.com/s/kFy9, abra"
        )

    def test_a_fence_inside_a_list_item_is_code(self):
        page = "1. Instalar:\n\n   ```bash\n   sudo apt install davfs2\n   ```\n\n2. Montar.\n"
        self.assertEqual(u.myst_code_blocks(page), ["sudo apt install davfs2"])
        self.assertNotIn("davfs2", u._without_fences(page))

    def test_a_quoted_english_message_is_not_english_prose(self):
        quoted = (
            "El navegador advertirá del fallo: «Failed to launch 'nc://...' "
            "because the scheme does not have a registered handler.»"
        )
        self.assertFalse(u.reads_english(quoted))
        self.assertTrue(u.reads_english("You can open the file in the sidebar and then share it with your team."))


class WovenUrlTest(unittest.TestCase):
    def test_upstream_urls_are_upstreams_to_keep_alive(self):
        page = (
            "# P\n\nVer <https://aps.example/propia> y <https://both.example/x>.\n\n"
            "````{upstream} user_manual/x.rst@3ad9158\nVer <https://up.example/a> y [b](https://up.example/b#ancla)"
            " y <https://both.example/x>.\n\n```bash\ncurl https://code.example/c\n```\n````\n"
        )
        self.assertEqual(u.woven_urls([page]), {"https://up.example/a", "https://up.example/b#ancla"})


class CodeByPositionTest(unittest.TestCase):
    """admin-manual-configuration-server-1: code detected by content misread two pages."""

    def test_an_ellipsis_paragraph_is_not_a_comment(self):
        rst = "... or a Memcached cluster, set::\n\n  'memcache.local' => 'x',\n\nDone.\n"
        self.assertEqual(u.rst_code_blocks(rst), ["'memcache.local' => 'x',"])

    def test_a_code_line_never_eats_a_prose_literal(self):
        rst = "Add ``[Install]`` to the unit::\n\n  [Install]\n  WantedBy=timers.target\n\nThen run ``freshclam``.\n\n.. code-block:: bash\n\n   freshclam\n"
        self.assertEqual(u.rst_inline_literals(rst), ["[Install]", "freshclam"])
        self.assertNotIn("WantedBy=timers.target", " ".join(u.rst_paragraphs(rst)))

    def test_a_literal_may_wrap_a_line(self):
        rst = "``man clamd.conf`` and ``man\nfreshclam.conf`` explain all the options. Refer to ``/etc/passwd``.\n"
        self.assertEqual(u.rst_inline_literals(rst), ["man clamd.conf", "man freshclam.conf", "/etc/passwd"])
        page = "`man clamd.conf` y `man\nfreshclam.conf` explican todas las opciones. Ver `/etc/passwd`.\n"
        self.assertEqual(u.myst_inline_literals(page), ["man clamd.conf", "man freshclam.conf", "/etc/passwd"])

class RenderTest(unittest.TestCase):
    """The block renders in source order: attribution, then its text, then its subsections."""

    def test_attribution_and_intro_precede_the_subsections(self):
        import tempfile
        from sphinx.application import Sphinx

        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp)
            (src / "conf.py").write_text(
                "import sys\n"
                f"sys.path.insert(0, {str(TOOLS.parent / '_ext')!r})\n"
                "extensions = ['myst_parser', 'upstream']\n"
                "myst_enable_extensions = ['colon_fence']\n",
                encoding="utf-8",
            )
            (src / "index.md").write_text(
                "# Página\n\n## Resumen\n\nResumen.\n\n"
                "````{upstream} user_manual/files/sharing.rst@3ad9158\n"
                "Texto inicial.\n\n### Sección\n\nTexto de la sección.\n````\n",
                encoding="utf-8",
            )
            app = Sphinx(str(src), str(src), str(src / "_out"), str(src / "_dt"),
                         "dummy", status=None, warning=None, freshenv=True)
            app.build()
            resumen = app.env.get_doctree("index").next_node(nodes.section).next_node(nodes.section)
            kinds = [
                "atribucion" if "atribucion" in c.get("classes", []) else c.tagname
                for c in resumen.children
                if c.tagname != "target"
            ]
            self.assertEqual(kinds, ["title", "paragraph", "atribucion", "paragraph", "section"])


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
