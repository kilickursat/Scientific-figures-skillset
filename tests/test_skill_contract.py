from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "scientific-visualization"


def test_required_skill_structure_exists():
    required = [
        SKILL / "SKILL.md",
        SKILL / "agents" / "openai.yaml",
        SKILL / "references" / "journal-profiles.md",
        SKILL / "references" / "scientific-integrity.md",
        SKILL / "references" / "qa-rubric.md",
        SKILL / "assets" / "journal_profiles.json",
        SKILL / "assets" / "palettes.json",
        SKILL / "scripts" / "figure_qc.py",
        SKILL / "scripts" / "scaffold_figure.py",
        SKILL / "scripts" / "finalize_manifest.py",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert not missing, f"missing required files: {missing}"


def test_skill_contains_non_negotiable_contract():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    required_phrases = [
        "600 dpi",
        "vector",
        "do not invent",
        "generative ai",
        "portrait",
        "landscape",
        "scientific question",
        "provenance",
        "manual qa",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text]
    assert not missing, f"missing contract phrases: {missing}"


def test_skill_is_progressively_disclosed_and_compact():
    lines = (SKILL / "SKILL.md").read_text(encoding="utf-8").splitlines()
    assert len(lines) < 500
    assert any("references/" in line for line in lines)
