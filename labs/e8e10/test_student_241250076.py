"""Independent expectations for 241250076's configuration/evidence scope."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from lab import commit, fixture, scan
from student_241250076 import e8, e9


class ConfigurationEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name)

    def test_helper_transitive_include_refreshes_and_preserves_baseline(self):
        e8(self.out)

    def test_flags_refresh_rejection_preserves_evidence_and_recovery_reuses(self):
        e9(self.out)

    def test_rejected_flags_stop_before_compiler_or_history_access(self):
        p = self.out / 'project'
        fixture(p)
        baseline = scan(p)
        original = (p / 'Makefile').read_text()
        for flags in ('-O2', '-O1 -include extra.h'):
            with self.subTest(flags=flags):
                (p / 'Makefile').write_text(original.replace('-O0', flags))
                commit(p, 'reject ' + flags)
                # Even a malformed history must not bypass the configuration gate.
                with patch('lab.run') as command:
                    for old in (None, baseline, {'invalid': 'history'}):
                        with self.assertRaisesRegex(ValueError, '^UNSUPPORTED_FLAGS$'):
                            scan(p, old)
                    command.assert_not_called()


if __name__ == '__main__':
    unittest.main()
