"""«Tema» names only what gestion-aio's theme has: each file it names is linked on its repository's main and is in that
repository's roster checkout, every other name it writes in code is in a file it links, it links the variable map
instead of copying it, and it keeps no reference to what the theme no longer has."""

import os
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_marca import COLOUR_LITERAL, ROOT  # noqa: E402

PAGE = ROOT / "desarrollo" / "tema.md"
# The roster checkouts, as the generators find them.
ORG_ROOT = Path(os.environ.get("APS_ORG_ROOT", "/opt/aps-conecta-org"))
# A file of the suite or of the org's shared workflows, as the page writes it in code.
NAMED = re.compile(r"`((?:aps|Containers|docs|scripts|\.github)/[^`\s]+)`")
# A link to a file on its repository's default branch: its repository and its path.
LINK = re.compile(r"\]\(https://github\.com/APS-Conecta/(gestion-aio|\.github)/blob/main/([^)\s]+)\)")
# Such a link whose text is a path in code: its text and its path.
LINKED = re.compile(r"\[`([^`]+)`\]\(https://github\.com/APS-Conecta/(?:gestion-aio|\.github)/blob/main/([^)\s]+)\)")
CODE = re.compile(r"`([^`]+)`")
ROLE = re.compile(r"\{\w+\}`[^`]*`")
VARIABLE_MAP = "https://github.com/APS-Conecta/gestion-aio/blob/main/aps/theme/apsconecta/core/css/variable-map.css"
# What gestion-aio's theme does not have: the provisioning phase that wrote theming, the theme folder at the repo's
# root, the logo font subset and its tool, the loading-indicator snippet, the restart after a change, the old bug ids.
STALE = re.compile(r"15-branding|provisioning/|(?<![/\w])themes/apsconecta/|embed-fonts|subconjunto|MAPEO\.md"
                   r"|aps-mount-|fix-mount-perms|logo-mark|reiniciar el contenedor|B-0\d\d")


class TemaTest(unittest.TestCase):
    def setUp(self):
        self.text = PAGE.read_text(encoding="utf-8")
        self.links = LINK.findall(self.text)

    def test_every_file_it_names_is_linked_on_its_repositorys_main(self):
        linked = {text for text, path in LINKED.findall(self.text) if text == path}
        self.assertEqual(sorted(set(NAMED.findall(self.text)) - linked), [])

    def test_a_link_shows_the_path_it_opens(self):
        self.assertEqual([(text, path) for text, path in LINKED.findall(self.text) if text != path], [])

    def test_every_file_it_links_is_in_the_roster_checkout(self):
        self.assertEqual([f"{repo}/{path}" for repo, path in self.links if not (ORG_ROOT / repo / path).is_file()], [])

    def test_every_name_it_writes_in_code_is_in_a_file_it_links(self):
        linked = "".join((ORG_ROOT / repo / path).read_text(encoding="utf-8") for repo, path in self.links)
        files = {path for _, path in self.links} | {Path(path).name for _, path in self.links}
        body = ROLE.sub("", self.text.split("\n---\n", 1)[1])
        absent = [name for name in sorted(set(CODE.findall(body)))
                  if name not in files and not (ROOT / name).is_file() and name not in linked]
        self.assertEqual(absent, [])

    def test_it_links_the_variable_map_and_does_not_copy_it(self):
        self.assertIn(f"({VARIABLE_MAP})", self.text)
        paired = [line for line in self.text.splitlines() if "--color-" in line and "--aps-" in line]
        self.assertEqual(paired, [])

    def test_it_writes_no_colour_and_no_stale_reference(self):
        self.assertEqual(COLOUR_LITERAL.findall(self.text), [])
        self.assertEqual(STALE.findall(self.text), [])

    def test_tema_and_marca_link_each_other(self):
        self.assertIn("{doc}`marca`", self.text)
        self.assertIn("{doc}`tema`", (ROOT / "desarrollo" / "marca.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
