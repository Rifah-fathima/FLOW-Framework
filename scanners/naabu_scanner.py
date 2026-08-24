"""
FLOW Framework
Naabu Scanner

Runs Naabu port discovery using the common
ScannerBase execution interface.
"""

from core.scanner_base import ScannerBase
from utils.logger import logger


class NaabuScanner(ScannerBase):
    """
    Naabu port discovery scanner.
    """

    def __init__(self):
        super().__init__("naabu")

    def scan(self, target):
        """
        Run Naabu against the target.

        Parameters
        ----------
        target : str
            Target hostname or IP address.

        Returns
        -------
        str
            Raw Naabu output.
        """

        logger.info(
            f"Starting Naabu Scan on {target}"
        )

        # ==================================================
        # TOOL CHECK
        # ==================================================

        if not self.tool_exists("naabu"):

            logger.error(
                "Naabu is not installed"
            )

            return ""

        # ==================================================
        # COMMAND
        # ==================================================

        command = [
            "naabu",
            "-host",
            target,
            "-silent"
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
                "Naabu Scan Completed"
            )

            return result["stdout"]

        # ==================================================
        # ERROR
        # ==================================================

        if result["error"]:

            logger.error(
                f"Naabu Error: {result['error']}"
            )

        elif result["stderr"]:

            logger.error(
                f"Naabu Error: {result['stderr'].strip()}"
            )

        else:

            logger.error(
                "Naabu Scan Failed"
            )

        return ""


# ==================================================
# BACKWARD-COMPATIBLE FUNCTION
# ==================================================

def run_naabu(target):
    """
    Backward-compatible Naabu scanner function.

    Existing FLOW workflow code can continue using:

        run_naabu(target)
    """

    scanner = NaabuScanner()

    return scanner.scan(target)