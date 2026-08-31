import importlib.util
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / ".agents" / "skills" / "scientific-visualization" / "scripts" / "finalize_manifest.py"


def load_module():
    spec = importlib.util.spec_from_file_location("finalize_manifest", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_finalize_manifest_populates_hashes_sizes_and_raster_dimensions(tmp_path):
    module = load_module()
    (tmp_path / "src").mkdir()
    (tmp_path / "output").mkdir()
    source = tmp_path / "src" / "plot.py"
    source.write_text("print('x')\n", encoding="utf-8")
    raster = tmp_path / "output" / "figure.png"
    Image.new("RGB", (600, 300), "white").save(raster, dpi=(600, 600))
    manifest = {
        "source_files": [{"path": "src/plot.py", "sha256": None, "bytes": None}],
        "outputs": [
            {
                "path": "output/figure.png",
                "format": "PNG",
                "role": "archive-raster",
                "sha256": None,
                "bytes": None,
                "dpi": None,
                "width_px": None,
                "height_px": None,
            }
        ],
    }
    manifest_path = tmp_path / "figure_manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    updated = module.finalize_manifest(manifest_path)
    assert updated["source_files"][0]["sha256"] == module.sha256_file(source)
    assert updated["outputs"][0]["width_px"] == 600
    assert updated["outputs"][0]["height_px"] == 300
    assert round(updated["outputs"][0]["dpi"]) == 600
