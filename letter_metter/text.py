"""Text normalisation helpers."""

from __future__ import annotations

import unicodedata

from letter_metter.layouts import Layout

# Private-use placeholder that shields "ñ" while diacritics are stripped.
_ENYE_PLACEHOLDER = ""


def clean_text(text: str) -> str:
    """Lowercase ``text`` and strip diacritics (á -> a, ü -> u, ç -> c) while keeping ``ñ``.

    Characters that are not letters (spaces, digits, punctuation) are left as they
    are; they are filtered out later by :func:`extract_keystrokes`.
    """
    # NFC first so a decomposed "n" + combining tilde is recognised as "ñ".
    text = unicodedata.normalize("NFC", text.lower()).replace("ñ", _ENYE_PLACEHOLDER)
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", stripped).replace(_ENYE_PLACEHOLDER, "ñ")


def extract_keystrokes(text: str, layout: Layout) -> list[str]:
    """Return, in order, the characters of ``text`` that exist on ``layout``."""
    return [char for char in text if char in layout]
