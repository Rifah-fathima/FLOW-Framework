import subprocess
from utils.logger import logger


def run_naabu(target):
    """
    Runs Naabu against the target and returns raw output.
    """

    logger.info(f"Starting Naabu Scan on {target}")

    command = [
        "naabu",
        "-host", target,
        "-silent"
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120
        )

        logger.info("Naabu Scan Completed")

        return result.stdout

    except subprocess.TimeoutExpired:

        logger.error("Naabu Scan Timed Out")
        return ""

    except Exception as e:

        logger.error(f"Naabu Error: {e}")
        return ""