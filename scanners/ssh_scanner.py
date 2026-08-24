"""
FLOW Framework
SSH Scanner

Runs ssh-audit using the common ScannerBase
execution interface.
"""

from core.scanner_base import ScannerBase
from utils.logger import logger


class SSHScanner(ScannerBase):
    """
    SSH security auditing scanner.
    """

    def __init__(self):
        super().__init__("ssh")

    def scan(self, target, port=22):
        """
        Run ssh-audit against the target.

        Parameters
        ----------
        target : str
            Target hostname or IP address.

        port : int
            SSH port. Default is 22.

        Returns
        -------
        str
            Raw ssh-audit output for parsing.
        """

        logger.info(
            f"Starting SSH Audit on {target}:{port}"
        )

        # ==================================================
        # TOOL CHECK
        # ==================================================

        if not self.tool_exists("ssh-audit"):

            logger.error(
                "ssh-audit not installed"
            )

            return (
                "[FLOW] ssh-audit is not installed.\n"
                "Install using:\n"
                "sudo apt install ssh-audit"
            )

        # ==================================================
        # COMMAND
        # ==================================================

        command = [
            "ssh-audit",
            "-p",
            str(port),
            target
        ]

        # ==================================================
        # EXECUTE
        # ==================================================

        result = self.execute(command)

        logger.info(
            "SSH Audit Completed"
        )

        # ==================================================
        # RETURN OUTPUT FOR PARSER
        # ==================================================

        if result["stdout"].strip():

            return result["stdout"]

        if result["stderr"].strip():

            return result["stderr"]

        # ==================================================
        # ERROR
        # ==================================================

        if result["error"]:

            logger.error(
                f"SSH Audit Error: {result['error']}"
            )

            return (
                f"[FLOW] SSH Audit Error: "
                f"{result['error']}"
            )

        return ""


# ==================================================
# BACKWARD-COMPATIBLE FUNCTION
# ==================================================

def run_ssh_audit(target, port=22):
    """
    Backward-compatible SSH scanner function.

    Existing FLOW workflow code can continue using:

        run_ssh_audit(target, port)
    """

    scanner = SSHScanner()

    return scanner.scan(
        target,
        port
    )