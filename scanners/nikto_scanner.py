import subprocess


def run_nikto(target, quick=True):
    """
    Runs a Nikto scan.

    quick=True  -> Fast scan (default)
    quick=False -> Full scan
    """

    print("\n[FLOW] Running Nikto...")

    if quick:
        print("[FLOW] Quick scan enabled (Max 3 minutes).")

        command = [
            "nikto",
            "-h",
            target,
            "-maxtime",
            "3m"
        ]

    else:

        print("[FLOW] Full scan enabled.")

        command = [
            "nikto",
            "-h",
            target
        ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=190,
            check=False
        )

        return result.stdout

    except subprocess.TimeoutExpired:

        print("[ERROR] Nikto scan timed out.")

        return None

    except FileNotFoundError:

        print("[ERROR] Nikto is not installed.")

        return None