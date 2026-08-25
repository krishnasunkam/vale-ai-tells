#!/usr/bin/env python3
"""Render Vale JSON (stdin) as the checkmyprose fingerprint reveal."""
import collections
import json
import os
import sys

dim, rst, bold = "\033[2m", "\033[0m", "\033[1m"
lilac, gold = "\033[38;5;183m", "\033[38;5;222m"
green, red = "\033[38;5;114m", "\033[38;5;210m"
if os.environ.get("NO_COLOR") or not sys.stdout.isatty():
    dim = rst = bold = lilac = gold = green = red = ""

data = json.loads(sys.stdin.read() or "{}")
by_rule = collections.Counter()
by_file = collections.Counter()
examples = {}
errors = 0
total = 0
for path, alerts in data.items():
    for a in alerts:
        rule = a["Check"].split(".", 1)[-1]
        by_rule[rule] += 1
        by_file[path] += 1
        total += 1
        if a["Severity"] == "error":
            errors += 1
        examples.setdefault(rule, (a["Match"][:44], a["Severity"]))

files = len(data)
if total == 0:
    print(f"   {green}not a single tell.{rst} {bold}your prose reads human.{rst}")
    print()
    sys.exit(0)

s_t = "s" if total != 1 else ""
s_f = "s" if files != 1 else ""
print(
    f"   {bold}{total} tell{s_t}{rst}{dim} across {files} file{s_f} — "
    f"{errors} mechanical (fix always), {total - errors} judgment calls{rst}"
)
print()
print(f"   {dim}your fingerprint:{rst}")
for rule, n in by_rule.most_common(5):
    ex, sev = examples[rule]
    mark = red if sev == "error" else gold
    print(f"     {mark}\u00b7{rst} {rule:<16}{dim}\u00d7{n:<4}\u201c{ex}\u201d{rst}")
if len(by_rule) > 5:
    print(f"     {dim}\u00b7 \u2026and {len(by_rule) - 5} more rules fired{rst}")
print()
worst, wn = by_file.most_common(1)[0]
print(f"   {lilac}most flagged:{rst} {worst} {dim}({wn} tells){rst}")
per = total / max(files, 1)
if errors == 0 and per < 3:
    verdict = f"{green}lightly touched \u2014 a quick pass and it is yours.{rst}"
elif errors < 5:
    verdict = f"{gold}the machine shows through in places.{rst}"
else:
    verdict = f"{red}reads machine-drafted \u2014 worth a real rewrite.{rst}"
print(f"   {bold}verdict:{rst} {verdict}")
print()
