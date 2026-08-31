# Automated Scientific Figure QC

**Status:** PASS
**Manifest:** `/mnt/data/scientific-visualization-skills/examples/calibration-figure-portrait/figure_manifest.json`
**Errors:** 0  
**Warnings:** 0  
**Information:** 15

## Findings

| Level | Code | File | Finding |
|---|---|---|---|
| INFO | `manifest.orientation` | `` | Orientation `portrait` matches physical dimensions. |
| INFO | `caption.present` | `/mnt/data/scientific-visualization-skills/examples/calibration-figure-portrait/caption.md` | caption_file is present and non-empty. |
| INFO | `alt-text.present` | `/mnt/data/scientific-visualization-skills/examples/calibration-figure-portrait/alt-text.md` | alt_text_file is present and non-empty. |
| INFO | `manual-qa.approved` | `/mnt/data/scientific-visualization-skills/examples/calibration-figure-portrait/qa/MANUAL_QA.md` | Manual QA is marked as passed and contains no unchecked boxes. |
| INFO | `source.hash` | `src/plot.py` | Source SHA-256 matches the manifest. |
| INFO | `source.hash` | `figure_request.json` | Source SHA-256 matches the manifest. |
| INFO | `output.hash` | `output/FigDemo_Calibration_portrait.pdf` | Output SHA-256 matches the manifest. |
| INFO | `pdf.page-size` | `/mnt/data/scientific-visualization-skills/examples/calibration-figure-portrait/output/FigDemo_Calibration_portrait.pdf` | PDF page size matches the manifest within 1 mm. |
| INFO | `pdf.fonts-embedded` | `/mnt/data/scientific-visualization-skills/examples/calibration-figure-portrait/output/FigDemo_Calibration_portrait.pdf` | Detected 2 embedded font resource(s). |
| INFO | `output.hash` | `output/FigDemo_Calibration_portrait.svg` | Output SHA-256 matches the manifest. |
| INFO | `svg.physical-size` | `/mnt/data/scientific-visualization-skills/examples/calibration-figure-portrait/output/FigDemo_Calibration_portrait.svg` | SVG physical size matches the manifest within 1 mm. |
| INFO | `output.hash` | `output/FigDemo_Calibration_portrait_600dpi.png` | Output SHA-256 matches the manifest. |
| INFO | `raster.effective-dpi` | `/mnt/data/scientific-visualization-skills/examples/calibration-figure-portrait/output/FigDemo_Calibration_portrait_600dpi.png` | Effective raster resolution passes at 599.9 DPI. |
| INFO | `output.hash` | `output/FigDemo_Calibration_portrait_600dpi.tiff` | Output SHA-256 matches the manifest. |
| INFO | `raster.effective-dpi` | `/mnt/data/scientific-visualization-skills/examples/calibration-figure-portrait/output/FigDemo_Calibration_portrait_600dpi.tiff` | Effective raster resolution passes at 599.9 DPI. |

## Limitations

- Automated QC cannot determine whether the scientific question is appropriate or the statistics are honest.
- Automated QC cannot reliably detect label overlap, visual crowding, color-vision failures, or metadata-preserving upsampling; manual rendered-output review is mandatory.
- Publisher profiles are starting points; exact target-journal instructions must be checked before submission.
