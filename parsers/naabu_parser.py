def parse_naabu_output(output):
    """
    Parse Naabu output into a list of unique open ports.
    """

    ports = []
    seen = set()

    for line in output.splitlines():

        line = line.strip()

        if not line:
            continue

        try:
            host, port = line.split(":")
            port = int(port)

            # Skip duplicate host:port combinations
            if (host, port) in seen:
                continue

            seen.add((host, port))

            ports.append({
                "host": host,
                "port": port
            })

        except ValueError:
            continue

    return ports