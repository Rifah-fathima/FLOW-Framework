import json
import requests

from config.settings import OLLAMA_MODEL, OLLAMA_URL
from ai.prompts import (
    NMAP_SUMMARY_PROMPT,
    GOBUSTER_SUMMARY_PROMPT,
)


def _send_prompt(prompt, scan_data):

    full_prompt = (
        prompt
        + "\n\nScan Results:\n"
        + json.dumps(scan_data, separators=(",", ":"))
    )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 120
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json().get("response", "No response.")

    except Exception as e:
        return f"AI Error: {e}"


def analyze_nmap(scan_results):

    services = []

    for item in scan_results:

        if item["state"] == "open":
            services.append({
                "port": item["port"],
                "service": item["service"]
            })

    return _send_prompt(
        NMAP_SUMMARY_PROMPT,
        {"open_services": services}
    )


def analyze_gobuster(scan_results):

    directories = []

    for item in scan_results:
        directories.append(item["path"])

    return _send_prompt(
        GOBUSTER_SUMMARY_PROMPT,
        {"directories": directories}
    )