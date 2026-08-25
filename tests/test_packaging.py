#!/usr/bin/env python3
"""Packaging gate: the skill assets exist, scripts parse, and the reveal renders.
Hermetic; no network. Requires bash and python3 only (vale not needed here)."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

passed = 0
failed = 0


def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"FAIL: {name}{' - ' + detail if detail else ''}")


# ---- completeness ----
for f in ["SKILL.md", "README.md", "LICENSE", "CONTRIBUTING.md", "checkmyprose.sh",
          "report.py", ".vale.ini", "examples/ai-prose.md", "examples/clean-prose.md",
          ".github/workflows/vale.yml"]:
    check(f"has {f}", os.path.exists(os.path.join(ROOT, f)))
check("has 17 rules", len([f for f in os.listdir(os.path.join(ROOT, "AiTells"))
                           if f.endswith(".yml")]) == 17)

# ---- SKILL.md contract ----
skill = open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
check("SKILL.md frontmatter name", "name: vale-ai-tells" in skill)
check("SKILL.md says when to use", "Use when" in skill)
check("SKILL.md ordered steps", "## Do this, in order" in skill)
check("SKILL.md Rules section", "## Rules" in skill)
check("SKILL.md forbids bulk rewrites", "never bulk-rewrites" in skill or "No bulk auto-recasting" in skill)

# ---- README journey ----
readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
check("README states prerequisites before command", readme.index("You need:") < readme.index("git clone"))
check("README has transcript", "c h e c k m y p r o s e" in readme)
check("README has Afterwards", "## Afterwards" in readme)
check("README states local-only posture", "never left your machine" in readme or "on your own machine" in readme)

# ---- script gates ----
script_path = os.path.join(ROOT, "checkmyprose.sh")
r = subprocess.run(["bash", "-n", script_path], capture_output=True)
check("checkmyprose.sh passes bash -n", r.returncode == 0, r.stderr.decode()[:120])
script = open(script_path, encoding="utf-8").read()
check("script respects NO_COLOR", "NO_COLOR" in script)
check("script privacy line", "never left your machine" in script)
check("script helpful preflight", "brew install vale" in script)

# ---- reveal renders from canned JSON (no vale needed) ----
canned = json.dumps({
    "doc.md": [
        {"Check": "AiTells.Dash", "Severity": "error", "Match": "\u2014"},
        {"Check": "AiTells.Adverb", "Severity": "suggestion", "Match": "quietly"},
    ]
})
r = subprocess.run([sys.executable, os.path.join(ROOT, "report.py")],
                   input=canned, capture_output=True, text=True)
check("report.py renders findings", r.returncode == 0 and "2 tells" in r.stdout, r.stdout[:120])
check("report.py names the fingerprint", "fingerprint" in r.stdout)
r2 = subprocess.run([sys.executable, os.path.join(ROOT, "report.py")],
                    input="{}", capture_output=True, text=True)
check("report.py clean verdict", "reads human" in r2.stdout)

print("-" * 60)
print(f"passed: {passed}  failed: {failed}")
sys.exit(0 if failed == 0 else 1)
