"""Independent declaration cases; shared by temporary tests and saved runs."""
import json
import tempfile
import unittest
from pathlib import Path

from lab import fixture, scan, commit, run, save, buildchecker

TARGETS = ['main.o', 'helper.o']
RD = ('REDUNDANT', 'main.o', 'unused.h')
CONFIG_MD = ('MISSING', 'main.o', 'config.h')
EXTRA_MD = ('MISSING', 'main.o', 'extra.h')


def findings(report):
    return {(f['type'], f['target'], f['dependency']) for f in report['findings']}


def equal_full(out, name, report):
    full = scan(out / 'project')
    save(out / (name + '-full.json'), full)
    for key in ['actual', 'declared', 'findings']:
        assert report[key] == full[key], (name, key)


def check_dynamic(out, name, report):
    directory = out / name
    buildchecker(out / 'project', directory)
    edges = json.loads((directory / 'actual-graph.json').read_text())
    projected = {t: sorted({e['dependency'] for e in edges if e['target'] == t})
                 for t in TARGETS}
    assert projected == report['actual']
    declared_edges = json.loads((directory / 'declared-graph.json').read_text())
    declared = {t: sorted({e['dependency'] for e in declared_edges if e['target'] == t})
                for t in TARGETS}
    assert declared == report['declared']


def run_e8(out, dynamic=False):
    """helper.c -> shared.h -> extra.h, alongside main.c -> config.h."""
    p = out / 'project'
    fixture(p)
    (p / 'shared.h').write_text('#include "extra.h"\n')
    (p / 'helper.c').write_text('#include "shared.h"\nint helper(void){return EXTRA;}\n')
    commit(p, 'P0 helper indirect shared header')
    expected_actual = {'main.o': ['config.h', 'main.c'],
                       'helper.o': ['extra.h', 'helper.c', 'shared.h']}
    expected_declared = {'main.o': ['main.c', 'unused.h'], 'helper.o': ['helper.c']}
    expected_findings = {CONFIG_MD, RD,
                         ('MISSING', 'helper.o', 'shared.h'),
                         ('MISSING', 'helper.o', 'extra.h')}
    save(out / 'independent-expectations.json', {
        'actual': expected_actual, 'declared': expected_declared,
        'findings': sorted(expected_findings),
        'input': 'helper.c includes shared.h which includes extra.h'})
    baseline = scan(p)
    assert baseline['actual'] == expected_actual
    assert baseline['declared'] == expected_declared
    assert findings(baseline) == expected_findings
    assert baseline['refreshed'] == TARGETS and baseline['reused'] == []
    (out / 'P0-build.log').write_text(run(['make', 'app'], p))
    assert run(['./app'], p).strip() == '1'
    if dynamic:
        check_dynamic(out, 'buildchecker', baseline)
        edges = json.loads((out / 'buildchecker/actual-graph.json').read_text())
        baseline['actual'] = {t: sorted({e['dependency'] for e in edges if e['target'] == t})
                              for t in TARGETS}
        baseline['baseline_source'] = 'BuildChecker actual-graph.json projected to object targets'
    save(out / 'baseline.json', baseline)
    incremental = scan(p, baseline)
    save(out / 'incremental.json', incremental)
    assert incremental['actual'] == expected_actual
    assert incremental['declared'] == expected_declared
    assert findings(incremental) == expected_findings
    assert incremental['reused'] == TARGETS and incremental['refreshed'] == []
    assert incremental['added'] == incremental['resolved'] == []
    full = scan(p)
    save(out / 'full.json', full)
    assert all(incremental[k] == full[k] for k in ['actual', 'declared', 'findings'])
    save(out / 'personal-gate.json', {
        'passed': True, 'case': 'helper-indirect-shared-header',
        'commits': {'P0': baseline['commit']},
        'independent_expectations': True, 'incremental_equals_full': True,
        'dynamic_buildchecker': 'passed' if dynamic else 'not executed',
        'program_output': '1'})
    return incremental


