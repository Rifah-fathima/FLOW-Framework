from scanners.nikto_scanner import run_nikto
from parsers.nikto_parser import parse_nikto_output
from summaries.nikto_summary import generate_nikto_summary

# Quick scan
output = run_nikto(
    "http://scanme.nmap.org",
    quick=True
)

if output:

    findings = parse_nikto_output(output)

    print("\n========== FINDINGS ==========")

    for finding in findings:
        print(finding)

    print("\n========== SUMMARY ==========")

    summary = generate_nikto_summary(findings)

    print(summary)