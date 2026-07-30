import subprocess


def run_sslscan(target):
    """
    Run SSLScan against a target.

    Args:
        target (str): Target hostname or IP.

    Returns:
        str: Raw SSLScan output.
    """

    command = [
        "sslscan",
        "--no-colour",
        target
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180
        )

        return result.stdout

    except subprocess.TimeoutExpired:
        return "[-] SSLScan timed out."

    except FileNotFoundError:
        return "[-] sslscan is not installed."

    except Exception as e:
        return f"[-] Error: {e}"