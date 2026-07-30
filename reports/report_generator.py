import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JSON_FILE = os.path.join(BASE_DIR, "report.json")
TEMPLATE_FILE = os.path.join(BASE_DIR, "templates", "report_template.html")
OUTPUT_FILE = os.path.join(BASE_DIR, "report.html")


# ==========================================================
# Risk Calculation
# ==========================================================

def calculate_overall_risk(findings):
    """
    Determine the highest severity present.
    """

    severity_order = [
        "critical",
        "high",
        "medium",
        "low",
        "informational",
    ]

    severities = [
        finding.get("severity", "").lower()
        for finding in findings
    ]

    for severity in severity_order:
        if severity in severities:
            return severity.capitalize()

    return "Informational"


# ==========================================================
# Severity Badge
# ==========================================================

def badge(severity):
    """
    Generate HTML severity badge.
    """

    sev = severity.lower()

    return (
        f'<span class="badge {sev}">'
        f'{severity}'
        f'</span>'
    )


# ==========================================================
# Dashboard Statistics
# ==========================================================

def calculate_dashboard_statistics(results, findings):
    """
    Calculate dashboard metrics.
    """

    ports = results.get("nmap", [])

    total_ports = len(ports)

    services = []

    unique_services = set()

    for port in ports:

        service = port.get("service", "Unknown")

        services.append(service)

        unique_services.add(service)

    modules = list(results.keys())

    stats = {

        "total_ports": total_ports,

        "total_services": len(unique_services),

        "total_modules": len(modules),

        "total_findings": len(findings),

        "unique_services": sorted(unique_services),

        "modules": modules,
    }

    return stats


# ==========================================================
# Risk Distribution
# ==========================================================

def build_risk_statistics(findings):
    """
    Build severity statistics table.
    """

    counter = {

        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0,
        "Informational": 0,
    }

    for finding in findings:

        severity = finding.get(
            "severity",
            "Informational",
        )

        if severity in counter:
            counter[severity] += 1

    html = """
    <table>

        <tr>
            <th>Severity</th>
            <th>Count</th>
        </tr>
    """

    for severity, count in counter.items():

        html += f"""
        <tr>

            <td>{badge(severity)}</td>

            <td>{count}</td>

        </tr>
        """

    html += "</table>"

    return html


# ==========================================================
# Attack Surface
# ==========================================================

def build_attack_surface(unique_services):
    """
    Display exposed services.
    """

    if not unique_services:
        return "<p>No exposed services detected.</p>"

    html = '<div class="attack-surface">'

    for service in unique_services:

        html += (
            f'<span class="service-chip">'
            f'{service.upper()}'
            f'</span>'
        )

    html += "</div>"

    return html

# ==========================================================
# Open Ports
# ==========================================================

def build_open_ports(results):

    html = """
    <table>

        <tr>
            <th>Port</th>
            <th>Service</th>
            <th>Version</th>
        </tr>
    """

    ports = results.get("nmap", [])

    if not ports:

        return "<p>No open ports detected.</p>"

    for port in ports:

        html += f"""
        <tr>

            <td>{port.get("port","Unknown")}</td>

            <td>{port.get("service","Unknown")}</td>

            <td>{port.get("version","N/A")}</td>

        </tr>
        """

    html += "</table>"

    return html


# ==========================================================
# Services
# ==========================================================

def build_services(results):

    ports = results.get("nmap", [])

    if not ports:

        return "<p>No services detected.</p>"

    unique = set()

    html = """
    <table>

        <tr>

            <th>Service</th>

            <th>Port</th>

        </tr>
    """

    for port in ports:

        service = port.get("service","Unknown")

        port_number = port.get("port","")

        key = (service, port_number)

        if key in unique:
            continue

        unique.add(key)

        html += f"""
        <tr>

            <td>{service}</td>

            <td>{port_number}</td>

        </tr>
        """

    html += "</table>"

    return html


# ==========================================================
# Modules
# ==========================================================

def build_modules(modules):

    if not modules:

        return "<p>No modules executed.</p>"

    html = '<div class="modules-grid">'

    for module in sorted(modules):

        html += f"""
        <div class="module-card">

            ✅ {module.upper()}

        </div>
        """

    html += "</div>"

    return html


# ==========================================================
# Findings
# ==========================================================

def build_findings(findings):

    if not findings:

        return "<p>No security findings detected.</p>"

    html = ""

    for finding in findings:

        severity = finding.get(
            "severity",
            "Informational"
        )

        title = finding.get(
            "title",
            "Untitled Finding"
        )

        description = finding.get(
            "description",
            "No description available."
        )

        recommendation = finding.get(
            "recommendation",
            "No recommendation."
        )

        html += f"""
        <div class="finding">

            <h3>

                {badge(severity)}

                {title}

            </h3>

            <p>

                <strong>Description</strong><br>

                {description}

            </p>

            <p>

                <strong>Recommendation</strong><br>

                {recommendation}

            </p>

        </div>
        """

    return html

# ==========================================================
# Recommendations
# ==========================================================

def build_recommendations(findings):
    """
    Build recommendations list.
    """

    recommendations = set()

    for finding in findings:

        recommendation = finding.get("recommendation", "").strip()

        if recommendation:
            recommendations.add(recommendation)

    if not recommendations:
        return "<p>No recommendations available.</p>"

    html = "<ul>"

    for recommendation in sorted(recommendations):

        html += f"<li>{recommendation}</li>"

    html += "</ul>"

    return html


# ==========================================================
# Executive Summary
# ==========================================================

def build_executive_summary(target, findings, stats, overall_risk):
    """
    Generate executive summary.
    """

    return f"""
    <p>

    The FLOW Framework completed an automated security
    assessment of <strong>{target}</strong>.

    The assessment identified
    <strong>{stats['total_findings']}</strong> finding(s)
    across
    <strong>{stats['total_ports']}</strong> open port(s)
    and
    <strong>{stats['total_services']}</strong> exposed service(s).

    The overall security posture is classified as

    <strong>{overall_risk}</strong>.

    Manual validation is recommended before
    remediation activities are performed.

    </p>
    """


# ==========================================================
# Conclusion
# ==========================================================

def build_conclusion(overall_risk):
    """
    Build conclusion section.
    """

    return f"""
    <p>

    FLOW successfully completed the automated penetration
    testing workflow.

    The assessment concluded with an overall risk rating of

    <strong>{overall_risk}</strong>.

    Organizations should prioritize remediation of
    Critical and High severity findings before
    production deployment.

    Manual verification and periodic reassessment are
    recommended to maintain a strong security posture.

    </p>
    """