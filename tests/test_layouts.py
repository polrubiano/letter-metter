import string

import pytest

from letter_metter import EYE_SENSE, QWERTY_ES, Layout

SPANISH_ALPHABET = frozenset(string.ascii_lowercase) | {"ñ"}


@pytest.mark.parametrize("layout", [EYE_SENSE, QWERTY_ES], ids=lambda layout: layout.name)
def test_layout_covers_spanish_alphabet(layout):
    assert layout.letters == SPANISH_ALPHABET


@pytest.mark.parametrize("layout", [EYE_SENSE, QWERTY_ES], ids=lambda layout: layout.name)
def test_coordinates_are_non_negative(layout):
    assert all(x >= 0 and y >= 0 for x, y in layout.keys.values())


@pytest.mark.parametrize("layout", [EYE_SENSE, QWERTY_ES], ids=lambda layout: layout.name)
def test_no_two_keys_share_a_position(layout):
    positions = list(layout.keys.values())
    assert len(positions) == len(set(positions))


def test_layout_keys_are_read_only():
    layout = Layout("tiny", {"a": (0, 0)})
    with pytest.raises(TypeError):
        layout.keys["b"] = (1, 1)
