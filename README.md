# vale-ai-tells

A [Vale](https://vale.sh) style-package that flags the tells of AI-written and spec-grade prose, so you can recast them in your own voice before you ship.

Modern writing tools make it easy to produce text that reads like a machine wrote it. That prose has a fingerprint: the em dash, the epigram (`is the hero, not a decoration`), the antithesis flourish (`reads as discipline, never confession`), the virtue tag (`done right`), the abstract-noun triad (`clarity, discipline, and trust`). AiTells names each one where it appears, in Markdown, HTML, or plain text, entirely on your own machine. It does not rewrite for you. It marks the tell so you fix it yourself.

## Try it on your own prose, in one command

> **You need:** macOS or Linux · [Vale](https://vale.sh) (`brew install vale`) · python3
> (ships with macOS). Under a minute, all of it on your machine.

```bash
git clone https://github.com/krishnasunkam/vale-ai-tells.git
cd vale-ai-tells && ./checkmyprose.sh ~/path/to/your-doc.md
```

```
   ╭─ ✦ c h e c k m y p r o s e
   │  the tells of machine-written text, found in yours
   ╰─────────────────────────────────────

   reading your prose… (it stays on this machine)

   22 tells across 1 file — 6 mechanical (fix always), 16 judgment calls

   your fingerprint:
     · Adverb          ×3   “quietly”
     · LinkText        ×2   “This page”
     · Cliche          ×2   “game-changer”
     · Passive         ×2   “was shipped”
     · …and 12 more rules fired

   most flagged: your-doc.md (22 tells)
   verdict: reads machine-drafted — worth a real rewrite.

   your prose never left your machine.
```

No arguments? It checks the markdown it finds nearby. The transcript above is a real run
against `examples/ai-prose.md`.

## Afterwards

The clone is disposable: the fingerprint is the product. To make the rules part of a
repo you own:

```bash
mkdir -p styles && cp -R /path/to/vale-ai-tells/AiTells styles/
```

Or skip the copy: point Vale straight at the release zip in your `.vale.ini`:

```ini
StylesPath = styles
Packages = https://github.com/krishnasunkam/vale-ai-tells/releases/latest/download/AiTells.zip

[*.{md,markdown,txt}]
BasedOnStyles = AiTells
```

Then `vale sync` pulls the rules for you.

If you copied the folder by hand instead, add the package to your `.vale.ini`:

```ini
StylesPath = styles
MinAlertLevel = suggestion

[*.{md,txt}]
BasedOnStyles = AiTells
```

Then sync and lint:

```bash
vale sync
vale your-doc.md
```

## Use as a Claude Code skill

Point Claude Code (or a compatible agent) at this repo and ask it to check your prose.
[`SKILL.md`](SKILL.md) has the agent run the linter, read the findings back as a table,
and offer recasts one at a time in your voice. It marks tells; it never bulk-rewrites.

## What it catches

Seventeen rules. Six gate as errors, the mechanical tells that should never ship. The rest are suggestions you weigh with judgment.

| Rule | Catches | Level |
|---|---|---|
| `Dash` | em and en dashes, including numeric ranges | error |
| `CodeToken` | `ALL_CAPS_UNDERSCORE` names and single-letter formulas | error |
| `FilePath` | raw file paths in prose | error |
| `StatusBracket` | inline status grades like `[ON TRACK, GREEN]` | error |
| `SectionCode` | section and source codes (`Section 4`, `S12`) | error |
| `NeverTag` | the antithesis flourish (a clause closing with `never`) | error |
| `EpigramContrast` | `is the hero, not a decoration` | suggestion |
| `NegParallel` | `not just X, but Y` | suggestion |
| `CopulaInflation` | `serves as a`, `is a testament to` | suggestion |
| `HiddenVerb` | `conduct an analysis` | suggestion |
| `Passive` | passive voice | suggestion |
| `Cliche` | stock phrases | suggestion |
| `WeakResume` | `responsible for`, `worked on` | suggestion |
| `VirtueHonest` | `an honest update`, `to be honest` | suggestion |
| `LinkText` | `click here` | suggestion |
| `AbstractTriad` | three stacked abstractions | suggestion |
| `Adverb` | filler adverbs | suggestion |

## The method

Think of this as a rule floor rather than a detector. It does not guess a probability that a machine wrote your text. It names a specific, mechanical tell and leaves the rewrite to you. The harder judgment, whether a sentence reads like it belongs on a keynote slide, is a matter of register that a regular expression cannot express, so this package does not reach for it.

The rules came from a corpus of real editing passes. I scored each one against a labeled benchmark rather than picking it by taste. The `bench/` folder holds a small synthetic version of that method: a labeled set and a scorer that reports recall and false fires, so you can see how a rule earns its place. A rule that raises false alarms on clean prose does not ship.

## Examples

`examples/ai-prose.md` collects prose that trips the rules. `examples/clean-prose.md` shows the recast that passes. Run `vale examples/ai-prose.md` to watch it work.

## Contributing

New rules are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). The bar is simple: a rule must catch a real tell and stay silent on the clean rewrite, proven by a fixture in `tests/`.

## License

MIT. See [LICENSE](LICENSE). Built and maintained by Krishna Sunkam.
