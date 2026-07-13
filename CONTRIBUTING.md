# Contributing to vale-ai-tells

Thanks for helping catch the tells of machine-written prose. New rules, better patterns, and false-fire reports are all welcome.

## The bar for a new rule

A rule ships only when it does two things: it catches a real tell, and it stays silent on the clean rewrite. Both are proven by a fixture, not by argument.

1. **Add the rule.** Write a YAML file under `AiTells/`, extending one of Vale's checks (`existence`, `substitution`, `occurrence`, `capitalization`, and so on). Keep the pattern tight. Vale uses Go's RE2 engine, which has no lookahead or backreferences, so write for that.
2. **Add fixtures.** In `tests/fixtures.jsonl`, add one line that must flag your rule and one clean line that must stay silent:
   ```json
   {"id": "my-rule-flag", "text": "the prose that trips it", "must_flag": "AiTells.MyRule"}
   {"id": "my-rule-clean", "text": "the recast that passes", "must_not_flag": "AiTells.MyRule"}
   ```
3. **Run the tests.** They must stay green.
   ```bash
   python3 tests/run_tests.py
   ```
4. **Check for false fires.** Run the scorer and confirm your rule does not raise alarms on the clean rows.
   ```bash
   python3 bench/score.py
   ```

## What does not belong here

This package catches mechanical tells that a pattern can express. It does not judge register, the sense that a sentence belongs on a keynote slide. That judgment is not a regular expression, so please do not force it into one. A rule that fires on good prose is worse than no rule.

## Cutting a release

Maintainers publish a package for `vale sync` by zipping the style directory and attaching it to a versioned GitHub release:

```bash
zip -r AiTells.zip AiTells
```

Create a new release with a SemVer tag (for example `v0.1.0`) and upload `AiTells.zip` as the asset. To list the package on the Vale hub, open a pull request against [vale-cli/packages](https://github.com/vale-cli/packages) following its current submission format.
