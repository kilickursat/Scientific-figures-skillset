# Contributing

Thank you for improving scientific figure quality and reproducibility.

## Contribution principles

A contribution must preserve the repository's evidence-first contract:

- never invent or normalize away scientific information;
- distinguish publisher-family defaults from exact journal requirements;
- avoid generative-image content in evidence-bearing examples;
- prefer deterministic checks over prose when a property is machine-verifiable;
- keep `SKILL.md` compact and move detail into one-level references;
- keep scripts local, inspectable, and network-free by default;
- retain the 600-DPI archival requirement independently of submission copies.

## Test-first workflow

1. Add a failing unit test, integration test, or behavior-eval case.
2. Run it and record the expected failure.
3. Implement the smallest change that satisfies the contract.
4. Run the complete test suite and skill validator.
5. Update documentation and the changelog.
6. Regenerate example outputs only when source or production behavior changes.

## Journal-profile changes

A profile pull request must include:

- the exact official source URL;
- access or verification date;
- affected journal, publisher family, article type, and submission stage;
- a distinction between archive and submission requirements;
- a test for every changed machine-readable field;
- explicit uncertainty where official guidance is inaccessible or journal-specific.

Do not copy copyrighted publisher templates, logos, or brand assets.

## Code quality

Run:

```bash
python -m pip install -e '.[test,demo]'
pytest -q
python scripts/validate_skill.py
python .agents/skills/scientific-visualization/scripts/figure_qc.py examples/calibration-figure --strict
python .agents/skills/scientific-visualization/scripts/figure_qc.py examples/calibration-figure-portrait --strict
```

Scripts should support `--help`, validate unsafe paths, produce actionable errors, and avoid silent fallback behavior.

## Pull-request checklist

- [ ] A failing test/eval existed before implementation.
- [ ] All tests pass.
- [ ] `SKILL.md` remains below 500 lines.
- [ ] JSON assets validate.
- [ ] Examples disclose synthetic data prominently.
- [ ] No confidential or proprietary data are included.
- [ ] Publisher sources and verification dates are documented.
- [ ] Changelog and citation metadata are updated when appropriate.
