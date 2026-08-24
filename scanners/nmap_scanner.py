"""
FLOW Framework
Nmap Scanner

Runs Nmap service/version detection using the common
ScannerBase execution interface.
"""

from core.scanner_base import ScannerBase


class NmapScanner(ScannerBase):
    """
    Nmap scanner implementation.
    """

    def __init__(self):
        super().__init__("nmap")

    def scan(self, target, ports=None):
        """
        Run Nmap service/version detection.

        Parameters
        ----------
        target : str
            Target hostname or IP address.

        ports : list, str, or None
            Optional ports to scan.

        Returns
        -------
        str
            Raw Nmap output.
        """

        # ==================================================
        # TOOL CHECK
        # ==================================================

        if not self.tool_exists("nmap"):
            return "[FLOW] ERROR: Nmap is not installed."

        # ==================================================
        # BUILD COMMAND
        # ==================================================

        command = [
            "nmap",
            "-Pn",
            "-sV"
        ]

        if ports:

            if isinstance(ports, list):
                port_string = ",".join(
                    str(port)
                    for port in ports
                )

            else:
                port_string = str(ports)

            command.extend([
                "-p",
                port_string
            ])

        command.append(target)

        # ==================================================
        # EXECUTE
        # ==================================================

        result = self.execute(command)

        # ==================================================
        # RETURN OUTPUT
        # ==================================================

        if result["success"]:
            return result["stdout"]

        if result["stderr"]:
            return result["stderr"]

        if result["error"]:
            return (
                f"[FLOW] ERROR: {result['error']}"
            )

        return (
            "[FLOW] ERROR: "
            f"Nmap exited with code "
            f"{result['return_code']}."
        )


# ==================================================
# BACKWARD-COMPATIBLE FUNCTION
# ==================================================

def run_nmap(target, ports=None):
    """
    Backward-compatible Nmap scanner function.

    Existing FLOW workflow code can continue using:

        run_nmap(target, ports)
    """

    scanner = NmapScanner()

    return scanner.scan(
        target,
        ports
    )