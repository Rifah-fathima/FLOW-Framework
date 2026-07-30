def generate_smb_summary(smb_data):
    """
    Generates a professional summary for SMB Enumeration.

    Parameters:
        smb_data (dict): Parsed SMB information.

    Returns:
        str: Formatted SMB summary.
    """

    summary = []

    summary.append("=" * 60)
    summary.append("SMB ENUMERATION SUMMARY")
    summary.append("=" * 60)
    summary.append("")

    summary.append("-" * 60)
    summary.append("SYSTEM INFORMATION")
    summary.append("-" * 60)

    summary.append(f"Computer Name   : {smb_data['computer_name']}")
    summary.append(f"Operating System: {smb_data['os']}")
    summary.append(f"Domain          : {smb_data['domain']}")
    summary.append(f"Workgroup       : {smb_data['workgroup']}")
    summary.append("")

    summary.append("-" * 60)
    summary.append("SECURITY")
    summary.append("-" * 60)

    summary.append(f"SMB Signing     : {smb_data['signing']}")

    if smb_data["anonymous_access"]:
        summary.append("Anonymous Login : ENABLED")
    else:
        summary.append("Anonymous Login : DISABLED")

    summary.append("")

    summary.append("-" * 60)
    summary.append("SHARED FOLDERS")
    summary.append("-" * 60)

    if smb_data["shares"]:

        for share in smb_data["shares"]:
            summary.append(f"• {share}")

    else:
        summary.append("No shared folders discovered.")

    summary.append("")

    summary.append("-" * 60)
    summary.append("RISK LEVEL")
    summary.append("-" * 60)

    summary.append(f"Overall Risk : {smb_data['risk']}")
    summary.append("")

    summary.append("-" * 60)
    summary.append("RECOMMENDATIONS")
    summary.append("-" * 60)

    if smb_data["anonymous_access"]:
        summary.append("• Disable anonymous SMB access.")
        summary.append("• Restrict share permissions.")
        summary.append("• Review exposed shared folders.")

    elif smb_data["signing"] == "Disabled":
        summary.append("• Enable SMB signing.")
        summary.append("• Review SMB security configuration.")

    else:
        summary.append("• SMB configuration appears secure.")
        summary.append("• Continue monitoring shared folders.")
        summary.append("• Keep SMB signing enabled.")

    summary.append("")
    summary.append("=" * 60)

    return "\n".join(summary)