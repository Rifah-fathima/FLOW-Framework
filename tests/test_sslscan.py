from scanners.sslscan_scanner import run_sslscan
from parsers.sslscan_parser import parse_sslscan_output
from summaries.sslscan_summary import generate_sslscan_summary

raw_output = run_sslscan("google.com")

parsed = parse_sslscan_output(raw_output)

summary = generate_sslscan_summary(parsed)

print(summary)