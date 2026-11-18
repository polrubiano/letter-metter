"""Distance and typing-speed calculations."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import pairwise

from letter_metter.layouts import EYE_SENSE, QWERTY_ES, Layout
from letter_metter.text import clean_text, extract_keystrokes


def path_distance(keystrokes: Sequence[str], layout: Layout, scale: float = 1.0) -> float:
    """Total straight-line distance (mm) travelled from key centre to key centre.

    ``scale`` resizes the whole layout (e.g. ``1.5`` for keys printed 50 % larger).
    Distance is linear in scale, so it is applied once to the total. Characters that
    are not on the layout are ignored.
    """
    points = [layout[char] for char in keystrokes if char in layout]
    return math.fsum(math.dist(a, b) for a, b in pairwise(points)) * scale


@dataclass(frozen=True)
class ComparisonResult:
    """Outcome of typing the same text on a baseline keyboard and on Eye Sense."""

    keystrokes: int
    kpm_baseline: float
    distance_baseline_mm: float
    distance_eye_mm: float
    scale_baseline: float = 1.0
    scale_eye: float = 1.0
    baseline_name: str = QWERTY_ES.name
    eye_name: str = EYE_SENSE.name

    @property
    def time_baseline_s(self) -> float:
        """Time needed on the baseline keyboard at the user's current KPM."""
        return self.keystrokes / self.kpm_baseline * 60

    @property
    def speed_mm_s(self) -> float:
        """The user's physical (eye) speed, deduced from the baseline keyboard."""
        return self.distance_baseline_mm / self.time_baseline_s

    @property
    def time_eye_s(self) -> float:
        """Time needed on Eye Sense moving at the same physical speed."""
        return self.distance_eye_mm / self.speed_mm_s

    @property
    def kpm_eye(self) -> float:
        """Extrapolated KPM on Eye Sense (= kpm_baseline * distance ratio)."""
        return self.kpm_baseline * self.distance_baseline_mm / self.distance_eye_mm

    @property
    def saved_distance_mm(self) -> float:
        """Positive when Eye Sense needs less movement than the baseline."""
        return self.distance_baseline_mm - self.distance_eye_mm

    @property
    def saved_distance_pct(self) -> float:
        return self.saved_distance_mm / self.distance_baseline_mm * 100

    @property
    def saved_time_s(self) -> float:
        return self.time_baseline_s - self.time_eye_s


def compare(
    text: str,
    kpm: float,
    eye_layout: Layout = EYE_SENSE,
    baseline_layout: Layout = QWERTY_ES,
    eye_scale: float = 1.0,
    baseline_scale: float = 1.0,
) -> ComparisonResult:
    """Compare the eye travel needed to type ``text`` on two layouts.

    Raises:
        ValueError: if ``kpm`` or a scale is not positive, the layouts do not cover
            the same letters, or the text has fewer than two typeable letters
            (or none of them produce any movement).
    """
    if kpm <= 0:
        raise ValueError(f"KPM must be greater than 0 (got {kpm}).")
    if eye_scale <= 0 or baseline_scale <= 0:
        raise ValueError("Scale factors must be greater than 0.")
    if eye_layout.letters != baseline_layout.letters:
        missing = sorted(eye_layout.letters ^ baseline_layout.letters)
        raise ValueError(f"Layouts must contain the same letters; mismatch: {missing}.")

    keystrokes = extract_keystrokes(clean_text(text), baseline_layout)
    if len(keystrokes) < 2:
        raise ValueError("Not enough valid letters to analyse (at least 2 are needed).")

    distance_baseline = path_distance(keystrokes, baseline_layout, baseline_scale)
    distance_eye = path_distance(keystrokes, eye_layout, eye_scale)
    if distance_baseline == 0 or distance_eye == 0:
        raise ValueError("The text produces no movement (it repeats a single letter).")

    return ComparisonResult(
        keystrokes=len(keystrokes),
        kpm_baseline=kpm,
        distance_baseline_mm=distance_baseline,
        distance_eye_mm=distance_eye,
        scale_baseline=baseline_scale,
        scale_eye=eye_scale,
        baseline_name=baseline_layout.name,
        eye_name=eye_layout.name,
    )
