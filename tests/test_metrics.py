from pathlib import Path

import pytest

from letter_metter import EYE_SENSE, QWERTY_ES, Layout, compare, path_distance

TEXTS = Path(__file__).resolve().parent.parent / "texts"

# Two tiny layouts with the same letters, handy for exact arithmetic.
TRIANGLE = Layout("triangle", {"a": (0, 0), "b": (3, 0), "c": (3, 4)})
TRIANGLE_X2 = Layout("triangle x2", {"a": (0, 0), "b": (6, 0), "c": (6, 8)})


class TestPathDistance:
    def test_adjacent_qwerty_keys_are_10_mm_apart(self):
        assert path_distance("qw", QWERTY_ES) == pytest.approx(10)

    def test_pythagoras(self):
        assert path_distance("ac", TRIANGLE) == pytest.approx(5)

    def test_accumulates_consecutive_segments(self):
        assert path_distance("abca", TRIANGLE) == pytest.approx(3 + 4 + 5)

    def test_scale_multiplies_distance(self):
        assert path_distance("abc", TRIANGLE, scale=1.5) == pytest.approx(7 * 1.5)

    def test_repeated_letter_is_zero(self):
        assert path_distance("aaaa", TRIANGLE) == 0

    @pytest.mark.parametrize("keys", ["", "a"])
    def test_fewer_than_two_keys_is_zero(self, keys):
        assert path_distance(keys, TRIANGLE) == 0

    def test_unknown_characters_are_ignored(self):
        assert path_distance("a? 1c", TRIANGLE) == pytest.approx(5)


class TestCompare:
    def test_kpm_scales_with_distance_ratio(self):
        result = compare("abcabc", kpm=15, eye_layout=TRIANGLE, baseline_layout=TRIANGLE_X2)
        assert result.keystrokes == 6
        assert result.distance_baseline_mm == pytest.approx(2 * result.distance_eye_mm)
        assert result.kpm_eye == pytest.approx(30)
        assert result.time_baseline_s == pytest.approx(6 / 15 * 60)
        assert result.time_eye_s == pytest.approx(result.time_baseline_s / 2)
        assert result.saved_time_s == pytest.approx(result.time_baseline_s / 2)
        assert result.saved_distance_pct == pytest.approx(50)

    def test_kpm_formula_on_real_layouts(self):
        result = compare("el ingenioso hidalgo", kpm=15)
        expected = 15 * result.distance_baseline_mm / result.distance_eye_mm
        assert result.kpm_eye == pytest.approx(expected)
        assert result.keystrokes / result.kpm_eye * 60 == pytest.approx(result.time_eye_s)

    def test_eye_layout_longer_gives_negative_savings(self):
        result = compare("abc", kpm=10, eye_layout=TRIANGLE_X2, baseline_layout=TRIANGLE)
        assert result.saved_distance_mm < 0
        assert result.saved_time_s < 0
        assert result.kpm_eye == pytest.approx(5)

    def test_scale_is_applied_per_layout(self):
        result = compare(
            "abc", kpm=10, eye_layout=TRIANGLE, baseline_layout=TRIANGLE, eye_scale=0.5
        )
        assert result.distance_eye_mm == pytest.approx(result.distance_baseline_mm / 2)

    @pytest.mark.parametrize("kpm", [0, -5])
    def test_rejects_non_positive_kpm(self, kpm):
        with pytest.raises(ValueError, match="KPM"):
            compare("hola", kpm=kpm)

    @pytest.mark.parametrize("scales", [{"eye_scale": 0}, {"baseline_scale": -1}])
    def test_rejects_non_positive_scale(self, scales):
        with pytest.raises(ValueError, match="Scale"):
            compare("hola", kpm=15, **scales)

    @pytest.mark.parametrize("text", ["", "a", "1234 !?"])
    def test_rejects_text_without_two_letters(self, text):
        with pytest.raises(ValueError, match="Not enough"):
            compare(text, kpm=15)

    def test_rejects_text_without_movement(self):
        with pytest.raises(ValueError, match="no movement"):
            compare("aaaa", kpm=15)

    def test_rejects_layouts_with_different_letters(self):
        with pytest.raises(ValueError, match="same letters"):
            compare("ab", kpm=15, eye_layout=TRIANGLE, baseline_layout=QWERTY_ES)


def test_regression_don_quijote():
    """Pin the full-novel figures so refactors cannot silently change the results."""
    text = (TEXTS / "don_quijote.txt").read_text(encoding="utf-8")
    result = compare(text, kpm=15, eye_layout=EYE_SENSE, baseline_layout=QWERTY_ES)
    # If you deliberately change the reference text or a layout, re-run the analysis and
    # update these numbers. Any other change that breaks this test is a real regression.
    assert result.keystrokes == 776_819
    assert result.distance_eye_mm == pytest.approx(13_320_256.11, abs=0.01)
    assert result.distance_baseline_mm == pytest.approx(28_414_649.12, abs=0.01)
