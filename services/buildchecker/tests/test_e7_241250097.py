"""E7: declaration path normalization and Make database evidence."""
import tempfile
import unittest
from pathlib import Path

from buildchecker.fullcheck import declaration_graph


class TestDeclarations241250097(unittest.TestCase):
    def test_normalized_paths_preserve_make_database_evidence(self):
        declaration = (
            "./build/../main.o: ./src/../main.c "
            "/course/project/include/../config.h ./unused.h"
        )
        database_text = (
            "# Files\n"
            "# E7 declaration normalization fixture\n"
            + declaration + "\n"
            "# files hash-table stats:\n"
        )

        with tempfile.TemporaryDirectory() as folder:
            database = Path(folder) / "make-db.txt"
            database.write_text(database_text, encoding="utf-8")
            declared = declaration_graph(database, "/course/project")

        self.assertEqual(set(declared), {"main.o"})
        dependencies = declared["main.o"]["dependencies"]
        self.assertEqual(
            set(dependencies), {"main.c", "config.h", "unused.h"}
        )
        for dependency in ("main.c", "config.h", "unused.h"):
            with self.subTest(dependency=dependency):
                self.assertEqual(
                    dependencies[dependency],
                    {
                        "source": "make_database",
                        "artifact": "make-db.txt",
                        "line": 3,
                        "declaration": declaration,
                    },
                )


if __name__ == "__main__":
    unittest.main()
