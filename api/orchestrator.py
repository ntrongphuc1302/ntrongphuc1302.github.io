"""
Orchestrator module — Flask app that generates the terminal SVG widget.
"""

from __future__ import annotations

import datetime
import os
from typing import Any, Optional

from flask import Flask, Response, render_template, request, redirect

from .config import svg_config, validate_hex_color

app = Flask(__name__)


def escape_xml(text: str) -> str:
    """Escape special characters for XML/SVG compatibility."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def get_current_time() -> str:
    """Get current time in Hanoi timezone (UTC+7)."""
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    hanoi = datetime.timezone(datetime.timedelta(hours=7))
    return utc_now.astimezone(hanoi).strftime("%H:%M:%S")


def truncate_text(text: str, max_chars: int) -> str:
    """Truncate text to max_chars, adding ellipsis if needed."""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1] + "\u2026"


def calculate_marquee(
    text: str, font_size: int, container_width: int = 300
) -> dict[str, Any]:
    """Calculate marquee scroll parameters if text overflows its container."""
    char_width = font_size * 0.6
    text_width = len(text) * char_width
    spacer_width = 30

    if text_width + (spacer_width / 2) <= container_width:
        return {"enabled": False}

    speed_px_per_sec = 30
    duration = round((text_width + spacer_width) / speed_px_per_sec, 1)
    return {"enabled": True, "duration": max(5.0, duration)}


def make_svg(
    background_color: str,
    border_color: str,
    accent_color: str,
    text_color: str,
    secondary_color: str,
    red_color: str,
    name: str = "Nguyen Trong Phuc",
    mono_accent: str = "PX03",
    tagline: str = "I build modern, scalable, and creative applications.",
    about: str = "Also known as PX03 around the internet.",
    github_link: str = "github.com/ntrongphuc1302",
    email_link: str = "ntrongphuc1302@gmail.com",
    profile_url: str = "https://ntrongphuc.io.vn",
) -> str:
    """Generate the terminal SVG widget."""

    cfg = svg_config

    # Truncate long text
    name = truncate_text(name, 25)
    tagline = truncate_text(tagline, 70)
    about = truncate_text(about, 90)
    github_link = truncate_text(github_link, 30)
    email_link = truncate_text(email_link, 30)

    # Marquee
    tagline_marquee = calculate_marquee(
        tagline, cfg.tagline_font_size, container_width=cfg.width - 120
    )
    about_marquee = calculate_marquee(
        about, cfg.about_font_size, container_width=cfg.width - 120
    )

    # Time
    current_time = get_current_time()

    template_data = {
        # Colors
        "background_color": background_color,
        "border_color": border_color,
        "accent_color": accent_color,
        "text_color": text_color,
        "secondary_color": secondary_color,
        "red_color": red_color,
        # Dimensions
        "width": cfg.width,
        "height": cfg.height,
        "border_radius": cfg.border_radius,
        "padding_top": cfg.padding_top,
        "padding_right": cfg.padding_right,
        "padding_bottom": cfg.padding_bottom,
        "padding_left": cfg.padding_left,
        "border_width": cfg.border_width,
        # Dot
        "dot_size": cfg.dot_size,
        "dot_margin_right": cfg.dot_margin_right,
        "dot_top_offset": cfg.dot_top_offset,
        # Clock
        "clock_font_size": cfg.clock_font_size,
        "clock_margin_left": cfg.clock_margin_left,
        "current_time": current_time,
        # Hero
        "name_font_size": cfg.name_font_size,
        "name_margin_top": cfg.name_margin_top,
        "tagline_font_size": cfg.tagline_font_size,
        "tagline_margin_top": cfg.tagline_margin_top,
        # About
        "about_font_size": cfg.about_font_size,
        "about_margin_top": cfg.about_margin_top,
        # Links
        "links_margin_top": cfg.links_margin_top,
        "link_font_size": cfg.link_font_size,
        "link_height": cfg.link_height,
        "link_gap": cfg.link_gap,
        "link_icon_size": cfg.link_icon_size,
        # Content
        "name": escape_xml(name),
        "mono_accent": escape_xml(mono_accent),
        "tagline": escape_xml(tagline),
        "about": escape_xml(about),
        "github_link": escape_xml(github_link),
        "email_link": escape_xml(email_link),
        "profile_url": profile_url,
        # Marquee
        "tagline_marquee": tagline_marquee,
        "about_marquee": about_marquee,
    }

    return render_template("terminal.html.j2", **template_data)


# ============================================================================
# Routes
# ============================================================================


@app.route("/api/orchestrator")
def orchestrator() -> Response:
    """Main route — serves the SVG widget."""
    bg = validate_hex_color(request.args.get("background_color", ""), svg_config.default_background)
    border = validate_hex_color(request.args.get("border_color", ""), svg_config.default_border)
    accent = validate_hex_color(request.args.get("accent_color", ""), svg_config.default_accent)
    text = validate_hex_color(request.args.get("text_color", ""), svg_config.default_text)
    secondary = validate_hex_color(request.args.get("secondary_color", ""), svg_config.default_secondary)
    red = validate_hex_color(request.args.get("red_color", ""), svg_config.default_red)

    svg = make_svg(
        background_color=bg,
        border_color=border,
        accent_color=accent,
        text_color=text,
        secondary_color=secondary,
        red_color=red,
    )

    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"
    return resp


@app.route("/api/health")
def health_check() -> Response:
    """Health check endpoint."""
    return Response("OK", status=200, mimetype="text/plain")


@app.route("/")
def root() -> Response:
    """Root redirect."""
    return redirect("https://ntrongphuc.io.vn")


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", debug=True, port=port)


# Vercel handler — wraps the Flask app as a WSGI entry point
def handler(environ, start_response):
    return app(environ, start_response)
