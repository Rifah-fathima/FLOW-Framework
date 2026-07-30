# ==============================
# Ollama Configuration
# ==============================

OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODEL = "llama3.2"

# ==============================
# AI Configuration
# ==============================

ENABLE_AI = True

# ==============================
# Scanner Configuration
# ==============================

DEFAULT_WORDLIST = "/usr/share/wordlists/dirb/common.txt"

NMAP_SCAN = [
    "nmap",
    "-sV"
]

# ==============================
# Reports
# ==============================

REPORT_FOLDER = "reports/generated"