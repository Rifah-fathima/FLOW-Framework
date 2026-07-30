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
        Raw ssh-audit output.
    """

    logger.info(f"Starting SSH Audit on {target}:{port}")

    ssh_audit_path = shutil.which("ssh-audit")

    print("\n========== SSH-AUDIT DEBUG ==========")
    print("Executable :", ssh_audit_path)
    print("Target     :", target)
    print("Port       :", port)
    print("=====================================\n")

    command = [
        "ssh-audit",
        "-p",
        str(port),
        target
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120
        )

        logger.info("SSH Audit Completed")

        print("\n========== SSH-AUDIT PROCESS ==========")
        print("Return Code :", result.returncode)

        print("\n----------- STDOUT -----------")
        print(result.stdout if result.stdout else "[EMPTY]")

        print("\n----------- STDERR -----------")
        print(result.stderr if result.stderr else "[EMPTY]")

        print("=======================================\n")

        # Prefer stdout if available
        if result.stdout.strip():
            return result.stdout

        # If stdout is empty, return stderr
        if result.stderr.strip():
            return result.stderr

        return ""

    except subprocess.TimeoutExpired:

        logger.error("SSH Audit Timed Out")

        return (
            "[FLOW] SSH Audit timed out.\n"
            "Target may be unreachable or filtering SSH."
        )

    except FileNotFoundError:

        logger.error("ssh-audit not installed")

        return (
            "[FLOW] ssh-audit is not installed.\n"
            "Install using:\n"
            "sudo apt install ssh-audit"
        )

    except Exception as e:

        logger.error(f"SSH Audit Error: {e}")

        return f"[FLOW] Error: {e}"