import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / ".agents" / "skills" / "scientific-visualization" / "assets" / "journal_profiles.json"


def test_required_journal_profiles_and_archive_contract():
    data = json.loads(PROFILES.read_text(encoding="utf-8"))
    assert data["archive_raster_dpi"] == 600
    required = {"nature", "science", "arxiv", "elsevier", "springer", "generic"}
    assert required <= set(data["profiles"])
    for name in required:
        profile = data["profiles"][name]
        assert profile["archive_raster_dpi"] == 600
        assert profile["orientations"] == ["portrait", "landscape"]
        assert profile["source_urls"]
