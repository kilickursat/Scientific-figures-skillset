import importlib.util
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / ".agents" / "skills" / "scientific-visualization" / "scripts" / "figure_qc.py"


def load_module():
    spec = importlib.util.spec_from_file_location("figure_qc_integration", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_project(tmp_path: Path, *, width_px: int, height_px: int, metadata_dpi: int, svg_extra: str = "") -> Path:
    module = load_module()
    project = tmp_path / "figure"
    (project / "src").mkdir(parents=True)
    (project / "output").mkdir()
    (project / "qa").mkdir()

    (project / "src" / "plot.py").write_text("print('reproducible')\n", encoding="utf-8")
    (project / "caption.md").write_text("Measured and predicted values are compared without changing the supplied pairs.\n", encoding="utf-8")
    (project / "alt-text.md").write_text("Scatter plot of measured versus predicted values with a one-to-one reference.\n", encoding="utf-8")
    (project / "qa" / "MANUAL_QA.md").write_text(
        "# Manual QA\n\nStatus: PASS\n\n- [x] Data reconciled.\n- [x] Render inspected at final size.\n",
        encoding="utf-8",
    )

    png = project / "output" / "Fig1_landscape_600dpi.png"
    Image.new("RGB", (width_px, height_px), "white").save(png, dpi=(metadata_dpi, metadata_dpi))
    svg = project / "output" / "Fig1_landscape.svg"
    svg.write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" width="152.4mm" height="76.2mm" viewBox="0 0 3600 1800">
        {svg_extra}<text x="100" y="100">Measured value</text><path d="M 0 0 L 10 10" stroke="#000"/>
        </svg>''',
        encoding="utf-8",
    )

    manifest = {
        "schema_version": "1.0.0",
        "figure_id": "Fig1",
        "scientific_question": "How closely do supplied predictions agree with measured values?",
        "synthetic_example": False,
        "target_journal": "nature",
        "target_journal_detail": "Nature",
        "journal_profile_verified_on": "2026-08-31",
        "journal_verification_status": "verified",
        "submission_stage": "draft",
        "orientation": "landscape",
        "width_class": "custom",
        "width_mm": 152.4,
        "height_mm": 76.2,
        "archive_raster_dpi": 600,
        "color_space": "RGB",
        "software": [{"name": "test", "version": "1"}],
        "transformations": [],
        "panel_provenance": [
            {"panel_id": "a", "provenance_class": "measured", "source": "source fixture", "notes": None}
        ],
        "source_files": [
            {
                "path": "src/plot.py",
                "sha256": module.sha256_file(project / "src" / "plot.py"),
                "bytes": (project / "src" / "plot.py").stat().st_size,
            }
        ],
        "outputs": [
            {
                "path": "output/Fig1_landscape.svg",
                "format": "SVG",
                "role": "vector-master",
                "sha256": module.sha256_file(svg),
                "bytes": svg.stat().st_size,
                "dpi": None,
                "width_px": None,
                "height_px": None,
            },
            {
                "path": "output/Fig1_landscape_600dpi.png",
                "format": "PNG",
                "role": "archive-raster",
                "sha256": module.sha256_file(png),
                "bytes": png.stat().st_size,
                "dpi": 600,
                "width_px": width_px,
                "height_px": height_px,
            },
        ],
        "caption_file": "caption.md",
        "alt_text_file": "alt-text.md",
        "manual_qa_file": "qa/MANUAL_QA.md",
        "unresolved_evidence": [],
        "limitations": [],
    }
    (project / "figure_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return project


def test_native_600_dpi_project_passes(tmp_path):
    module = load_module()
    project = write_project(tmp_path, width_px=3600, height_px=1800, metadata_dpi=600)
    report = module.run_qc(project)
    assert report["passed"], [f for f in report["findings"] if f["level"] == "error"]


def test_metadata_only_600_dpi_does_not_hide_low_effective_resolution(tmp_path):
    module = load_module()
    project = write_project(tmp_path, width_px=1800, height_px=900, metadata_dpi=600)
    report = module.run_qc(project)
    assert not report["passed"]
    assert any(f["code"] == "raster.effective-dpi" and f["level"] == "error" for f in report["findings"])


def test_svg_gradients_are_flagged_as_anti_slop_failure(tmp_path):
    module = load_module()
    project = write_project(
        tmp_path,
        width_px=3600,
        height_px=1800,
        metadata_dpi=600,
        svg_extra='<defs><linearGradient id="g"><stop offset="0"/></linearGradient></defs>',
    )
    report = module.run_qc(project)
    assert not report["passed"]
    assert any(f["code"] == "svg.gradient" for f in report["findings"])


def test_tiff_dpi_metadata_is_json_serializable(tmp_path):
    import json as json_module

    module = load_module()
    tiff = tmp_path / "archive.tiff"
    Image.new("RGB", (1200, 600), "white").save(tiff, dpi=(600, 600), compression="tiff_lzw")
    findings, inspection = module.inspect_raster(tiff, 50.8, 25.4, 600, "archive-raster")
    json_module.dumps({"findings": findings, "inspection": inspection})
