import os
import json
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "logs", "query_log.json")

def log_query(sql: str, status: str, error: str = ""):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "status": status,
        "sql": sql,
        "error": error,
    }

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")