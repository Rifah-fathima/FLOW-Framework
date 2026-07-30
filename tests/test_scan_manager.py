from manager.scan_manager import ScanManager

scan = ScanManager("http://scanme.nmap.org")

print("\nRunning Nikto...\n")

summary = scan.run_nikto()

print(summary)

scan.save()

print("\nStored Findings:\n")

print(scan.get_results())