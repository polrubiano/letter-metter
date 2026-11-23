"""Keyboard layouts expressed as key-centre coordinates in millimetres.

Conventions:
    * Every key fits in a 10 x 10 mm bounding box.
    * The origin (0, 0) is the top-left corner of the keyboard; Y grows downwards.
    * Coordinates are the centre of each key.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

Point = tuple[float, float]


@dataclass(frozen=True)
class Layout:
    """A named keyboard layout mapping each letter to its key-centre (x, y) in mm."""

    name: str
    keys: Mapping[str, Point] = field(repr=False)

    def __post_init__(self) -> None:
        # Freeze the mapping so a shared layout cannot be mutated by accident.
        object.__setattr__(self, "keys", MappingProxyType(dict(self.keys)))

    @property
    def letters(self) -> frozenset[str]:
        """The set of characters this layout can type."""
        return frozenset(self.keys)

    def __contains__(self, char: object) -> bool:
        return char in self.keys

    def __getitem__(self, char: str) -> Point:
        return self.keys[char]


# Hexagonal Eye Sense Keyboard layout (Compose rewrite, Spanish preset).
# Space (two merged hexagons at the right-hand end of the bottom row)
# is not a letter, so it isn't listed.
EYE_SENSE_KEYBOARD = Layout(
    name="Eye Sense Keyboard",
    keys={
        "x": (15, 5.77), "b": (25, 5.77), "g": (35, 5.77), "v": (45, 5.77), "k": (55, 5.77),
        "ñ": (10, 14.43), "p": (20, 14.43), "n": (30, 14.43), "i": (40, 14.43), "y": (50, 14.43), "w": (60, 14.43),
        "j": (5, 23.09), "m": (15, 23.09), "r": (25, 23.09), "e": (35, 23.09), "a": (45, 23.09), "d": (55, 23.09), "q": (65, 23.09),
        "z": (10, 31.75), "u": (20, 31.75), "s": (30, 31.75), "o": (40, 31.75), "l": (50, 31.75), "h": (60, 31.75),
        "f": (15, 40.41), "t": (25, 40.41), "c": (35, 40.41),
    },
)  # fmt: skip

# Original hexagonal Eye Sense layout, kept to reproduce earlier results. Its key
# centres are 9.8 mm apart horizontally and 8.5 mm vertically because the 10 mm box
# was fitted to the hexagon's sharp vertices instead of its rounded edge, so the keys
# are slightly narrower than 10 mm (see the erratum in the README). EYE_SENSE_KEYBOARD
# uses the corrected geometry.
EYE_SENSE = Layout(
    name="Eye Sense",
    keys={
        "f": (9.6, 5), "m": (19.4, 5), "t": (29.2, 5), "b": (39, 5), "q": (48.8, 5),
        "z": (4.7, 13.5), "i": (14.5, 13.5), "d": (24.3, 13.5), "s": (34.1, 13.5), "u": (43.9, 13.5), "j": (53.7, 13.5), "w": (63.6, 13.5),
        "l": (9.6, 22), "a": (19.4, 22), "e": (29.2, 22), "o": (39, 22), "g": (48.8, 22), "x": (58.7, 22),
        "h": (4.7, 30.5), "c": (14.5, 30.5), "r": (24.3, 30.5), "n": (34.1, 30.5), "p": (43.9, 30.5), "y": (53.7, 30.5), "k": (63.6, 30.5),
        "v": (9.6, 39), "ñ": (58.7, 39),
    },
)  # fmt: skip

# Spanish QWERTY with the real row stagger (0, 3 and 8 mm offsets).
QWERTY_ES = Layout(
    name="QWERTY",
    keys={
        "q": (5, 5), "w": (15, 5), "e": (25, 5), "r": (35, 5), "t": (45, 5),
        "y": (55, 5), "u": (65, 5), "i": (75, 5), "o": (85, 5), "p": (95, 5),
        "a": (8, 15), "s": (18, 15), "d": (28, 15), "f": (38, 15), "g": (48, 15),
        "h": (58, 15), "j": (68, 15), "k": (78, 15), "l": (88, 15), "ñ": (98, 15),
        "z": (13, 25), "x": (23, 25), "c": (33, 25), "v": (43, 25), "b": (53, 25),
        "n": (63, 25), "m": (73, 25),
    },
)  # fmt: skip

# Layouts that can be compared against the QWERTY baseline from the CLI (``--layout``).
# Keys are the command-line names; add new layouts here to make them selectable.
LAYOUTS: Mapping[str, Layout] = MappingProxyType(
    {
        "eye-sense": EYE_SENSE,
        "eye-sense-keyboard": EYE_SENSE_KEYBOARD,
    }
)
DEFAULT_LAYOUT = "eye-sense-keyboard"
