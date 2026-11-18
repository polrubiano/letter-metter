"""Human-readable formatting of distances and durations."""

from __future__ import annotations


def format_distance(distance_mm: float) -> str:
    """Format a distance in mm, switching to m (>= 1 000 mm) or km (>= 1 000 000 mm)."""
    magnitude = abs(distance_mm)
    if magnitude >= 1_000_000:
        return f"{distance_mm / 1_000_000:.3f} km"
    if magnitude >= 1_000:
        return f"{distance_mm / 1_000:.2f} m"
    return f"{distance_mm:.2f} mm"


def format_time(seconds: float) -> str:
    """Format a duration as ``s``, ``min s`` or ``h min``. Negative values keep their sign."""
    sign = "-" if seconds < 0 else ""
    magnitude = abs(seconds)
    if magnitude >= 3600:
        hours, remainder = divmod(int(magnitude), 3600)
        return f"{sign}{hours} h {remainder // 60} min"
    if magnitude >= 60:
        minutes, secs = divmod(magnitude, 60)
        return f"{sign}{int(minutes)} min {secs:.1f} s"
    return f"{sign}{magnitude:.2f} s"
