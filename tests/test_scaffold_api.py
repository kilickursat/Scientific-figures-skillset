import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / ".agents" / "skills" / "scientific-visualization" / "scripts" / "scaffold_figure.py"


def load_module():
    spec = importlib.util.spec_from_file_location("scaffold_figure", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_scaffold_creates_reproducible_project(tmp_path):
    module = load_module()
    project = module.create_project(
        destination=tmp_path,
        name="calibration-figure",
        journal="nature",
        orientation="landscape",
        language="python",
        width_class="double",
    )
    assert (project / "data").is_dir()
    assert (project / "src" / "plot.py").is_file()
    assert (project / "output").is_dir()
    manifest = json.loads((project / "figure_manifest.json").read_text(encoding="utf-8"))
    assert manifest["target_journal"] == "nature"
    assert manifest["orientation"] == "landscape"
    assert manifest["archive_raster_dpi"] == 600
