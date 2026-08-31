# Scientific Visualization Skill Design

**Date:** 2026-08-31  
**Status:** Implemented and release-verified  
**Owner:** Kursat Kilic

## 1. Purpose

Create a portable, open-source Agent Skill that enables Claude and Codex to design, regenerate, audit, and export publication-grade scientific figures without changing the underlying evidence. The skill must support quantitative plots, multi-panel figures, scientific schematics, workflows, image-plus-quantitative layouts, and graphical abstracts for Nature, Science, arXiv, Elsevier, Springer, and comparable journals.

## 2. Non-negotiable contract

The skill must enforce all of the following:

1. Scientific evidence and quantitative fidelity take priority over aesthetics.
2. Missing values, samples, uncertainty, significance, labels, mechanisms, or results are never invented.
3. Generative-image tools are prohibited for data-bearing figures and scientific evidence panels.
4. Vector masters are required for plots, text, axes, symbols, arrows, and schematics whenever technically possible.
5. Every figure package contains a native 600-DPI raster archival master; changing only DPI metadata is not acceptable.
6. Journal-specific submission files may differ from the archive master when the publisher requires another format or resolution.
7. Portrait and landscape layouts are both supported. Reflowing panels must not alter the data mapping or scientific meaning.
8. All outputs must be accessible in grayscale and for common forms of color-vision deficiency.
9. Every output must be reproducible from source data and source code or must declare precisely which evidence layer is preserved as raster.
10. The skill must reject visual decoration that has no scientific role, including faux 3-D, gradients, glow, shadows, stock icons, ornamental textures, and generic AI-style cards.

## 3. Architecture

Use one canonical skill named `scientific-visualization`, organized with progressive disclosure:

- `SKILL.md`: compact control plane, workflow, hard rules, and deliverables.
- `references/`: detailed scientific integrity, design system, journal profiles, plot archetypes, schematic rules, export rules, accessibility, QA, and prompt examples.
- `assets/`: machine-readable journal profiles, palettes, request and manifest schemas, and plotting templates.
- `scripts/`: deterministic project scaffolding and output quality control.
- `agents/openai.yaml`: ChatGPT/Codex interface metadata.

The repository keeps the canonical skill at `.agents/skills/scientific-visualization/`. An installer copies it to `.claude/skills/scientific-visualization/` for Claude Code or to other project/user locations. The same skill bundle is packaged as `skill.zip` for upload-capable clients.

## 4. Workflow boundary

The skill accepts one or more of:

- raw tabular data;
- plotting scripts;
- a manuscript and figure captions;
- existing figure files;
- a scientific method or workflow description;
- target-journal and final-size constraints.

It produces:

- an evidence contract;
- a panel plan;
- source code;
- vector and raster outputs;
- a manifest with dimensions, hashes, provenance, and transformations;
- caption and alt text;
- an automated and manual QA report.

The skill stops rather than fabricates when evidence is insufficient.

## 5. Scientific figure families

The workflow classifies each request as one of:

- quantitative plot;
- quantitative multi-panel figure;
- scientific schematic or mechanism;
- workflow or architecture diagram;
- image-plus-quantitative evidence;
- map or spatial figure;
- graphical abstract;
- audit-only review.

Each family uses a specific reference file and QA rubric.

## 6. Journal profiles

Journal profiles are configurable starting points, not publisher endorsements. The agent must verify the specific target journal before final submission when network access is available. Profiles distinguish:

- final physical width and maximum height;
- typography and panel-label convention;
- vector and raster submission formats;
- photographic, combination, and line-art resolution;
- color space;
- initial-submission versus production requirements;
- arXiv file-efficiency and TeX-engine constraints.

The mandatory 600-DPI archival output remains independent of lower-resolution submission copies.

## 7. Deterministic QA

`scripts/figure_qc.py` validates:

- effective raster DPI at final physical size;
- pixel dimensions and metadata consistency;
- PDF page size, embedded fonts, and embedded-image resolution;
- SVG dimensions, text preservation, external links, gradients, and filters;
- journal profile constraints;
- file hashes and manifest completeness;
- portrait/landscape declaration;
- presence of source, caption, alt text, and manual QA sign-off.

Automated QA does not claim to detect statistical dishonesty, label overlap, or scientific misinterpretation; those remain explicit manual review gates.

## 8. Repository deliverables

The repository includes:

- Apache-2.0 license;
- README, contribution and security guidance;
- install and packaging scripts;
- automated tests and GitHub Actions;
- behavior-evaluation scenarios for Claude and Codex;
- a generated demonstration package used only for smoke testing.

## 9. Success criteria

The implementation is complete when:

- the skill validates and packages successfully;
- all unit and integration tests pass;
- a generated 600-DPI figure bundle passes automated QC;
- a deliberately 300-DPI archive fails QC;
- Claude and Codex installation paths are documented;
- no placeholder, invented scientific claim, or decorative AI-style instruction remains.
