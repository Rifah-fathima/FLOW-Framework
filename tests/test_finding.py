from models.finding import Finding

finding = Finding(
    tool="Nikto",
    severity="HIGH",
    category="Web Server",
    title="Outdated Apache Version",
    description="Apache 2.4.7 is outdated.",
    target="http://scanme.nmap.org",
    recommendation="Upgrade Apache to the latest supported version."
)

print(finding)
print()
print(finding.to_dict())