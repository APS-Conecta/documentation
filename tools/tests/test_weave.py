"""Tests for tools/weave.py batch planning (scribe W-runs).

A woven page must land inside a toctree, so the batch that creates a folder's index page has to
merge before the batches that fill the folder. These tests pin that order and the guard.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location("weave", TOOLS / "weave.py")
weave = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weave)


def entry(doc, page):
    return {"doc": doc, "page": page, "difiere": ""}


DESKTOP = [
    entry(f"user_manual/desktop/{n}", f"usuario/escritorio/{n}.md")
    for n in ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k")
] + [entry("user_manual/desktop/index", "usuario/escritorio/index.md")]


class GroupTest(unittest.TestCase):
    def test_folder_index_opens_the_first_batch(self):
        out = weave.group(sorted(DESKTOP, key=lambda e: e["doc"]))
        self.assertEqual(
            [b["id"] for b in out], ["user-manual-desktop-1", "user-manual-desktop-2"]
        )
        self.assertEqual(out[0]["docs"][0]["doc"], "user_manual/desktop/index")
        self.assertEqual(len(out[0]["docs"]), weave.BATCH)

    def test_ids_do_not_move_when_docs_are_done(self):
        done = {e["doc"] for e in DESKTOP[:9]} | {"user_manual/desktop/index"}
        out = weave.group(sorted(DESKTOP, key=lambda e: e["doc"]), done)
        self.assertEqual([b["id"] for b in out], ["user-manual-desktop-2"])


class NeedsTest(unittest.TestCase):
    def plan(self, on_disk=()):
        out = weave.group(sorted(DESKTOP, key=lambda e: e["doc"]))
        weave.link(out, lambda page: page in on_disk)
        return {b["id"]: b["needs"] for b in out}

    def test_a_batch_waits_for_the_batch_that_creates_its_folder_index(self):
        self.assertEqual(
            self.plan(),
            {
                "user-manual-desktop-1": [],
                "user-manual-desktop-2": ["user-manual-desktop-1"],
            },
        )

    def test_an_index_already_on_disk_is_no_dependency(self):
        self.assertEqual(
            self.plan({"usuario/escritorio/index.md"})["user-manual-desktop-2"], []
        )

    def test_a_parent_folder_index_from_another_directory_counts(self):
        out = weave.group(
            [
                entry("developer_manual/index", "desarrollo/plataforma/index.md"),
                entry("developer_manual/basics/x", "desarrollo/plataforma/basics/x.md"),
            ]
        )
        weave.link(out, lambda page: False)
        self.assertEqual(
            {b["id"]: b["needs"] for b in out},
            {
                "developer-manual-1": [],
                "developer-manual-basics-1": ["developer-manual-1"],
            },
        )


if __name__ == "__main__":
    unittest.main()
