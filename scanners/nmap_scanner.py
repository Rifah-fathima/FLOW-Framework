import subprocess


def run_nmap(target, ports=None):
    """
    Runs an Nmap service/version scan against the target.
    If ports are provided, only those ports are scanned.
    """

    command = [
        "nmap",
        "-Pn",
        "-sV"
    ]

    if ports:

        if isinstance(ports, list):
            port_string = ",".join(ports)
        else:
            port_string = str(ports)

        command.extend(["-p", port_string])

    command.append(target)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180
        )

        return result.stdout

    except subprocess.TimeoutExpired:
        return "[FLOW] ERROR: Nmap scan timed out after 180 seconds."

    except subprocess.CalledProcessError as error:
        return error.stderr

    except FileNotFoundError:
        return "[FLOW] ERROR: Nmap is not installed."

    except Exception as error:
        return f"[FLOW] ERROR: {error}"