def parse_nmap_output(output):
    """
    Parses Nmap output and extracts open ports,
    services, and versions.
    """

    parsed_results = []

    lines = output.splitlines()

    for line in lines:

        if "/tcp" in line or "/udp" in line:

            parts = line.split()

            if len(parts) >= 3:

                parsed_results.append({
                    "port": parts[0],
                    "state": parts[1],
                    "service": parts[2],
                    "version": " ".join(parts[3:]) if len(parts) > 3 else ""
                })

    return parsed_results