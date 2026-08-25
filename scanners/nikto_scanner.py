"""
FLOW Framework
Nikto Scanner

Runs Nikto web-server scanning using the common
ScannerBase execution interface.
"""

from core.scanner_base import ScannerBase
from utils.logger import logger


class NiktoScanner(ScannerBase):
    """
    Nikto web-server scanner.
    """

    def __init__(self):
        super().__init__("nikto")

    def scan(self, target, quick=True):
        """
        Run a Nikto scan.

        Parameters
        ----------
        target : str
            Target hostname or IP address.

        quick : bool
            If True, run a maximum 3-minute scan.
            If False, run a full scan.

        Returns
        -------
        str or None
            Raw Nikto output.
        """

        logger.info(
            f"Starting Nikto Scan on {target}"
        )

        # ==================================================
        # TOOL CHECK
        # ==================================================

        if not self.tool_exists("nikto"):

            logger.error(
                "Nikto is not installed"
            )

            return None

        # ==================================================
        # COMMAND
        # ==================================================

        if quick:

            logger.info(
                "Nikto quick scan enabled "
                "(Max 3 minutes)."
            )

            command = [
                "nikto",
                "-h",
                target,
                "-maxtime",
                "3m"
            ]

        else:

            logger.info(
                "Nikto full scan enabled."
            )

            command = [
                "nikto",
                "-h",
                target
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
                "Nikto Scan Completed"
            )

            return result["stdout"]

        # ==================================================
        # ERROR
        # ==================================================

        if result["error"]:

            logger.error(
                f"Nikto Error: {result['error']}"
            )

        elif result["stderr"]:

            logger.error(
                f"Nikto Error: "
                f"{result['stderr'].strip()}"
            )

        else:

            logger.error(
                "Nikto Scan Failed"
            )

        # Return stdout if Nikto produced useful
        # output despite a non-zero return code.
        if result["stdout"].strip():

            return result["stdout"]

        return None


# ==================================================
# BACKWARD-COMPATIBLE FUNCTION
# ==================================================

def run_nikto(target, quick=True):
    """
    Backward-compatible Nikto scanner function.

    Existing FLOW workflow code can continue using:

        run_nikto(target)
        run_nikto(target, quick=False)
    """

    scanner = NiktoScanner()

    return scanner.scan(
        target,
        quick
    )