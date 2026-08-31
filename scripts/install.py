#!/usr/bin/env python3
"""Install the canonical scientific-visualization skill for Codex and/or Claude."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / ".agents" / "skills" / "scientific-visualization"
TARGETS = {"codex", "claude", "both"}
SCOPES = {"project", "user"}


def _destinations(*, project: Path | None, target: str, scope: str, home: Path | None = None) -> list[Path]:
    target = target.lower()
    scope = scope.lower()
    if target not in TARGETS:
        raise ValueError(f"target must be one of {sorted(TARGETS)}")
    if scope not in SCOPES:
        raise ValueError(f"scope must be one of {sorted(SCOPES)}")

    clients = ["codex", "claude"] if target == "both" else [target]
    if scope == "project":
        if project is None:
            raise ValueError("project path is required for project-scope installation")
        base = Path(project).expanduser().resolve()
        mappings = {
            "codex": base / ".agents" / "skills" / "scientific-visualization",
            "claude": base / ".claude" / "skills" / "scientific-visualization",
        }
    else:
        base = Path(home or Path.home()).expanduser().resolve()
        mappings = {
            "codex": base / ".agents" / "skills" / "scientific-visualization",
            "claude": base / ".claude" / "skills" / "scientific-visualization",
        }
    return [mappings[client] for client in clients]


def install_skill(
    *,
    project: Path | str | None = None,
    target: str = "both",
    scope: str = "project",
    force: bool = False,
    source: Path | str = DEFAULT_SOURCE,
    home: Path | str | None = None,
) -> list[Path]:
    """Copy the canonical skill and return installed `SKILL.md` paths.

    All destinations are preflighted before any copy occurs, preventing a
    partial `both` installation. Existing destinations are never overwritten
    unless `force=True`.
    """
    source_path = Path(source).expanduser().resolve()
    if not (source_path / "SKILL.md").is_file():
        raise FileNotFoundError(f"canonical skill not found: {source_path}")

    project_path = Path(project) if project is not None else None
    home_path = Path(home) if home is not None else None
    destinations = _destinations(project=project_path, target=target, scope=scope, home=home_path)

    for destination in destinations:
        if destination.exists() and not force:
            raise FileExistsError(f"refusing to overwrite existing skill without --force: {destination}")
        try:
            destination.resolve().relative_to(source_path)
        except ValueError:
            pass
        else:
            raise ValueError(f"destination cannot be inside canonical source: {destination}")

    installed: list[Path] = []
    for destination in destinations:
        if destination.exists():
            shutil.rmtree(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_path, destination)
        installed.append(destination / "SKILL.md")
    return installed


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="both", choices=sorted(TARGETS))
    parser.add_argument("--scope", default="project", choices=sorted(SCOPES))
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Project root for project scope")
    parser.add_argument("--home", type=Path, help="Override home directory for user scope (mainly for testing)")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Canonical skill directory")
    parser.add_argument("--force", action="store_true", help="Replace existing installed copies")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    installed = install_skill(
        project=args.project,
        target=args.target,
        scope=args.scope,
        force=args.force,
        source=args.source,
        home=args.home,
    )
    for skill_file in installed:
        print(skill_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
