"""
FLOW Framework
Statistics Module

Calculates dashboard statistics used by the HTML report.
"""

from collections import Counter


SEVERITY_ORDER = [
    "Critical",
    "High",
    "Medium",
    "Low",
    "Informational",
]


def calculate_overall_risk(findings):
    """
    Return the highest severity found.
    """

    severities = {
        finding.get("severity", "Informational").capitalize()
        for finding in findings
    }

    for severity in SEVERITY_ORDER:
        if severity in severities:
            return severity

    return "Informational"


def count_open_ports(results):
    """
    Count open ports from parsed Nmap results.
    """

    return len(results.get("nmap", []))


def count_services(results):
    """
    Count unique detected services.
    """

    services = {
        port.get("service", "Unknown")
        for port in results.get("nmap", [])
        if port.get("service")
    }

    return len(services)


def get_unique_services(results):
    """
    Return sorted list of unique services.
    """

    return sorted(
        {
            port.get("service", "Unknown")
            for port in results.get("nmap", [])
            if port.get("service")
        }
    )


def count_modules(results):
    """
    Count executed modules that returned data.
    """

    total = 0

    for value in results.values():

        if isinstance(value, list) and value:
            total += 1

        elif isinstance(value, dict) and value:
            total += 1

    return total


def calculate_risk_distribution(findings):
    """
    Count findings by severity.
    """

    counter = Counter()

    for finding in findings:

        severity = finding.get(
            "severity",
            "Informational",
        ).capitalize()

        if severity not in SEVERITY_ORDER:
            severity = "Informational"

        counter[severity] += 1

    return {
        severity: counter.get(severity, 0)
        for severity in SEVERITY_ORDER
    }


def calculate_dashboard_statistics(results, findings):
    """
    Build dashboard statistics dictionary.
    """

    unique_services = get_unique_services(results)

    return {
        "overall_risk": calculate_overall_risk(findings),
        "total_ports": count_open_ports(results),
        "total_services": len(unique_services),
        "total_modules": count_modules(results),
        "total_findings": len(findings),
        "unique_services": unique_services,
        "risk_distribution": calculate_risk_distribution(findings),
    }