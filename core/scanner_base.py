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

    Provides:
        - Common scanner identity
        - Security tool availability checking
        - Standardized command execution
        - Configurable execution timeout
        - Standardized execution results
    """

    def __init__(self, module_name):
        self.module_name = module_name

    # ==================================================
    # TOOL AVAILABILITY
    # ==================================================

    def tool_exists(self, tool_name):
        """
        Check whether the required security tool is installed.

        Parameters
        ----------
        tool_name : str
            Name of the executable to check.

        Returns
        -------
        bool
            True if the tool is available.
        """

        return shutil.which(tool_name) is not None

    # ==================================================
    # SCANNER INTERFACE
    # ==================================================

    def scan(self, *args, **kwargs):
        """
        Common scanner interface.

        Child scanner classes should override this method
        with their own scan implementation.
        """

        raise NotImplementedError(
            f"{self.__class__.__name__} must implement "
            f"the scan() method."
        )

    # ==================================================
    # COMMAND EXECUTION
    # ==================================================

    def execute(self, command, timeout=600):
        """
        Execute a security tool command and return a
        standardized result.

        Parameters
        ----------
        command : list
            Command and arguments to execute.

        timeout : int or float
            Maximum execution time in seconds.

        Returns
        -------
        dict
            Standardized execution result.
        """

        start = time.time()

        try:

            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            end = time.time()

            return {
                "module": self.module_name,
                "success": process.returncode == 0,
                "return_code": process.returncode,
                "execution_time": round(
                    end - start,
                    2
                ),
                "stdout": process.stdout,
                "stderr": process.stderr,
                "error": None
            }

        # ==================================================
        # TIMEOUT
        # ==================================================

        except subprocess.TimeoutExpired:

            end = time.time()

            return {
                "module": self.module_name,
                "success": False,
                "return_code": -1,
                "execution_time": round(
                    end - start,
                    2
                ),
                "stdout": "",
                "stderr": "",
                "error": "Execution timed out."
            }

        # ==================================================
        # GENERAL ERROR
        # ==================================================

        except Exception as e:

            end = time.time()

            return {
                "module": self.module_name,
                "success": False,
                "return_code": -1,
                "execution_time": round(
                    end - start,
                    2
                ),
                "stdout": "",
                "stderr": "",
                "error": str(e)
            }