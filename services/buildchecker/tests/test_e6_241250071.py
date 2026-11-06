"""E6 coverage: a temporary artifact renamed to the final target."""
import tempfile
import unittest
from pathlib import Path

from buildchecker.fullcheck import execution_graph


class TestE6241250071(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)
        self.root = "/course/project"

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, text):
        path = self.folder / name
        path.write_text(text, encoding="utf-8")

    def test_renamed_temporary_output_is_attributed_to_final_target(self):
        self.write(
            "t.10",
            'execve("/usr/bin/make", ["make", "unit.o"], []) = 0\n'
            'clone(child_stack=NULL, flags=SIGCHLD) = 11\n',
        )
        self.write(
            "t.11",
            'execve("/usr/bin/cc", ["cc", "-c", "unit.c", "-o", "unit.o"], []) = 0\n'
            'clone(child_stack=NULL, flags=SIGCHLD) = 12\n'
            'clone(child_stack=NULL, flags=SIGCHLD) = 13\n',
        )
        self.write(
            "t.12",
            'execve("/usr/bin/cc1", ["cc1", "unit.c"], []) = 0\n'
            'openat(AT_FDCWD, "unit.c", O_RDONLY) = 3\n'
            'openat(AT_FDCWD, "needed.h", O_RDONLY) = 4\n',
        )
        self.write(
            "t.13",
            'execve("/usr/bin/as", ["as", "-o", "unit.o"], []) = 0\n'
            'openat(AT_FDCWD, "temporary.o", O_RDWR|O_CREAT|O_TRUNC, 0666) = 3\n'
            'openat(AT_FDCWD, "temporary.o", O_RDONLY) = 4\n'
            'rename("temporary.o", "unit.o") = 0\n',
        )

        targets, _ = execution_graph(self.folder, self.root)

        self.assertEqual(set(targets), {"unit.o"})
        self.assertEqual(
            set(targets["unit.o"]["dependencies"]),
            {"unit.c", "needed.h"},
        )
        self.assertNotIn("temporary.o", targets["unit.o"]["dependencies"])
        self.assertEqual(targets["unit.o"]["output_evidence"]["operation"], "rename")
        self.assertEqual(targets["unit.o"]["output_evidence"]["trace_file"], "t.13")


if __name__ == "__main__":
    unittest.main()
