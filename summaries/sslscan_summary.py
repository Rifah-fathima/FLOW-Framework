def generate_sslscan_summary(data):
    """
    Generate a human-readable SSLScan summary.
    """

    lines = []

    lines.append("=" * 50)
    lines.append("SSL/TLS SECURITY SUMMARY")
    lines.append("=" * 50)

    # Protocols
    lines.append("\nSupported Protocols:")

    for protocol, enabled in data["tls_versions"].items():
        if enabled:
            if protocol in ["TLSv1.0", "TLSv1.1"]:
                lines.append(f"⚠ {protocol} enabled (Legacy)")
            else:
                lines.append(f"✔ {protocol}")
        else:
            lines.append(f"✘ {protocol}")

    # Compression
    lines.append("\nCompression:")
    lines.append(
        "✔ Disabled"
        if not data["compression"]
        else "⚠ Enabled"
    )

    # Heartbleed
    lines.append("\nHeartbleed:")
    lines.append(
        "✔ Not Vulnerable"
        if not data["heartbleed"]
        else "❌ Vulnerable"
    )

    # Renegotiation
    lines.append("\nSecure Renegotiation:")
    lines.append(
        "✔ Supported"
        if data["secure_renegotiation"]
        else "⚠ Not Supported"
    )

    # Certificate
    cert = data["certificate"]

    lines.append("\nCertificate")
    lines.append(f"Subject : {cert['subject']}")
    lines.append(f"Issuer  : {cert['issuer']}")
    lines.append(f"Valid From : {cert['valid_from']}")
    lines.append(f"Valid To   : {cert['valid_to']}")

    # Cipher count
    lines.append("\nCipher Suites")
    lines.append(
        f"Supported Ciphers : {len(data['supported_ciphers'])}"
    )

    # Overall Rating
    lines.append("\nOverall Assessment")

    if data["heartbleed"]:
        rating = "HIGH RISK"
    elif data["tls_versions"].get("TLSv1.0") or data["tls_versions"].get("TLSv1.1"):
        rating = "GOOD (Legacy TLS Detected)"
    else:
        rating = "SECURE"

    lines.append(rating)

    return "\n".join(lines)