# Scientific Visualization Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Build, validate, and package one portable open-source Agent Skill that gives Claude and Codex an integrity-first workflow for publication-grade scientific figures, journal profiles, 600-DPI archival exports, portrait/landscape layouts, and deterministic QA.

**Architecture:** Keep the canonical skill under `.agents/skills/scientific-visualization/`. Use `SKILL.md` as a compact control plane, progressively loaded references for detailed guidance, JSON assets for deterministic profile/schema data, and dependency-light Python tools for project scaffolding and output QA. Repository-level installation, tests, examples, CI, citation, and contribution files surround the portable skill without inflating the upload bundle.

**Tech Stack:** Agent Skills open format, Markdown, JSON Schema 2020-12, Python 3.10+, Pillow, pypdf, pytest, Matplotlib demo, optional R/ggplot2 template.

**Spec:** `docs/superpowers/specs/2026-08-31-scientific-visualization-design.md`

## Global Constraints

- Scientific evidence and quantitative fidelity always outrank visual decoration.
- Never invent observations, values, uncertainty, significance, labels, mechanisms, or sample sizes.
- Do not use generative-image tools for data-bearing or observational figure content.
- Require vector masters whenever possible and a native 600-DPI PNG/TIFF archival master at final physical size.
- Preserve portrait/landscape scientific equivalence and record panel provenance.
- Target-journal instructions override publisher-family defaults and must be re-verified before submission.
- Keep the final `skill.zip` at or below 25 MB and name it exactly `skill.zip`.

---

### Task 1: Lock the Skill Contract and Progressive References

**Files:**
- Create/modify: `.agents/skills/scientific-visualization/SKILL.md`
- Create: `.agents/skills/scientific-visualization/references/*.md`
- Test: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: design spec requirements.
- Produces: discoverable skill entrypoint and one-level reference map.

- [x] Write failing structure and phrase tests.
- [x] Run tests and verify missing resources fail.
- [x] Write the minimal control plane and references.
- [x] Re-run tests and retain fewer than 500 lines in `SKILL.md`.

### Task 2: Add Machine-Readable Profiles, Palettes, and Schemas

**Files:**
- Create: `.agents/skills/scientific-visualization/assets/journal_profiles.json`
- Create: `.agents/skills/scientific-visualization/assets/palettes.json`
- Create: `.agents/skills/scientific-visualization/assets/figure_request.schema.json`
- Create: `.agents/skills/scientific-visualization/assets/figure_manifest.schema.json`
- Test: `tests/test_profiles.py`, `tests/test_schemas.py`

**Interfaces:**
- Produces: profile lookup by journal slug; JSON contracts for requests/manifests.

- [x] Write failing profile contract test.
- [x] Add profile and schema tests for required fields and valid examples.
- [x] Implement conservative profiles with source URLs and verification status.
- [x] Verify all tests pass.

### Task 3: Implement Project Scaffolding

**Files:**
- Create: `.agents/skills/scientific-visualization/scripts/scaffold_figure.py`
- Create: `.agents/skills/scientific-visualization/assets/templates/matplotlib_publication.py`
- Create: `.agents/skills/scientific-visualization/assets/templates/ggplot2_publication.R`
- Test: `tests/test_scaffold_api.py`

**Interfaces:**
- Produces: `create_project(destination, name, journal, orientation, language, width_class) -> Path`.

- [x] Write the failing scaffold API test.
- [x] Implement safe project naming, profile lookup, templates, request/manifest, and directories.
- [x] Run API and CLI tests.

### Task 4: Implement Deterministic Figure QC

**Files:**
- Create: `.agents/skills/scientific-visualization/scripts/figure_qc.py`
- Test: `tests/test_qc_api.py`, `tests/test_qc_integration.py`

**Interfaces:**
- Produces: `effective_dpi`, `orientation_for_dimensions`, `run_qc`, Markdown/JSON reports, strict nonzero exit on failures.

- [x] Write failing public API tests.
- [x] Add 600-DPI pass, 300-DPI fail, SVG anti-slop, PDF page/font, manifest, provenance, and required-file tests.
- [x] Implement dependency-light inspectors with explicit unsupported-check warnings.
- [x] Run all QC tests and CLI smoke tests.

### Task 5: Add Portable Installation and Repository Governance

**Files:**
- Create: `scripts/install.py`, `README.md`, `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `AGENTS.md`, `CLAUDE.md`, `pyproject.toml`
- Test: `tests/test_install.py`

**Interfaces:**
- Produces: project/user installation for Claude, Codex, or both; documented open-source contribution path.

- [x] Write installer tests before implementation.
- [x] Implement copy-based idempotent installer with overwrite protection.
- [x] Add documentation and governance files.
- [x] Run installer tests.

### Task 6: Build and Inspect a Real Demonstration Package

**Files:**
- Create: `examples/calibration-figure/*`
- Test: `tests/test_demo.py`

**Interfaces:**
- Produces: reproducible vector PDF/SVG, 600-DPI PNG/TIFF, manifest, caption, alt text, and QA reports.

- [x] Write a demo acceptance test.
- [x] Generate a scientifically meaningful synthetic calibration example with an explicit synthetic-data label.
- [x] Run strict QC and verify a deliberately 300-DPI fixture fails.
- [x] Render the PDF to PNG and visually inspect for clipping, overlap, and broken glyphs.

### Task 7: Add Behavior Evals, CI, and Package Validation

**Files:**
- Create: `evals/skill-evals.jsonl`, `evals/README.md`, `.github/workflows/test.yml`
- Modify: `.agents/skills/scientific-visualization/agents/openai.yaml`

**Interfaces:**
- Produces: pressure scenarios for missing data, decorative pressure, metadata-only DPI, journal conflict, and orientation invariance.

- [x] Add eval cases with explicit expected/forbidden behavior.
- [x] Add CI for tests, skill validation, and package smoke checks.
- [x] Run quick validator and fix every issue.

### Task 8: Package and Verify Deliverables

**Files:**
- Create: `dist/skill.zip`, `dist/scientific-visualization-skills-repo.zip`, `dist/SHA256SUMS.txt`

**Interfaces:**
- Produces: exact upload bundle and full repository archive.

- [x] Run the official skill packager.
- [x] Verify archive paths, hashes, and size limit.
- [x] Run a clean extraction smoke test.
- [x] Report deterministic test results and note that live Claude/Codex agent evals require those runtimes.
