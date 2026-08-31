import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QC_PATH = ROOT / ".agents" / "skills" / "scientific-visualization" / "scripts" / "figure_qc.py"
DEMO = ROOT / "examples" / "calibration-figure"


def load_qc():
    spec = importlib.util.spec_from_file_location("figure_qc_demo", QC_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_demo_package_exists_and_passes_strict_qc():
    required = [
        DEMO / "figure_request.json",
        DEMO / "figure_manifest.json",
        DEMO / "src" / "plot.py",
        DEMO / "output" / "FigDemo_Calibration_landscape.pdf",
        DEMO / "output" / "FigDemo_Calibration_landscape.svg",
        DEMO / "output" / "FigDemo_Calibration_landscape_600dpi.png",
        DEMO / "output" / "FigDemo_Calibration_landscape_600dpi.tiff",
        DEMO / "qa" / "MANUAL_QA.md",
    ]
    assert not [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    report = load_qc().run_qc(DEMO)
    assert report["passed"], [f for f in report["findings"] if f["level"] == "error"]
    assert report["counts"]["warning"] == 0, report["findings"]


def test_portrait_demo_package_exists_and_passes_strict_qc():
    portrait = ROOT / "examples" / "calibration-figure-portrait"
    required = [
        portrait / "figure_manifest.json",
        portrait / "output" / "FigDemo_Calibration_portrait.pdf",
        portrait / "output" / "FigDemo_Calibration_portrait.svg",
        portrait / "output" / "FigDemo_Calibration_portrait_600dpi.png",
        portrait / "output" / "FigDemo_Calibration_portrait_600dpi.tiff",
    ]
    assert not [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    report = load_qc().run_qc(portrait)
    assert report["passed"], [f for f in report["findings"] if f["level"] == "error"]
    assert report["counts"]["warning"] == 0, report["findings"]
