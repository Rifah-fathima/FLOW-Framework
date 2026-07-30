import subprocess
from utils.logger import logger


def run_smb_scan(target):
    """
    Runs SMB Enumeration.

    Features:
    - SMB OS Discovery
    - SMB Security Mode
    - SMB Share Enumeration

    Parameters:
        target (str): Target IP address or hostname.

    Returns:
        dict: Raw outputs from Nmap and smbclient.
    """

    logger.info(f"Starting SMB Enumeration on {target}:445")

    nmap_command = [
        "nmap",
        "-Pn",
        "-p445",
        "--script",
        "smb-os-discovery,smb-security-mode",
        target
    ]

    smbclient_command = [
        "smbclient",
        "-L",
        f"//{target}",
        "-N"
    ]

    try:

        nmap_result = subprocess.run(
            nmap_command,
            capture_output=True,
            text=True
        )

        if nmap_result.returncode != 0:
            logger.warning(
                f"Nmap returned exit code {nmap_result.returncode}"
            )

        smb_result = subprocess.run(
            smbclient_command,
            capture_output=True,
            text=True
        )

        if smb_result.returncode != 0:
            logger.warning(
                f"smbclient returned exit code {smb_result.returncode}"
            )

        logger.info("SMB Enumeration Completed")

        return {
            "nmap_output": nmap_result.stdout + nmap_result.stderr,
            "smbclient_output": smb_result.stdout + smb_result.stderr
        }

    except FileNotFoundError as error:

        logger.error(f"Required tool not found: {error}")

        return {
            "nmap_output": "",
            "smbclient_output": "",
            "error": str(error)
        }

    except Exception as error:

        logger.error(f"SMB Enumeration Failed: {error}")

        return {
            "nmap_output": "",
            "smbclient_output": "",
            "error": str(error)
        }