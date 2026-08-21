"""
FLOW Framework
Charts Module

Generates HTML charts and visual summaries.
"""


def build_risk_distribution(findings):
    """
    Generate the Risk Distribution HTML.
    """

    severity_count = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0,
        "Informational": 0,
    }

    for finding in findings:

        severity = finding.get("severity", "Informational")

        if severity not in severity_count:
            severity = "Informational"

        severity_count[severity] += 1

    html = """
    <table class="risk-table">
        <tr>
            <th>Severity</th>
            <th>Count</th>
        </tr>
    """

    colors = {
        "Critical": "#d32f2f",
        "High": "#f57c00",
        "Medium": "#fbc02d",
        "Low": "#388e3c",
        "Informational": "#1976d2",
    }

    for severity, count in severity_count.items():

        html += f"""
        <tr>
            <td>
                <span style="
                    color:white;
                    background:{colors[severity]};
                    padding:4px 10px;
                    border-radius:5px;
                    font-weight:bold;">
                    {severity}
                </span>
            </td>
            <td>{count}</td>
        </tr>
        """

    html += "</table>"

    return html