"""Independent configuration/evidence scenarios; run inside the course image."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from lab import buildchecker, commit, fixture, run, save, scan

TARGETS = ['main.o', 'helper.o']
ACTUAL = {'main.o': ['config.h', 'main.c'], 'helper.o': ['helper.c']}
DECLARED = {'main.o': ['main.c', 'unused.h'], 'helper.o': ['helper.c']}
FINDINGS = {('MISSING', 'main.o', 'config.h'),
            ('REDUNDANT', 'main.o', 'unused.h')}


def findings(report):
    return {(f['type'], f['target'], f['dependency']) for f in report['findings']}


def expect(report, actual=ACTUAL, expected=FINDINGS):
    assert report['actual'] == actual, report['actual']
    assert report['declared'] == DECLARED, report['declared']
    assert findings(report) == expected, report['findings']


def same_graphs(incremental, full):
    for key in ('actual', 'declared', 'findings'):
        assert incremental[key] == full[key], key


def snapshot(out):
    """Hash existing evidence, excluding only the changing fixture and step log."""
    return {str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in out.rglob('*') if p.is_file()
            and p.relative_to(out).parts[0] not in ('project', 'steps')}


def preserved(out, before):
    for name, digest in before.items():
        assert hashlib.sha256((out / name).read_bytes()).hexdigest() == digest, name


def dynamic(out, name, report):
    directory = out / name
    buildchecker(out / 'project', directory)
    edges = json.loads((directory / 'actual-graph.json').read_text())
    actual = {t: sorted({e['dependency'] for e in edges if e['target'] == t})
              for t in TARGETS}
    result = json.loads((directory / 'findings.json').read_text())
    projected = {tuple(f[k] for k in ('type', 'target', 'dependency'))
                 for f in result['findings'] if f['target'] in TARGETS}
    assert actual == report['actual'], actual
    assert projected == findings(report), projected
    return actual


def build(out, name):
    p = out / 'project'
    # Configuration changes alone need not cause Make to rebuild old objects.
    log = run(['make', 'clean'], p) + run(['make', 'app'], p)
    output = run(['./app'], p).strip()
    (out / (name + '-build.log')).write_text(log + '\nAPP_OUTPUT=' + output + '\n')
    assert output == '1', output


def e8(out, with_dynamic=False):
    """helper.c -> bridge.h -> extra.h, distinct from main.c's config.h."""
    p = out / 'project'
    fixture(p)
    baseline = scan(p)
    expect(baseline)
    if with_dynamic:
        baseline['actual'] = dynamic(out, 'buildchecker', baseline)
        baseline['baseline_source'] = 'BuildChecker actual-graph.json projected to object targets'
    save(out / 'baseline.json', baseline)
    old = copy.deepcopy(baseline)
    evidence = snapshot(out)
    (p / 'bridge.h').write_text('#include "extra.h"\n')
    (p / 'helper.c').write_text('#include "bridge.h"\nint helper(void){return EXTRA;}\n')
    commit(p, 'P1 helper includes bridge and transitive extra header')
    incremental = scan(p, baseline)
    full = scan(p)
    actual = {'main.o': ['config.h', 'main.c'],
              'helper.o': ['bridge.h', 'extra.h', 'helper.c']}
    added = {('MISSING', 'helper.o', 'bridge.h'), ('MISSING', 'helper.o', 'extra.h')}
    expect(incremental, actual, FINDINGS | added)
    assert incremental['refreshed'] == TARGETS and incremental['reused'] == []
    assert {tuple(f) for f in incremental['added']} == added
    assert incremental['resolved'] == []
    same_graphs(incremental, full)
    assert baseline == old
    preserved(out, evidence)
    save(out / 'P1.json', incremental)
    save(out / 'P1-full.json', full)
    build(out, 'P1')
    if with_dynamic:
        dynamic(out, 'P1-buildchecker', incremental)
    unchanged = scan(p, incremental)
    assert unchanged['reused'] == TARGETS and unchanged['refreshed'] == []
    assert unchanged['added'] == [] and unchanged['resolved'] == []
    same_graphs(unchanged, full)
    save(out / 'incremental.json', unchanged)
    return {'commits': {'C0': baseline['commit'], 'P1': incremental['commit']},
            'indirect_edges_exact': True, 'old_evidence_preserved': True,
            'incremental_equals_full': True, 'unchanged_reuses_both': True,
            'dynamic_checked': with_dynamic}


