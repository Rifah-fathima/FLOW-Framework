from scanners.nmap_scanner import run_nmap
from scanners.gobuster_scanner import run_gobuster
from scanners.nikto_scanner import run_nikto
from scanners.sslscan_scanner import run_sslscan

from parsers.nmap_parser import parse_nmap_output
from parsers.gobuster_parser import parse_gobuster_output
from parsers.nikto_parser import parse_nikto_output
from parsers.sslscan_parser import parse_sslscan_output

from summaries.nmap_summary import generate_nmap_summary
from summaries.gobuster_summary import generate_gobuster_summary
from summaries.nikto_summary import generate_nikto_summary
from summaries.sslscan_summary import generate_sslscan_summary

from findings.findings_manager import FindingsManager


class ScanManager:

    def __init__(self, target):

        self.target = target
        self.findings = FindingsManager(target)

    # ==========================================
    # NMAP
    # ==========================================

    def run_nmap(self):

        output = run_nmap(self.target)

        parsed = parse_nmap_output(output)

        summary = generate_nmap_summary(parsed)

        self.findings.add_results("nmap", parsed)

        return summary

    # ==========================================
    # GOBUSTER
    # ==========================================

    def run_gobuster(self):

        output = run_gobuster(self.target)

        parsed = parse_gobuster_output(output)

        summary = generate_gobuster_summary(parsed)

        self.findings.add_results("gobuster", parsed)

        return summary

    # ==========================================
    # NIKTO
    # ==========================================

    def run_nikto(self):

        output = run_nikto(
            self.target,
            quick=True
        )

        parsed = parse_nikto_output(output)

        summary = generate_nikto_summary(parsed)

        self.findings.add_results("nikto", parsed)

        return summary

    # ==========================================
    # SSLSCAN
    # ==========================================

    def run_sslscan(self):

        output = run_sslscan(self.target)

        parsed = parse_sslscan_output(output)

        summary = generate_sslscan_summary(parsed)

        self.findings.add_results("sslscan", parsed)

        return summary

    # ==========================================
    # SAVE FINDINGS
    # ==========================================

    def save(self):

        self.findings.save_json()

    # ==========================================
    # GET RESULTS
    # ==========================================

    def get_results(self):

        return self.findings.get_all()