import re


def parse_smb_output(scan_data):
    """
    Parses SMB scan results from Nmap and smbclient.

    Parameters:
        scan_data (dict):
            {
                "nmap_output": "...",
                "smbclient_output": "..."
            }

    Returns:
        dict: Parsed SMB information.
    """

    nmap_output = scan_data.get("nmap_output", "")
    smb_output = scan_data.get("smbclient_output", "")

    parsed = {
        "computer_name": "Unknown",
        "os": "Unknown",
        "domain": "Unknown",
        "workgroup": "Unknown",
        "signing": "Unknown",
        "anonymous_access": False,
        "shares": [],
        "risk": "Low"
    }

    # -----------------------------
    # Computer Name
    # -----------------------------
    match = re.search(r"Computer name:\s*(.*)", nmap_output)
    if match:
        parsed["computer_name"] = match.group(1).strip()

    # -----------------------------
    # Operating System
    # -----------------------------
    match = re.search(r"OS:\s*(.*)", nmap_output)
    if match:
        parsed["os"] = match.group(1).strip()

    # -----------------------------
    # Domain
    # -----------------------------
    match = re.search(r"Domain name:\s*(.*)", nmap_output)
    if match:
        parsed["domain"] = match.group(1).strip()

    # -----------------------------
    # Workgroup
    # -----------------------------
    match = re.search(r"Workgroup:\s*(.*)", nmap_output)
    if match:
        parsed["workgroup"] = match.group(1).strip()

    # -----------------------------
    # SMB Signing
    # -----------------------------
    match = re.search(r"Message signing enabled but not required", nmap_output)

    if match:
        parsed["signing"] = "Enabled (Not Required)"

    elif "Message signing enabled and required" in nmap_output:
        parsed["signing"] = "Required"

    elif "Message signing disabled" in nmap_output:
        parsed["signing"] = "Disabled"

    # -----------------------------
    # Anonymous Login
    # -----------------------------
    if "Anonymous login successful" in smb_output:
        parsed["anonymous_access"] = True

    # -----------------------------
    # Shares
    # -----------------------------
    for line in smb_output.splitlines():

        line = line.strip()

        if (
            line
            and "Disk" in line
            and "Sharename" not in line
            and "---------" not in line
        ):

            parts = line.split()

            if parts:
                parsed["shares"].append(parts[0])

    # -----------------------------
    # Risk Calculation
    # -----------------------------
    if parsed["anonymous_access"]:
        parsed["risk"] = "High"

    elif parsed["signing"] == "Disabled":
        parsed["risk"] = "Medium"

    return parsed