"""
FLOW Framework
Scanner Base

Provides a common interface for all scanners.
"""

import shutil
import subprocess
import time


class ScannerBase:
    """
    Base class for all FLOW scanners.
    """

    def __init__(self, module_name):
        self.module_name = module_name

    def tool_exists(self, tool_name):
        """
        Check whether the required tool is installed.
        """
        return shutil.which(tool_name) is not None

    def execute(self, command):
        """
        Execute a command and return a standardized result.
        """

        start = time.time()

        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=600
            )

            end = time.time()

            return {
                "module": self.module_name,
                "success": process.returncode == 0,
                "return_code": process.returncode,
                "execution_time": round(end - start, 2),
                "stdout": process.stdout,
                "stderr": process.stderr,
                "error": None
            }

        except subprocess.TimeoutExpired:

            end = time.time()

            return {
                "module": self.module_name,
                "success": False,
                "return_code": -1,
                "execution_time": round(end - start, 2),
                "stdout": "",
                "stderr": "",
                "error": "Execution timed out."
            }

        except Exception as e:

            end = time.time()

            return {
                "module": self.module_name,
                "success": False,
                "return_code": -1,
                "execution_time": round(end - start, 2),
                "stdout": "",
                "stderr": "",
                "error": str(e)
            }