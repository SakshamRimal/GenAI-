import json
import os
from datetime import datetime, timezone

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs", "query_logs.json")


def _ensure_log_dir():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def log_event(event: dict):
    _ensure_log_dir()
    event["timestamp"] = datetime.now(timezone.utc).isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")


def log_step(question: str, step: str, detail: dict):
    log_event({"question": question, "step": step, **detail})
