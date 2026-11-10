"""E7 / 241250088: findings affect the exit code only when the gate is enabled."""

from contextlib import redirect_stdout
import io
import json
import unittest
from unittest.mock import patch

from buildchecker.cli import main


class TestFindingsExitPolicy(unittest.TestCase):
    def test_findings_gate_changes_exit_code_but_preserves_report(self):
        report = {
            "status": "SUCCEEDED",
            "findings": [
                {"type": "MISSING", "target": "main.o", "dependency": "config.h"}
            ],
        }
        args = ["full-check", "--out", "evidence"]

        with patch("buildchecker.cli.full_check", return_value=report):
            for extra_args, expected_exit in (
                ([], 0),
                (["--fail-on-findings"], 1),
            ):
                with self.subTest(gate_enabled=bool(extra_args)):
                    stdout = io.StringIO()
                    with redirect_stdout(stdout):
                        exit_code = main([*args, *extra_args])

                    self.assertEqual(exit_code, expected_exit)
                    self.assertEqual(json.loads(stdout.getvalue()), report)