def e9(out, with_dynamic=False):
    """O0 -> O1 refresh; reject O2 without touching history; recover O1."""
    p = out / 'project'
    fixture(p)
    baseline = scan(p)
    expect(baseline)
    save(out / 'baseline.json', baseline)
    build(out, 'P0')
    if with_dynamic:
        dynamic(out, 'buildchecker', baseline)
    old = copy.deepcopy(baseline)
    before = snapshot(out)
    makefile = p / 'Makefile'
    makefile.write_text(makefile.read_text().replace('-O0', '-O1'))
    commit(p, 'P1 supported optimization configuration change')
    incremental = scan(p, baseline)
    full = scan(p)
    expect(incremental)
    assert baseline['key']['flags'] == '-O0'
    assert incremental['key']['flags'] == '-O1' and incremental['key'] != baseline['key']
    assert incremental['refreshed'] == TARGETS and incremental['reused'] == []
    assert incremental['added'] == [] and incremental['resolved'] == []
    same_graphs(incremental, full)
    assert baseline == old
    preserved(out, before)
    save(out / 'P1.json', incremental)
    save(out / 'P1-full.json', full)
    build(out, 'P1')
    if with_dynamic:
        dynamic(out, 'P1-buildchecker', incremental)
    previous = copy.deepcopy(incremental)
    before_rejection = snapshot(out)
    makefile.write_text(makefile.read_text().replace('-O1', '-O2'))
    rejected_commit = commit(p, 'P2 unsupported optimization configuration')
    errors = []
    for history in (incremental, None):
        try:
            scan(p, history)
        except ValueError as ex:
            assert str(ex) == 'UNSUPPORTED_FLAGS', str(ex)
            errors.append(str(ex))
        else:
            raise AssertionError('Unsupported configuration accepted')
    assert incremental == previous and baseline == old
    preserved(out, before_rejection)
    assert not (out / 'P2.json').exists()
    save(out / 'P2-rejected.json', {'commit': rejected_commit, 'flags': '-O2',
         'incremental_error': errors[0], 'full_error': errors[1],
         'old_evidence_sha256': before_rejection, 'old_evidence_preserved': True})
    makefile.write_text(makefile.read_text().replace('-O2', '-O1'))
    commit(p, 'P3 restore supported configuration after rejection')
    recovery = scan(p, incremental)
    recovery_full = scan(p)
    expect(recovery)
    assert recovery['reused'] == TARGETS and recovery['refreshed'] == []
    assert recovery['added'] == [] and recovery['resolved'] == []
    assert recovery['commit'] != incremental['commit']
    same_graphs(recovery, recovery_full)
    preserved(out, before_rejection)
    save(out / 'P3.json', recovery)
    save(out / 'P3-full.json', recovery_full)
    build(out, 'P3')
    return {'commits': {'C0': baseline['commit'], 'P1': incremental['commit'],
                       'P2': rejected_commit, 'P3': recovery['commit']},
            'configuration_refreshes_both': True, 'incremental_equals_full': True,
            'unsupported_incremental_and_full_rejected': True,
            'old_evidence_preserved': True, 'recovery_reuses_both': True,
            'dynamic_checked': with_dynamic}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['e8', 'e9'])
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    out = args.out.resolve()
    if not out.is_relative_to(root / 'work') or out == root / 'work':
        parser.error('--out must be a new directory below work/')
    # lab_new_run creates only identity files before this runner is invoked.
    if not out.is_dir() or (out / 'project').exists():
        parser.error('use lab_new_run and a fresh OUT without project/')
    for name in ('student-source-commit.txt', 'environment-image-id.txt'):
        if not (out / name).is_file():
            parser.error('missing identity file: ' + name)
    source = (out / 'student-source-commit.txt').read_text().strip()
    if source != run(['git', 'rev-parse', 'HEAD'], root).strip():
        parser.error('OUT source SHA does not match HEAD')
    if run(['git', 'status', '--porcelain'], root).strip():
        parser.error('commit source changes before running personal evidence')
    result = {'e8': e8, 'e9': e9}[args.stage](out, with_dynamic=True)
    assert not run(['git', 'status', '--porcelain'], out / 'project').strip()
    save(out / 'personal-gate.json', dict(result, passed=True, source_sha=source,
         stage=args.stage, student='241250076'))
    print('PERSONAL_PASS', args.stage, json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
