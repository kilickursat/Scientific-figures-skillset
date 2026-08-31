#!/usr/bin/env python3
"""Dependency-light validation for the canonical scientific-visualization skill."""
from __future__ import annotations

import argparse
import json
import py_compile
import re
from pathlib import Path
from typing import Any

MAX_SKILL_BYTES = 25 * 1024 * 1024
REQUIRED = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/scientific-integrity.md",
    "references/journal-profiles.md",
    "references/visual-design-system.md",
    "references/qa-rubric.md",
    "assets/journal_profiles.json",
    "assets/palettes.json",
    "assets/figure_request.schema.json",
    "assets/figure_manifest.schema.json",
    "scripts/figure_qc.py",
    "scripts/scaffold_figure.py",
    "scripts/finalize_manifest.py",
]


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not terminated")
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, body


def validate_skill(skill_dir: Path | str) -> dict[str, Any]:
    root = Path(skill_dir).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    checked: list[str] = []

    if not root.is_dir():
        return {"valid": False, "errors": [f"skill directory not found: {root}"], "warnings": [], "checked": []}

    for relative in REQUIRED:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")
        else:
            checked.append(relative)

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        text = skill_path.read_text(encoding="utf-8")
        try:
            frontmatter, body = _parse_frontmatter(text)
        except ValueError as exc:
            errors.append(str(exc))
            frontmatter, body = {}, ""
        allowed_keys = {"name", "description"}
        extra = set(frontmatter) - allowed_keys
        if extra:
            errors.append(f"frontmatter contains unsupported keys: {sorted(extra)}")
        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        if name != root.name:
            errors.append(f"frontmatter name `{name}` must match directory `{root.name}`")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append("skill name must use lowercase letters, digits, and single hyphens")
        if not description.startswith("Use when "):
            errors.append("description must start with `Use when `")
        if len(description) < 80:
            warnings.append("description may be too short for reliable discovery")
        if len(text.splitlines()) >= 500:
            errors.append("SKILL.md must remain below 500 lines")
        required_phrases = [
            "600 DPI",
            "vector",
            "Do not invent",
            "generative AI",
            "portrait",
            "landscape",
            "scientific question",
            "provenance",
            "manual QA",
        ]
        lowered = text.lower()
        for phrase in required_phrases:
            if phrase.lower() not in lowered:
                errors.append(f"SKILL.md is missing required contract phrase: {phrase}")
        for reference in re.findall(r"`((?:references|assets|scripts)/[^`]+)`", text):
            candidate = root / reference
            if not candidate.exists():
                errors.append(f"SKILL.md references a missing resource: {reference}")
        if re.search(r"\b(TODO|TBD|PLACEHOLDER)\b", body, flags=re.IGNORECASE):
            errors.append("SKILL.md contains an unresolved placeholder")

    for path in sorted((root / "assets").glob("*.json")) if (root / "assets").exists() else []:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid JSON in {path.relative_to(root)}: {exc}")
        else:
            checked.append(str(path.relative_to(root)))

    for path in sorted((root / "scripts").glob("*.py")) if (root / "scripts").exists() else []:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"Python compile failure in {path.relative_to(root)}: {exc.msg}")
        else:
            checked.append(str(path.relative_to(root)))

    total_bytes = 0
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"symlinks are not allowed in the upload skill: {path.relative_to(root)}")
        elif path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            total_bytes += path.stat().st_size
    if total_bytes > MAX_SKILL_BYTES:
        errors.append(f"skill is {total_bytes} bytes; maximum is {MAX_SKILL_BYTES}")

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "checked": sorted(set(checked)),
        "bytes": total_bytes,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skill_dir",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / ".agents" / "skills" / "scientific-visualization",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    result = validate_skill(args.skill_dir)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("PASS" if result["valid"] else "FAIL")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
        print(f"Checked {len(result['checked'])} resources; {result.get('bytes', 0)} bytes")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
