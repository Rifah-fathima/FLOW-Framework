
def generate_gobuster_summary(results):
    """
    Generate a readable summary from parsed Gobuster results.
    Risk reflects potentially relevant discoveries, not
    confirmed vulnerabilities.
    """

    summary = [
        "=" * 50,
        "        FLOW - Gobuster Summary",
        "=" * 50,
        "",
    ]

    if not results:
        summary.append("No directories or files were discovered.")
        summary.append("")
        summary.append("Risk Level : Low")
        summary.append("Next Action: Continue Enumeration")
        return "\n".join(summary)

    summary.append("Discovered Paths")
    summary.append("-" * 20)

    for item in results:
        summary.append(
            f"✓ {item['path']}   (HTTP {item['status']})"
        )

    summary.append("")

    interesting_paths = {
        "/admin",
        "/login",
        "/backup",
        "/config",
        "/uploads",
        "/images",
    }

    sensitive_prefixes = (
        "/.git",
        "/.svn",
        "/.env",
        "/.htpasswd",
    )

    high_priority = False
    needs_verification = False

    for item in results:
        path = item.get("path", "").lower().rstrip("/")
        status = item.get("status", 0)

        # Ignore paths that explicitly deny access.
        if status == 403:
            continue

        # A successful response to a sensitive-looking path
        # warrants verification, but does not prove exposure.
        if (
            status in (200, 206)
            and any(
                path == prefix or path.startswith(prefix + "/")
                for prefix in sensitive_prefixes
            )
        ):
            high_priority = True

        # Redirects to sensitive-looking paths need inspection.
        elif (
            status in (301, 302, 307, 308)
            and any(
                path == prefix or path.startswith(prefix + "/")
                for prefix in sensitive_prefixes
            )
        ):
            needs_verification = True

        # These paths are enumeration leads, not proof of a flaw.
        elif status in (200, 206) and path in interesting_paths:
            needs_verification = True

    if high_priority:
        risk = "High"
        action = "Verify sensitive-path access and inspect response content"
    elif needs_verification:
        risk = "Medium"
        action = "Manually verify discovered paths and continue enumeration"
    else:
        risk = "Low"
        action = "Continue web enumeration and verify relevant discoveries"

    summary.append(f"Risk Level : {risk}")
    summary.append(f"Next Action: {action}")

    return "\n".join(summary)
