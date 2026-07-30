from dataclasses import dataclass, asdict


@dataclass
class Finding:
    tool: str
    severity: str
    category: str
    title: str
    description: str
    target: str
    evidence: str = ""
    reference: str = ""
    recommendation: str = ""
    cve: str = ""
    cvss: float = 0.0

    def to_dict(self):
        return asdict(self)