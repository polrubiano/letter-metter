import unicodedata

import pytest

from letter_metter import QWERTY_ES, clean_text, extract_keystrokes


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Canción", "cancion"),
        ("ÁÉÍÓÚ", "aeiou"),
        ("pingüino", "pinguino"),
        ("España", "españa"),
        ("NIÑO", "niño"),
        ("à la française", "a la francaise"),
        ("¡Hola, mundo!", "¡hola, mundo!"),
        ("", ""),
    ],
)
def test_clean_text(raw, expected):
    assert clean_text(raw) == expected


def test_clean_text_handles_decomposed_enye():
    # "n" + combining tilde (NFD form, common in macOS file names) must still become "ñ".
    decomposed = unicodedata.normalize("NFD", "año")
    assert len(decomposed) == 4
    assert clean_text(decomposed) == "año"


def test_extract_keystrokes_keeps_order_and_drops_unknown_chars():
    assert extract_keystrokes("¡hola, año 2024!", QWERTY_ES) == list("holaaño")
