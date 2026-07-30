from findings.findings_manager import FindingsManager

manager = FindingsManager("scanme.nmap.org")

manager.add_results(
    "nmap",
    [
        {
            "port": "80/tcp",
            "service": "http",
            "state": "open"
        }
    ]
)

manager.add_results(
    "gobuster",
    [
        {
            "path": "/admin",
            "status": 403
        }
    ]
)

print(manager.get_all())

manager.save_json()