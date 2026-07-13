#!/usr/bin/env python3
"""Assert each AiTells rule fires on a tell and stays silent on the clean rewrite.
Synthetic fixtures only; no external content. Requires the `vale` binary on PATH.

Run:  python3 tests/run_tests.py     # exit 0 = all green
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = os.path.join(ROOT, '.vale.ini')
FIX = os.path.join(HERE, 'fixtures.jsonl')


def checks_fired(text):
    """Return the set of AiTells checks Vale reports on one snippet."""
    with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, dir=ROOT,
                                     encoding='utf-8') as f:
        f.write(text + '\n')
        path = f.name
    try:
        out = subprocess.run(['vale', '--config', CFG, '--output=JSON', path],
                             capture_output=True, text=True)
        data = json.loads(out.stdout or '{}')
        return {a['Check'] for _f, lst in data.items() for a in lst}
    except FileNotFoundError:
        sys.exit('vale not found on PATH. Install it: https://vale.sh')
    finally:
        os.unlink(path)


def main():
    fixtures = [json.loads(l) for l in open(FIX, encoding='utf-8') if l.strip()]
    fails = []
    for fx in fixtures:
        fired = checks_fired(fx['text'])
        if 'must_flag' in fx and fx['must_flag'] not in fired:
            fails.append('%-22s MISSED %-22s (fired: %s)'
                         % (fx['id'], fx['must_flag'], ','.join(sorted(fired)) or 'none'))
        if 'must_not_flag' in fx and fx['must_not_flag'] in fired:
            fails.append('%-22s FALSE+ %s on clean text' % (fx['id'], fx['must_not_flag']))
    if fails:
        print('FAILED %d/%d' % (len(fails), len(fixtures)))
        for f in fails:
            print('  ' + f)
        sys.exit(1)
    print('all %d fixtures green' % len(fixtures))


if __name__ == '__main__':
    main()
