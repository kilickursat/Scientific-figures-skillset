#!/usr/bin/env python3
"""Validate and package one Agent Skill as an exact `skill.zip` upload bundle."""
from __future__ import annotations

import argparse
import importlib.util
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILL = REPO_ROOT / ".agents" / "skills" / "scientific-visualization"
VALIDATOR_PATH = Path(__file__).resolve().with_name("validate_skill.py")
EXCLUDED_PARTS = {"__pycache__", ".pytest_cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def _load_validator():
    spec = importlib.util.spec_from_file_location("local_skill_validator", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def package_skill(skill_dir: Path | str, output: Path | str) -> Path:
    skill = Path(skill_dir).expanduser().resolve()
    output_path = Path(output).expanduser().resolve()
    if output_path.is_dir() or output_path.suffix.lower() != ".zip":
        output_path = output_path / "skill.zip"
    elif output_path.name != "skill.zip":
        output_path = output_path.with_name("skill.zip")

    result = _load_validator().validate_skill(skill)
    if result["errors"]:
        formatted = "\n".join(f"- {error}" for error in result["errors"])
        raise ValueError(f"skill validation failed:\n{formatted}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(skill.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(skill)
            if any(part in EXCLUDED_PARTS for part in relative.parts) or path.suffix in EXCLUDED_SUFFIXES:
                continue
            archive.write(path, arcname=str(Path(skill.name) / relative))
    return output_path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", nargs="?", type=Path, default=DEFAULT_SKILL)
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "dist" / "skill.zip")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    output = package_skill(args.skill_dir, args.output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
