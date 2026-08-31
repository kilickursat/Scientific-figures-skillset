#!/usr/bin/env python3
"""Integrity-first Matplotlib template for a two-panel relationship figure.

The script never invents data during normal use. Supply a CSV with columns
``observed`` and ``predicted``. The optional ``--demo`` flag creates a clearly
labelled synthetic dataset solely to test the rendering pipeline.
"""
from __future__ import annotations

import argparse
import csv
import math
import re
from pathlib import Path
from typing import Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

FIGURE_ID = "FigDemo_Calibration"
WIDTH_MM = 89
HEIGHT_MM = 160
ORIENTATION = "portrait"
ARCHIVE_DPI = 600


def mm_to_inch(value_mm: float) -> float:
    return value_mm / 25.4


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
            "font.size": 7,
            "axes.labelsize": 7,
            "axes.titlesize": 8,
            "xtick.labelsize": 6.5,
            "ytick.labelsize": 6.5,
            "legend.fontsize": 6.5,
            "axes.linewidth": 0.6,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "xtick.major.size": 3,
            "ytick.major.size": 3,
            "lines.linewidth": 1.0,
            "lines.markersize": 3.5,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "savefig.facecolor": "white",
            "savefig.edgecolor": "white",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def read_csv(path: Path) -> tuple[np.ndarray, np.ndarray]:
    observed: list[float] = []
    predicted: list[float] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        required = {"observed", "predicted"}
        if not required <= fields:
            raise ValueError(f"CSV must contain columns {sorted(required)}; found {sorted(fields)}")
        for row_number, row in enumerate(reader, start=2):
            try:
                observed.append(float(row["observed"]))
                predicted.append(float(row["predicted"]))
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Non-numeric value at CSV row {row_number}") from exc
    if len(observed) < 3:
        raise ValueError("At least three paired observations are required")
    return np.asarray(observed), np.asarray(predicted)


def synthetic_demo() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(20260831)
    observed = np.linspace(0.5, 10.5, 48)
    predicted = observed * 0.94 + 0.32 + rng.normal(0.0, 0.62, observed.size)
    return observed, predicted


def robust_limits(*arrays: Iterable[float]) -> tuple[float, float]:
    values = np.concatenate([np.asarray(a, dtype=float) for a in arrays])
    lo = float(np.nanmin(values))
    hi = float(np.nanmax(values))
    pad = max((hi - lo) * 0.06, 0.1)
    return lo - pad, hi + pad


def build_figure(observed: np.ndarray, predicted: np.ndarray, synthetic: bool) -> plt.Figure:
    configure_matplotlib()
    figsize = (mm_to_inch(WIDTH_MM), mm_to_inch(HEIGHT_MM))
    if ORIENTATION == "portrait":
        fig, axes = plt.subplots(2, 1, figsize=figsize)
        fig.subplots_adjust(left=0.16, right=0.96, bottom=0.09, top=0.96, hspace=0.34)
    else:
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        fig.subplots_adjust(left=0.075, right=0.985, bottom=0.145, top=0.93, wspace=0.27)

    ax_a, ax_b = np.ravel(axes)
    point_color = "#0072B2"
    model_color = "#D55E00"
    neutral = "#5F6368"

    limits = robust_limits(observed, predicted)
    ax_a.scatter(
        observed,
        predicted,
        s=17,
        facecolors="white",
        edgecolors=point_color,
        linewidths=0.8,
        label=f"Paired observations (n={observed.size})",
        zorder=3,
    )
    ax_a.plot(limits, limits, color=neutral, linestyle=(0, (3, 2)), linewidth=0.9, label="1:1 reference")
    slope, intercept = np.polyfit(observed, predicted, deg=1)
    x_line = np.linspace(*limits, 100)
    ax_a.plot(x_line, slope * x_line + intercept, color=model_color, linewidth=1.2, label="Least-squares fit")
    ax_a.set(xlim=limits, ylim=limits, xlabel="Observed value (unit)", ylabel="Predicted value (unit)")
    ax_a.set_aspect("equal", adjustable="box")
    ax_a.legend(frameon=False, loc="upper left", handlelength=2.2)

    residual = predicted - observed
    ax_b.scatter(
        observed,
        residual,
        s=17,
        facecolors="white",
        edgecolors=point_color,
        linewidths=0.8,
        zorder=3,
    )
    ax_b.axhline(0.0, color=neutral, linestyle=(0, (3, 2)), linewidth=0.9)
    rmse = math.sqrt(float(np.mean(np.square(residual))))
    bias = float(np.mean(residual))
    ax_b.set(xlabel="Observed value (unit)", ylabel="Residual, predicted - observed (unit)")
    ax_b.text(
        0.03,
        0.97,
        f"RMSE = {rmse:.2f}\nBias = {bias:.2f}",
        transform=ax_b.transAxes,
        ha="left",
        va="top",
    )

    for label, ax in zip(("a", "b"), (ax_a, ax_b), strict=True):
        ax.text(-0.12, 1.04, label, transform=ax.transAxes, fontsize=8, fontweight="bold", va="bottom")
        ax.grid(False)

    if synthetic:
        fig.text(
            0.5,
            0.025,
            "SYNTHETIC DEMONSTRATION - NOT SCIENTIFIC EVIDENCE",
            ha="center",
            va="bottom",
            fontsize=6,
            fontweight="bold",
        )
    return fig


def set_svg_physical_size(path: Path) -> None:
    """Declare the intended physical canvas in millimetres without rasterizing text."""
    text = path.read_text(encoding="utf-8")
    text, width_count = re.subn(
        r'(<svg\b[^>]*\bwidth=")[^"]+("[^>]*>)',
        lambda match: f'{match.group(1)}{WIDTH_MM:g}mm{match.group(2)}',
        text,
        count=1,
    )
    text, height_count = re.subn(
        r'(<svg\b[^>]*\bheight=")[^"]+("[^>]*>)',
        lambda match: f'{match.group(1)}{HEIGHT_MM:g}mm{match.group(2)}',
        text,
        count=1,
    )
    if width_count != 1 or height_count != 1:
        raise RuntimeError("Could not set SVG physical dimensions")
    path.write_text(text, encoding="utf-8")


def export_figure(fig: plt.Figure, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{FIGURE_ID}_{ORIENTATION}"
    fig.savefig(output_dir / f"{stem}.pdf", bbox_inches=None)
    svg_path = output_dir / f"{stem}.svg"
    fig.savefig(svg_path, bbox_inches=None)
    set_svg_physical_size(svg_path)
    fig.savefig(output_dir / f"{stem}_600dpi.png", dpi=ARCHIVE_DPI, bbox_inches=None)
    fig.savefig(
        output_dir / f"{stem}_600dpi.tiff",
        dpi=ARCHIVE_DPI,
        bbox_inches=None,
        pil_kwargs={"compression": "tiff_lzw"},
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, help="CSV with observed,predicted columns")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "output")
    parser.add_argument("--demo", action="store_true", help="Render a clearly labelled synthetic pipeline test")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.demo:
        observed, predicted = synthetic_demo()
    elif args.data is not None:
        observed, predicted = read_csv(args.data)
    else:
        raise SystemExit("Provide --data. Use --demo only for a labelled synthetic rendering test.")
    fig = build_figure(observed, predicted, synthetic=args.demo)
    export_figure(fig, args.output)
    plt.close(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
