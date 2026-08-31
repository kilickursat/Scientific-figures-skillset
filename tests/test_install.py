import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "install.py"


def load_module():
    spec = importlib.util.spec_from_file_location("install_skill", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_project_install_copies_same_skill_to_codex_and_claude(tmp_path):
    module = load_module()
    installed = module.install_skill(project=tmp_path, target="both", scope="project", force=False)
    assert tmp_path / ".agents" / "skills" / "scientific-visualization" / "SKILL.md" in installed
    assert tmp_path / ".claude" / "skills" / "scientific-visualization" / "SKILL.md" in installed
    for path in installed:
        assert path.is_file()


def test_installer_refuses_to_overwrite_without_force(tmp_path):
    module = load_module()
    module.install_skill(project=tmp_path, target="codex", scope="project", force=False)
    try:
        module.install_skill(project=tmp_path, target="codex", scope="project", force=False)
    except FileExistsError:
        pass
    else:
        raise AssertionError("installer overwrote an existing skill without force")
