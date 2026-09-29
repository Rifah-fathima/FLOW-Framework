import json

from dataclasses import asdict, is_dataclass


class FindingsManager:
    """
    Central Findings Manager for FLOW

    Stores:
    - Scan Results
    - Security Findings
    - Severity Levels
    - Recommendations
    """

    def __init__(self, target):

        self.target = target

        self.results = {}

        self.findings = []

    # ==================================================
    # STORE RAW SCAN RESULTS
    # ==================================================

    def add_results(self, module, results):

        self.results[module] = results

    def get_results(self, module):

        return self.results.get(module, None)

    # ==================================================
    # STORE SECURITY FINDINGS
    # ==================================================

    def add_finding(
        self,
        module,
        severity,
        title,
        description,
        recommendation
    ):

        finding = {
            "module": module,
            "severity": severity,
            "title": title,
            "description": description,
            "recommendation": recommendation
        }

        self.findings.append(finding)

    # ==================================================
    # GET ALL FINDINGS
    # ==================================================

    def get_findings(self):

        return self.findings

    # ==================================================
    # PRINT SECURITY SUMMARY
    # ==================================================

    def generate_security_summary(self):

        print("\n" + "=" * 70)
        print("FLOW SECURITY SUMMARY")
        print("=" * 70)

        if not self.findings:

            print("No security findings detected.")
            print("=" * 70)
            return

        severity_order = [
            "Critical",
            "High",
            "Medium",
            "Low",
            "Informational"
        ]

        for severity in severity_order:

            severity_findings = [
                finding
                for finding in self.findings
                if finding["severity"] == severity
            ]

            if not severity_findings:
                continue

            print(f"\n{severity.upper()}")

            print("-" * len(severity))

            for finding in severity_findings:

                print(
                    f"• [{finding['module']}] "
                    f"{finding['title']}"
                )

        print("\n" + "=" * 70)

        print(f"Total Findings : {len(self.findings)}")

        print("=" * 70)

    # ==================================================
    # JSON SERIALIZATION HELPER
    # ==================================================

    @staticmethod
    def _serialize_object(obj):
        """
        Convert dataclass objects such as Finding
        into JSON-serializable dictionaries.
        """

        if is_dataclass(obj):
            return asdict(obj)

        if isinstance(obj, list):
            return [
                FindingsManager._serialize_object(item)
                for item in obj
            ]

        if isinstance(obj, dict):
            return {
                key: FindingsManager._serialize_object(value)
                for key, value in obj.items()
            }

        return obj

    # ==================================================
    # EXPORT JSON REPORT
    # ==================================================

    def save_json(self, filename="reports/report.json"):

        report = {
            "target": self.target,
            "results": self._serialize_object(self.results),
            "findings": self._serialize_object(self.findings)
        }

        with open(filename, "w") as file:

            json.dump(
                report,
                file,
                indent=4
            )

        print(
            f"\n[FLOW] Report saved -> {filename}"
        )