import re


def parse_gobuster_output(output):
    """
    Parses Gobuster output into structured data.
    """

    results = []

    pattern = r"^(\S+)\s+\(Status:\s+(\d+)\)"

    for line in output.splitlines():

        match = re.match(pattern, line)

        if match:
            path = "/" + match.group(1).lstrip("/")
            status = int(match.group(2))

            results.append({
                "path": path,
                "status": status
            })

    return results