---
name: vale-ai-tells
description: Lint prose for the tells of AI-written text (em-dash habits, epigrams, abstract-noun triads, virtue tags) using a Vale style package, then help the author recast flagged lines in their own voice. Use when someone wants to check whether a README, doc, blog post, or PR description reads like a machine wrote it, or before shipping AI-drafted prose.
---

# vale-ai-tells

Flags the fingerprint of AI-written and spec-grade prose: seventeen rules covering the
em dash reflex, the epigram (`is the hero, not a decoration`), the antithesis flourish,
the virtue tag (`done right`), the abstract-noun triad, and twelve more. It marks the
tell; the human recasts it. **Never rewrite the user's prose without being asked**:
the entire point is that the fix happens in their voice, not another machine's.

## Do this, in order

### 1. Check the tools

```bash
vale --version || brew install vale   # other platforms: https://vale.sh
```

### 2. Lint the prose

From this package's directory, lint any file or directory the user names:

```bash
vale --config .vale.ini --output=JSON path/to/their-doc.md
```

Or run the narrated version they can watch:

```bash
./checkmyprose.sh path/to/their-doc.md
```

To install the package into the user's own repo instead, copy `AiTells/` there and add
to their `.vale.ini`:

```ini
StylesPath = styles
MinAlertLevel = suggestion

[*.{md,markdown,txt}]
BasedOnStyles = AiTells
```

### 3. Read the findings back as a table

One row per rule that fired: rule, severity, count, and one real example from their
text. Then a one-line verdict. Do not narrate each finding in paragraphs.

| Rule | Level | Count | Example from the text |
|---|---|---|---|
| Dash | error | 7 | "the fix (and it matters)" recast from their dashes |
| AbstractTriad | suggestion | 2 | "clarity, discipline, and trust" |

**Verdict: 9 tells across 2 files. Reads machine-drafted in places.**

### 4. Offer recasts, one at a time, in their voice

For each flagged line the user wants help with: quote the original, name the tell,
propose **one** recast that keeps their vocabulary and rhythm, and let them accept,
edit, or skip. Errors (the six mechanical tells) are worth fixing every time;
suggestions are judgment calls, and you say so.

### 5. Optional: make it stick

Offer to add the package and a CI step to their repo so the tells stop shipping
(copy this repo's `.github/workflows/vale.yml` as the starting point). Only do this if
they ask.

## Rules

- **Mark, don't rewrite.** No bulk auto-recasting. One proposed recast at a time, user
  approves each.
- **Local only.** Vale runs on their machine; no prose leaves it.
- **Report honestly.** If nothing fires, say the prose is clean and stop. Do not
  invent style feedback beyond what the rules found.
- **Respect the levels.** Errors are mechanical and safe to fix; suggestions require
  the user's judgment. Do not present a suggestion as a must-fix.
