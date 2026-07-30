import re


def parse_sslscan_output(output):
    """
    Parse raw SSLScan output into a structured dictionary.
    """

    results = {
        "tls_versions": {},
        "heartbleed": False,
        "compression": False,
        "secure_renegotiation": False,
        "certificate": {
            "subject": None,
            "issuer": None,
            "valid_from": None,
            "valid_to": None,
        },
        "supported_ciphers": []
    }

    # ----------------------------
    # TLS Versions
    # ----------------------------
    protocols = [
        "SSLv2",
        "SSLv3",
        "TLSv1.0",
        "TLSv1.1",
        "TLSv1.2",
        "TLSv1.3"
    ]

    for protocol in protocols:
        match = re.search(rf"{re.escape(protocol)}\s+(enabled|disabled)", output)
        if match:
            results["tls_versions"][protocol] = (
                match.group(1).lower() == "enabled"
            )

    # ----------------------------
    # Compression
    # ----------------------------
    if "Compression disabled" in output:
        results["compression"] = False
    elif "Compression enabled" in output:
        results["compression"] = True

    # ----------------------------
    # Secure Renegotiation
    # ----------------------------
    if "Secure session renegotiation supported" in output:
        results["secure_renegotiation"] = True

    # ----------------------------
    # Heartbleed
    # ----------------------------
    if "not vulnerable to heartbleed" in output.lower():
        results["heartbleed"] = False
    elif "vulnerable to heartbleed" in output.lower():
        results["heartbleed"] = True

    # ----------------------------
    # Certificate
    # ----------------------------
    subject = re.search(r"Subject:\s+(.*)", output)
    if subject:
        results["certificate"]["subject"] = subject.group(1).strip()

    issuer = re.search(r"Issuer:\s+(.*)", output)
    if issuer:
        results["certificate"]["issuer"] = issuer.group(1).strip()

    valid_from = re.search(r"Not valid before:\s+(.*)", output)
    if valid_from:
        results["certificate"]["valid_from"] = valid_from.group(1).strip()

    valid_to = re.search(r"Not valid after:\s+(.*)", output)
    if valid_to:
        results["certificate"]["valid_to"] = valid_to.group(1).strip()

    # ----------------------------
    # Cipher Suites
    # ----------------------------
    for line in output.splitlines():
        if line.startswith("Accepted") or line.startswith("Preferred"):
            results["supported_ciphers"].append(line.strip())

    return results