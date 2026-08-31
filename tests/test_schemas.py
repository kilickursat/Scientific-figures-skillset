import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / ".agents" / "skills" / "scientific-visualization" / "assets"


def test_request_and_manifest_schemas_accept_complete_examples():
    request_schema = json.loads((ASSETS / "figure_request.schema.json").read_text(encoding="utf-8"))
    manifest_schema = json.loads((ASSETS / "figure_manifest.schema.json").read_text(encoding="utf-8"))

    request = {
        "schema_version": "1.0.0",
        "figure_id": "Fig1",
        "task": "create",
        "figure_family": "quantitative-plot",
        "scientific_question": "How closely do predictions agree with measured values?",
        "target_journal": "nature",
        "target_journal_detail": "Nature",
        "submission_stage": "draft",
        "orientation": "landscape",
        "width_class": "double",
        "height_mm": 100,
        "archive_raster_dpi": 600,
        "claims_allowed": ["Agreement can be described using supplied pairs."],
        "evidence_sources": [
            {
                "path_or_uri": "data/pairs.csv",
                "role": "paired measurements",
                "provenance_class": "measured",
                "sha256": "0" * 64,
                "notes": None,
            }
        ],
        "allowed_transformations": ["panel reflow"],
        "prohibited_transformations": ["invent values"],
        "panels": [],
        "unresolved_evidence": [],
        "notes": None,
    }
    manifest = {
        "schema_version": "1.0.0",
        "figure_id": "Fig1",
        "scientific_question": request["scientific_question"],
        "synthetic_example": False,
        "target_journal": "nature",
        "target_journal_detail": "Nature",
        "journal_profile_verified_on": "2026-08-31",
        "journal_verification_status": "verified",
        "submission_stage": "draft",
        "orientation": "landscape",
        "width_class": "double",
        "width_mm": 183,
        "height_mm": 100,
        "archive_raster_dpi": 600,
        "color_space": "RGB",
        "software": [{"name": "Python", "version": "3.13"}],
        "transformations": ["none"],
        "panel_provenance": [
            {"panel_id": "a", "provenance_class": "measured", "source": "data/pairs.csv", "notes": None}
        ],
        "source_files": [{"path": "src/plot.py", "sha256": "0" * 64, "bytes": 1}],
        "outputs": [
            {
                "path": "output/Fig1.pdf",
                "format": "PDF",
                "role": "vector-master",
                "sha256": "0" * 64,
                "bytes": 1,
                "dpi": None,
                "width_px": None,
                "height_px": None,
            }
        ],
        "caption_file": "caption.md",
        "alt_text_file": "alt-text.md",
        "manual_qa_file": "qa/MANUAL_QA.md",
        "unresolved_evidence": [],
        "limitations": [],
    }

    jsonschema.Draft202012Validator(request_schema).validate(request)
    jsonschema.Draft202012Validator(manifest_schema).validate(manifest)


def test_palettes_have_accessible_semantic_and_qualitative_options():
    palettes = json.loads((ASSETS / "palettes.json").read_text(encoding="utf-8"))
    assert "okabe_ito" in palettes["palettes"]
    assert "scientific_neutral" in palettes["palettes"]
    assert palettes["rules"]["color_alone"].lower().startswith("never")
