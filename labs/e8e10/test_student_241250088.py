"""Independent E8/E9 cases for student 241250088."""

import copy
import tempfile
import unittest
from pathlib import Path

from lab import commit, fixture, scan
from student_241250088_e9 import run_personal


class Student241250088Tests(unittest.TestCase):
    def test_e9_body_reuse_then_existing_header_invalidation(self):
        with tempfile.TemporaryDirectory() as tmp:
            gate = run_personal(Path(tmp) / 'e9')
            self.assertTrue(gate['body_reuses_both'])
            self.assertEqual(gate['header_only_changed_files'], ['bridge.h'])
            self.assertTrue(gate['header_refreshes_both'])
            self.assertTrue(gate['incremental_equals_full'])

    def test_helper_indirect_include_invalidates_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / 'project'
            fixture(project)
            baseline = scan(project)
            original = copy.deepcopy(baseline)

            (project / 'bridge.h').write_text('#include "extra.h"\n')
            (project / 'helper.c').write_text(
                '#include "bridge.h"\nint helper(void){return EXTRA;}\n'
            )
            changed_commit = commit(project, 'Add helper indirect include')

            incremental = scan(project, baseline)
            full = scan(project)

            expected_actual = {
                'main.o': ['config.h', 'main.c'],
                'helper.o': ['bridge.h', 'extra.h', 'helper.c'],
            }
            expected_declared = {
                'main.o': ['main.c', 'unused.h'],
                'helper.o': ['helper.c'],
            }
            expected_findings = {
                ('MISSING', 'main.o', 'config.h'),
                ('REDUNDANT', 'main.o', 'unused.h'),
                ('MISSING', 'helper.o', 'bridge.h'),
                ('MISSING', 'helper.o', 'extra.h'),
            }
            self.assertEqual(incremental['actual'], expected_actual)
            self.assertEqual(incremental['declared'], expected_declared)
            self.assertEqual(
                {(f['type'], f['target'], f['dependency'])
                 for f in incremental['findings']},
                expected_findings,
            )
            self.assertEqual(
                {tuple(f) for f in incremental['added']},
                {('MISSING', 'helper.o', 'bridge.h'),
                 ('MISSING', 'helper.o', 'extra.h')},
            )
            self.assertEqual(incremental['resolved'], [])
            self.assertEqual(incremental['reused'], [])
            self.assertEqual(incremental['refreshed'], ['main.o', 'helper.o'])
            self.assertNotEqual(incremental['key'], baseline['key'])
            self.assertEqual(incremental['commit'], changed_commit)
            self.assertNotEqual(changed_commit, baseline['commit'])
            for key in ['actual', 'declared', 'findings']:
                self.assertEqual(incremental[key], full[key], key)
            self.assertEqual(baseline, original)


if __name__ == '__main__':
    unittest.main()
