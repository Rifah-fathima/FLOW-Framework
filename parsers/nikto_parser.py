"""
FLOW Nikto Parser
"""

import re


def parse_nikto_output(output):
    """
    Parses Nikto output into a structured dictionary.
    """

    findings = []

    if not output:
        return {
            "total_findings": 0,
            "highlights": [],
            "risk": "Low"
        }

    for line in output.splitlines():

        line = line.strip()

        if line.startswith("+ ["):

            match = re.match(r"\+ \[(.*?)\] (.*)", line)

            if match:

                findings.append({
                    "id": match.group(1),
                    "description": match.group(2)
                })

    descriptions = [item["description"] for item in findings]

    total = len(findings)

    if total >= 10:
        risk = "High"
    elif total >= 5:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "total_findings": total,
        "highlights": descriptions,
        "findings": findings,
        "risk": risk
    }