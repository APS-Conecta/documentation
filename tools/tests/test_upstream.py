"""Tests for the upstream machinery: upstreamlib, upstream-fidelity, rebrand-check (scribe S2b).

Every fidelity rule has a passing fixture and a planted violation, so a rule that stops firing
shows up here before it shows up as a wrong page on the site.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

import re

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


    def test_the_vendor_keeps_its_name(self):
        # audit (user-manual-desktop-1): «APS Conecta Gestión ofrece oficialmente el cliente como
        # AppImage» on a page linking to nextcloud.com is a false claim
        cfg = dict(CFG, rename=dict(CFG["rename"], keep_hosts=["nextcloud.com", "github.com/nextcloud"]))
        self.assertTrue(u.vendor_link("https://nextcloud.com/download/", cfg))
        self.assertTrue(u.vendor_link("https://www.nextcloud.com/x", cfg))
        self.assertTrue(u.vendor_link("https://github.com/nextcloud/server/wiki", cfg))
        self.assertFalse(u.vendor_link("https://github.com/APS-Conecta/gestion", cfg))
        self.assertFalse(u.vendor_link("https://notnextcloud.com/", cfg))
        html = (
            '<p><a href="https://nextcloud.com/download">página de descargas de Nextcloud</a> '
            '<span class="vendor">Nextcloud</span> ofrece la AppImage; '
            '<a href="otra.html">Nextcloud</a></p>'
        )
        self.assertEqual(len(u.leftovers(rebrand_check.visible_text(html, (), cfg), cfg)), 1)

    def test_an_autolink_shows_its_url_not_prose(self):
        # user-manual-groupware-2: <https://www.reddit.com/r/Nextcloud/…> is URL text, which the
        # build leaves alone (rebrand.py: reference text == refuri); the check must agree
        url = "https://www.reddit.com/r/Nextcloud/comments/5rcypb/x/"
        html = f'<p>Gracias: <a class="reference external" href="{url}">{url}</a>. <a href="{url}">foro de Nextcloud</a></p>'
        self.assertEqual(len(u.leftovers(rebrand_check.visible_text(html), CFG)), 1)

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

    def test_any_docutils_adornment_marks_a_section(self):
        # developer calendar_provider: «!!!!» subsections; docutils takes any non-alphanumeric
        # printable ASCII character as an adornment
        rst = "Top\n===\n\nSub\n---\n\nHelper\n!!!!!!\n\nText.\n\nOther\n!!!!!\n\nDeep\n$$$$\n\nMore.\n"
        self.assertEqual([lv for lv, _, _ in u.rst_headings(rst)], [1, 2, 3, 3, 4])

    def test_a_backtick_adornment_is_not_a_literal(self):
        # developer basics/events underlines titles with backticks
        rst = "Naming scheme\n`````````````\n\nSuffix with ``Event``.\n\n```\nremote.php/comments\n```\n"
        # the Markdown fence (WebDAV/comments) stays the one literal docutils renders
        self.assertEqual(u.rst_inline_literals(rst), ["Event", "` remote.php/comments `"])
        self.assertEqual([t for _, t, _ in u.rst_headings(rst)], ["Naming scheme"])

    def test_a_literal_may_wrap_a_line(self):
        rst = "``man clamd.conf`` and ``man\nfreshclam.conf`` explain all the options. Refer to ``/etc/passwd``.\n"
        self.assertEqual(u.rst_inline_literals(rst), ["man clamd.conf", "man freshclam.conf", "/etc/passwd"])
        page = "`man clamd.conf` y `man\nfreshclam.conf` explican todas las opciones. Ver `/etc/passwd`.\n"
        self.assertEqual(u.myst_inline_literals(page), ["man clamd.conf", "man freshclam.conf", "/etc/passwd"])


class ContractV3Test(unittest.TestCase):
    """Blind spots the first omission audit found: dropped toctrees, dangling lead-ins, short sections."""

    TOC = (
        "Calls\n=====\n\n.. toctree::\n   :maxdepth: 1\n\n   call\n   Ver pantalla <call_screenshare>\n   *\n\n"
        ".. toctree::\n   :hidden:\n\n   secret\n"
    )

    def test_a_visible_toctree_is_a_list_of_doc_links(self):
        self.assertEqual(
            u.rst_toctree(self.TOC, "user_manual/talk/call_index"),
            ["user_manual/talk/call", "user_manual/talk/call_screenshare"],
        )
        self.assertIn(("doc", "user_manual/talk/call"), u.rst_xrefs(self.TOC, "user_manual/talk/call_index"))

    def test_a_bare_url_is_not_a_link(self):
        # no linkify on this site: a bare URL renders as plain text (audit, user-manual-desktop-1)
        self.assertEqual(
            u.bare_urls("Ver https://a.example/x y <https://b.example/y>, [c](https://c.example/z).\n\n"
                        "| Alpine | https://d.example/p |\n\n[Ref]: https://e.example/r\n\n`https://f.example/code`\n"),
            ["https://a.example/x", "https://d.example/p"],
        )

    def test_a_url_template_is_not_a_bare_url(self):
        # desktop commandline: «--httpproxy *http://[user@pass:]<server>:<port>*» is an argument shape
        self.assertEqual(u.bare_urls("- `--httpproxy` *http://[user@pass:]\\<server\\>:\\<port\\>*: proxy.\n"), [])

    def test_dangling_lead_in_and_short_section_warn(self):
        up = "Title\n=====\n\nIntro.\n\nPart\n----\n\n" + " ".join(["word"] * 60) + ".\n"
        page = "Introducción.\n\n### Parte\n\nEn Talk:\n\nPocas palabras aquí.\n"
        warns = fidelity.warnings(page, u.rst_section(up))
        self.assertTrue(any("ends in «:»" in w for w in warns), warns)
        self.assertTrue(any("words" in w for w in warns), warns)
        ok = "Introducción.\n\n### Parte\n\nPara instalar:\n\n```bash\nls\n```\n\n" + " ".join(["palabra"] * 70) + ".\n"
        self.assertEqual(fidelity.warnings(ok, u.rst_section(up)), [])


class UiLabelTest(unittest.TestCase):
    """Talk and desktop audits: upstream writes buttons as ``literals``, so the page kept English
    UI labels the Spanish interface never shows."""

    UI = {"Start call": {"Comenzar llamada"}, "Settings": {"Ajustes"}, "Updates": {"Actualizaciones"},
          "Start recording": {"Empezar a grabar"}}
    UP = "Title\n=====\n\nClick ``Start call``, then ``Settings -> Updates`` and ``occ``.\n"

    def check(self, content):
        blk = block(content, "user_manual/files/x.rst@3ad9158")
        return fidelity.check_block(blk, "usuario/archivos/x.md", self.UP, {}, CFG, ui=self.UI)[0]

    def test_a_ui_literal_may_become_its_spanish_label(self):
        ok = "Hacer clic en {guilabel}`Comenzar llamada`, luego en {guilabel}`Ajustes` → {guilabel}`Actualizaciones` y `occ`.\n"
        self.assertEqual(self.check(ok), [])
        bad = "Hacer clic en {guilabel}`Empezar`, luego en `Settings -> Updates` y `occ`.\n"
        self.assertTrue(any("inline literals" in f for f in self.check(bad)))

    def test_an_official_lead_in_may_end_in_a_period(self):
        # user-root audit: «Simplemente introduzca su código:» introduced a dropped screenshot
        up = "Title\n=====\n\nNow, just enter your code:\n"
        cat = {"Now, just enter your code:": "Simplemente introduzca su código:"}
        blk = block("Simplemente introduzca su código.\n", "user_manual/files/x.rst@3ad9158")
        self.assertEqual(fidelity.check_block(blk, "usuario/archivos/x.md", up, cat, CFG, ui={})[0], [])

    def test_a_quote_inside_fenced_code_is_code(self):
        # config-database-1: «mysql> SHOW VARIABLES LIKE "version";» read as a quoted UI string
        page = "Hacer clic en `Start call`, luego en `Settings -> Updates` y `occ`.\n\n```\nmysql> SHOW VARIABLES LIKE \"Settings\";\n```\n"
        self.assertFalse(any("UI string" in f for f in self.check(page)), self.check(page))

    def test_a_quoted_english_ui_string_with_spanish_is_wrong(self):
        page = "Hacer clic en `Start call`, luego en `Settings -> Updates` y `occ`. Marcar \"Start recording\".\n"
        self.assertTrue(any("Empezar a grabar" in f for f in self.check(page)))

class ConfigServer2Test(unittest.TestCase):
    """admin-manual-configuration-server-2: three gate defects its reviewer proved."""

    def test_a_quoted_literal_block_is_code(self):
        # RST: after «::», an unindented block whose lines start with the same punctuation is literal
        rst = "Check the port::\n\n# netstat -pant\n# ss -tlnp\n\nThen continue.\n"
        self.assertEqual(u.rst_code_blocks(rst), ["# netstat -pant\n# ss -tlnp"])
        self.assertNotIn("netstat", " ".join(u.rst_paragraphs(rst)))
        plain = "Not literal::\n\nPlain text follows.\n"
        self.assertEqual(u.rst_code_blocks(plain), [])

    def test_a_url_in_strong_emphasis_ends_before_the_stars(self):
        rst = "Served at **https://example.com/nextcloud**, behind a proxy.\n"
        self.assertEqual(u.rst_links(rst), {"https://example.com/nextcloud"})
        self.assertEqual(u.myst_links("Servido en **<https://example.com/nextcloud>**.\n"), {"https://example.com/nextcloud"})

    def test_a_path_component_keeps_its_name(self):
        # desktop-2: *$HOME/.config/Nextcloud/nextcloud.cfg* rendered a path that does not exist
        self.assertEqual(u.rename("Borrar $HOME/.config/Nextcloud/nextcloud.cfg y %APPDATA%\\Nextcloud\\x de Nextcloud.", CFG),
                         "Borrar $HOME/.config/Nextcloud/nextcloud.cfg y %APPDATA%\\Nextcloud\\x de APS Conecta Gestión.")


class FilesGroupwareAuditTest(unittest.TestCase):
    """Round-2 omission audit (files, groupware): blind spots of the warnings and the UI check."""

    SECTION = "Title\n=====\n\nText.\n"

    def leads(self, page):
        return [w for w in fidelity.warnings(page, u.rst_section(self.SECTION)) if "ends in «:»" in w]

    def test_a_list_step_ending_in_a_colon_before_its_sibling_warns(self):
        self.assertTrue(self.leads("1. Abrir el menú **Ir**:\n2. Elegir el servidor.\n"))
        self.assertEqual(self.leads("1. Ejecutar:\n\n   ```\n   ls\n   ```\n\n2. Fin.\n"), [])
        self.assertEqual(self.leads("1. Elegir:\n   - uno\n   - dos\n"), [])
        self.assertEqual(self.leads("Para instalar:\n\n```bash\nls\n```\n"), [])
        self.assertEqual(self.leads("1. Desinstalar con msiexec:\n\n```shell\nmsiexec /x\n```\n\n2. Fin.\n"), [])

    def test_a_lead_in_closing_an_admonition_warns(self):
        self.assertTrue(self.leads(":::{note}\nUse `dav://` en lugar de `davs://`:\n:::\n\nTexto.\n"))
        self.assertEqual(self.leads(":::{note}\nEjecutar:\n\n```\nls\n```\n:::\n"), [])

    def test_third_party_ui_strings_are_not_nextcloud_labels(self):
        up = "Title\n=====\n\nIn WinSCP, click \"Save\".\n"
        page = "En WinSCP, hacer clic en «Save».\n"
        ui = {"Save": {"Guardar"}}
        cfg = dict(CFG, ui_third_party=["user_manual/files/access_*"])
        third = block(page, "user_manual/files/access_webdav.rst@3ad9158")
        own = block(page, "user_manual/files/x.rst@3ad9158")
        self.assertEqual(fidelity.check_block(third, "usuario/archivos/access-webdav.md", up, {}, cfg, ui=ui)[0], [])
        self.assertTrue(any("Guardar" in f for f in fidelity.check_block(own, "usuario/archivos/x.md", up, {}, cfg, ui=ui)[0]))

    def test_a_literal_the_docs_official_msgstr_translates_may_become_its_label(self):
        # calendario: «+ New calendar» stayed English next to the official «+ Nuevo calendario»
        up = "Title\n=====\n\nClick ``+ New calendar``.\n\nThen use ``+ New calendar`` again.\n"
        cat = {"Click ``+ New calendar``.": "Haga clic en ``+ Nuevo calendario``."}
        page = "Haga clic en `+ Nuevo calendario`.\n\nLuego usar {guilabel}`+ Nuevo calendario` otra vez.\n"
        blk = block(page, "user_manual/files/x.rst@3ad9158")
        self.assertEqual(fidelity.check_block(blk, "usuario/archivos/x.md", up, cat, CFG, ui={})[0], [])


class LdapDocTest(unittest.TestCase):
    """admin-manual-configuration-user-1 (user_auth_ldap): two places the gate read RST unlike docutils."""

    def test_a_markdown_fence_in_rst_is_one_inline_literal(self):
        # docutils reads ```\nTLS_REQCERT ALLOW\n``` as the literal «` TLS_REQCERT ALLOW `»
        rst = "* Add this line:\n\n  ```\n  TLS_REQCERT ALLOW\n  ```\n\nNext ``occ``.\n"
        self.assertEqual(u.rst_inline_literals(rst), ["` TLS_REQCERT ALLOW `", "occ"])
        page = "- Añadir esta línea:\n\n  `` ` TLS_REQCERT ALLOW ` ``\n\nLuego `occ`.\n"
        self.assertEqual(u.myst_inline_literals(page), ["` TLS_REQCERT ALLOW `", "occ"])

    def test_an_embedded_url_split_across_lines_is_one_url(self):
        rst = "This is described `here <https://a.example/q/1/what-are\n-required/2#2>`_.\n"
        self.assertEqual(u.rst_links(rst), {"https://a.example/q/1/what-are-required/2#2"})
        two = "See `the long\nguide <https://a.example/x\n-y>`_ and `this <https://b.example/z>`_.\n"
        self.assertEqual(u.rst_links(two), {"https://a.example/x-y", "https://b.example/z"})


class MaintenanceDocTest(unittest.TestCase):
    """admin-manual-maintenance-1: two RST readings unlike docutils, one warning false positive."""

    def test_a_target_whose_url_is_on_the_next_line_is_not_a_label(self):
        rst = "Text.\n\n.. _install_target:\n\nHeading\n-------\n\n.. _nextcloud.com/install/:\n   https://nextcloud.com/install/\n"
        self.assertEqual([lab for lab, _ in u.rst_labels(rst)], ["install_target"])

    def test_a_url_may_hold_an_apostrophe(self):
        rst = "See `the FAQ <https://github.com/x/y/wiki/FAQ's>`_ or 'https://a.example/b'.\n"
        self.assertEqual(u.rst_links(rst), {"https://github.com/x/y/wiki/FAQ's", "https://a.example/b"})
        self.assertEqual(u.myst_links("Ver [las FAQ](https://github.com/x/y/wiki/FAQ's).\n"), {"https://github.com/x/y/wiki/FAQ's"})

    def test_a_lead_in_before_a_command_paragraph_introduced_it(self):
        sec = "Title\n=====\n\nText.\n"
        page = "Para actualizar, ejecutar:\n\n`sudo snap refresh nextcloud`\n"
        self.assertEqual([w for w in fidelity.warnings(page, u.rst_section(sec)) if "ends in «:»" in w], [])


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

    def test_a_bare_doc_link_takes_the_woven_page_title(self):
        import tempfile
        from sphinx.application import Sphinx

        import os
        from unittest import mock

        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp)
            # the unwoven link's fallback URL names the major: a fixture org, not this box's gestion
            (src / "org" / "gestion").mkdir(parents=True)
            (src / "org" / "gestion" / "compose.yaml").write_text("image: nextcloud:34\n", encoding="utf-8")
            env = mock.patch.dict(os.environ, {"APS_ORG_ROOT": str(src / "org")})
            env.start()
            self.addCleanup(env.stop)
            (src / "conf.py").write_text(
                "import sys\n"
                f"sys.path.insert(0, {str(TOOLS.parent / '_ext')!r})\n"
                "extensions = ['myst_parser', 'upstream']\n"
                "exclude_patterns = ['org', '_out', '_dt']\n",
                encoding="utf-8",
            )
            block = "````{{upstream}} user_manual/{d}.rst@3ad9158\nTexto.\n````\n"
            (src / "index.md").write_text(
                "# Inicio\n\n```{toctree}\nuno\nvarios\n```\n\n"
                "- {nc-doc}`user_manual/uno`\n- {nc-doc}`user_manual/b`\n- {nc-doc}`user_manual/nada`\n"
                "- {nc-doc}`Texto propio <user_manual/uno>`\n",
                encoding="utf-8",
            )
            (src / "uno.md").write_text("# Página uno\n\n## Resumen\n\n" + block.format(d="uno"), encoding="utf-8")
            (src / "varios.md").write_text(
                "# Varios\n\n## Resumen\n\n### Doc A\n\n" + block.format(d="a")
                + "\n### Doc B\n\n" + block.format(d="b"), encoding="utf-8")
            app = Sphinx(str(src), str(src), str(src / "_out"), str(src / "_dt"),
                         "html", status=None, warning=None, freshenv=True)
            app.build()
            html = (src / "_out" / "index.html").read_text(encoding="utf-8")
            links = re.findall(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', html)
            text = {re.sub(r"<[^>]+>", "", t).strip() for h, t in links if "#upstream-" in h or "docs.nextcloud" in h}
            self.assertEqual(text, {"Página uno", "Doc B", "user_manual/nada", "Texto propio"})


class GlobToctreeTest(unittest.TestCase):
    def test_a_glob_toctree_lists_every_matching_doc_as_sphinx_does(self):
        # configuration_server/index: «:glob:» + «*» renders every document of the folder upstream
        rst = "Index\n=====\n\n.. toctree::\n   :glob:\n\n   security_setup_warnings\n   *\n   */index\n"
        docs = ["admin_manual/x/index", "admin_manual/x/a", "admin_manual/x/security_setup_warnings",
                "admin_manual/x/b", "admin_manual/x/sub/index", "admin_manual/x/sub/c", "admin_manual/y/z"]
        self.assertEqual(u.rst_toctree(rst, "admin_manual/x/index", docs), [
            "admin_manual/x/security_setup_warnings", "admin_manual/x/a", "admin_manual/x/b",
            "admin_manual/x/sub/index"])
        no_glob = rst.replace("   :glob:\n", "")
        self.assertEqual(u.rst_toctree(no_glob, "admin_manual/x/index", docs), ["admin_manual/x/security_setup_warnings"])


class RoleLineTest(unittest.TestCase):
    def test_a_line_opened_by_a_role_continues_its_paragraph(self):
        # primary_storage, amazons3: the wrapped line «:code:`https://hostname.domain/bucket` instead.»
        rst = ("Setting :code:`use_path_style` to true makes requests like\n"
               ":code:`https://hostname.domain/bucket` instead.\n\n"
               ".. figure:: a.png\n   :alt: A screenshot\n\nText.\n")
        self.assertEqual(u.rst_links(rst), {"https://hostname.domain/bucket"})
        self.assertEqual(u.rst_paragraphs(rst), [
            "Setting :code:`use_path_style` to true makes requests like :code:`https://hostname.domain/bucket` instead.",
            "Text."])


class DocJoinTest(unittest.TestCase):
    def test_dotdot_stops_at_the_manual_root_as_sphinx_does(self):
        # admin-manual-1: each manual is its own Sphinx project; docname_join('occ_database',
        # '../groupware/calendar') is 'groupware/calendar' there, i.e. admin_manual/groupware/calendar
        self.assertEqual(u.absolute_doc("admin_manual/occ_database", "../groupware/calendar"),
                         "admin_manual/groupware/calendar")
        self.assertEqual(u.absolute_doc("admin_manual/x/y", "../z"), "admin_manual/z")
        self.assertEqual(u.absolute_doc("admin_manual/x/y", "/a/b"), "admin_manual/a/b")


class W6GateTest(unittest.TestCase):
    """admin-manual-desktop-1 and -release-notes-1: three readings unlike docutils/Sphinx."""

    def test_a_short_overline_is_not_a_title(self):
        # docutils: an overline shorter than 4 characters and than the text is text (short_overline)
        rst = "Title\n=====\n\nPart\n----\n\nRun:\n\n```\nnextcloud --logdir /tmp/logs\n```\n\nDone.\n"
        self.assertEqual([t for _, t, _ in u.rst_headings(rst)], ["Title", "Part"])

    def test_a_toctree_entry_may_carry_its_suffix(self):
        rst = "Notes\n=====\n\n.. toctree::\n\n   upgrade_to_33.rst\n   upgrade_to_32\n"
        self.assertEqual(u.rst_toctree(rst, "admin_manual/release_notes/index"),
                         ["admin_manual/release_notes/upgrade_to_33", "admin_manual/release_notes/upgrade_to_32"])

    def test_code_is_not_english_prose(self):
        # issues-1: a line block holding one SQL literal read as untranslated prose
        sql = "`DELETE FROM oc_cards_properties WHERE name = 'CLOUD' AND addressbookid = (select id from oc_addressbooks where principaluri = 'principals/system/system')`"
        self.assertFalse(u.reads_english(sql))
        self.assertTrue(u.reads_english("Click the {guilabel}`Save` button and then go to the settings of the app."))
        # an all-caps keyword (an SMTP header) is not English prose
        self.assertFalse(u.reads_english("Dirección FROM que sustituye a las direcciones FROM integradas `a@b.c` y `d@e.f`."))

    def test_a_bare_doc_link_list_is_not_english(self):
        page = "- {nc-doc}`admin_manual/release_notes/upgrade_to_33`\n- {nc-doc}`admin_manual/release_notes/upgrade_to_32`\n"
        self.assertFalse(u.reads_english(u.plain(page)))


class W7GateTest(unittest.TestCase):
    """admin-manual-exapps-management-1 and -office-1."""

    def test_a_diagram_is_dropped_content_not_prose(self):
        rst = ("Intro.\n\n.. mermaid::\n\n   graph LR\n   classDef d background: url(https://raw.example/x.png)\n\n"
               "Text https://a.example/y here.\n")
        self.assertEqual(u.rst_links(rst), {"https://a.example/y"})
        self.assertEqual(u.rst_code_blocks(rst), [])

    def test_a_url_in_angle_brackets_is_read_whole(self):
        rst = "It has `fixed parameters <https://g.example/a.php#L52-L74)>`_:\n"
        self.assertEqual(u.rst_links(rst), {"https://g.example/a.php#L52-L74)"})
        page = "Tiene [parámetros fijos][A]:\n\n[A]: <https://g.example/a.php#L52-L74)>\n"
        self.assertEqual(u.myst_links(page), {"https://g.example/a.php#L52-L74)"})


class W8GateTest(unittest.TestCase):
    """admin-manual-installation-1 and -2."""

    def test_a_literal_block_ends_where_docutils_ends_it(self):
        # example_openbsd: the first line is indented 4, the closing brace 2; docutils keeps both
        rst = "Add a virtual host::\n\n    server \"domain.tld\" {\n        listen on *\n  }\n\nThen restart.\n"
        self.assertEqual(u.rst_code_blocks(rst), ['  server "domain.tld" {\n      listen on *\n}'])
        nested = "#. Edit it::\n\n      a = 1\n\n   More text.\n"
        self.assertEqual(u.rst_code_blocks(nested), ["a = 1"])

    def test_a_directive_may_space_its_colons(self):
        # developer debugging: «.. code-block :: sql» is a code block for docutils
        rst = "Log queries.\n\n.. code-block :: sql\n\n  SET GLOBAL general_log = 'ON';\n\nDone.\n"
        self.assertEqual(u.rst_code_blocks(rst), ["SET GLOBAL general_log = 'ON';"])

    def test_a_url_keeps_balanced_parentheses(self):
        url = "https://github.com/x/wiki/Managing-HTTP-encryption-(HTTPS)"
        rst = f"See `Managing <{url}>`_ (and https://a.example/b).\n"
        self.assertEqual(u.rst_links(rst), {url, "https://a.example/b"})
        self.assertEqual(u.myst_links(f"Ver [Gestionar]({url}) (y https://a.example/b).\n"), {url, "https://a.example/b"})


class Round4WarnTest(unittest.TestCase):
    """Round-4 audit: lead-in warnings that taught reviewers to ignore the check."""

    def leads(self, page):
        return [w for w in fidelity.warnings(page, u.rst_section("Title\n=====\n\nText.\n")) if "ends in «:»" in w]

    def test_a_list_of_code_spans_or_a_bold_label_is_introduced(self):
        self.assertEqual(self.leads("Claves disponibles:\n\n`displaynameScope`, `emailScope`, `phoneScope`.\n"), [])
        self.assertEqual(self.leads("La forma más sencilla es la línea de comandos:\n\n**MySQL**:\n\nTexto.\n"), [])
        self.assertTrue(self.leads("Los campos son:\n\nTexto sin nada más.\n"))


class BareRefTitleTest(unittest.TestCase):
    """configuration_server audit: a bare :ref: showed its raw label, so translators invented text."""

    def test_a_bare_ref_link_takes_its_sections_title(self):
        import os
        import tempfile
        from unittest import mock
        from sphinx.application import Sphinx

        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp)
            (src / "org" / "gestion").mkdir(parents=True)
            (src / "org" / "gestion" / "compose.yaml").write_text("image: nextcloud:34\n", encoding="utf-8")
            env = mock.patch.dict(os.environ, {"APS_ORG_ROOT": str(src / "org")})
            env.start()
            self.addCleanup(env.stop)
            (src / "conf.py").write_text(
                "import sys\n"
                f"sys.path.insert(0, {str(TOOLS.parent / '_ext')!r})\n"
                "extensions = ['myst_parser', 'upstream']\n"
                "exclude_patterns = ['org', '_out', '_dt']\n",
                encoding="utf-8",
            )
            (src / "index.md").write_text(
                "# Inicio\n\n```{toctree}\nuno\n```\n\n"
                "- {nc-ref}`use_https_label`\n- {nc-ref}`Texto propio <use_https_label>`\n",
                encoding="utf-8",
            )
            (src / "uno.md").write_text(
                "# Uno\n\n## Resumen\n\n````{upstream} admin_manual/x.rst@3ad9158\nTexto.\n\n"
                "(nc-use_https_label)=\n#### Usar HTTPS en Nextcloud\n\nMás texto.\n````\n", encoding="utf-8")
            app = Sphinx(str(src), str(src), str(src / "_out"), str(src / "_dt"),
                         "html", status=None, warning=None, freshenv=True)
            app.build()
            html = (src / "_out" / "index.html").read_text(encoding="utf-8")
            links = re.findall(r'<a class="reference external" href="([^"]+)"[^>]*>(.*?)</a>', html)
            # the std domain records the title before the rename: the link text is renamed here
            self.assertEqual([re.sub(r"<[^>]+>", "", t).strip() for _, t in links],
                             ["Usar HTTPS en APS Conecta Gestión", "Texto propio"])


class DifiereLinkTest(unittest.TestCase):
    def test_the_difiere_notice_links_to_the_aps_section(self):
        # admin collectives: the notice said «Ver la página de APS Conecta Gestión» and linked to its own page
        import os
        import tempfile
        from unittest import mock
        from sphinx.application import Sphinx

        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp)
            (src / "org" / "gestion").mkdir(parents=True)
            (src / "org" / "gestion" / "compose.yaml").write_text("image: nextcloud:34\n", encoding="utf-8")
            env = mock.patch.dict(os.environ, {"APS_ORG_ROOT": str(src / "org")})
            env.start()
            self.addCleanup(env.stop)
            (src / "conf.py").write_text(
                "import sys\n"
                f"sys.path.insert(0, {str(TOOLS.parent / '_ext')!r})\n"
                "extensions = ['myst_parser', 'upstream']\n"
                "exclude_patterns = ['org', '_out', '_dt']\n",
                encoding="utf-8",
            )
            (src / "index.md").write_text("# Inicio\n\n```{toctree}\nuno\ndos\n```\n", encoding="utf-8")
            block = "````{{upstream}} admin_manual/{d}.rst@3ad9158\n:difiere: {t}\nTexto.\n````\n"
            (src / "uno.md").write_text("# Uno\n\n## Resumen\n\n" + block.format(d="uno", t="uno")
                                        + "\n## En APS Conecta Gestión\n\nLa suite no lo instala.\n", encoding="utf-8")
            (src / "dos.md").write_text("# Dos\n\n## Resumen\n\n" + block.format(d="dos", t="index"), encoding="utf-8")
            app = Sphinx(str(src), str(src), str(src / "_out"), str(src / "_dt"),
                         "html", status=None, warning=None, freshenv=True)
            app.build()
            uno = (src / "_out" / "uno.html").read_text(encoding="utf-8")
            self.assertRegex(uno, r'<a [^>]*href="#en-aps-conecta-gestion"[^>]*>Ver «En APS Conecta Gestión»</a>')
            dos = (src / "_out" / "dos.html").read_text(encoding="utf-8")
            self.assertRegex(dos, r'<a [^>]*href="index.html"[^>]*>Ver la página de APS Conecta Gestión</a>')


class W9GateTest(unittest.TestCase):
    """admin-manual-ai-2: a malformed upstream role, vendor sub-hosts, anonymous labels."""

    def test_a_backtick_inside_a_role_does_not_close_it(self):
        rst = "See :ref:`other apps making use of the core `Text-To-Speech Task type<t2s-consumer-apps>`.\n"
        self.assertEqual(u.rst_xrefs(rst, "admin_manual/ai/x"), [("ref", "t2s-consumer-apps")])
        self.assertEqual(u.rst_xrefs("A :doc:`plain` and :ref:`Text <lab>`.\n", "admin_manual/x"),
                         [("doc", "admin_manual/plain"), ("ref", "lab")])

    def test_a_vendor_host_covers_its_subdomains(self):
        cfg = dict(CFG, rename=dict(CFG["rename"], keep_hosts=["nextcloud.com", "github.com/nextcloud"]))
        self.assertTrue(u.vendor_link("https://apps.nextcloud.com/apps/assistant", cfg))
        self.assertTrue(u.vendor_link("https://docs.nextcloud.com/server/34/x.html", cfg))
        self.assertFalse(u.vendor_link("https://notnextcloud.com/", cfg))
        self.assertFalse(u.vendor_link("https://github.com/nextcloudfoo/x", cfg))

    def test_vendor_product_names_keep_their_name(self):
        cfg = u.config()
        self.assertEqual(u.rename("Nextcloud-AIO y Nextcloud Mail en Nextcloud.", cfg),
                         "Nextcloud-AIO y Nextcloud Mail en APS Conecta Gestión.")

    def test_a_ref_to_a_label_before_a_paragraph_stays_on_the_site(self):
        import os
        import tempfile
        from unittest import mock
        from sphinx.application import Sphinx

        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp)
            (src / "org" / "gestion").mkdir(parents=True)
            (src / "org" / "gestion" / "compose.yaml").write_text("image: nextcloud:34\n", encoding="utf-8")
            env = mock.patch.dict(os.environ, {"APS_ORG_ROOT": str(src / "org")})
            env.start()
            self.addCleanup(env.stop)
            (src / "conf.py").write_text(
                "import sys\n"
                f"sys.path.insert(0, {str(TOOLS.parent / '_ext')!r})\n"
                "extensions = ['myst_parser', 'upstream']\n"
                "exclude_patterns = ['org', '_out', '_dt']\n",
                encoding="utf-8",
            )
            (src / "index.md").write_text("# Inicio\n\n```{toctree}\nuno\n```\n\nVer {nc-ref}`las apps <t2s-consumer-apps>`.\n",
                                          encoding="utf-8")
            (src / "uno.md").write_text("# Uno\n\n## Resumen\n\n````{upstream} admin_manual/x.rst@3ad9158\nTexto.\n\n"
                                        "(nc-t2s-consumer-apps)=\nApps que usan la tarea.\n````\n", encoding="utf-8")
            app = Sphinx(str(src), str(src), str(src / "_out"), str(src / "_dt"),
                         "html", status=None, warning=None, freshenv=True)
            app.build()
            html = (src / "_out" / "index.html").read_text(encoding="utf-8")
            self.assertRegex(html, r'href="uno.html#nc-t2s-consumer-apps"[^>]*>las apps<')


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
