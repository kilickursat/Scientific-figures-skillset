# Scientific Visualization Skills for Claude and Codex

An open-source, integrity-first Agent Skill for producing publication-grade scientific figures, plots, workflows, maps, schematics, and graphical abstracts without altering the underlying evidence.

The project is designed for researchers who need figures that are **scientifically defensible, reproducible, accessible, vector-first, and visually deliberate**—not generic AI-generated decoration. It supports Nature, Science/AAAS, arXiv, Elsevier, Springer Nature, and a conservative generic profile, while treating the exact target journal's current instructions as the final authority.

> **Non-negotiable archive contract:** every completed figure package keeps editable vector masters whenever possible and a native 600-DPI PNG or TIFF master at final physical size. A journal-specific 300-DPI submission copy does not replace the 600-DPI archive.

## Why this exists

Large language models can write plotting code, but they often optimize the appearance before they understand the evidence. Common failures include invented sample sizes, silent data changes, unsupported uncertainty bands, decorative gradients, faux 3-D, random icons, unreadable final-size text, and low-resolution files relabelled as “600 DPI.” This repository converts the figure task into a governed scientific workflow with explicit stop conditions and deterministic preflight checks.

The central rule is simple:

> A publication figure is part of the scientific record, not an illustration prompt.

## What the skill covers

- Quantitative plots and statistical graphics
- Multi-panel result figures
- Scientific workflows and system architecture
- Mechanism diagrams and explanatory schematics
- Image-plus-quantitative layouts
- Maps, sections, matrices, and heatmaps
- Graphical abstracts with evidence boundaries
- Existing-figure regeneration without value changes
- Journal-format conversion and production audits
- Portrait and landscape variants from the same data and logic

The skill does **not** use generative-image tools for data-bearing figures, microscopy, field photographs, geological evidence, maps presented as observations, or mechanisms presented as established fact.

## Scientific quality contract

Every figure workflow must:

1. State the scientific question before choosing a chart.
2. Record which claims the supplied evidence can support.
3. Preserve values, units, categories, exclusions, missingness, uncertainty, and sample structure.
4. Distinguish observed, measured, derived, modelled, assumed, proxy, reconstructed, explanatory, and unresolved content.
5. Refuse to invent missing values, labels, sample counts, significance, mechanisms, or thresholds.
6. Use vector objects for text, axes, symbols, lines, arrows, and schematic geometry whenever possible.
7. Create a native 600-DPI raster archive at declared final millimetre dimensions.
8. Keep portrait and landscape variants scientifically equivalent.
9. Provide source code, a request contract, a provenance manifest, hashes, caption, alt text, and QA reports.
10. Pass automated production checks and human scientific review.

## “No AI slop” means something testable

The skill rejects visual elements that do not encode data, method, comparison, uncertainty, or navigation. By default it removes:

- gradients, glow, drop shadows, glass effects, bevels, and faux depth;
- 3-D charts and perspective distortion;
- generic rounded cards around every item;
- decorative brains, gears, circuits, DNA, test tubes, leaves, and stock icons;
- ornamental arrows or background textures;
- promotional copy, generic buzzwords, and unsupported “breakthrough” language;
- random palette changes between panels;
- image-generation output that could be confused with observed evidence.

“High impact” is achieved through evidence hierarchy, composition, typography, spacing, scale discipline, direct annotation, uncertainty communication, and reviewer-readable structure.

## Repository layout

```text
.
├── .agents/skills/scientific-visualization/   # canonical portable skill
│   ├── SKILL.md                               # control plane
│   ├── agents/openai.yaml                     # interface metadata
│   ├── references/                            # progressively loaded guidance
│   ├── assets/                                # profiles, palettes, schemas, templates
│   └── scripts/                               # scaffold and deterministic QC
├── scripts/                                   # install, validate, and package utilities
├── tests/                                     # unit and integration tests
├── evals/                                     # Claude/Codex behavior scenarios
├── examples/                                  # verified portrait and landscape demos
└── docs/superpowers/                          # design and implementation records
```

## Installation

### Codex project installation

The canonical skill already lives at the cross-client project path:

```text
.agents/skills/scientific-visualization/
```

Clone or copy the repository into a project, or run:

