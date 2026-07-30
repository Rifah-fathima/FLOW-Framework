import ipaddress
import re


def validate_target(target):
    """
    Validate whether the input is
    - IPv4
    - IPv6
    - Domain Name
    """

    # Check IP Address
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        pass

    # Check Domain Name
    domain_pattern = (
        r"^(?!-)[A-Za-z0-9-]{1,63}"
        r"(?<!-)(\.[A-Za-z]{2,})+$"
    )

    if re.match(domain_pattern, target):
        return True

    return False