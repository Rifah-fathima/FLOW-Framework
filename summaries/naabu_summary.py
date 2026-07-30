def generate_naabu_summary(parsed_ports):

    summary = []

    summary.append("=" * 50)
    summary.append("FLOW - Naabu Summary")
    summary.append("=" * 50)
    summary.append("")

    if parsed_ports:

        summary.append("Open Ports")
        summary.append("-" * 20)

        for port in parsed_ports:
            summary.append(f"✓ {port['port']}")

    else:

        summary.append("No open ports found.")

    summary.append("")
    summary.append(f"Total Open Ports : {len(parsed_ports)}")
    summary.append("")
    summary.append("Next Action : Run Nmap Service Detection")

    return "\n".join(summary)