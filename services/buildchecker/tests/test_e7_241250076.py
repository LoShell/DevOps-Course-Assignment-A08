"""Preserve existing evidence when a full-check output directory is reused."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from buildchecker.fullcheck import full_check


@unittest.skipUnless(os.name == "posix", "Full collection requires Linux")
class TestEvidencePreservation(unittest.TestCase):
    def test_nonempty_output_is_rejected_without_changing_old_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = root / "fixture"
            fixture.mkdir()
            (fixture / "Makefile").write_text("app:\n\t@echo fixture\n", encoding="utf-8")
            (fixture / "unit.c").write_text("int main(void) { return 0; }\n", encoding="utf-8")
            output = root / "evidence"
            output.mkdir()
            (output / "clean.log").write_bytes(b"old clean log\r\n\x00\xff\n")
            (output / "findings.json").write_bytes(b'{"trace_id":"previous-run"}\n')
            (output / "trace").mkdir()
            (output / "trace" / "t.10").write_bytes(b"old syscall transcript\n")
            (output / "empty-directory").mkdir()

            def snapshot():
                return {
                    path.relative_to(output).as_posix(): (
                        "file", path.read_bytes()
                    ) if path.is_file() else ("directory", None)
                    for path in sorted(output.rglob("*"))
                }

            before = snapshot()
            with patch("buildchecker.fullcheck.execute") as execute:
                with self.assertRaisesRegex(ValueError, "fresh empty output directory"):
                    full_check(fixture, output)
                execute.assert_not_called()

            self.assertTrue(output.is_dir())
            self.assertEqual(snapshot(), before)


if __name__ == "__main__":
    unittest.main()
