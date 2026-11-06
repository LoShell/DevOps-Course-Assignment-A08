"""E6 / 241250088: matching execution and declaration produce no findings."""

import tempfile
import unittest
from pathlib import Path

from buildchecker.fullcheck import analyze


class TestMatchingDependencies(unittest.TestCase):
    def test_matching_dependencies_have_no_findings_and_complete_graphs(self):
        # The compiler and assembler are siblings in one recipe job.
        traces = {
            "t.101": (
                'execve("/usr/bin/make", ["make", "unit.o"], []) = 0\n'
                'clone(child_stack=NULL, flags=SIGCHLD) = 102\n'
            ),
            "t.102": (
                'execve("/usr/bin/cc", ["cc", "-c", "unit.c", "-o", "unit.o"], []) = 0\n'
                'clone(child_stack=NULL, flags=SIGCHLD) = 103\n'
                'clone(child_stack=NULL, flags=SIGCHLD) = 104\n'
            ),
            "t.103": (
                'execve("/usr/bin/cc1", ["cc1", "unit.c"], []) = 0\n'
                'openat(AT_FDCWD, "unit.c", O_RDONLY) = 3\n'
                'openat(AT_FDCWD, "needed.h", O_RDONLY) = 4\n'
            ),
            "t.104": (
                'execve("/usr/bin/as", ["as", "-o", "unit.o"], []) = 0\n'
                'openat(AT_FDCWD, "unit.o", O_RDWR|O_CREAT|O_TRUNC, 0666) = 3\n'
            ),
        }
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            trace_dir = folder / "trace"
            trace_dir.mkdir()
            for name, contents in traces.items():
                (trace_dir / name).write_text(contents, encoding="utf-8")

            database = folder / "make-db.txt"
            # Reverse the input order to exercise dependency-set comparison.
            database.write_text(
                "# Files\n"
                "unit.o: needed.h unit.c\n"
                "# files hash-table stats:\n",
                encoding="utf-8",
            )
            result = analyze(trace_dir, database, "/course/project")

        expected_edges = {("unit.o", "unit.c"), ("unit.o", "needed.h")}
        self.assertEqual(result["observed_targets"], ["unit.o"])
        self.assertEqual(result["findings"], [])
        for name in ("actual_graph", "declared_graph"):
            with self.subTest(graph=name):
                edges = result[name]
                self.assertEqual(len(edges), 2)
                self.assertEqual(
                    {(edge["target"], edge["dependency"]) for edge in edges},
                    expected_edges,
                )


if __name__ == "__main__":
    unittest.main()
