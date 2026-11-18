"""Command-line interface: ``letter-metter TEXT_FILE --kpm 15``."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

from letter_metter import __version__
from letter_metter.formatting import format_distance, format_time
from letter_metter.metrics import ComparisonResult, compare

SEPARATOR = "-" * 45


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="letter-metter",
        description="Compare the eye travel needed to type a text on QWERTY and on Eye Sense.",
    )
    parser.add_argument("text_file", type=Path, help="UTF-8 text file to analyse")
    parser.add_argument(
        "--kpm",
        type=float,
        default=15.0,
        help="user's current keystrokes per minute on QWERTY (default: 15, i.e. 4 s per key)",
    )
    parser.add_argument(
        "--eye-scale",
        type=float,
        default=1.0,
        help="size multiplier of the Eye Sense prototype (default: 1.0 = 10 mm keys)",
    )
    parser.add_argument(
        "--qwerty-scale",
        type=float,
        default=1.0,
        help="size multiplier of the QWERTY keyboard (default: 1.0 = 10 mm keys)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def print_report(result: ComparisonResult, source: str, out: TextIO | None = None) -> None:
    """Print a plain-text report of ``result`` to ``out`` (default: current ``sys.stdout``)."""
    out = out or sys.stdout

    def line(text: str = "") -> None:
        print(text, file=out)

    base, eye = result.baseline_name, result.eye_name
    width = max(len(base), len(eye)) + len("Distance ") + 2

    line(f"File processed: {source}")
    line(f"Valid keystrokes: {result.keystrokes}")
    line(f"Scale applied -> {eye}: {result.scale_eye:g}x | {base}: {result.scale_baseline:g}x")
    line()
    line(SEPARATOR)
    line(f"{'Distance ' + base + ':':<{width}}{format_distance(result.distance_baseline_mm)}")
    line(f"{'Distance ' + eye + ':':<{width}}{format_distance(result.distance_eye_mm)}")
    line(SEPARATOR)

    saved = result.saved_distance_mm
    if saved > 0:
        line(
            f"Saved distance: {format_distance(saved)} "
            f"({result.saved_distance_pct:.1f}% less movement)"
        )
    elif saved < 0:
        line(
            f"{eye} requires {format_distance(-saved)} more distance "
            f"({-result.saved_distance_pct:.1f}% more movement)"
        )
    else:
        line("Both keyboards require exactly the same distance.")
    line()

    t_base, t_eye = result.time_baseline_s, result.time_eye_s
    n = result.keystrokes
    width = max(len(base), len(eye)) + len("Time on ") + 2
    line(
        f"{'Time on ' + base + ':':<{width}}{format_time(t_base):<15} -> "
        f"Baseline of {result.kpm_baseline:.1f} KPM ({t_base / n:.1f} sec/keystroke)"
    )
    line(
        f"{'Time on ' + eye + ':':<{width}}{format_time(t_eye):<15} -> "
        f"Extrapolated to {result.kpm_eye:.1f} KPM ({t_eye / n:.1f} sec/keystroke)"
    )
    label = "Total time saved:" if result.saved_time_s >= 0 else "Extra time needed:"
    line(f"{label:<{width}}{format_time(abs(result.saved_time_s))}")


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point. Returns the process exit code."""
    args = build_parser().parse_args(argv)

    try:
        text = args.text_file.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"Error: file not found: '{args.text_file}'.", file=sys.stderr)
        return 1
    except (OSError, UnicodeDecodeError) as exc:
        print(f"Error: cannot read '{args.text_file}': {exc}", file=sys.stderr)
        return 1

    try:
        result = compare(
            text,
            kpm=args.kpm,
            eye_scale=args.eye_scale,
            baseline_scale=args.qwerty_scale,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print_report(result, source=str(args.text_file))
    return 0
