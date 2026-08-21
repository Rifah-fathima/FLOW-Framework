"""
FLOW Framework
Module Registry

Maps detected services to scanner modules.
"""

MODULE_REGISTRY = {
    "ssh": [
        "ssh",
    ],

    "http": [
        "gobuster",
        "nikto",
        "whatweb",
    ],

    "https": [
        "gobuster",
        "nikto",
        "whatweb",
        "sslscan",
    ],

    "ftp": [
        "ftp",
    ],

    "smb": [
        "smb",
    ],
}


def get_modules(services):
    """
    Return unique modules based on detected services.

    Parameters
    ----------
    services : list

    Returns
    -------
    list
    """

    modules = []

    for service in services:

        service = service.lower()

        if service in MODULE_REGISTRY:

            for module in MODULE_REGISTRY[service]:

                if module not in modules:
                    modules.append(module)

    return modules