def run_e9(out, dynamic=False):
    """Repair config alone, introduce extra include, then repair extra alone."""
    p = out / 'project'
    fixture(p)
    baseline = scan(p)
    assert findings(baseline) == {CONFIG_MD, RD}
    save(out / 'baseline.json', baseline)
    (out / 'P0-build.log').write_text(run(['make', 'app'], p))
    assert run(['./app'], p).strip() == '1'
    make = p / 'Makefile'
    make.write_text(make.read_text().replace('main.c unused.h', 'main.c unused.h config.h'))
    commit(p, 'P1 declare config only and retain unused')
    one = scan(p, baseline)
    save(out / 'P1.json', one)
    assert one['key'] == baseline['key'] and one['actual'] == baseline['actual']
    assert one['declared'] == {'main.o': ['config.h', 'main.c', 'unused.h'],
                               'helper.o': ['helper.c']}
    assert one['reused'] == TARGETS and one['refreshed'] == []
    assert one['added'] == [] and one['resolved'] == [list(CONFIG_MD)]
    assert findings(one) == {RD}
    equal_full(out, 'P1', one)
    (out / 'P1-build.log').write_text(run(['make', 'app'], p))
    if dynamic:
        check_dynamic(out, 'P1-buildchecker', one)
    source = p / 'main.c'
    source.write_text('#include "extra.h"\n' + source.read_text().replace(
        'VALUE+helper()', 'VALUE+helper()+EXTRA'))
    commit(p, 'P2 add and use extra include after config repair')
    two = scan(p, one)
    save(out / 'P2.json', two)
    assert two['actual'] == {'main.o': ['config.h', 'extra.h', 'main.c'],
                             'helper.o': ['helper.c']}
    assert two['declared'] == one['declared']
    assert two['refreshed'] == TARGETS and two['reused'] == []
    assert two['added'] == [list(EXTRA_MD)] and two['resolved'] == []
    assert findings(two) == {EXTRA_MD, RD}
    equal_full(out, 'P2', two)
    # Ensure the saved build is current even on filesystems with coarse timestamps.
    (out / 'P2-build.log').write_text(run(['make', '-B', 'app'], p))
    assert run(['./app'], p).strip() == '1'
    make.write_text(make.read_text().replace('main.c unused.h config.h',
                                            'main.c unused.h config.h extra.h'))
    commit(p, 'P3 declare extra only and retain unused')
    three = scan(p, two)
    save(out / 'P3.json', three)
    assert three['key'] == two['key'] and three['actual'] == two['actual']
    assert three['declared'] == {'main.o': ['config.h', 'extra.h', 'main.c', 'unused.h'],
                                 'helper.o': ['helper.c']}
    assert three['reused'] == TARGETS and three['refreshed'] == []
    assert three['added'] == [] and three['resolved'] == [list(EXTRA_MD)]
    assert findings(three) == {RD}
    equal_full(out, 'P3', three)
    (out / 'P3-build.log').write_text(run(['make', 'app'], p))
    if dynamic:
        check_dynamic(out, 'P3-buildchecker', three)
    assert run(['./app'], p).strip() == '1'
    assert run(['git', 'status', '--porcelain'], p).strip() == ''
    save(out / 'independent-expectations.json', {
        'P0': sorted({CONFIG_MD, RD}), 'P1': [RD],
        'P2': sorted({EXTRA_MD, RD}), 'P3': [RD],
        'P1_resolved': [CONFIG_MD], 'P2_added': [EXTRA_MD], 'P3_resolved': [EXTRA_MD]})
    save(out / 'personal-gate.json', {
        'passed': True, 'case': 'separate-config-and-extra-declaration-repair',
        'commits': {'P0': baseline['commit'], 'P1': one['commit'],
                    'P2': two['commit'], 'P3': three['commit']},
        'independent_expectations': True, 'all_incremental_equal_full': True,
        'dynamic_buildchecker': 'P1 and P3 passed' if dynamic else 'not executed',
        'program_output': '1'})
    return three


class Student241250097Tests(unittest.TestCase):
    def test_e8_helper_indirect_shared_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_e8(Path(tmp))

    def test_e9_separate_declaration_repairs_preserve_redundant(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_e9(Path(tmp))


if __name__ == '__main__':
    unittest.main()
