"""
Centralized configuration module for the terminal SVG widget.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Tuple

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

RGBColor = Tuple[int, int, int]
ColorPalette = list[RGBColor]

HEX_COLOR_PATTERN = re.compile(r"^[0-9a-fA-F]{6}$")


@dataclass(frozen=True)
class SVGConfig:
    """SVG widget configuration and defaults."""

    width: int = 540
    height: int = 180
    border_radius: int = 8

    padding_top: int = 16
    padding_right: int = 20
    padding_bottom: int = 16
    padding_left: int = 20
    border_width: int = 1

    # Status dot
    dot_size: int = 8
    dot_margin_right: int = 8
    dot_top_offset: int = 20

    # Clock
    clock_font_size: int = 11
    clock_margin_left: int = 10

    # Hero section
    name_font_size: int = 28
    name_margin_top: int = 8
    tagline_font_size: int = 13
    tagline_margin_top: int = 2

    # About
    about_font_size: int = 12
    about_margin_top: int = 10
    about_max_lines: int = 2

    # Links section
    links_margin_top: int = 10
    link_font_size: int = 12
    link_height: int = 26
    link_gap: int = 6
    link_icon_size: int = 14

    # Default colors (hex without #)
    default_background: str = "0c0c0c"
    default_border: str = "1f1f1f"
    default_accent: str = "3cff65"
    default_text: str = "e2e2e2"
    default_secondary: str = "888888"
    default_red: str = "e50914"


def validate_hex_color(color: str, default: str) -> str:
    """Validate a hex color string (without #)."""
    if color and HEX_COLOR_PATTERN.match(color):
        return color.lower()
    return default


svg_config = SVGConfig()
