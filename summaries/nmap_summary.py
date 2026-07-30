def generate_nmap_summary(scan_results):
    """
    Generate a human-readable summary from parsed Nmap results.
    """

    open_services = []

    for item in scan_results:
        if item["state"] == "open":
            open_services.append({
                "port": item["port"],
                "service": item["service"]
            })

    summary = []

    summary.append("=" * 50)
    summary.append("          FLOW - Nmap Summary")
    summary.append("=" * 50)
    summary.append("")

    if not open_services:
        summary.append("No open services were detected.")
        summary.append("")
        summary.append("Risk Level : Low")
        summary.append("Next Action: None")
        return "\n".join(summary)

    summary.append("Open Services")
    summary.append("-" * 20)

    for service in open_services:
        summary.append(
            f"✓ {service['port']}  ->  {service['service'].upper()}"
        )

    summary.append("")

    # Risk Calculation
    if any(s["service"] in ["http", "https"] for s in open_services):
        risk = "Medium"
        action = "Run Gobuster"

    elif any(s["service"] == "ssh" for s in open_services):
        risk = "Low"
        action = "Perform SSH Enumeration"

    else:
        risk = "Low"
        action = "Continue Enumeration"

    summary.append(f"Risk Level : {risk}")
    summary.append(f"Next Action: {action}")

    return "\n".join(summary)