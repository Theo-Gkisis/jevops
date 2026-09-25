import os

import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/alpha/decisions"


def classify(line: str) -> tuple[str, float]:
    """Ask JEV to classify a log line's severity."""
    response = requests.post(
        OPENROUTER_URL,
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
        json={
            "model": "typesafe/jev-1.13",
            "state": {"line": line},
            "questions": {
                "severity": {
                    "type": "choice",
                    "instructions": "What severity level does this log line indicate?",
                    "criteria": {
                        "normal": "Routine operation, no problem",
                        "warning": "Unusual but not critical",
                        "error": "Something failed or broke",
                        "critical": "Severe failure requiring immediate attention",
                    },
                }
            },
        },
    )
    answer = response.json()["answers"]["severity"]
    return answer["choice"], answer["confidence"]
