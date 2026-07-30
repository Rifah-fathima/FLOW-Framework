import re
from models.finding import Finding


def parse_whatweb_output(output, target):

    findings = []

    if not output:
        return findings

    # Remove the URL portion
    output = re.sub(r"^https?://\S+\s+\[200 OK\]\s*", "", output)

    technologies = [tech.strip() for tech in output.split(",")]

    for tech in technologies:

        if "[" in tech:
            title = tech.split("[")[0]
        else:
            title = tech

        findings.append(
            Finding(
                tool="WhatWeb",
                severity="INFO",
                category="Technology Fingerprinting",
                title=title,
                description=tech,
                target=target,
                recommendation="Review detected technology and ensure it is up to date."
            )
        )

    return findings