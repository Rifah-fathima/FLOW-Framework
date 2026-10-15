
"""
FLOW Framework
Gobuster Findings

Converts security-relevant Gobuster discoveries
into normalized FLOW security findings.
"""


def generate_gobuster_findings(manager, results):
    """Generate findings while considering HTTP status codes."""

    sensitive_paths = {
        "/.git": ("Exposed Git Repository", "version-control files"),
        "/.svn": ("Exposed SVN Repository", "version-control metadata"),
        "/.htpasswd": ("Exposed Password File", "password files"),
        "/.env": ("Exposed Environment Configuration", "environment configuration"),
    }

    for item in results:
        path = item.get("path", "").strip()
        status = item.get("status", 0)
        normalized_path = path.lower().rstrip("/")

        # Ignore unrelated paths.
        matched = next(
            (
                (prefix, details)
                for prefix, details in sensitive_paths.items()
                if normalized_path == prefix
                or normalized_path.startswith(prefix + "/")
            ),
            None,
        )

        if not matched:
            continue

        prefix, (title, resource_type) = matched

        # HTTP 403 means access was forbidden, not that exposure occurred.
        if status == 403:
            continue

        if status in (200, 206):
            severity = "High"
            description = (
                f"Potentially sensitive {resource_type} may be accessible "
                f"at {path} (HTTP {status}). Verify the response content "
                "before confirming exposure."
            )
        elif status in (301, 302, 307, 308):
            severity = "Informational"
            description = (
                f"A potentially sensitive path was discovered at {path} "
                f"(HTTP {status}). Follow and inspect the redirect to "
                "determine whether sensitive content is accessible."
            )
        else:
            # Do not classify unexpected status codes as confirmed exposure.
            continue

        manager.add_finding(
            module="Gobuster",
            severity=severity,
            title=title if status in (200, 206) else f"Potential {title}",
            description=description,
            recommendation=(
                f"Verify access controls for {resource_type}. "
                "Remove sensitive files from the web root and restrict "
                "public access where appropriate."
            ),
        )
