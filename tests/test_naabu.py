from scanners.naabu_scanner import run_naabu
from parsers.naabu_parser import parse_naabu_output
from summaries.naabu_summary import generate_naabu_summary


target = input("Target: ")

output = run_naabu(target)

parsed = parse_naabu_output(output)

print(generate_naabu_summary(parsed))