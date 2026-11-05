"""Reject nested evidence paths before collecting or changing fixture inputs."""
import hashlib
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from buildchecker.fullcheck import full_check


@unittest.skipUnless(os.name == "posix", "Full collection requires Linux")
class TestFullCheckOutputBoundary(unittest.TestCase):
    def test_output_inside_fixture_is_rejected_without_side_effects(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / "fixture"
            fixture.mkdir()
            (fixture / "Makefile").write_text("all:\n\t@echo fixture\n", encoding="utf-8")
            (fixture / "unit.c").write_text("int main(void) { return 0; }\n", encoding="utf-8")
            output = fixture / "result"

            def input_hashes():
                return {
                    path.relative_to(fixture).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in sorted(fixture.rglob("*")) if path.is_file()
                }

            before = input_hashes()
            with patch("buildchecker.fullcheck.execute") as execute:
                with self.assertRaisesRegex(ValueError, "Output must be outside"):
                    full_check(fixture, output)
                execute.assert_not_called()

            self.assertEqual(input_hashes(), before)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
