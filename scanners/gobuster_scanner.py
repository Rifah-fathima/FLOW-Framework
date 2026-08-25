"""
FLOW Framework
Gobuster Scanner

Runs Gobuster directory enumeration using the common
ScannerBase execution interface.
"""

from core.scanner_base import ScannerBase

from config.settings import DEFAULT_WORDLIST
from utils.logger import logger


class GobusterScanner(ScannerBase):
    """
    Gobuster directory enumeration scanner.
    """

    def __init__(self):
        super().__init__("gobuster")

    def scan(self, target):
        """
        Run Gobuster directory enumeration.

        Parameters
        ----------
        target : str
            Target hostname or IP address.

        Returns
        -------
        str
            Raw Gobuster output.
        """

        logger.info("Starting Gobuster Scan")

        # ==================================================
        # TOOL CHECK
        # ==================================================

        if not self.tool_exists("gobuster"):

            logger.error(
                "Gobuster is not installed"
            )

            return ""

        # ==================================================
        # WORDLIST CHECK
        # ==================================================

        if not DEFAULT_WORDLIST:

            logger.error(
                "Gobuster wordlist is not configured"
            )

            return ""

        # ==================================================
        # COMMAND
        # ==================================================

        command = [
            "gobuster",
            "dir",
            "-u",
            f"http://{target}",
            "-w",
            DEFAULT_WORDLIST,
        ]

        # ==================================================
        # EXECUTE
        # ==================================================

        result = self.execute(command)

        # ==================================================
        # SUCCESS
        # ==================================================

        if result["success"]:

            logger.info(
                "Gobuster Scan Completed"
            )

            return result["stdout"]

        # ==================================================
        # ERROR
        # ==================================================

        if result["error"]:

            logger.error(
                f"Gobuster Error: {result['error']}"
            )

        elif result["stderr"]:

            logger.error(
                f"Gobuster Error: "
                f"{result['stderr'].strip()}"
            )

        else:

            logger.error(
                "Gobuster Scan Failed"
            )

        return ""


# ==================================================
# BACKWARD-COMPATIBLE FUNCTION
# ==================================================

def run_gobuster(target):
    """
    Backward-compatible Gobuster scanner function.

    Existing FLOW workflow code can continue using:

        run_gobuster(target)
    """

    scanner = GobusterScanner()

    return scanner.scan(target)