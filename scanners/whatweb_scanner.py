"""
FLOW Framework
WhatWeb Scanner

Web technology fingerprinting using WhatWeb.
"""

from core.scanner_base import ScannerBase


class WhatWebScanner(ScannerBase):
    """
    Scanner implementation for WhatWeb.

    Performs web technology fingerprinting against a target.
    """

    def __init__(self):
        super().__init__("whatweb")

    def scan(self, target):
        print("[FLOW] Running WhatWeb...")

        if not self.tool_exists("whatweb"):
            print("[ERROR] WhatWeb is not installed.")
            return ""

        # Ensure WhatWeb receives a complete URL.
        if not target.startswith(("http://", "https://")):
            target = f"http://{target}"

        cmd = ["whatweb", target]

        print("Command:", " ".join(cmd))

        result = self.execute(
            cmd,
            timeout=180
        )

        print("Return code:", result["return_code"])

        print("STDOUT:")
        print(result["stdout"])

        print("STDERR:")
        print(result["stderr"])

        if result["error"]:
            print("[ERROR]", result["error"])

        return result["stdout"]


def run_whatweb(target):
    """
    Backward-compatible wrapper used by FLOW workflow.
    """

    scanner = WhatWebScanner()

    return scanner.scan(target)