"""
FLOW Framework
Sections Module

Generates all HTML sections used by the report builder.
"""
from reports.html_utils import (
    badge,
    build_table,
    service_chip,
    module_card,
    unordered_list,
    empty_message,
)
from reports.statistics import (
    calculate_dashboard_statistics,
)
def build_executive_summary(target, findings, stats):
    """
    Generate the executive summary section.

    Parameters
    ----------
    target : str
        Target host.

    findings : list
        Security findings.

    stats : dict
        Dashboard statistics returned by
        calculate_dashboard_statistics().
    """

    total_ports = stats.get("total_ports", 0)
    total_services = stats.get("total_services", 0)
    total_findings = stats.get("total_findings", 0)
    overall_risk = stats.get("overall_risk", "Informational")

    html = f"""
    <p>

    FLOW Framework completed an automated security assessment
    against

    <strong>{target}</strong>.

    The assessment identified

    <strong>{total_findings}</strong>
    security finding(s),

    <strong>{total_ports}</strong>
    open port(s),

    and

    <strong>{total_services}</strong>
    exposed network service(s).

    Based on the discovered attack surface and identified
    vulnerabilities, the overall security posture is classified as

    {badge(overall_risk)}.

    The findings presented in this report should be manually
    validated before remediation activities are performed.

    </p>
    """

    return html

def build_attack_surface(results):
    """
    Build the Attack Surface section.

    Displays all unique exposed network services
    discovered by Nmap.
    """

    ports = results.get("nmap", [])

    if not ports:
        return empty_message("No exposed services detected.")

    services = set()

    for port in ports:

        service = port.get("service", "").strip()

        if service:
            services.add(service.upper())

    if not services:
        return empty_message("No exposed services detected.")

    html = '<div class="attack-surface">'

    for service in sorted(services):

        html += service_chip(service)

    html += "</div>"

    return html

def build_open_ports(results):
    """
    Build the Open Ports section.

    Displays all open ports discovered during the
    Nmap service scan.
    """

    ports = results.get("nmap", [])

    if not ports:
        return empty_message("No open ports detected.")

    headers = [
        "Port",
        "Protocol",
        "Service",
        "Version",
    ]

    rows = []

    for port in ports:

        rows.append([
            port.get("port", "Unknown"),
            port.get("protocol", "tcp"),
            port.get("service", "Unknown"),
            port.get("version", "N/A"),
        ])

    return build_table(headers, rows)

def build_services(results):
    """
    Build the Detected Services section.

    Displays all unique services and the ports
    on which they were discovered.
    """

    ports = results.get("nmap", [])

    if not ports:
        return empty_message("No services detected.")

    headers = [
        "Service",
        "Port",
        "Version",
    ]

    rows = []
    seen = set()

    for port in ports:

        service = port.get("service", "Unknown")
        port_number = port.get("port", "Unknown")
        version = port.get("version", "N/A")

        key = (service, port_number)

        if key in seen:
            continue

        seen.add(key)

        rows.append([
            service,
            port_number,
            version,
        ])

    return build_table(headers, rows)


def build_modules(results):
    """
    Build the Executed Modules section.

    Displays all FLOW modules that returned results
    during the scan.
    """

    if not results:
        return empty_message("No modules executed.")

    html = '<div class="modules-grid">'

    for module_name, module_result in sorted(results.items()):

        # Skip empty results
        if isinstance(module_result, list) and not module_result:
            continue

        if isinstance(module_result, dict) and not module_result:
            continue

        html += module_card(module_name)

    html += "</div>"

    return html


def build_findings(findings):
    """
    Build the Security Findings section.

    Displays all findings collected by the
    FindingsManager.
    """

    if not findings:
        return empty_message("No security findings detected.")

    html = ""

    for finding in findings:

        severity = finding.get(
            "severity",
            "Informational"
        )

        module = finding.get(
            "module",
            "Unknown"
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
            "No recommendation available."
        )

        html += f"""
        <div class="finding">

            <h3>
                {badge(severity)}
                {title}
            </h3>

            <p>

                <strong>Module:</strong>

                {module.upper()}

            </p>

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


def build_recommendations(findings):
    """
    Build the Recommendations section.

    Collects all unique recommendations from
    the findings list.
    """

    if not findings:
        return empty_message("No recommendations available.")

    recommendations = []
    seen = set()

    for finding in findings:

        recommendation = (
            finding.get("recommendation", "")
            .strip()
        )

        if not recommendation:
            continue

        if recommendation in seen:
            continue

        seen.add(recommendation)
        recommendations.append(recommendation)

    if not recommendations:
        return empty_message("No recommendations available.")

    return unordered_list(recommendations)


def build_conclusion(overall_risk):
    """
    Build the report conclusion.

    Parameters
    ----------
    overall_risk : str
        Overall risk level calculated by the
        statistics module.

    Returns
    -------
    str
        HTML conclusion section.
    """

    html = f"""
    <p>

    FLOW Framework successfully completed the automated
    penetration testing workflow.

    Based on the assessment, the target environment has an
    overall security rating of

    <strong>{overall_risk}</strong>.

    Organizations should prioritize remediation of
    <strong>Critical</strong> and
    <strong>High</strong> severity findings before
    deploying systems into production.

    Security assessments should be performed regularly,
    vulnerabilities should be remediated promptly,
    and continuous monitoring should be implemented to
    maintain a strong security posture.

    </p>
    """

    return html