def generate_gobuster_summary(results):
    """
    Generate a readable summary from parsed Gobuster results.
    """

    summary = []

    summary.append("=" * 50)
    summary.append("        FLOW - Gobuster Summary")
    summary.append("=" * 50)
    summary.append("")

    if not results:
        summary.append("No directories or files were discovered.")
        summary.append("")
        summary.append("Risk Level : Low")
        summary.append("Next Action: Continue Enumeration")

        return "\n".join(summary)

    summary.append("Discovered Paths")
    summary.append("-" * 20)

    for item in results:
        summary.append(
            f"✓ {item['path']}   (HTTP {item['status']})"
        )

    summary.append("")

    interesting = [
        "/admin",
        "/login",
        "/backup",
        "/config",
        "/uploads",
        "/images"
    ]

    found = False

    for item in results:
        if item["path"].lower() in interesting:
            found = True
            break

    if found:
        risk = "High"
        action = "Run Nikto and perform manual verification"

    else:
        risk = "Medium"
        action = "Continue web enumeration"

    summary.append(f"Risk Level : {risk}")
    summary.append(f"Next Action: {action}")

    return "\n".join(summary)