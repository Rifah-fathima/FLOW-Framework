from scanners.gobuster_scanner import run_gobuster
from parsers.gobuster_parser import parse_gobuster_output

target = "scanme.nmap.org"

print("\nRunning Gobuster...\n")

raw_output = run_gobuster(target)

print("\nRaw Output:\n")
print(raw_output)

print("\n==========================")
print("Parsed Results")
print("==========================")

parsed_results = parse_gobuster_output(raw_output)

for result in parsed_results:
    print(result)