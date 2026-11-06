"""E6: reject a cycle in phony prerequisites."""
import tempfile
import unittest
from pathlib import Path

from buildchecker.fullcheck import Unsupported, declaration_graph


class TestPhonyCycle241250097(unittest.TestCase):
    def test_phony_prerequisite_cycle_raises_unsupported(self):
        database_text = (
            "# Files\n"
            ".PHONY: prepare loop\n"
            "prepare: loop\n"
            "loop: prepare\n"
            "unit.o: unit.c prepare\n"
            "# files hash-table stats:\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            database = Path(folder) / "make-db.txt"
            database.write_text(database_text, encoding="utf-8")

            with self.assertRaisesRegex(
                Unsupported, "Cycle in phony prerequisites"
            ):
                declaration_graph(database, "/course/project")


if __name__ == "__main__":
    unittest.main()
