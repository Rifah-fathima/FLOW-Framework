"""
FLOW Framework
FTP Scanner

Runs FTP enumeration using Nmap FTP NSE scripts.
"""

from core.scanner_base import ScannerBase
from utils.logger import logger


class FTPScanner(ScannerBase):
    """
    FTP enumeration scanner.

    Uses Nmap to perform:
        - FTP version detection
        - Anonymous FTP login check
        - FTP system information detection
    """

    def __init__(self):
        super().__init__("ftp")

    # ==================================================
    # FTP SCAN
    # ==================================================

    def scan(self, target):
        """
        Run FTP enumeration against the target.

        Parameters
        ----------
        target : str
            Target IP address or hostname.

        Returns
        -------
        str
            Raw Nmap FTP scan output.
        """

        logger.info(
            f"Starting FTP Enumeration on {target}:21"
        )

        # ==================================================
        # TOOL CHECK
        # ==================================================

        if not self.tool_exists("nmap"):

            logger.error(
                "Nmap is not installed or not found in PATH."
            )

            return "ERROR: Nmap not found."

        # ==================================================
        # COMMAND
        # ==================================================

        command = [
            "nmap",
            "-Pn",
            "-sV",
            "-p21",
            "--script",
            "ftp-anon,ftp-syst",
            target
        ]

        # ==================================================
        # EXECUTE
        # ==================================================

        result = self.execute(
            command,
            timeout=180
        )

        # ==================================================
        # LOG NON-ZERO EXIT
        # ==================================================

        if not result["success"]:

            if result["return_code"] != -1:

                logger.warning(
                    f"Nmap returned exit code "
                    f"{result['return_code']}"
                )

            if result["error"]:

                logger.error(
                    f"FTP Enumeration Error: "
                    f"{result['error']}"
                )

        else:

            logger.info(
                "FTP Enumeration Completed"
            )

        # ==================================================
        # RETURN OUTPUT
        # ==================================================

        # Preserve the old scanner behavior:
        # stdout + stderr
        output = (
            result["stdout"] +
            result["stderr"]
        )

        return output


# ==================================================
# BACKWARD-COMPATIBLE FUNCTION
# ==================================================

def run_ftp_scan(target):
    """
    Backward-compatible FTP scanner function.

    Existing FLOW workflow code can continue using:

        run_ftp_scan(target)
    """

    scanner = FTPScanner()

    return scanner.scan(target)