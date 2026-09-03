"""
FLOW Framework
SMB Scanner

Runs SMB enumeration using Nmap and smbclient.
"""

from core.scanner_base import ScannerBase
from utils.logger import logger


class SMBScanner(ScannerBase):
    """
    SMB enumeration scanner.

    Performs:
        - SMB OS discovery
        - SMB security mode detection
        - SMB share enumeration
    """

    def __init__(self):
        super().__init__("smb")

    # ==================================================
    # SMB SCAN
    # ==================================================

    def scan(self, target):
        """
        Run SMB enumeration against the target.

        Parameters
        ----------
        target : str
            Target IP address or hostname.

        Returns
        -------
        dict
            Raw outputs from Nmap and smbclient.
        """

        logger.info(
            f"Starting SMB Enumeration on {target}:445"
        )

        # ==================================================
        # TOOL AVAILABILITY
        # ==================================================

        if not self.tool_exists("nmap"):

            logger.error(
                "Nmap is not installed or not found in PATH."
            )

            return {
                "nmap_output": "",
                "smbclient_output": "",
                "error": "Nmap not found."
            }

        if not self.tool_exists("smbclient"):

            logger.error(
                "smbclient is not installed or not found in PATH."
            )

            return {
                "nmap_output": "",
                "smbclient_output": "",
                "error": "smbclient not found."
            }

        # ==================================================
        # NMAP COMMAND
        # ==================================================

        nmap_command = [
            "nmap",
            "-Pn",
            "-p445",
            "--script",
            "smb-os-discovery,smb-security-mode",
            target
        ]

        # ==================================================
        # SMBCLIENT COMMAND
        # ==================================================

        smbclient_command = [
            "smbclient",
            "-L",
            f"//{target}",
            "-N"
        ]

        # ==================================================
        # RUN NMAP
        # ==================================================

        nmap_result = self.execute(
            nmap_command,
            timeout=180
        )

        if not nmap_result["success"]:

            if nmap_result["return_code"] != -1:

                logger.warning(
                    f"Nmap returned exit code "
                    f"{nmap_result['return_code']}"
                )

            if nmap_result["error"]:

                logger.error(
                    f"Nmap SMB enumeration error: "
                    f"{nmap_result['error']}"
                )

        # Preserve original behavior:
        # stdout + stderr
        nmap_output = (
            nmap_result["stdout"] +
            nmap_result["stderr"]
        )

        # ==================================================
        # RUN SMBCLIENT
        # ==================================================

        smb_result = self.execute(
            smbclient_command,
            timeout=120
        )

        if not smb_result["success"]:

            if smb_result["return_code"] != -1:

                logger.warning(
                    f"smbclient returned exit code "
                    f"{smb_result['return_code']}"
                )

            if smb_result["error"]:

                logger.error(
                    f"smbclient enumeration error: "
                    f"{smb_result['error']}"
                )

        # Preserve original behavior:
        # stdout + stderr
        smbclient_output = (
            smb_result["stdout"] +
            smb_result["stderr"]
        )

        logger.info(
            "SMB Enumeration Completed"
        )

        # ==================================================
        # RETURN PARSER-COMPATIBLE RESULT
        # ==================================================

        return {
            "nmap_output": nmap_output,
            "smbclient_output": smbclient_output
        }


# ==================================================
# BACKWARD-COMPATIBLE FUNCTION
# ==================================================

def run_smb_scan(target):
    """
    Backward-compatible SMB scanner function.

    Existing FLOW workflow code can continue using:

        run_smb_scan(target)
    """

    scanner = SMBScanner()

    return scanner.scan(target)