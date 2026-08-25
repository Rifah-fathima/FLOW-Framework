"""
FLOW Framework
SSLScan Scanner

Runs SSLScan using the common ScannerBase execution interface.
"""

from core.scanner_base import ScannerBase
from utils.logger import logger


class SSLScanScanner(ScannerBase):
    """
    SSL/TLS security scanner.
    """

    def __init__(self):
        super().__init__("sslscan")

    def scan(self, target):
        """
        Run SSLScan against the target.

        Parameters
        ----------
        target : str
            Target hostname or IP address.

        Returns
        -------
        str
            Raw SSLScan output.
        """

        logger.info(
            f"Starting SSLScan on {target}"
        )

        # ==================================================
        # TOOL CHECK
        # ==================================================

        if not self.tool_exists("sslscan"):

            logger.error(
                "SSLScan is not installed"
            )

            return "[-] sslscan is not installed."

        # ==================================================
        # COMMAND
        # ==================================================

        command = [
            "sslscan",
            "--no-colour",
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
        # SUCCESS
        # ==================================================

        if result["success"]:

            logger.info(
                "SSLScan Completed"
            )

            return result["stdout"]

        # ==================================================
        # FALLBACK OUTPUT
        # ==================================================

        if result["stdout"].strip():

            logger.info(
                "SSLScan completed with non-zero status "
                "but produced output."
            )

            return result["stdout"]

        if result["stderr"].strip():

            logger.error(
                f"SSLScan Error: "
                f"{result['stderr'].strip()}"
            )

            return result["stderr"]

        # ==================================================
        # EXECUTION ERROR
        # ==================================================

        if result["error"]:

            logger.error(
                f"SSLScan Error: {result['error']}"
            )

            return (
                f"[-] SSLScan Error: "
                f"{result['error']}"
            )

        return ""


# ==================================================
# BACKWARD-COMPATIBLE FUNCTION
# ==================================================

def run_sslscan(target):
    """
    Backward-compatible SSLScan function.

    Existing FLOW workflow code can continue using:

        run_sslscan(target)
    """

    scanner = SSLScanScanner()

    return scanner.scan(target)