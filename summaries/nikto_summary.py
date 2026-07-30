"""
FLOW Nikto Summary
"""


def truncate(text, max_length=85):
    """
    Truncate long text for cleaner console output.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def generate_nikto_summary(data):
    """
    Generates a professional console summary for Nikto.
    """

    summary = []

    summary.append("=" * 60)
    summary.append("NIKTO SUMMARY")
    summary.append("=" * 60)
    summary.append("")

    summary.append(f"Total Findings : {data['total_findings']}")
    summary.append("")

    summary.append("-" * 60)
    summary.append("HIGHLIGHTS")
    summary.append("-" * 60)

    if data["highlights"]:

        for finding in data["highlights"][:5]:
            summary.append(f"• {truncate(finding)}")

        remaining = data["total_findings"] - 5

        if remaining > 0:
            summary.append("")
            summary.append(f"... and {remaining} more findings.")

    else:
        summary.append("No significant findings.")

    summary.append("")
    summary.append("-" * 60)
    summary.append("RISK LEVEL")
    summary.append("-" * 60)
    summary.append(f"Overall Risk : {data['risk']}")

    summary.append("")
    summary.append("-" * 60)
    summary.append("RECOMMENDATIONS")
    summary.append("-" * 60)

    recommendations = [
        "Update outdated web server software.",
        "Enable missing HTTP security headers.",
        "Review exposed files and directories.",
        "Mitigate information disclosure issues.",
        "Perform manual verification of findings."
    ]

    for recommendation in recommendations:
        summary.append(f"• {recommendation}")

    summary.append("")
    summary.append("=" * 60)

    return "\n".join(summary)