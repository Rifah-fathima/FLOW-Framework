# FLOW Framework

## A PentestAI Framework

FLOW is a modular automated penetration-testing framework designed to
automate reconnaissance, service detection, enumeration, security
analysis, findings generation, and HTML report generation.

---

## Features

FLOW currently supports:

- Automated target validation
- Naabu port discovery
- Nmap service detection
- SSH security auditing
- Gobuster directory enumeration
- Nikto web-server scanning
- SSLScan
- WhatWeb
- WPScan
- Automated module recommendation
- SSH security findings
- Risk classification
- JSON report generation
- HTML report generation
- Automated dependency checking
- Modular scanner/parser/summary architecture
- Ollama integration foundation

---

## Architecture

```text
FLOW
│
├── ai/
│   ├── ollama_client.py
│   └── prompts.py
│
├── config/
│   └── settings.py
│
├── core/
│   ├── scanner_base.py
│   └── dependency_checker.py
│
├── dashboard/
│
├── database/
│
├── engine/
│   ├── decision_engine.py
│   └── module_registry.py
│
├── findings/
│   ├── findings_manager.py
│   └── ssh_findings.py
│
├── manager/
│   └── scan_manager.py
│
├── models/
│   └── finding.py
│
├── parsers/
│
├── reports/
│   ├── charts.py
│   ├── html_utils.py
│   ├── report_builder.py
│   ├── report_generator.py
│   ├── sections.py
│   ├── statistics.py
│   └── templates/
│
├── scanners/
│
├── summaries/
│
├── tests/
│
├── utils/
│
├── workflow/
│   └── pentest_workflow.py
│
├── main.py
├── requirements.txt
└── README.md
