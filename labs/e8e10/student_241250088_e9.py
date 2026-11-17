"""Persist the independent E9 body-reuse and existing-header invalidation case."""

import copy
import time
from pathlib import Path

from lab import buildchecker, commit, fixture, run, save, scan


def run_personal(out, dynamic=False):
    out = Path(out)
    project = out / 'project'
    if project.exists():
        raise ValueError('PROJECT_MUST_BE_NEW')
    out.mkdir(parents=True, exist_ok=True)
    fixture(project)

    # Establish the bridge before the baseline. P2 changes only its contents.
    (project / 'bridge.h').write_text('/* initially no includes */\n')
    (project / 'helper.c').write_text(
        '#include "bridge.h"\nint helper(void){return 0;}\n'
    )
    makefile = project / 'Makefile'
    makefile.write_text(makefile.read_text().replace(
        'helper.o: helper.c', 'helper.o: helper.c bridge.h'
    ))
    commit(project, 'P0 establish declared helper bridge')
    (out / 'P0-build.log').write_text(run(['make', 'app'], project))
    assert run(['./app'], project).strip() == '1'
    baseline = scan(project)
    save(out / 'baseline.json', baseline)
    baseline_copy = copy.deepcopy(baseline)
    expected_actual = {
        'main.o': ['config.h', 'main.c'],
        'helper.o': ['bridge.h', 'helper.c'],
    }
    expected_declared = {
        'main.o': ['main.c', 'unused.h'],
        'helper.o': ['bridge.h', 'helper.c'],
    }
    expected_findings = {
        ('MISSING', 'main.o', 'config.h'),
        ('REDUNDANT', 'main.o', 'unused.h'),
    }
    findings = lambda report: {
        (f['type'], f['target'], f['dependency']) for f in report['findings']
    }
    assert baseline['actual'] == expected_actual
    assert baseline['declared'] == expected_declared
    assert findings(baseline) == expected_findings

    time.sleep(1.05)
    (project / 'helper.c').write_text(
        '#include "bridge.h"\nint helper(void){return (0 + 0);}\n'
    )
    body_commit = commit(project, 'P1 helper body only')
    body_build = run(['make', 'app'], project)
    (out / 'P1-build.log').write_text(body_build)
    assert run(['./app'], project).strip() == '1'
    body = scan(project, baseline)
    body_full = scan(project)
    save(out / 'P1.json', body)
    save(out / 'P1-full.json', body_full)
    assert body['commit'] == body_commit != baseline['commit']
    assert body['key'] == baseline['key']
    assert body['actual'] == expected_actual
    assert body['declared'] == expected_declared
    assert findings(body) == expected_findings
    assert body['reused'] == ['main.o', 'helper.o']
    assert body['refreshed'] == []
    assert body['added'] == body['resolved'] == []
    assert 'gcc -O0 -c helper.c -o helper.o' in body_build
    assert 'gcc -O0 -c main.c -o main.o' not in body_build
    assert 'gcc main.o helper.o -o app' in body_build
    for key in ['actual', 'declared', 'findings']:
        assert body[key] == body_full[key], ('P1', key)
    assert baseline == baseline_copy
    body_copy = copy.deepcopy(body)

    time.sleep(1.05)
    (project / 'bridge.h').write_text('#include "extra.h"\n')
    header_commit = commit(project, 'P2 existing bridge adds indirect include')
    changed_files = run(
        ['git', 'diff', '--name-only', body_commit, header_commit], project
    ).splitlines()
    assert changed_files == ['bridge.h']
    header_build = run(['make', 'app'], project)
    (out / 'P2-build.log').write_text(header_build)
    assert run(['./app'], project).strip() == '1'
    header = scan(project, body)
    header_full = scan(project)
    save(out / 'P2.json', header)
    save(out / 'P2-full.json', header_full)
    assert header['commit'] == header_commit
    assert header['key'] != body['key']
    assert header['actual'] == {
        'main.o': ['config.h', 'main.c'],
        'helper.o': ['bridge.h', 'extra.h', 'helper.c'],
    }
    assert header['declared'] == expected_declared
    assert findings(header) == expected_findings | {
        ('MISSING', 'helper.o', 'extra.h')
    }
    assert header['added'] == [['MISSING', 'helper.o', 'extra.h']]
    assert header['resolved'] == []
    assert header['reused'] == []
    assert header['refreshed'] == ['main.o', 'helper.o']
    for key in ['actual', 'declared', 'findings']:
        assert header[key] == header_full[key], ('P2', key)
    assert body == body_copy

    if dynamic:
        buildchecker(project, out / 'buildchecker')
    gate = {
        'passed': True,
        'case': 'helper-body-reuse-then-existing-header-invalidation',
        'commits': {'P0': baseline['commit'], 'P1': body_commit,
                    'P2': header_commit},
        'body_reuses_both': True,
        'header_only_changed_files': changed_files,
        'header_refreshes_both': True,
        'incremental_equals_full': True,
        'dynamic_crosscheck': dynamic,
    }
    save(out / 'personal-gate.json', gate)
    return gate
