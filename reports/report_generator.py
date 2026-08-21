"""
FLOW Framework
HTML Report Generator

Reads report.json and generates report.html using
report_template.html.
"""

import json
import os
from datetime import datetime

from reports.statistics import (
    calculate_dashboard_statistics,
)

from reports.report_builder import (
    build_html_report,
)

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JSON_FILE = os.path.join(
    BASE_DIR,
    "report.json",
)

TEMPLATE_FILE = os.path.join(
    BASE_DIR,
    "templates",
    "report_template.html",
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "report.html",
)

# ==========================================================
# JSON Loader
# ==========================================================

def load_report():
    """
    Load report.json.
    """

    if not os.path.exists(JSON_FILE):
        raise FileNotFoundError(
            f"Report JSON not found: {JSON_FILE}"
        )

    with open(
        JSON_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)

# ==========================================================
# HTML Report Generator
# ==========================================================

def generate_html_report():
    """
    Generate the HTML report from report.json.
    """

    # Load JSON report
    report = load_report()

    target = report.get("target", "Unknown Target")
    results = report.get("results", {})
    findings = report.get("findings", [])

    # Calculate statistics
    stats = calculate_dashboard_statistics(
        results,
        findings,
    )

    # Build HTML
    html = build_html_report(
        target=target,
        results=results,
        findings=findings,
        stats=stats,
    )

    # Save HTML report
    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(html)

    print(f"[FLOW] HTML Report Generated -> {OUTPUT_FILE}")

    return OUTPUT_FILE

# ==========================================================
# Standalone Execution
# ==========================================================

if __name__ == "__main__":
    generate_html_report()