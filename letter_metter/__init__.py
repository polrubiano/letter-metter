"""Letter Metter: measure the eye travel needed to type a text on different keyboard layouts."""

from letter_metter.formatting import format_distance, format_time
from letter_metter.layouts import EYE_SENSE, EYE_SENSE_KEYBOARD, LAYOUTS, QWERTY_ES, Layout
from letter_metter.metrics import ComparisonResult, compare, path_distance
from letter_metter.text import clean_text, extract_keystrokes

__version__ = "1.0.0"

__all__ = [
    "EYE_SENSE",
    "EYE_SENSE_KEYBOARD",
    "LAYOUTS",
    "QWERTY_ES",
    "ComparisonResult",
    "Layout",
    "__version__",
    "clean_text",
    "compare",
    "extract_keystrokes",
    "format_distance",
    "format_time",
    "path_distance",
]
