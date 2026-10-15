
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
            If True, use a 1-minute Nikto scan limit.
            If False, run without Nikto's internal time limit.

        Returns
        -------
        str or None
            Raw Nikto output, or None if execution fails.
        """

        logger.info(f"Starting Nikto Scan on {target}")

        # ==================================================
        # TOOL CHECK
        # ==================================================

        if not self.tool_exists("nikto"):
            logger.error("Nikto is not installed")
            return None

        # ==================================================
        # COMMAND
        # ==================================================

        if quick:
            logger.info(
                "Nikto quick scan enabled (Max 1 minute)."
            )

            command = [
                "nikto",
                "-h", target,
                "-maxtime", "1m"
            ]

            execution_timeout = 90

        else:
            logger.info("Nikto full scan enabled.")

            command = [
                "nikto",
                "-h", target
            ]

            execution_timeout = 600

        # ==================================================
        # EXECUTE
        # ==================================================

        result = self.execute(
            command,
            timeout=execution_timeout
        )

        # ==================================================
        # HANDLE TIMEOUT / ERROR
        # ==================================================

        if result["error"]:
            logger.error(
                f"Nikto execution error: {result['error']}"
            )

            # Preserve any output produced before a timeout.
            if result["stdout"].strip():
                return result["stdout"]

            return None

        # ==================================================
        # SUCCESS
        # ==================================================

        if result["success"]:
            logger.info("Nikto Scan Completed")
            return result["stdout"]

        # ==================================================
        # NON-ZERO EXIT
        # ==================================================

        logger.warning(
            f"Nikto exited with code {result['return_code']}"
        )

        if result["stderr"].strip():
            logger.warning(result["stderr"].strip())

        # Preserve useful output even if Nikto exits non-zero.
        if result["stdout"].strip():
            return result["stdout"]

        return None


# ==================================================
# BACKWARD-COMPATIBLE FUNCTION
# ==================================================

def run_nikto(target, quick=True):
    """
    Backward-compatible Nikto scanner function.

    Examples:
        run_nikto(target)
        run_nikto(target, quick=False)
    """

    scanner = NiktoScanner()

    return scanner.scan(
        target,
        quick
    )
