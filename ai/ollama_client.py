
import json
import requests

from config.settings import ENABLE_AI, OLLAMA_MODEL, OLLAMA_URL
from ai.prompts import (
    NMAP_SUMMARY_PROMPT,
    GOBUSTER_SUMMARY_PROMPT,
    AI_SECURITY_ASSESSMENT_PROMPT,
)


def _send_prompt(prompt, scan_data, num_predict=120):
    """Send a prompt and scan data to the Ollama API."""

    if not ENABLE_AI:
        return "AI disabled in configuration."

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
            "num_predict": num_predict,
        },
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120,
        )
        response.raise_for_status()

        text = response.json().get("response", "").strip()

        if not text:
            return "AI Error: Ollama returned an empty response."

        return text

    except requests.RequestException as exc:
        return f"AI Error: {exc}"
    except (ValueError, TypeError) as exc:
        return f"AI Error: Invalid response from Ollama: {exc}"


def analyze_nmap(scan_results):
    """Generate an AI summary of open Nmap services."""

    services = []

    for item in scan_results:
        if item.get("state") == "open":
            services.append({
                "port": item.get("port"),
                "service": item.get("service", "unknown"),
            })

    return _send_prompt(
        NMAP_SUMMARY_PROMPT,
        {"open_services": services},
    )


def analyze_gobuster(scan_results):
    """Generate an AI summary of Gobuster discoveries."""

    directories = [
        item.get("path")
        for item in scan_results
        if isinstance(item, dict) and item.get("path")
    ]

    return _send_prompt(
        GOBUSTER_SUMMARY_PROMPT,
        {"directories": directories},
    )


def generate_security_assessment(target, results, findings):
    """Generate an AI assessment from FLOW's existing scan data."""

    scan_data = {
        "target": target,
        "results": results,
        "findings": findings,
    }

    return _send_prompt(
        AI_SECURITY_ASSESSMENT_PROMPT,
        scan_data,
        num_predict=700,
    )
