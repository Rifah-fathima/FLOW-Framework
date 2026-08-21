import subprocess
import shutil

from utils.logger import logger


def run_ssh_audit(target, port=22):
    """
    Runs ssh-audit against the target.

    Parameters
    ----------
    target : str
        Target hostname or IP address.

    port : int
        SSH port (default: 22)

    Returns
    -------
    str
        Raw ssh-audit output for parsing.
    """

    logger.info(
        f"Starting SSH Audit on {target}:{port}"
    )

    # ==================================================
    # SSH-AUDIT AVAILABILITY
    # ==================================================

    ssh_audit_path = shutil.which("ssh-audit")

    if not ssh_audit_path:

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
        ssh_audit_path,
        "-p",
        str(port),
        target
    ]

    # ==================================================
    # RUN SSH-AUDIT
    # ==================================================

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120
        )

        logger.info(
            "SSH Audit Completed"
        )

        # ==================================================
        # RETURN OUTPUT FOR PARSER
        # ==================================================

        # Prefer stdout
        if result.stdout.strip():
            return result.stdout

        # Fall back to stderr
        if result.stderr.strip():
            return result.stderr

        return ""

    # ==================================================
    # TIMEOUT
    # ==================================================

    except subprocess.TimeoutExpired:

        logger.error(
            "SSH Audit Timed Out"
        )

        return (
            "[FLOW] SSH Audit timed out.\n"
            "Target may be unreachable or filtering SSH."
        )

    # ==================================================
    # COMMAND NOT FOUND
    # ==================================================

    except FileNotFoundError:

        logger.error(
            "ssh-audit not installed"
        )

        return (
            "[FLOW] ssh-audit is not installed.\n"
            "Install using:\n"
            "sudo apt install ssh-audit"
        )

    # ==================================================
    # GENERAL ERROR
    # ==================================================

    except Exception as e:

        logger.error(
            f"SSH Audit Error: {e}"
        )

        return f"[FLOW] Error: {e}"