"""E7 coverage: reassemble an unfinished/resumed read-open syscall."""
import tempfile
import unittest
from pathlib import Path

from buildchecker.fullcheck import execution_graph


class TestE7241250071(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)
        self.root = "/course/project"

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, text):
        path = self.folder / name
        path.write_text(text, encoding="utf-8")

    def test_unfinished_resumed_openat_is_dependency_with_start_line_evidence(self):
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
            'openat(AT_FDCWD, "needed.h", O_RDONLY <unfinished ...>\n'
            '<... openat resumed>) = 4\n',
        )
        self.write(
            "t.13",
            'execve("/usr/bin/as", ["as", "-o", "unit.o"], []) = 0\n'
            'openat(AT_FDCWD, "unit.o", O_RDWR|O_CREAT|O_TRUNC, 0666) = 3\n',
        )

        targets, _ = execution_graph(self.folder, self.root)

        self.assertEqual(set(targets), {"unit.o"})
        self.assertEqual(
            set(targets["unit.o"]["dependencies"]),
            {"unit.c", "needed.h"},
        )

        evidence = targets["unit.o"]["dependencies"]["needed.h"]
        self.assertEqual(
            evidence,
            {
                "source": "system_call",
                "trace_file": "t.12",
                "line": 3,
                "pid": 12,
                "operation": "openat",
            },
        )


if __name__ == "__main__":
    unittest.main()
