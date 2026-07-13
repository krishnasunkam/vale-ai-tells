# vale-ai-tells

A [Vale](https://vale.sh) style-package that flags the tells of AI-written and spec-grade prose, so you can recast them in your own voice before you ship.

Modern writing tools make it easy to produce text that reads like a machine wrote it. That prose has a fingerprint: the em dash, the epigram (`is the hero, not a decoration`), the antithesis flourish (`reads as discipline, never confession`), the virtue tag (`done right`), the abstract-noun triad (`clarity, discipline, and trust`). AiTells names each one where it appears, in Markdown, HTML, or plain text, entirely on your own machine. It does not rewrite for you. It marks the tell so you fix it yourself.

## Install

```bash
brew install vale            # macOS; see vale.sh for other platforms
```

Add the package to your `.vale.ini`:

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
