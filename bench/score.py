#!/usr/bin/env python3
"""Score AiTells against a small synthetic labeled set: recall on the tells, and
false fires on the clean rewrites. This is the method in miniature, so a rule has
to earn its place rather than be added by taste. Requires the `vale` binary.

Run:  python3 bench/score.py
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = os.path.join(ROOT, '.vale.ini')
BENCH = os.path.join(HERE, 'mini-bench.jsonl')


def checks_fired(text):
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
    rows = [json.loads(l) for l in open(BENCH, encoding='utf-8') if l.strip()]
    flag = [r for r in rows if r['expect'] == 'flag']
    clean = [r for r in rows if r['expect'] == 'clean']
    hit = sum(1 for r in flag if r['check'] in checks_fired(r['text']))
    false = sum(1 for r in clean if r['check'] in checks_fired(r['text']))
    print('AiTells mini-bench (%d rows: %d tells, %d clean rewrites)'
          % (len(rows), len(flag), len(clean)))
    print('  recall on tells      : %d/%d = %.0f%%'
          % (hit, len(flag), 100 * hit / len(flag) if flag else 0))
    print('  false fires on clean : %d/%d' % (false, len(clean)))
    # a rule earns its place only if it catches the tell and spares the rewrite
    sys.exit(0 if hit == len(flag) and false == 0 else 1)


if __name__ == '__main__':
    main()