```bash
python scripts/install.py --target codex --scope project --project /path/to/project
```

### Claude Code project installation

```bash
python scripts/install.py --target claude --scope project --project /path/to/project
```

This copies the same skill to:

```text
.claude/skills/scientific-visualization/
```

### Install for both runtimes

```bash
python scripts/install.py --target both --scope project --project /path/to/project
```

User-level installation is also supported:

```bash
python scripts/install.py --target both --scope user
```

The installer preflights all destinations and refuses to overwrite an existing skill unless `--force` is supplied.

### Upload bundle

The release process creates `dist/skill.zip`, containing exactly one validated skill directory. Use this archive in clients that support skill upload.

## Quick start

### 1. Ask the agent to use the skill

Example prompts:

```text
Use the scientific-visualization skill to regenerate these manuscript figures
for Nature. Preserve every value and result. Produce landscape and portrait
layouts, vector PDF/SVG masters, native 600-DPI PNG/TIFF archives, source code,
manifest, caption, alt text, and QA reports.
```

```text
Audit these Elsevier figures for scientific integrity, final physical size,
font legibility, effective DPI, embedded fonts, grayscale accessibility, and
journal-production readiness. Do not redesign before reporting evidence gaps.
```

```text
Turn this method description into a journal workflow schematic. Distinguish
observed inputs, implemented processing, assumptions, hypotheses, and human
review gates. Do not add stock icons or generated scientific imagery.
```

### 2. Scaffold a reproducible figure project

```bash
python .agents/skills/scientific-visualization/scripts/scaffold_figure.py \
  --name calibration-figure \
  --journal nature \
  --orientation landscape \
  --width-class double \
  --language python \
  --destination ./figures
```

The scaffold intentionally contains unresolved evidence fields rather than fabricated data. The Python and R templates require real input unless the operator explicitly enables a visibly labelled synthetic rendering test.

### 3. Complete the evidence contract

Edit `figure_request.json` to define:

- scientific question;
- claims allowed;
- authoritative evidence sources and hashes;
- units, exclusions, missing-value handling, and uncertainty;
- allowed and prohibited transformations;
- panel questions, encodings, provenance classes, and reviewer risks.

Do not proceed while required evidence remains ambiguous.

### 4. Render vector and archive outputs

The bundled Matplotlib template sets final dimensions in millimetres, preserves editable SVG text, embeds outline fonts in PDF, and exports lossless 600-DPI PNG/TIFF masters. An R/ggplot2 template is included for projects using `ggplot2`, `patchwork`, `svglite`, and `ragg`.

### 5. Finalize hashes and run deterministic QC

Populate file hashes, byte counts, and raster metadata after rendering:

```bash
python .agents/skills/scientific-visualization/scripts/finalize_manifest.py \
  ./figures/calibration-figure/figure_manifest.json
```

Then run QC:

```bash
python .agents/skills/scientific-visualization/scripts/figure_qc.py \
  ./figures/calibration-figure \
  --report-md ./figures/calibration-figure/qa/AUTOMATED_QC.md \
  --report-json ./figures/calibration-figure/qa/AUTOMATED_QC.json \
  --strict
```

The checker inspects:

- manifest schema and unresolved evidence;
- declared orientation and physical dimensions;
- file presence, byte size, and SHA-256 hashes;
- effective raster DPI calculated from pixels and final millimetres;
- misleading DPI metadata mismatches;
- PDF page size, Type 3 fonts, and font embedding;
- SVG viewBox, editable text, external links, gradients, and filter effects;
- caption, alt text, source files, panel provenance, and manual QA sign-off.

Automated QC cannot decide whether a statistical analysis is honest, whether a label overlaps after a particular typesetting workflow, or whether an upsampled image contains genuine detail. The rendered files and scientific logic must still be reviewed by a qualified human.

## Journal profiles

Profiles are production starting points, not visual imitation presets or publisher endorsements.

