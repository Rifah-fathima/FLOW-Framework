def generate_ssh_findings(manager, parsed_data):
    """
    Generate SSH security findings and send them
    to the Findings Manager.
    """

    # ------------------------------------------------
    # Overall SSH Risk
    # ------------------------------------------------

    if parsed_data["risk"] != "Low":

        manager.add_finding(

            module="SSH",

            severity=parsed_data["risk"],

            title="SSH Security Issues Detected",

            description=(
                f"{parsed_data['fail_count']} FAIL and "
                f"{parsed_data['warn_count']} WARN findings detected."
            ),

            recommendation="Review ssh-audit recommendations."

        )

    # ------------------------------------------------
    # Banner Disclosure
    # ------------------------------------------------

    if parsed_data["banner"]:

        manager.add_finding(

            module="SSH",

            severity="Informational",

            title="SSH Banner Disclosure",

            description=parsed_data["banner"],

            recommendation="Hide or minimize version disclosure where possible."

        )

    # ------------------------------------------------
    # Weak Algorithms
    # ------------------------------------------------

    weak_algorithms = (
        parsed_data["fail_count"] +
        parsed_data["warn_count"]
    )

    if weak_algorithms > 0:

        manager.add_finding(

            module="SSH",

            severity="Medium",

            title="Weak SSH Algorithms Detected",

            description=(
                f"{weak_algorithms} weak or deprecated "
                "algorithms identified."
            ),

            recommendation=(
                "Disable deprecated KEX, ciphers, MACs "
                "and weak host keys."
            )

        )

    # ------------------------------------------------
    # Recommendations Available
    # ------------------------------------------------

    if parsed_data["recommendations"]:

        manager.add_finding(

            module="SSH",

            severity="Low",

            title="SSH Hardening Recommendations",

            description=(
                f"{len(parsed_data['recommendations'])} "
                "recommendations available."
            ),

            recommendation="Review ssh-audit recommendations."

        )