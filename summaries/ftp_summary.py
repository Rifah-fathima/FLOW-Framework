"""
FLOW FTP Summary

Generates a professional FTP Enumeration summary.
"""


def generate_ftp_summary(ftp_data):
    """
    Generates a formatted FTP summary.

    Parameters:
        ftp_data (dict): Parsed FTP results.

    Returns:
        str: Formatted FTP summary.
    """

    summary = []

    summary.append("=" * 60)
    summary.append("FTP ENUMERATION SUMMARY")
    summary.append("=" * 60)

    summary.append(f"Port            : {ftp_data['port']}")
    summary.append(f"State           : {ftp_data['state']}")
    summary.append(f"Service         : {ftp_data['service']}")
    summary.append(f"Banner          : {ftp_data['banner']}")

    if ftp_data["server_os"]:
        summary.append(f"Server          : {ftp_data['server_os']}")

    summary.append("")

    summary.append("-" * 60)
    summary.append("AUTHENTICATION")
    summary.append("-" * 60)

    if ftp_data["anonymous_login"]:
        summary.append("Anonymous Login : ENABLED")
    else:
        summary.append("Anonymous Login : DISABLED")

    summary.append("")

    summary.append("-" * 60)
    summary.append("DIRECTORY LISTING")
    summary.append("-" * 60)

    if ftp_data["directories"]:

        for directory in ftp_data["directories"]:
            summary.append(f"• {directory}")

    else:
        summary.append("No directories discovered.")

    summary.append("")

    summary.append("-" * 60)
    summary.append("SECURITY")
    summary.append("-" * 60)

    summary.append(f"Risk Level      : {ftp_data['risk']}")

    summary.append("")

    summary.append("-" * 60)
    summary.append("RECOMMENDATIONS")
    summary.append("-" * 60)

    if ftp_data["recommendations"]:

        for recommendation in ftp_data["recommendations"]:
            summary.append(f"• {recommendation}")

    else:
        summary.append("No recommendations.")

    summary.append("")
    summary.append("=" * 60)

    return "\n".join(summary)