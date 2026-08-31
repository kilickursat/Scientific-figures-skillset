import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / ".agents" / "skills" / "scientific-visualization" / "scripts" / "figure_qc.py"


def load_module():
    spec = importlib.util.spec_from_file_location("figure_qc", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_effective_dpi_calculation():
    module = load_module()
    assert round(module.effective_dpi(3600, 152.4), 1) == 600.0


def test_orientation_classification():
    module = load_module()
    assert module.orientation_for_dimensions(183, 100) == "landscape"
    assert module.orientation_for_dimensions(89, 170) == "portrait"
    assert module.orientation_for_dimensions(100, 100) == "square"
