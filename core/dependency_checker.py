"""
FLOW Framework
Dependency Checker

Checks Python and external tool dependencies required by FLOW.
"""

import shutil
import sys


PYTHON_PACKAGES = {
    "requests": "requests",
}

SYSTEM_TOOLS = {
    "nmap": "Nmap",
    "naabu": "Naabu",
    "gobuster": "Gobuster",
    "nikto": "Nikto",
    "ssh-audit": "SSH Audit",
    "sslscan": "SSLScan",
    "whatweb": "WhatWeb",
    "wpscan": "WPScan",
}


def check_python_packages():
    """
    Check required Python packages.

    Returns
    -------
    dict
        Package name -> availability.
    """

    results = {}

    for package, module in PYTHON_PACKAGES.items():

        try:
            __import__(module)
            results[package] = True

        except ImportError:
            results[package] = False

    return results


def check_system_tools():
    """
    Check required external security tools.

    Returns
    -------
    dict
        Tool name -> availability.
    """

    results = {}

    for command in SYSTEM_TOOLS:
        results[command] = shutil.which(command) is not None

    return results


def run_dependency_check():
    """
    Run the complete FLOW dependency check.

    Returns
    -------
    bool
        True if all dependencies are available.
    """

    python_results = check_python_packages()
    system_results = check_system_tools()

    print("=" * 60)
    print("                 FLOW SYSTEM CHECK")
    print("=" * 60)

    print("\nPython")
    print("-" * 60)
    print(f"Python version : {sys.version.split()[0]}")

    print("\nPython Packages")
    print("-" * 60)

    python_ok = True

    for package, available in python_results.items():

        if available:
            print(f"✓ {package}")
        else:
            print(f"✗ {package}  [MISSING]")
            python_ok = False

    print("\nSecurity Tools")
    print("-" * 60)

    tools_ok = True

    for command, available in system_results.items():

        display_name = SYSTEM_TOOLS[command]

        if available:
            print(f"✓ {display_name}")
        else:
            print(f"✗ {display_name}  [MISSING]")
            tools_ok = False

    print("\n" + "=" * 60)

    if python_ok and tools_ok:
        print("FLOW dependency check: PASSED")
        print("All required dependencies are available.")
    else:
        print("FLOW dependency check: FAILED")
        print("One or more dependencies are missing.")

    print("=" * 60)

    return python_ok and tools_ok


if __name__ == "__main__":
    run_dependency_check()
