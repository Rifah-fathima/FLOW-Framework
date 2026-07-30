def generate_whatweb_summary(findings):
    """
    Generates a summary of detected technologies.
    """

    summary = {
        "total_technologies": len(findings),
        "technologies": []
    }

    for finding in findings:
        summary["technologies"].append(finding.title)

    return summary