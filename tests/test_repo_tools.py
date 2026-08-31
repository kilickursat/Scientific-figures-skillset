import importlib.util
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_skill.py"
PACKAGER = ROOT / "scripts" / "package.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_local_skill_validator_accepts_canonical_skill():
    module = load(VALIDATOR, "validate_skill_local")
    result = module.validate_skill(ROOT / ".agents" / "skills" / "scientific-visualization")
    assert result["errors"] == [], result


def test_packager_creates_single_skill_zip(tmp_path):
    module = load(PACKAGER, "package_skill_local")
    output = module.package_skill(
        ROOT / ".agents" / "skills" / "scientific-visualization",
        tmp_path / "skill.zip",
    )
    assert output.name == "skill.zip"
    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
    assert "scientific-visualization/SKILL.md" in names
    assert not any(name.startswith("examples/") for name in names)