| Profile | Typical widths included | Panel-label default | Important note |
|---|---:|---|---|
| Nature | 89 / 183 mm | lowercase bold | Main figures prioritize editable vectors; Extended Data may need a separate 300-DPI copy. |
| Science/AAAS | 55 / 120 / 183 mm | uppercase bold | Science-family titles vary; verify the exact journal and revision stage. |
| arXiv | derived from manuscript | manuscript convention | Optimize compiled PDF portability, fonts, and file size; retain the 600-DPI archive separately. |
| Elsevier | 90 / 190 mm | journal-specific | The individual journal Guide for Authors overrides the publisher-family profile. |
| Springer Nature | 84 / 174 mm | commonly `(a)`, `(b)` | Halftone, combination, and line-art requirements differ; check the journal page. |
| Generic | 89 / 180 mm | lowercase bold | Marks target-journal verification as unresolved. |

Machine-readable values and source URLs are stored in `assets/journal_profiles.json`. Update `verified_on` whenever a numerical rule changes.

## 600 DPI: what the checker actually verifies

Resolution is calculated from physical size, not trusted from a metadata label:

```text
effective DPI = pixel dimension / (millimetres / 25.4)
```

A 900-pixel image labelled “600 DPI” cannot be a 183-mm-wide 600-DPI figure; its effective resolution is only about 125 DPI. The QC script flags this. It also records a limitation: software cannot always prove whether a correctly sized raster was created natively or upsampled before inspection, so provenance and visual review remain mandatory.

## Portrait and landscape equivalence

Orientation variants must be generated from the same source data and analytical code. Permitted changes include:

- panel reflow;
- annotation placement;
- legend position;
- shared-axis placement;
- white-space allocation.

The following are not permitted merely to make a layout fit:

- changing values, filters, categories, axis transformations, or uncertainty;
- transposing a matrix when row/column meaning changes;
- hiding inconvenient points or panels;
- changing color semantics between variants;
- introducing a different statistical summary.

Verified examples are included under `examples/calibration-figure/` and `examples/calibration-figure-portrait/`. Both use clearly labelled deterministic synthetic data solely to test production and layout; they make no scientific claim.

## Testing

Install development dependencies and run:

```bash
python -m pip install -e '.[test,demo]'
pytest -q
python scripts/validate_skill.py
```

The test suite includes positive and adversarial cases:

- required skill structure and discovery language;
- profile and schema contracts;
- project scaffolding;
- native 600-DPI pass;
- metadata-only 600-DPI failure;
- SVG gradient failure;
- TIFF metadata JSON serialization;
- safe Claude/Codex installation;
- strict QC of portrait and landscape demonstration packages.

Behavioral pressure scenarios live in `evals/skill-evals.jsonl`. They are designed to test whether an agent refuses invented values, decorative pressure, generative evidence, and DPI shortcuts. Deterministic repository tests run locally and in CI; live behavioral evaluation requires a configured Claude or Codex runtime.

## Updating publisher guidance

Before changing a profile:

1. Check the exact publisher or journal instructions.
2. Record the page URL and access date.
3. Separate archival policy from submission requirements.
4. Add or update tests before changing machine-readable values.
5. Explain uncertainty in `references/journal-profiles.md`.
6. Never claim a publisher endorsement or reproduce a proprietary template.

Primary starting sources are listed in the profile files, including the Agent Skills specification, Nature Research Figure Guide, arXiv submission documentation, Elsevier artwork guidance, and Springer Nature artwork instructions.

## Contributing

Contributions are welcome for:

- verified journal profiles;
- scientific plot archetypes;
- accessibility checks;
- deterministic QC inspectors;
- tested Python or R templates;
- domain modules that preserve evidence boundaries;
- adversarial eval cases.

Read `CONTRIBUTING.md` before opening a pull request. Every behavioral rule or code change requires a failing test or evaluation case first.

## Security and privacy

The bundled scaffold and QC tools are local and require no network access. Review all third-party skills and plotting scripts before execution. Do not commit confidential manuscripts, participant data, protected health information, unpublished site data, credentials, or proprietary figures to a public repository. See `SECURITY.md`.

## Citation

See `CITATION.cff`. Suggested text:

> Kilic, K. (2026). *Scientific Visualization Skills for Claude and Codex* (Version 0.1.0) [Computer software].

## License

Apache License 2.0. See `LICENSE`.

## Disclaimer

This software supports figure production and review; it does not replace statistical review, research-integrity review, domain expertise, copyright clearance, or the target journal's current author instructions. Publisher and journal names are used descriptively to identify compatibility profiles. No affiliation or endorsement is implied.
