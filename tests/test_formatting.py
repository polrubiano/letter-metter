import pytest

from letter_metter import format_distance, format_time


@pytest.mark.parametrize(
    ("mm", "expected"),
    [
        (0, "0.00 mm"),
        (999.99, "999.99 mm"),
        (1_000, "1.00 m"),
        (1_234.5, "1.23 m"),
        (999_999, "1000.00 m"),
        (1_000_000, "1.000 km"),
        (2_163_654, "2.164 km"),
        (-1_500, "-1.50 m"),
    ],
)
def test_format_distance(mm, expected):
    assert format_distance(mm) == expected


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0, "0.00 s"),
        (59.99, "59.99 s"),
        (60, "1 min 0.0 s"),
        (125.5, "2 min 5.5 s"),
        (3_599, "59 min 59.0 s"),
        (3_600, "1 h 0 min"),
        (242_892, "67 h 28 min"),
        (-90, "-1 min 30.0 s"),
        (-7_200, "-2 h 0 min"),
    ],
)
def test_format_time(seconds, expected):
    assert format_time(seconds) == expected
