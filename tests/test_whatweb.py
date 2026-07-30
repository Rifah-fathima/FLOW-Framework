from scanners.whatweb_scanner import run_whatweb
from parsers.whatweb_parser import parse_whatweb_output
from summaries.whatweb_summary import generate_whatweb_summary

target = "http://scanme.nmap.org"

output = run_whatweb(target)

if output:

    findings = parse_whatweb_output(output, target)

    print("\n===== FINDINGS =====\n")

    for finding in findings:
        print(finding)

    summary = generate_whatweb_summary(findings)

    print("\n===== SUMMARY =====\n")

    print(summary)