import re

from models.finding import Finding


def parse_whatweb_output(output, target):
    """
    Parse WhatWeb output and extract detected technologies.

    WhatWeb may return ANSI color/control sequences when executed
    from a terminal. These sequences are removed before parsing.
    """

    findings = []

    if not output:
        return findings

    # ==================================================
    # REMOVE ANSI ESCAPE SEQUENCES
    # ==================================================

    ansi_escape = re.compile(
        r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
    )

    output = ansi_escape.sub("", output)

    # ==================================================
    # REMOVE URL / HTTP STATUS PREFIX
    # ==================================================

    output = re.sub(
        r"^https?://\S+\s+\[200 OK\]\s*",
        "",
        output
    )

    # ==================================================
    # EXTRACT TECHNOLOGIES
    # ==================================================

    technologies = [
        tech.strip()
        for tech in output.split(",")
        if tech.strip()
    ]

    for tech in technologies:

        if "[" in tech:
            title = tech.split("[", 1)[0].strip()
        else:
            title = tech.strip()

        if not title:
            continue

        findings.append(
            Finding(
                tool="WhatWeb",
                severity="INFO",
                category="Technology Fingerprinting",
                title=title,
                description=tech,
                target=target,
                recommendation=(
                    "Review detected technology and ensure it is up to date."
                )
            )
        )

    return findings