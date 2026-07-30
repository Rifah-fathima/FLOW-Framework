import subprocess
from utils.logger import logger


def run_ftp_scan(target):
    """
    Runs FTP Enumeration using Nmap.

    Features:
    - FTP Version Detection
    - Anonymous Login Check
    - FTP System Information

    Parameters:
        target (str): Target IP address or hostname.

    Returns:
        str: Raw Nmap FTP scan output.
    """

    logger.info(f"Starting FTP Enumeration on {target}:21")

    command = [
        "nmap",
        "-Pn",
        "-sV",
        "-p21",
        "--script",
        "ftp-anon,ftp-syst",
        target
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            logger.warning(
                f"Nmap returned exit code {result.returncode}"
            )

        logger.info("FTP Enumeration Completed")

        return result.stdout + result.stderr

    except FileNotFoundError:

        logger.error("Nmap is not installed or not found in PATH.")

        return "ERROR: Nmap not found."

    except Exception as error:

        logger.error(f"FTP Enumeration Failed: {error}")

        return str(error)