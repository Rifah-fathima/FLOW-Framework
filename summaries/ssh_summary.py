def generate_ssh_summary(parsed_data):
    """
    Generates a human-readable SSH security summary.

    Parameters
    ----------
    parsed_data : dict

    Returns
    -------
    str
    """

    summary = []

    summary.append("=" * 60)
    summary.append("SSH ENUMERATION SUMMARY")
    summary.append("=" * 60)

    summary.append(f"Banner          : {parsed_data['banner']}")
    summary.append(f"Software        : {parsed_data['software']}")
    summary.append(f"Compression     : {parsed_data['compression']}")
    summary.append("")

    summary.append("-" * 60)
    summary.append("STATISTICS")
    summary.append("-" * 60)

    summary.append(f"KEX Algorithms      : {len(parsed_data['kex_algorithms'])}")
    summary.append(f"Host Keys           : {len(parsed_data['host_keys'])}")
    summary.append(f"Ciphers             : {len(parsed_data['ciphers'])}")
    summary.append(f"MAC Algorithms      : {len(parsed_data['macs'])}")
    summary.append(f"Fingerprints        : {len(parsed_data['fingerprints'])}")
    summary.append(f"Recommendations     : {len(parsed_data['recommendations'])}")
    summary.append("")

    summary.append("-" * 60)
    summary.append("SECURITY FINDINGS")
    summary.append("-" * 60)

    summary.append(f"FAIL Findings : {parsed_data['fail_count']}")
    summary.append(f"WARN Findings : {parsed_data['warn_count']}")
    summary.append(f"INFO Findings : {parsed_data['info_count']}")
    summary.append("")
    summary.append(f"Overall Risk : {parsed_data['risk']}")
    summary.append("")

    if parsed_data["recommendations"]:
        summary.append("-" * 60)
        summary.append("TOP RECOMMENDATIONS")
        summary.append("-" * 60)

        for recommendation in parsed_data["recommendations"][:10]:
            summary.append(f"• {recommendation}")

        if len(parsed_data["recommendations"]) > 10:
            summary.append("")
            summary.append(
                f"... and {len(parsed_data['recommendations']) - 10} more recommendations."
            )

    summary.append("")
    summary.append("=" * 60)

    return "\n".join(summary)