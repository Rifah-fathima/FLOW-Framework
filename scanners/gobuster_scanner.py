import subprocess

from config.settings import DEFAULT_WORDLIST
from utils.logger import logger


def run_gobuster(target):
    """
    Runs Gobuster directory enumeration against the target.
    Returns the raw output.
    """

    logger.info("Starting Gobuster Scan")

    command = [
        "gobuster",
        "dir",
        "-u",
        f"http://{target}",
        "-w",
        DEFAULT_WORDLIST,
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )

        logger.info("Gobuster Scan Completed")

        if result.stderr:
            print("Gobuster STDERR:")
            print(result.stderr)

        return result.stdout

    except Exception as error:
        logger.error(f"Gobuster Error: {error}")
        return ""