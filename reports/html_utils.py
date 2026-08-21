"""
FLOW Framework
HTML Utility Functions

Reusable HTML components used by the reporting engine.
"""

from html import escape
from typing import Any, Iterable, List


# ==========================================================
# HTML Escape
# ==========================================================

def html_escape(value: Any) -> str:
    """
    Escape HTML special characters safely.
    """

    if value is None:
        return ""

    return escape(str(value), quote=True)


# ==========================================================
# Severity Badge
# ==========================================================

def badge(severity: str) -> str:
    """
    Return a colored severity badge.
    """

    if not severity:
        severity = "Informational"

    severity = severity.capitalize()

    css = {
        "Critical": "critical",
        "High": "high",
        "Medium": "medium",
        "Low": "low",
        "Informational": "informational",
    }

    css_class = css.get(severity, "informational")

    return (
        f'<span class="badge {css_class}">'
        f'{html_escape(severity)}'
        f'</span>'
    )


# ==========================================================
# Dashboard Card
# ==========================================================

def dashboard_card(title: str, value: Any) -> str:
    """
    Create dashboard statistic card.
    """

    return f"""
    <div class="card">
        <h3>{html_escape(title)}</h3>
        <p>{html_escape(value)}</p>
    </div>
    """


# ==========================================================
# Service Chip
# ==========================================================

def service_chip(service: str) -> str:
    """
    Render service chip.
    """

    return (
        f'<span class="service-chip">'
        f'{html_escape(service).upper()}'
        f'</span>'
    )


# ==========================================================
# Module Card
# ==========================================================

def module_card(module: str) -> str:
    """
    Render executed module card.
    """

    return f"""
    <div class="module-card">
        ✅ {html_escape(module).upper()}
    </div>
    """


# ==========================================================
# Generic Table Builder
# ==========================================================

def build_table(headers: List[str], rows: Iterable[Iterable[Any]]) -> str:
    """
    Build a reusable HTML table.
    """

    html = "<table>"

    html += "<tr>"

    for header in headers:
        html += f"<th>{html_escape(header)}</th>"

    html += "</tr>"

    for row in rows:

        html += "<tr>"

        for column in row:
            html += f"<td>{html_escape(column)}</td>"

        html += "</tr>"

    html += "</table>"

    return html


# ==========================================================
# HTML List
# ==========================================================

def unordered_list(items: Iterable[str]) -> str:
    """
    Render unordered HTML list.
    """

    items = list(items)

    if not items:
        return "<p>No data available.</p>"

    html = "<ul>"

    for item in items:
        html += f"<li>{html_escape(item)}</li>"

    html += "</ul>"

    return html


# ==========================================================
# Report Section
# ==========================================================

def section(title: str, body: str) -> str:
    """
    Wrap report section.
    """

    return f"""
<section>

<h2>{html_escape(title)}</h2>

{body}

</section>
"""


# ==========================================================
# Message Boxes
# ==========================================================

def info_box(message: str) -> str:
    return f'<div class="info-box">{html_escape(message)}</div>'


def warning_box(message: str) -> str:
    return f'<div class="warning-box">{html_escape(message)}</div>'


def error_box(message: str) -> str:
    return f'<div class="error-box">{html_escape(message)}</div>'


def success_box(message: str) -> str:
    return f'<div class="success-box">{html_escape(message)}</div>'


# ==========================================================
# Divider
# ==========================================================

def divider() -> str:
    """
    Horizontal rule.
    """

    return "<hr>"


# ==========================================================
# Empty Message
# ==========================================================

def empty_message(message: str = "No data available.") -> str:
    """
    Standard empty data message.
    """

    return f"<p>{html_escape(message)}</p>"