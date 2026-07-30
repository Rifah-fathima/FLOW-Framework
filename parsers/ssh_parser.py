import re


def parse_ssh_output(output):
    """
    Parse ssh-audit output into structured data.
    """

    # Remove ANSI escape sequences
    output = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", output)

    parsed = {
        "banner": "",
        "software": "",
        "compression": "",
        "kex_algorithms": [],
        "host_keys": [],
        "ciphers": [],
        "macs": [],
        "fingerprints": [],
        "recommendations": [],
        "fail_count": 0,
        "warn_count": 0,
        "info_count": 0,
        "risk": "Low",
    }

    for raw_line in output.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        # ----------------------------
        # General Information
        # ----------------------------

        if "(gen) banner:" in line:
            parsed["banner"] = line.split("banner:", 1)[1].strip()

        elif "(gen) software:" in line:
            parsed["software"] = line.split("software:", 1)[1].strip()

        elif "(gen) compression:" in line:
            parsed["compression"] = line.split("compression:", 1)[1].strip()

        # ----------------------------
        # Security Findings
        # ----------------------------

        parsed["fail_count"] += line.count("[fail]")
        parsed["warn_count"] += line.count("[warn]")
        parsed["info_count"] += line.count("[info]")

        # ----------------------------
        # KEX
        # ----------------------------

        if "(kex)" in line:
            value = line.split("(kex)", 1)[1]
            value = value.split("--", 1)[0].strip()
            if value:
                parsed["kex_algorithms"].append(value)

        # ----------------------------
        # Host Keys
        # ----------------------------

        elif "(key)" in line:
            value = line.split("(key)", 1)[1]
            value = value.split("--", 1)[0].strip()
            if value:
                parsed["host_keys"].append(value)

        # ----------------------------
        # Ciphers
        # ----------------------------

        elif "(enc)" in line:
            value = line.split("(enc)", 1)[1]
            value = value.split("--", 1)[0].strip()
            if value:
                parsed["ciphers"].append(value)

        # ----------------------------
        # MACs
        # ----------------------------

        elif "(mac)" in line:
            value = line.split("(mac)", 1)[1]
            value = value.split("--", 1)[0].strip()
            if value:
                parsed["macs"].append(value)

        # ----------------------------
        # Fingerprints
        # ----------------------------

        elif "(fin)" in line:
            value = line.split("(fin)", 1)[1].strip()
            if value:
                parsed["fingerprints"].append(value)

        # ----------------------------
        # Recommendations
        # ----------------------------

        elif "(rec)" in line:
            value = line.split("(rec)", 1)[1].strip()
            if value:
                parsed["recommendations"].append(value)

    # Remove duplicates
    parsed["kex_algorithms"] = list(dict.fromkeys(parsed["kex_algorithms"]))
    parsed["host_keys"] = list(dict.fromkeys(parsed["host_keys"]))
    parsed["ciphers"] = list(dict.fromkeys(parsed["ciphers"]))
    parsed["macs"] = list(dict.fromkeys(parsed["macs"]))
    parsed["fingerprints"] = list(dict.fromkeys(parsed["fingerprints"]))
    parsed["recommendations"] = list(dict.fromkeys(parsed["recommendations"]))

    # Risk Rating
    if parsed["fail_count"] >= 20:
        parsed["risk"] = "Critical"
    elif parsed["fail_count"] >= 10:
        parsed["risk"] = "High"
    elif parsed["warn_count"] >= 10:
        parsed["risk"] = "Medium"
    else:
        parsed["risk"] = "Low"

    return parsed