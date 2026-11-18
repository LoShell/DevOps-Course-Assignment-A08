"""E8 personal coverage: indirect include invalidates cached dependency graph."""
import tempfile
import unittest
from pathlib import Path

from lab import commit, fixture, scan


class TestStudent241250071(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name) / "project"
        fixture(self.project)

    def tearDown(self):
        self.temp.cleanup()

    def test_indirect_include_invalidates_cached_dependencies(self):
        baseline = scan(self.project)
        c0 = baseline["commit"]

        self.assertEqual(baseline["commit"], c0)
        self.assertEqual(
            set(baseline["actual"]["main.o"]),
            {"main.c", "config.h"},
        )

        (self.project / "config.h").write_text(
            '#include "extra.h"\n#define VALUE 1\n',
            encoding="utf-8",
        )
        c1 = commit(self.project, "C1 add indirect include")

        incremental = scan(self.project, baseline)
        full = scan(self.project)

        self.assertNotEqual(c0, c1)
        self.assertEqual(incremental["commit"], c1)
        self.assertEqual(
            set(incremental["actual"]["main.o"]),
            {"main.c", "config.h", "extra.h"},
        )
        self.assertEqual(
            set(incremental["actual"]["helper.o"]),
            {"helper.c"},
        )
        self.assertEqual(incremental["reused"], [])
        self.assertEqual(
            set(incremental["refreshed"]),
            {"main.o", "helper.o"},
        )
        self.assertEqual(
            incremental["added"],
            [["MISSING", "main.o", "extra.h"]],
        )
        self.assertEqual(
            {
                (item["type"], item["target"], item["dependency"])
                for item in incremental["findings"]
            },
            {
                ("MISSING", "main.o", "config.h"),
                ("MISSING", "main.o", "extra.h"),
                ("REDUNDANT", "main.o", "unused.h"),
            },
        )

        self.assertEqual(incremental["actual"], full["actual"])
        self.assertEqual(incremental["declared"], full["declared"])
        self.assertEqual(incremental["findings"], full["findings"])


if __name__ == "__main__":
    unittest.main()
