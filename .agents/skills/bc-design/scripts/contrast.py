"""WCAG 2.x contrast helpers shared by BC Design workflows."""

from __future__ import annotations

import re


def linearize_channel(channel):
    value = channel / 255.0
    if value <= 0.03928:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    red, green, blue = (linearize_channel(channel) for channel in rgb)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def parse_hex_color(hex_str):
    """Parse #RGB or #RRGGBB into an RGB tuple."""
    value = hex_str.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(char * 2 for char in value)
    if not re.fullmatch(r"[0-9A-Fa-f]{6}", value):
        raise ValueError(f"Expected a hex color like #FFFFFF or FFFFFF, got {hex_str!r}")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def compute_contrast(hex1, hex2):
    """Return the WCAG relative-luminance contrast ratio."""
    luminance_one = relative_luminance(parse_hex_color(hex1))
    luminance_two = relative_luminance(parse_hex_color(hex2))
    lighter, darker = max(luminance_one, luminance_two), min(luminance_one, luminance_two)
    return (lighter + 0.05) / (darker + 0.05)

