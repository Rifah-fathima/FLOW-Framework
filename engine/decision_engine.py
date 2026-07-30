"""
FLOW Decision Engine

This module decides which scanners or enumeration steps
should run based on the services detected by Nmap.
"""


def get_next_actions(scan_results):

    actions = []

    for service in scan_results:

        service_name = service["service"].lower().strip()
        port = service["port"]
        state = service["state"].lower().strip()

        if state != "open":
            continue

        port_number = port.split("/")[0]

        # -----------------------------------------
        # HTTP
        # -----------------------------------------

        if service_name == "http" or port_number == "80":

            if "gobuster" not in actions:
                actions.append("gobuster")

            if "nikto" not in actions:
                actions.append("nikto")

        # -----------------------------------------
        # HTTPS
        # -----------------------------------------

        elif (
            service_name in [
                "https",
                "ssl/http",
                "ssl/https",
                "https?"
            ]
            or port_number == "443"
        ):

            if "gobuster" not in actions:
                actions.append("gobuster")

            if "nikto" not in actions:
                actions.append("nikto")

            if "sslscan" not in actions:
                actions.append("sslscan")

        # -----------------------------------------
        # SSH
        # -----------------------------------------

        elif (
            port_number == "22"
            or service_name in [
                "ssh",
                "tcpwrapped"
            ]
        ):

            if "ssh_enum" not in actions:
                actions.append("ssh_enum")

        # -----------------------------------------
        # FTP
        # -----------------------------------------

        elif (
            port_number == "21"
            or service_name.startswith("ftp")
        ):

            if "ftp_enum" not in actions:
                actions.append("ftp_enum")

        # -----------------------------------------
        # SMB
        # -----------------------------------------

        elif (
            port_number == "445"
            or port_number == "139"
            or service_name in [
                "microsoft-ds",
                "netbios-ssn",
                "smb"
            ]
        ):

            if "smb_enum" not in actions:
                actions.append("smb_enum")

        # -----------------------------------------
        # DNS
        # -----------------------------------------

        elif (
            port_number == "53"
            or service_name == "domain"
        ):

            if "dns_enum" not in actions:
                actions.append("dns_enum")

    return actions